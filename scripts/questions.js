const questions = [
  {
    id: 1,
    type: "long_answer",
    tags: ["mechanics", "density", "errors"],
    dynamic: true,
    question: function() {
    // Random values
    const mass = (Math.random() * 0.3 + 0.1).toFixed(3); // between 0.1 kg and 0.4 kg
    const length = (Math.random() * 0.05 + 0.02).toFixed(4); // between 0.02 m and 0.07 m
    const width = (Math.random() * 0.05 + 0.02).toFixed(4);
    const height = (Math.random() * 0.02 + 0.01).toFixed(4);

    // Uncertainties (small % of value)
    const massUnc = 0.001; // fixed ±0.001 kg
    const lengthUnc = 0.0005; // ±0.0005 m
    const widthUnc = 0.0005;
    const heightUnc = 0.0005;

    // Calculations
    const volume = (length * width * height).toFixed(6);
    const density = (mass / volume).toFixed(0); // nearest kg/m³

    const relMassUnc = (massUnc / mass);
    const relLengthUnc = (lengthUnc / length);
    const relWidthUnc = (widthUnc / width);
    const relHeightUnc = (heightUnc / height);

    const relVolumeUnc = relLengthUnc + relWidthUnc + relHeightUnc;
    const relDensityUnc = (relMassUnc + relVolumeUnc);
    const percentageDensityUnc = (relDensityUnc * 100).toFixed(1); // 1 d.p.

    return {
      mainText: "This question is about determining the density of a metal block.",

      parts: [
        {
          partText: "a) Define density.",
          answer: "mass per unit volume",
          modelAnswer: "Density is defined as mass per unit volume: \\( \\rho = \\frac{m}{V} \\)",
          marks: [
            { point: "Mentioned mass", awarded: false },
            { point: "Mentioned volume", awarded: false }
          ]
        },
        {
          partText: `b)(i) A metal block has a mass of ${mass} kg, and dimensions ${length} m × ${width} m × ${height} m. Calculate the density of the block.`,
          answer: density.toString(),
          modelAnswer: `Volume = ${length} × ${width} × ${height} = ${volume} \\( \\text{m}^3 \\)  
Then \\( \\rho = \\frac{${mass}}{${volume}} = ${density} \\text{ kg/m}^3 \\)`,
          marks: [
            { point: "Correct formula used for volume", awarded: false },
            { point: "Correct formula used for density", awarded: false },
            { point: "Correct final answer", awarded: false }
          ]
        },
        {
          partText: `b)(ii) Calculate the percentage uncertainty in the density.`,
          answer: percentageDensityUnc.toString(),
          modelAnswer: `Relative uncertainty in mass = \\( \\frac{${massUnc}}{${mass}} \\)  
Relative uncertainty in volume = sum of relative uncertainties in dimensions.  
Total relative uncertainty = ${relDensityUnc.toFixed(3)}  
Percentage uncertainty = ${percentageDensityUnc}%`,
          marks: [
            { point: "Correct method for combining uncertainties", awarded: false },
            { point: "Correct final percentage uncertainty", awarded: false }
          ]
        },
        {
          partText: `c) Suggest one possible systematic error affecting the mass or dimensions measured.`,
          answer: "zero error or incorrect calibration",
          modelAnswer: "Possible systematic errors include a zero error on the calipers or balance, or incorrect calibration of the measuring devices.",
          marks: [
            { point: "Identified valid systematic error", awarded: false }
          ]
        }
      ],

      diagram: function(canvas) {
        // Optional: Could draw a simple block sketch if wanted later
      }
    };
  }
}
  ];
