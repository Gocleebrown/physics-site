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

// --- 2) String interpolation helper (with rounding for numbers) ---
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

// --- 2b) Raw interpolation (NO rounding) for JSON blobs like graphSpec ---
function interpolateRaw(str, ctx) {
  return (str || "").replace(/\$\{([^}]+)\}/g, (_, expr) => {
    try {
      const fn = new Function(...Object.keys(ctx), `return (${expr});`);
      const val = fn(...Object.values(ctx));
      return (val === null || val === undefined) ? "" : String(val);
    } catch {
      return "";
    }
  });
}

// --- 3) Format number to a specific number of significant figures ---
function formatToSigFigs(num, digits) {
  if (num === 0) return "0";
  const precision = digits || 3;
  return parseFloat(num.toPrecision(precision)).toString();
}

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

// --- 5) Build marks from keyword columns (supports B2) ---
function buildMarksFromRow(row, ctx) {
  const types = ["A", "C2", "C1", "M", "B", "B2"];
  const marks = [];

  types.forEach((type) => {
    const rawKey = row[type + "_keywords"];
    if (!rawKey) return;
    const raw = window.interpolate(rawKey, ctx).trim();
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
      type === "B" || type === "B2" ? "B" : type.startsWith("C") ? "C" : type;
    const level = type === "C2" ? 2 : type === "C1" ? 1 : undefined;

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
      ctx[k] = +(Math.random() * (max - min) + min).toFixed(6);
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

  // assemble mainText + image
  const mainText = window.interpolate(mainRow.mainText || "", ctx);
  let imageBelow = "";
  if (mainRow.imageBelowMain) {
    const filename = mainRow.imageBelowMain;
    const imageSrc = filename.endsWith(".png") ? filename : `${filename}.png`;
    imageBelow = `<img src="assets/${imageSrc}" style="margin-top:1em;max-width:100%;" />`;
  }

  const q = { id, type, mainText: mainText + imageBelow, parts: [] };

  // 6.5 build each part
  parts
    .sort((a, b) => +a.partIndex - +b.partIndex)
    .forEach((row) => {
      const partText = window.interpolate(row.partText || "", ctx);

      let imageAfter = "";
      if (row.imageAfterPart) {
        const filename = row.imageAfterPart;
        const imageSrc = filename.endsWith(".png") ? filename : `${filename}.png`;
        imageAfter = `<img src="assets/${imageSrc}" style="margin-top:1em;max-width:100%;" />`;
      }

      const modelAnswer = window.interpolate(row.modelAnswer || "", ctx);
      const explanation = window.interpolate(row.explanation || "", ctx);
      const marks = buildMarksFromRow(row, ctx);

      const partObj = {
        partText: partText + imageAfter,
        modelAnswer,
        explanation,
        marks,
      };

      // ── NEW: pass graphSpec from the sheet (string or JSON), with raw interpolation (no rounding)
      if (row.graphSpec) {
        const raw = String(row.graphSpec).trim();
        partObj.graphSpec = interpolateRaw(raw, ctx); // leave as JSON string for the renderer
      }

      // stress-strain special case (kept; only if CSV didn't already provide a graphSpec)
      if (!partObj.graphSpec && type === "stress-strain" && +row.partIndex === 0) {
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
