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

// --- 2) String interpolation helper with 3 sig-fig support ---
window.interpolate = function (str, ctx) {
  return (str || "").replace(/\$\{([^}]+)\}/g, (_, expr) => {
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

// --- 4) Compute derived values from formulas ---
function computeValues(params, formulas) {
  const computed = {};
  for (const key in formulas) {
    try {
      const fn = new Function(
        "params",
        "computed",
        `
        with(params) { with(computed) { return ${formulas[key]}; }}
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
  const types = ["A", "C2", "C1", "M", "B"];
  const marks = [];
  types.forEach((type) => {
    const raw = interpolate(row[type + "_keywords"], ctx).trim();
    if (!raw) return;
    let parsed = null;
    if (raw.startsWith("[")) {
      try {
        parsed = JSON.parse(raw.replace(/'/g, '"'));
      } catch {}
    }
    let groups = [];
    // parsed as flat array
    if (
      Array.isArray(parsed) &&
      parsed.every((e) => typeof e === "string" || typeof e === "number")
    ) {
      groups = [parsed.map((e) => String(e).toLowerCase().trim())];
    }
    // parsed as array of arrays
    else if (Array.isArray(parsed) && parsed.every((g) => Array.isArray(g))) {
      groups = parsed.map((g) => g.map((e) => String(e).toLowerCase().trim()));
    }
    // fallback: split raw
    else {
      const flat = raw
        .split(/[,;]+/)
        .map((e) => e.toLowerCase().trim())
        .filter(Boolean);
      if (flat.length) groups = [flat];
    }
    if (groups.length) {
      marks.push({
        type: type.startsWith("C") ? "C" : type,
        level: type === "C2" ? 2 : type === "C1" ? 1 : undefined,
        keywords: groups,
        awarded: false,
      });
    }
  });
  return marks;
}

// --- 6) Generic builder from CSV for all question types ---
window.genericBuilder = function ({ id, type, params, parts }) {
  const ctx = {};
  // 6.1 seed random params
  for (const k in params) {
    if (Array.isArray(params[k]) && typeof params[k][0] === "number") {
      const [min, max] = params[k];
      ctx[k] = +(Math.random() * (max - min) + min).toFixed(6);
    } else {
      ctx[k] = params[k];
    }
  }
  // 6.2 mainRow
  const mainRow = parts.find((r) => +r.partIndex === 0) || parts[0];
  // 6.3 apply main computed
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
  // 6.4 apply tableRequest
  if (mainRow.tableRequest) {
    try {
      const def = JSON.parse(mainRow.tableRequest);
      const rows = def.map((t) => ({
        Quantity: t.label,
        Value: formatTo3SigFigs(ctx[t.val]) || "",
        Uncertainty: "±" + formatTo3SigFigs(ctx[t.unc]) || "",
      }));
      ctx.dimsTable = makeTable(rows, ["Quantity", "Value", "Uncertainty"]);
    } catch {
      console.warn("Invalid tableRequest in", id, "main part");
    }
  }
  // 6.5 mainText + image
  const mainText = interpolate(mainRow.mainText || "", ctx);
  const imageBelow = mainRow.imageBelowMain
    ? `<img src="assets/${mainRow.imageBelowMain}.png" style="margin-top:1em;max-width:100%;" />`
    : "";
  const q = { id, type, mainText: mainText + imageBelow, parts: [] };
  // 6.6 build parts
  parts
    .sort((a, b) => +a.partIndex - +b.partIndex)
    .forEach((row) => {
      const local = { ...ctx };
      if (row.computedValues) {
        try {
          Object.assign(
            local,
            computeValues(local, JSON.parse(row.computedValues))
          );
        } catch {
          console.warn("Bad computedValues in", id, "part", row.partIndex);
        }
      }
      const partText = interpolate(row.partText || "", local);
      const modelAnswer = interpolate(row.modelAnswer || "", local);
      const explanation = interpolate(row.explanation || "", local);
      const marks = buildMarksFromRow(row, local);
      const partObj = { partText, modelAnswer, explanation, marks };
      // auto‐graph for stress-strain
      if (type === "stress-strain") {
        const s = local.max_strain,
          m = local.module_plot;
        partObj.graphSpec = {
          points: [
            [0, 0],
            [s, s * m],
          ],
          xMax: s,
          yMax: s * m,
          xLabel: "Strain",
          yLabel: "Stress (×10⁶ Pa)",
          xTicks: [0, s],
          yTicks: [0, m],
        };
      }
      q.parts.push(partObj);
    });
  return q;
};
