// scripts/questions.js

const questions = [
  {
    id: 1,
    type: "long_answer",
    tags: ["mechanics", "density", "errors"],
    dynamic: true,
    question: function() {
      // --- Random measurements in metres ---
      const mass   = (Math.random() * 0.3  + 0.1 ).toFixed(3);   // 0.100–0.400 kg
      const length = (Math.random() * 0.05 + 0.02).toFixed(4);   // 0.0200–0.0700 m
      const width  = (Math.random() * 0.05 + 0.02).toFixed(4);
      const height = (Math.random() * 0.02 + 0.01).toFixed(4);

      // --- Random uncertainties ---
      const massUnc   = (Math.random() * 0.002  + 0.0005).toFixed(4);
      const lengthUnc = (Math.random() * 0.0008 + 0.0002).toFixed(5);
      const widthUnc  = (Math.random() * 0.0008 + 0.0002).toFixed(5);
      const heightUnc = (Math.random() * 0.0008 + 0.0002).toFixed(5);

      // --- Pick two dimensions to display in cm ---
      const dims = [
        { label: "Length (l)",  val: +length, unc: +lengthUnc, unit: "m" },
        { label: "Width (w)",   val: +width,  unc: +widthUnc,  unit: "m" },
        { label: "Height (h)",  val: +height, unc: +heightUnc, unit: "m" }
      ];
      const pick = [];
      while (pick.length < 2) {
        const r = Math.floor(Math.random() * 3);
        if (!pick.includes(r)) pick.push(r);
      }
      dims.forEach((d,i) => {
        if (pick.includes(i)) {
          d.valDisplay   = (d.val * 100).toFixed(2);
          d.uncDisplay   = (d.unc * 100).toFixed(2);
          d.unitDisplay  = "cm";
        } else {
          d.valDisplay   = d.val.toFixed(4);
          d.uncDisplay   = d.unc.toFixed(5);
          d.unitDisplay  = "m";
        }
      });

      // --- Calculations in SI ---
      const volume               = (length * width * height).toFixed(6);
      const density              = (mass / volume).toFixed(0);
      const relMassUnc           = massUnc / mass;
      const relVolUnc            = (lengthUnc/length + widthUnc/width + heightUnc/height);
      const relDenUnc            = relMassUnc + relVolUnc;
      const percentageDensityUnc = (relDenUnc * 100).toFixed(1);

      return {
        mainText: "This question is about determining the density of a metal block.",
        parts: [
          {
            partText: "a) Define density.",
           answer: [
        "mass per unit volume",
        "mass divided by volume",
        "mass per volume",
        "mass divided by unit volume"
      ],
      modelAnswer: "Density is defined as mass per unit volume, i.e. ρ = m/V.",
      explanation: "Density (ρ) represents how much mass there is in each unit of volume.",
      marks: [
        // 1 mark total for any correct definition
        { point: "Correct definition of density", awarded: false }
      ]
          },
          {
            partText:
`<b>b(i)</b> A metal block has the following measurements:<br>
<table>
  <tr><th>Quantity</th><th>Value</th><th>Uncertainty</th></tr>
  <tr><td>${dims[0].label}</td><td>${dims[0].valDisplay} ${dims[0].unitDisplay}</td><td>±${dims[0].uncDisplay} ${dims[0].unitDisplay}</td></tr>
  <tr><td>${dims[1].label}</td><td>${dims[1].valDisplay} ${dims[1].unitDisplay}</td><td>±${dims[1].uncDisplay} ${dims[1].unitDisplay}</td></tr>
  <tr><td>${dims[2].label}</td><td>${dims[2].valDisplay} ${dims[2].unitDisplay}</td><td>±${dims[2].uncDisplay} ${dims[2].unitDisplay}</td></tr>
</table>
Calculate the density of the block.`,
            answer: density.toString(),
            modelAnswer:
`First calculate volume: V = l × w × h = ${length} × ${width} × ${height} = ${volume} m³.<br>
Then ρ = m/V = ${mass}/${volume} = ${density} kg/m³.`,
            explanation:
"You must first find the volume from the three dimensions (ensure any cm values are converted back to m).<br>"
+ "Then use ρ = m/V with mass in kg and volume in m³ to get density in kg/m³.",
            marks: [
              { point: "Formulas for both volume (V=l×w×h) and density (ρ=m/V)", awarded: false },
           { point: "Correct final numerical answer",                             awarded: false }

            ]
          },
          {
            partText: "b(ii) Calculate the percentage uncertainty in the density.",
            answer: percentageDensityUnc.toString(),
            modelAnswer:
`Relative uncertainty in mass = ${relMassUnc.toFixed(3)}<br>
Relative uncertainty in volume = ${relVolUnc.toFixed(3)}<br>
Total relative uncertainty = ${relDenUnc.toFixed(3)}<br>
Percentage uncertainty = ${percentageDensityUnc}%`,
            explanation:
"Sum the fractional uncertainties: mass fraction + volume fraction, then ×100 to get percentage uncertainty.",
            marks: [
              { point: "Method for combining uncertainties", awarded: false },
              { point: "Correct final percentage uncertainty", awarded: false }
              { point: "Working out one fractional uncertainty (e.g. Δm/m)", awarded: false }
            ]
          },
          {
            partText: "c) Suggest one possible systematic error affecting the mass or dimensions.",
            answer: "zero error or incorrect calibration",
            modelAnswer: "A systematic zero-error on the balance or calipers (or a mis-calibrated instrument).",
            explanation: "Systematic errors shift all measurements by the same amount, e.g. a zero offset on the balance or caliper.",
            marks: [
              { point: "Identified valid systematic error", awarded: false }
            ]
          }
        ],
        diagram: null
      };
    }
  }
]; // end of questions array
