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
        Value: formatToSigFigs(ctx[t.val], t.valSf), // For the 'Value' column
        Uncertainty: "±" + formatToSigFigs(ctx[t.unc], t.uncSf), // For the 'Uncertainty' column
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
          if (group.length === 0) return;
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
