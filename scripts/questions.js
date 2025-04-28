const questions = [
  {
    id: 1,
    type: "long_answer",
    tags: ["mechanics", "density", "errors"],
    dynamic: true,
    question: function() {
      // --- Random measurements ---
      const mass    = (Math.random() * 0.3  + 0.1  ).toFixed(3);  // 0.100–0.400 kg
      const length  = (Math.random() * 0.05 + 0.02 ).toFixed(4);  // 0.0200–0.0700 m
      const width   = (Math.random() * 0.05 + 0.02 ).toFixed(4);
      const height  = (Math.random() * 0.02 + 0.01 ).toFixed(4);

      // --- Dynamic uncertainties ---
      const massUnc    = (Math.random() * 0.002 + 0.0005).toFixed(4);   // ±0.0005–0.0025 kg
      const lengthUnc  = (Math.random() * 0.0008 + 0.0002).toFixed(5);  // ±0.00020–0.00100 m
      const widthUnc   = (Math.random() * 0.0008 + 0.0002).toFixed(5);
      const heightUnc  = (Math.random() * 0.0008 + 0.0002).toFixed(5);

      // --- Calculations ---
      const volume               = (length * width * height).toFixed(6);
      const density              = (mass / volume).toFixed(0);      // nearest kg/m³
      const relMassUnc           = massUnc / mass;
      const relLengthUnc         = lengthUnc / length;
      const relWidthUnc          = widthUnc  / width;
      const relHeightUnc         = heightUnc / height;
      const relVolumeUnc         = relLengthUnc + relWidthUnc + relHeightUnc;
      const relDensityUnc        = relMassUnc + relVolumeUnc;
      const percentageDensityUnc = (relDensityUnc * 100).toFixed(1);

      return {
        mainText: "This question is about determining the density of a metal block.",

        parts: [
          {
            partText: "a) Define density.",
            answer: "mass per unit volume",
            modelAnswer: "Density is defined as mass per unit volume: \\(\\rho = \\tfrac{m}{V}\\).",
            marks: [
              { point: "Mentioned mass",    awarded: false },
              { point: "Mentioned volume",  awarded: false }
            ]
          },
          {
            partText: `<b>b(i)</b> A metal block has the following measurements:<br>
<table>
  <tr><th>Quantity</th><th>Value</th><th>Uncertainty</th></tr>
  <tr><td>Mass (m)</td><td>${mass} kg</td><td>±${massUnc} kg</td></tr>
  <tr><td>Length (l)</td><td>${length} m</td><td>±${lengthUnc} m</td></tr>
  <tr><td>Width (w)</td><td>${width} m</td><td>±${widthUnc} m</td></tr>
  <tr><td>Height (h)</td><td>${height} m</td><td>±${heightUnc} m</td></tr>
</table>
Calculate the density of the block.`,
            answer: density.toString(),
            modelAnswer: `Volume = ${length} × ${width} × ${height} = ${volume} m³<br>
Then \\(\\rho = \\frac{${mass}}{${volume}} = ${density}\\,\\text{kg/m}^3\\).`,
            marks: [
              { point: "Correct formula for volume",    awarded: false },
              { point: "Correct formula for density",   awarded: false },
              { point: "Correct final answer",          awarded: false }
            ]
          },
          {
            partText: "b(ii) Calculate the percentage uncertainty in the density.",
            answer: percentageDensityUnc.toString(),
            modelAnswer: `Relative uncertainty in mass = ${relMassUnc.toFixed(3)}<br>
Relative uncertainty in volume = ${relVolumeUnc.toFixed(3)}<br>
Total relative uncertainty = ${relDensityUnc.toFixed(3)}<br>
Percentage uncertainty = ${percentageDensityUnc}%`,
            marks: [
              { point: "Method for combining uncertainties", awarded: false },
              { point: "Correct final percentage",            awarded: false }
            ]
          },
          {
            partText: "c) Suggest one possible systematic error affecting the mass or dimensions.",
            answer: "zero error or incorrect calibration",
            modelAnswer: "A possible systematic error is a zero‐error on the balance or calipers, or incorrect calibration of the measuring device.",
            marks: [
              { point: "Identified a valid systematic error", awarded: false }
            ]
          }
        ],

        diagram: function(canvas) {
          // no diagram for this question
        }
      };
    }
  }
];

