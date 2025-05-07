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

  // 6.4 apply tableRequest on main
  if (mainRow.tableRequest) {
    try {
      const tableDef = JSON.parse(mainRow.tableRequest);
      const tableRows = tableDef.map((t) => ({
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

  // assemble mainText + imageBelowMain
  const mainText = interpolate(mainRow.mainText || "", ctx);
  const imageBelow = mainRow.imageBelowMain
    ? `<img src="assets/${mainRow.imageBelowMain}.png" style="margin-top:1em;max-width:100%;" />`
    : "";

  const q = { id, type, mainText: mainText + imageBelow, parts: [] };

  // 6.5 build each part
  parts
    .sort((a, b) => +a.partIndex - +b.partIndex)
    .forEach((row) => {
      const local = { ...ctx };

      // apply computedValues per part
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

      // ── AUTO-EXPAND GENERIC NUMERIC SYNONYMS ──
      partObj.marks.forEach((mark) => {
        if (mark.type !== "A") return;
        mark.keywords.forEach((group) => {
          const base = parseFloat(group[0].replace(/[^0-9eE+\-.]/g, ""));
          if (isNaN(base)) return;
          const sf2 = base.toPrecision(2);
          const exp2 = base.toExponential(2).replace(/e\+?/, "×10^");
          const intRnd = Math.round(base).toString();
          const dec1 = base.toFixed(1);
          const plain = base.toString();
          [sf2, exp2, intRnd, dec1, plain].forEach((v) => {
            const low = v.toLowerCase().trim();
            if (low && !group.includes(low)) group.push(low);
          });
        });
      });

      // ── auto-graph for stress-strain with a small plastic plateau ───
      if (type === "stress-strain" && +row.partIndex === 0) {
        const s = local.max_strain; // εₘₐₓ from computedValues
        const m = local.module_plot; // E (Young’s modulus)
        const σ_limit = s * m; // yield stress
        const plateauWidth = 0.002; // horizontal plateau length

        partObj.graphSpec = {
          points: [
            [0, 0],
            [s, σ_limit],
            [s + plateauWidth, σ_limit],
          ],
          xMax: s + plateauWidth,
          yMax: σ_limit * 1.1,
          xLabel: "Strain",
          yLabel: "Stress (Pa)",
          xTicks: [0, s, s + plateauWidth],
          yTicks: [0, σ_limit],
        };
      }

      q.parts.push(partObj);
    });

  return q;
};
