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

// --- 2) String interpolation helper with 3-sig-fig support ---
window.interpolate = function (str, ctx) {
  return str.replace(/\$\{([^}]+)\}/g, (_, expr) => {
    try {
      const fn = new Function(...Object.keys(ctx), `return ${expr}`);
      const result = fn(...Object.values(ctx));
      return typeof result === "number" ? formatTo3SigFigs(result) : result;
    } catch {
      return "";
    }
  });
};

// --- 3) Format number to 3 significant figures ---
function formatTo3SigFigs(num) {
  if (num === 0) return "0";
  const digits = 3;
  const power = Math.floor(Math.log10(Math.abs(num)));
  const factor = Math.pow(10, digits - 1 - power);
  return (Math.round(num * factor) / factor).toString();
}

// --- 4) Compute derived values (supports dependencies) ---
function computeValues(params, formulas) {
  const computed = {};
  for (const key in formulas) {
    const expr = formulas[key];
    try {
      const fn = new Function(
        "params",
        "computed",
        `
        with (params) {
          with (computed) {
            return ${expr};
          }
        }
      `
      );
      computed[key] = fn(params, computed);
    } catch {
      computed[key] = null;
    }
  }
  return computed;
}

// --- 5) Build marks from keyword columns ---
function buildMarksFromRow(row, ctx) {
  const markTypes = ["A", "C2", "C1", "M", "B"];
  const marks = [];

  markTypes.forEach((type) => {
    // interpolate any ${…} in the CSV cell
    const raw = window.interpolate(row[type + "_keywords"] || "", ctx).trim();
    if (!raw) return;

    const level = type === "C2" ? 2 : type === "C1" ? 1 : undefined;
    let keywordsList = [],
      parsed = null;

    if (raw.startsWith("[")) {
      try {
        const safe = raw.replace(/'/g, '"').replace(/,\s*]/g, "]");
        parsed = JSON.parse(safe);
      } catch {}
    }

    // flat array of strings → OR
    if (Array.isArray(parsed) && parsed.every((e) => typeof e === "string")) {
      keywordsList = [parsed.map((e) => e.toLowerCase().trim())];
    }
    // nested arrays of strings → AND-of-ORs
    else if (
      Array.isArray(parsed) &&
      parsed.every(
        (grp) => Array.isArray(grp) && grp.every((e) => typeof e === "string")
      )
    ) {
      keywordsList = parsed.map((grp) =>
        grp.map((e) => e.toLowerCase().trim())
      );
    }
    // fallback split on commas/semicolons
    else if (!raw.startsWith("[{")) {
      const flat = raw
        .split(/[,;]+/)
        .map((e) => e.toLowerCase().trim())
        .filter(Boolean);
      if (flat.length) keywordsList = [flat];
    }

    if (keywordsList.length) {
      marks.push({
        type: type.startsWith("C") ? "C" : type,
        level,
        keywords: keywordsList,
        awarded: false,
      });
    }
  });

  return marks;
}

// --- 6) Generic builder from CSV for all question types ---
window.genericBuilder = function ({ id, params, parts }) {
  const ctx = {};

  // 6.1: Randomise any numeric-array params into ctx
  for (const k in params) {
    if (Array.isArray(params[k]) && typeof params[k][0] === "number") {
      const [min, max] = params[k];
      ctx[k] = +(Math.random() * (max - min) + min).toFixed(6);
    } else {
      ctx[k] = params[k];
    }
  }

  // 6.2: Identify mainRow (partIndex = 0)
  const mainRow = parts.find((r) => +r.partIndex === 0) || parts[0];

  // 6.3: Build mainText & imageBelowMain from mainRow only
  const mainText = window.interpolate(mainRow.mainText || "", ctx);
  const imageBelow = mainRow.imageBelowMain
    ? `<img src="assets/${mainRow.imageBelowMain}.png" style="margin-top:1em;max-width:100%;" />`
    : "";

  const q = { id, mainText: mainText + imageBelow, parts: [] };

  // 6.4: Build each part (computeValues + optional tableRequest + marks)
  parts
    .sort((a, b) => +a.partIndex - +b.partIndex)
    .forEach((row) => {
      const localCtx = { ...ctx };

      // 6.4.1: Per-part computedValues
      if (row.computedValues) {
        try {
          Object.assign(
            localCtx,
            computeValues(localCtx, JSON.parse(row.computedValues))
          );
        } catch {
          console.warn("Bad computedValues in", id, "part", row.partIndex);
        }
      }

      // 6.4.2: Per-part tableRequest (only for partIndex = 0)
      if (+row.partIndex === 0 && row.tableRequest) {
        try {
          const def = JSON.parse(row.tableRequest);
          const tableRows = def.map((t) => ({
            Quantity: t.label,
            Value: formatTo3SigFigs(localCtx[t.val]) || "",
            Uncertainty: "±" + formatTo3SigFigs(localCtx[t.unc]) || "",
          }));
          localCtx.dimsTable = makeTable(tableRows, [
            "Quantity",
            "Value",
            "Uncertainty",
          ]);
        } catch {
          console.warn("Invalid tableRequest in", id, "part", row.partIndex);
        }
      }

      // 6.4.3: Interpolate partText, modelAnswer, explanation
      const partText = window.interpolate(row.partText || "", localCtx);
      const modelAnswer = window.interpolate(row.modelAnswer || "", localCtx);
      const explanation = window.interpolate(row.explanation || "", localCtx);
      const imageAfter = row.imageAfterPart
        ? `<img src="assets/${row.imageAfterPart}.png" style="margin-top:1em;max-width:100%;" />`
        : "";

      // 6.4.4: Build marks
      const marks = buildMarksFromRow(row, localCtx);

      q.parts.push({
        partText: partText + imageAfter,
        modelAnswer,
        explanation,
        marks,
      });
    });

  return q;
};
