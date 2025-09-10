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
      // Use the flexible formatting function for numbers found during interpolation
      return typeof result === "number" ? formatToSigFigs(result) : result;
    } catch {
      return "";
    }
  });
};

// --- 3) Format number to a specific number of significant figures ---
function formatToSigFigs(num, digits) {
  if (num === 0) return "0";
  // Default to 3 significant figures if not specified
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
      type === "B" || type === "B2" ? "B" : type.startsWith("C") ? "C" : type;
    const level = type === "C2" ? 2 : type === "C1" ? 1 : undefined;

    if ((type === "B" || type === "B2") && groups.length > 1) {
      // multiple B-subgroups → separate B-marks
      groups.forEach((sub) => {
        marks.push({ type: "B", keywords: [sub], awarded: false });
      });
    } else {
      marks.push({ type: markType, level, keywords: groups, awarded: false });
    }
  });

  return marks;
}

// --- 6) Generic builder from CSV ---
window.genericBuilder = function ({ id, type, params, parts }) {
  const ctx = {};
  // 6.1 randomise parameters
  for (const k in params) {
    if (Array.isArray(params[k]) && typeof params[k][0] === "number") {
      const [min, max] = params[k];
      ctx[k] = +(Math.random() * (max - min) + min).toFixed(6);
    } else {
      ctx[k] = params[k];
    }
  }

  // 6.2 mainRow (partIndex=0)
  const mainRow = parts.find((r) => +r.partIndex === 0) || parts[0];

  // 6.3 apply computedValues on main
  if (mainRow.computedValues) {
    try {
      Object.assign(
        ctx,
        computeValues(ctx, JSON.parse(mainRow.computedValues))
      );
    } catch {
      console.warn("Bad computedValues in", id, "main part");
    }
  }

  // assemble mainText + imageBelowMain
  const mainText = interpolate(mainRow.mainText || "", ctx);
  const imageBelow = mainRow.imageBelowMain
    ? `<img src="assets/${mainRow.imageBelowMain}" style="margin-top:1em;max-width:100%;" />`
    : "";

  const q = { id, type, mainText: mainText + imageBelow, parts: [] };

  // 6.5 build each part
  parts
    .sort((a, b) => +a.partIndex - +b.partIndex)
    .forEach((row) => {
      const partText = interpolate(row.partText || "", ctx);
      const imageAfter = row.imageAfterPart
        ? `<img src="assets/${row.imageAfterPart}" style="margin-top:1em;max-width:100%;" />`
        : "";
      const modelAnswer = interpolate(row.modelAnswer || "", ctx);
      const explanation = interpolate(row.explanation || "", ctx);
      const marks = buildMarksFromRow(row, ctx);

      const partObj = {
        partText: partText + imageAfter,
        modelAnswer,
        explanation,
        marks,
      };

      // Path 1: Keep the original, dedicated stress-strain graph logic
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
      // Path 2: Dedicated handler for the waves interference graph
      else if (id === "waves-1" && +row.partIndex === 3) {
        const gradient = ctx.gradient_x_vs_D;
        const D_start = 2.0;
        const D_end = 3.5;
        const x_start = D_start * gradient;
        const x_end = D_end * gradient;

        partObj.graphSpec = {
          points: [
            [D_start, x_start],
            [D_end, x_end],
          ],
          xMin: 2.0,
          xMax: 3.5,
          yMax: 10.0,
          xLabel: "D / m",
          yLabel: "x / mm",
        };
      }

      q.parts.push(partObj);
    });

  return q;
};
