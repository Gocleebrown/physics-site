// scripts/questionBuilders.js

// --- 1) Table-builder helper ---
window.makeTable = function (rows, cols) {
  let html = `<table><tr>${cols.map((c) => `<th>${c}</th>`).join("")}</tr>`;
  rows.forEach((r) => {
    html += `<tr>${cols.map((c) => `<td>${r[c] || ""}</td>`).join("")}</tr>`;
  });
  html += `</table>`;
  return html;
};

// --- 2) String interpolation helper ---
window.interpolate = function (str, ctx) {
  return (str || "").replace(/\$\{([^}]+)\}/g, (_, expr) => {
    try {
      const fn = new Function(...Object.keys(ctx), `return ${expr}`);
      const result = fn(...Object.values(ctx));
      return typeof result === "number" ? formatToSigFigs(result) : result;
    } catch {
      return "";
    }
  });
};

// --- 3) Format number to a specific number of significant figures ---
function formatToSigFigs(num, digits) {
  if (num === 0) return "0";
  const precision = digits || 3;
  return parseFloat(num.toPrecision(precision)).toString();
}

// --- 3b) Resolve an asset filename to a src path, preserving any given
//     extension (svg/png/jpg/...) and only defaulting to .png when the
//     filename has no extension at all. Previously this always forced
//     .png, which silently broke any .svg asset reference. ---
window.resolveAssetSrc = function (filename) {
  if (!filename) return "";
  const hasExt = /\.[a-zA-Z0-9]+$/.test(filename);
  const withExt = hasExt ? filename : `${filename}.png`;
  return `assets/${withExt}`;
};

// --- 4) Compute derived values from formulas ---
function computeValues(params, formulas) {
  const computed = {};
  for (const key in formulas) {
    try {
      const fn = new Function(
        "params",
        "computed",
        `with(params){with(computed){return ${formulas[key]};}}`
      );
      computed[key] = fn(params, computed);
    } catch {
      computed[key] = null;
    }
  }
  return computed;
}

// --- 5) Build marks from keyword columns (supports B2), plus imageChoice ---
function buildMarksFromRow(row, ctx) {
  // imageChoice parts don't use keyword columns at all — they're worth a
  // fixed number of marks (imageChoiceMarks, default 1), awarded as a
  // block when the correct option is picked.
  if ((row.answerType || "").trim() === "imageChoice") {
    const n = parseInt(row.imageChoiceMarks, 10) || 1;
    const marks = [];
    for (let i = 0; i < n; i++) {
      marks.push({ type: "B", keywords: null, awarded: false });
    }
    return marks;
  }

  // table parts: one independent mark per cell, in row-major order.
  if ((row.answerType || "").trim() === "table") {
    let cellKeywords = [];
    try {
      cellKeywords = JSON.parse(interpolate(row.tableCellKeywords || "[]", ctx));
    } catch {
      console.warn("Bad tableCellKeywords in row", row.id, row.partIndex);
    }
    const marks = [];
    cellKeywords.forEach((rowArr) =>
      (rowArr || []).forEach(() => marks.push({ type: "B", keywords: null, awarded: false }))
    );
    return marks;
  }

  const types = ["A", "C3", "C2", "C1", "M", "B", "B2", "B3"];
  const marks = [];

  types.forEach((type) => {
    const rawKey = row[type + "_keywords"];
    if (!rawKey) return;
    const raw = interpolate(rawKey, ctx).trim();
    if (!raw) return;

    let parsed = null;
    if (raw.startsWith("[")) {
      try {
        parsed = JSON.parse(raw.replace(/'/g, '"'));
      } catch {}
    }

    let groups = [];
    if (
      Array.isArray(parsed) &&
      parsed.every((e) => typeof e === "string" || typeof e === "number")
    ) {
      groups = [parsed.map((e) => String(e).toLowerCase().trim())];
    } else if (Array.isArray(parsed) && parsed.every((g) => Array.isArray(g))) {
      groups = parsed.map((g) => g.map((e) => String(e).toLowerCase().trim()));
    } else {
      const flat = raw
        .split(/[,;]+/)
        .map((e) => e.toLowerCase().trim())
        .filter(Boolean);
      if (flat.length) groups = [flat];
    }

    const markType =
      type.startsWith("B") ? "B" : type.startsWith("C") ? "C" : type;
    const level = type === "C3" ? 3 : type === "C2" ? 2 : type === "C1" ? 1 : undefined;

    marks.push({ type: markType, level, keywords: groups, awarded: false });
  });

  return marks;
}

// --- 6) Generic builder from CSV ---
window.genericBuilder = function ({ id, type, params, parts }) {
  const ctx = {};

  // 6.1 randomise parameters (shared across all parts)
  for (const k in params) {
    if (Array.isArray(params[k]) && typeof params[k][0] === "number") {
      const [min, max] = params[k];
      ctx[k] = Math.random() * (max - min) + min;
    } else {
      ctx[k] = params[k];
    }
  }

  // 6.2 collect ALL computedValues across all parts
  const allFormulas = {};
  parts.forEach((row) => {
    if (row.computedValues) {
      try {
        Object.assign(allFormulas, JSON.parse(row.computedValues));
      } catch {
        console.warn("Bad computedValues in", id, "part", row.partIndex);
      }
    }
  });
  Object.assign(ctx, computeValues(ctx, allFormulas));

  // 6.3 mainRow
  const mainRow = parts.find((r) => +r.partIndex === 0) || parts[0];

  // 6.4 tableRequest (only mainRow)
  if (mainRow.tableRequest) {
    try {
      const tableDef = JSON.parse(mainRow.tableRequest);
      const tableRows = tableDef.map((t) => ({
        Quantity: t.label,
        Value: formatToSigFigs(ctx[t.val], t.valSf),
        Uncertainty: "±" + formatToSigFigs(ctx[t.unc], t.uncSf),
      }));
      ctx.dimsTable = makeTable(tableRows, [
        "Quantity",
        "Value",
        "Uncertainty",
      ]);
    } catch {
      console.warn("Invalid tableRequest in", id, "main part");
    }
  }

  // main text + optional image below (PNG/SVG in /assets)
  const mainText = interpolate(mainRow.mainText || "", ctx);
  let imageBelow = "";
  if (mainRow.imageBelowMain) {
    imageBelow = `<img src="${resolveAssetSrc(mainRow.imageBelowMain)}" style="margin-top:1em;max-width:480px;width:100%;" />`;
  }

  const q = { id, type, mainText: mainText + imageBelow, parts: [] };

  // 6.5 build each part
  parts
    .sort((a, b) => +a.partIndex - +b.partIndex)
    .forEach((row) => {
      const partText = interpolate(row.partText || "", ctx);

      let imageAfter = "";
      if (row.imageAfterPart) {
        imageAfter = `<img src="${resolveAssetSrc(row.imageAfterPart)}" style="margin-top:1em;max-width:480px;width:100%;" />`;
      }

      const modelAnswer = interpolate(row.modelAnswer || "", ctx);
      const explanation = interpolate(row.explanation || "", ctx);
      const marks = buildMarksFromRow(row, ctx);

      const partObj = {
        partText: partText + imageAfter,
        modelAnswer,
        explanation,
        marks,
        answerType: (row.answerType || "text").trim(),
      };

      // ── imageChoice: pass through the option list + correct index
      if (partObj.answerType === "imageChoice") {
        try {
          partObj.imageOptions = JSON.parse(row.imageOptions || "[]");
        } catch {
          console.warn("Bad imageOptions in", id, "part", row.partIndex);
          partObj.imageOptions = [];
        }
        partObj.correctImageIndex = parseInt(row.correctImageIndex, 10);
      }

      // ── table: pass through row/col labels, per-cell keywords + answers
      if (partObj.answerType === "table") {
        try {
          partObj.tableRowLabels = JSON.parse(interpolate(row.tableRowLabels || "[]", ctx));
        } catch {
          partObj.tableRowLabels = [];
        }
        try {
          partObj.tableColLabels = JSON.parse(interpolate(row.tableColLabels || "[]", ctx));
        } catch {
          partObj.tableColLabels = [];
        }
        try {
          partObj.tableCellKeywords = JSON.parse(interpolate(row.tableCellKeywords || "[]", ctx));
        } catch {
          console.warn("Bad tableCellKeywords in", id, "part", row.partIndex);
          partObj.tableCellKeywords = [];
        }
        try {
          partObj.tableCellAnswers = JSON.parse(interpolate(row.tableCellAnswers || "[]", ctx));
        } catch {
          partObj.tableCellAnswers = [];
        }
      }

      // ── Pass-through graphSpec from sheet (supports ${...} placeholders)
      if (row.graphSpec) {
        const gs = interpolate(row.graphSpec, ctx);
        partObj.graphSpec = gs; // leave as string; drawGraph will parse
      }
      if (row.graphSpec2) {
        partObj.graphSpec2 = interpolate(row.graphSpec2, ctx);
      }

      // ── Stress–strain special (kept exactly as before)
      if (type === "stress-strain" && +row.partIndex === 0) {
        const s = ctx.max_strain;
        const m = ctx.module_plot;
        const σ_limit = s * m;
        const plateauWidth = 0.0005;

        partObj.graphSpec = {
          points: [
            [0, 0],
            [s, σ_limit],
            [s + plateauWidth, σ_limit],
          ],
          xMax: s + plateauWidth,
          yMax: σ_limit * 1.1,
          xLabel: "Strain",
          yLabel: "Stress (×10⁶ Pa)",
        };
      }

      q.parts.push(partObj);
    });

  return q;
};
