// scripts/questionBuilders.js

// --- 1) Table‐builder helper ---
window.makeTable = function (rows, cols) {
  let html = `<table><tr>${cols.map((c) => `<th>${c}</th>`).join("")}</tr>`;
  rows.forEach((r) => {
    html += `<tr>${cols.map((c) => `<td>${r[c] || ""}</td>`).join("")}</tr>`;
  });
  html += `</table>`;
  return html;
};

// --- 2) String interpolation (3-sig-fig) ---
window.interpolate = function (str, ctx) {
  return str.replace(/\$\{([^}]+)\}/g, (_, expr) => {
    try {
      const fn = new Function(...Object.keys(ctx), `return ${expr}`);
      const val = fn(...Object.values(ctx));
      return typeof val === "number" ? formatTo3SigFigs(val) : val;
    } catch {
      return "";
    }
  });
};

// --- 3) Format to 3 significant figures ---
function formatTo3SigFigs(num) {
  if (num === 0) return "0";
  const power = Math.floor(Math.log10(Math.abs(num)));
  const factor = Math.pow(10, 2 - power);
  return (Math.round(num * factor) / factor).toString();
}

// --- 4) Compute derived values (with dependencies) ---
function computeValues(params, formulas) {
  const computed = {};
  for (const k in formulas) {
    try {
      const fn = new Function(
        "params",
        "computed",
        `
        with(params){ with(computed){ return ${formulas[k]}; }}
      `
      );
      computed[k] = fn(params, computed);
    } catch {
      computed[k] = null;
    }
  }
  return computed;
}

// --- 5) Build marks from keyword columns ---
function buildMarksFromRow(row, ctx) {
  const markTypes = ["A", "C2", "C1", "M", "B"];
  const marks = [];

  markTypes.forEach((type) => {
    const raw = window.interpolate(row[type + "_keywords"] || "", ctx).trim();
    if (!raw) return;
    let parsed = null;
    if (raw.startsWith("[")) {
      try {
        parsed = JSON.parse(raw.replace(/'/g, '"'));
      } catch {}
    }
    let groups = [];
    if (Array.isArray(parsed) && parsed.every((e) => typeof e === "string")) {
      groups = [parsed.map((e) => e.toLowerCase().trim())];
    } else if (Array.isArray(parsed) && parsed.every((g) => Array.isArray(g))) {
      groups = parsed.map((g) => g.map((e) => e.toLowerCase().trim()));
    } else {
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

// --- 6) Generic builder ---
window.genericBuilder = function ({ id, type, params, parts }) {
  const ctx = {};

  // 6.1 seed ctx from params
  for (const k in params) {
    if (Array.isArray(params[k]) && typeof params[k][0] === "number") {
      const [min, max] = params[k];
      ctx[k] = +(Math.random() * (max - min) + min).toFixed(6);
    } else {
      ctx[k] = params[k];
    }
  }

  // 6.2 identify mainRow
  const mainRow = parts.find((r) => +r.partIndex === 0) || parts[0];

  // 6.3 apply computedValues on mainRow
  if (mainRow.computedValues) {
    try {
      Object.assign(
        ctx,
        computeValues(ctx, JSON.parse(mainRow.computedValues))
      );
    } catch {}
  }

  // 6.4 apply tableRequest on mainRow
  if (mainRow.tableRequest) {
    try {
      const def = JSON.parse(mainRow.tableRequest);
      const rows = def.map((t) => ({
        Quantity: t.label,
        Value: formatTo3SigFigs(ctx[t.val]) || "",
        Uncertainty: "±" + formatTo3SigFigs(ctx[t.unc]) || "",
      }));
      ctx.dimsTable = makeTable(rows, ["Quantity", "Value", "Uncertainty"]);
    } catch {}
  }

  // 6.5 build mainText/image
  const mainText = window.interpolate(mainRow.mainText || "", ctx);
  const imageBelow = mainRow.imageBelowMain
    ? `<img src="assets/${mainRow.imageBelowMain}.png" style="margin-top:1em;max-width:100%;" />`
    : "";

  const q = { id, type, mainText: mainText + imageBelow, parts: [] };

  // 6.6 build each part
  parts
    .sort((a, b) => +a.partIndex - +b.partIndex)
    .forEach((row) => {
      const local = { ...ctx };

      // per-part computedValues
      if (row.computedValues) {
        try {
          Object.assign(
            local,
            computeValues(local, JSON.parse(row.computedValues))
          );
        } catch {}
      }

      const partText = window.interpolate(row.partText || "", local);
      const modelAnswer = window.interpolate(row.modelAnswer || "", local);
      const explanation = window.interpolate(row.explanation || "", local);
      const marks = buildMarksFromRow(row, local);
      const partObj = { partText, modelAnswer, explanation, marks };

      // --- universal graphSpec support ---
      if (row.graphSpec) {
        // interpolate placeholders then parse JSON
        const specStr = window.interpolate(row.graphSpec, local);
        try {
          partObj.graphSpec = JSON.parse(specStr);
        } catch {
          console.warn("Bad graphSpec in", id, "part", row.partIndex);
        }
      }

      q.parts.push(partObj);
    });

  return q;
}; // scripts/questionBuilders.js

// --- 1) Table-builder helper ---
window.makeTable = function (rows, cols) {
  let html = `<table><tr>${cols.map((c) => `<th>${c}</th>`).join("")}</tr>`;
  rows.forEach((r) => {
    html += `<tr>${cols.map((c) => `<td>${r[c] || ""}</td>`).join("")}</tr>`;
  });
  html += `</table>`;
  return html;
};

// --- 2) String interpolation with 3-sig-fig support ---
window.interpolate = function (str, ctx) {
  return str.replace(/\$\{([^}]+)\}/g, (_, expr) => {
    try {
      const fn = new Function(...Object.keys(ctx), `return ${expr}`);
      const val = fn(...Object.values(ctx));
      return typeof val === "number" ? formatTo3SigFigs(val) : val;
    } catch {
      return "";
    }
  });
};

// --- 3) Format number to 3 significant figures ---
function formatTo3SigFigs(num) {
  if (num === 0) return "0";
  const power = Math.floor(Math.log10(Math.abs(num)));
  const factor = Math.pow(10, 2 - power);
  return (Math.round(num * factor) / factor).toString();
}

// --- 4) Compute derived values (with dependencies) ---
function computeValues(params, formulas) {
  const computed = {};
  for (const key in formulas) {
    try {
      const fn = new Function(
        "params",
        "computed",
        `
        with (params) {
          with (computed) {
            return ${formulas[key]};
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
    const raw = window.interpolate(row[type + "_keywords"] || "", ctx).trim();
    if (!raw) return;

    let parsed = null;
    if (raw.startsWith("[")) {
      try {
        parsed = JSON.parse(raw.replace(/'/g, '"'));
      } catch {}
    }

    let groups = [];
    if (Array.isArray(parsed) && parsed.every((e) => typeof e === "string")) {
      groups = [parsed.map((e) => e.toLowerCase().trim())];
    } else if (Array.isArray(parsed) && parsed.every((g) => Array.isArray(g))) {
      groups = parsed.map((g) => g.map((e) => e.toLowerCase().trim()));
    } else {
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

  // 6.1 Seed ctx with randomized params
  for (const k in params) {
    if (Array.isArray(params[k]) && typeof params[k][0] === "number") {
      const [min, max] = params[k];
      ctx[k] = +(Math.random() * (max - min) + min).toFixed(6);
    } else {
      ctx[k] = params[k];
    }
  }

  // 6.2 Identify mainRow (partIndex=0)
  const mainRow = parts.find((r) => +r.partIndex === 0) || parts[0];

  // 6.3 Apply mainRow computedValues
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

  // 6.4 Apply mainRow tableRequest
  if (mainRow.tableRequest) {
    try {
      const def = JSON.parse(mainRow.tableRequest);
      const tableRows = def.map((t) => ({
        Quantity: t.label,
        Value: formatTo3SigFigs(ctx[t.val]) || "",
        Uncertainty: "±" + formatTo3SigFigs(ctx[t.unc]) || "",
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

  // 6.5 Build mainText & imageBelowMain
  const mainText = window.interpolate(mainRow.mainText || "", ctx);
  const imageBelow = mainRow.imageBelowMain
    ? `<img src="assets/${mainRow.imageBelowMain}.png" style="margin-top:1em;max-width:100%;"/>`
    : "";

  const q = { id, type, mainText: mainText + imageBelow, parts: [] };

  // 6.6 Build each part
  parts
    .sort((a, b) => +a.partIndex - +b.partIndex)
    .forEach((row) => {
      const localCtx = { ...ctx };

      // Per-part computedValues
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

      const partText = window.interpolate(row.partText || "", localCtx);
      const modelAnswer = window.interpolate(row.modelAnswer || "", localCtx);
      const explanation = window.interpolate(row.explanation || "", localCtx);
      const marks = buildMarksFromRow(row, localCtx);
      const partObj = { partText, modelAnswer, explanation, marks };

      // --- universal graphSpec support ---
      if (row.graphSpec) {
        // interpolate placeholders then parse JSON
        const specStr = window.interpolate(row.graphSpec, localCtx);
        try {
          partObj.graphSpec = JSON.parse(specStr);
        } catch {
          console.warn("Bad graphSpec in", id, "part", row.partIndex);
        }
      }

      q.parts.push(partObj);
    });

  return q;
};
