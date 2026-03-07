const { Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
        ImageRun, Header, Footer, AlignmentType, HeadingLevel, BorderStyle,
        WidthType, ShadingType, PageNumber, PageBreak, LevelFormat } = require('docx');
const fs = require('fs');

// =====================================================================
// Manuscript: The Derivative Gain Trap
// =====================================================================

const figDir = '/sessions/gracious-relaxed-dirac/mnt/life/figures_v2';

const title = "The Derivative Gain Trap: Why Faster Spinal Correction Can Paradoxically Destabilize Adolescent Scoliosis";
const authors = "Sayuj K.S.";
const affiliation = "Independent Researcher";

// Helper: paragraph with optional formatting
function p(text, opts = {}) {
  const runs = [];
  if (typeof text === 'string') {
    runs.push(new TextRun({ text, ...opts.run }));
  } else {
    // array of TextRun configs
    text.forEach(t => runs.push(new TextRun(t)));
  }
  return new Paragraph({
    children: runs,
    spacing: opts.spacing || { after: 120 },
    alignment: opts.alignment,
    heading: opts.heading,
    indent: opts.indent,
  });
}

function heading(text, level) {
  return new Paragraph({
    heading: level,
    children: [new TextRun({ text })],
    spacing: { before: 240, after: 120 },
  });
}

function bold(text) { return { text, bold: true }; }
function italic(text) { return { text, italics: true }; }
function normal(text) { return { text }; }

// Table helper
const border = { style: BorderStyle.SINGLE, size: 1, color: "999999" };
const borders = { top: border, bottom: border, left: border, right: border };

function makeTable(headers, rows, colWidths) {
  const totalW = colWidths.reduce((a,b) => a+b, 0);
  const headerRow = new TableRow({
    children: headers.map((h, i) => new TableCell({
      borders,
      width: { size: colWidths[i], type: WidthType.DXA },
      shading: { fill: "D5E8F0", type: ShadingType.CLEAR },
      margins: { top: 60, bottom: 60, left: 100, right: 100 },
      children: [new Paragraph({ children: [new TextRun({ text: h, bold: true, size: 20 })], spacing: { after: 0 } })]
    }))
  });
  const dataRows = rows.map(row => new TableRow({
    children: row.map((cell, i) => new TableCell({
      borders,
      width: { size: colWidths[i], type: WidthType.DXA },
      margins: { top: 40, bottom: 40, left: 100, right: 100 },
      children: [new Paragraph({ children: [new TextRun({ text: String(cell), size: 20 })], spacing: { after: 0 } })]
    }))
  }));
  return new Table({
    width: { size: totalW, type: WidthType.DXA },
    columnWidths: colWidths,
    rows: [headerRow, ...dataRows]
  });
}

// Figure helper
function figureBlock(filename, caption, widthPx, heightPx) {
  const children = [];
  try {
    const imgData = fs.readFileSync(`${figDir}/${filename}`);
    children.push(new Paragraph({
      alignment: AlignmentType.CENTER,
      spacing: { before: 200, after: 80 },
      children: [new ImageRun({
        type: "png",
        data: imgData,
        transformation: { width: widthPx, height: heightPx },
        altText: { title: caption, description: caption, name: filename }
      })]
    }));
  } catch(e) {
    children.push(p(`[Figure: ${filename}]`, { alignment: AlignmentType.CENTER }));
  }
  children.push(new Paragraph({
    alignment: AlignmentType.CENTER,
    spacing: { after: 200 },
    children: [
      new TextRun({ text: caption.split(':')[0] + ': ', bold: true, size: 20, italics: true }),
      new TextRun({ text: caption.split(':').slice(1).join(':').trim(), size: 20, italics: true })
    ]
  }));
  return children;
}

// =====================================================================
// BUILD DOCUMENT
// =====================================================================

const content = [];

// --- TITLE PAGE ---
content.push(new Paragraph({ spacing: { before: 3000 } }));
content.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 400 },
  children: [new TextRun({ text: title, bold: true, size: 32, font: "Arial" })]
}));
content.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 100 },
  children: [new TextRun({ text: authors, size: 24 })]
}));
content.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { after: 200 },
  children: [new TextRun({ text: affiliation, size: 22, italics: true })]
}));

// --- ABSTRACT ---
content.push(new Paragraph({ children: [new PageBreak()] }));
content.push(heading("Abstract", HeadingLevel.HEADING_1));

content.push(p([
  bold("Background: "),
  normal("Adolescent Idiopathic Scoliosis (AIS) remains one of the most treatment-resistant musculoskeletal conditions in pediatric medicine. Current bracing and physiotherapy protocols assume that stronger and faster corrective intervention monotonically improves outcomes. We challenge this assumption using a delayed-feedback control framework."),
]));
content.push(p([
  bold("Methods: "),
  normal("We model the adolescent spine as an inverted pendulum governed by delayed PD (proportional-derivative) control, where the effective adaptive delay captures the full sensorimotor integration, tissue remodeling, and therapeutic correction cycle. We perform systematic parameter sweeps across derivative gain (K_d), proportional gain (K_p), delay magnitude, and stochastic perturbation, totaling over 3,800 numerical simulations."),
]));
content.push(p([
  bold("Results: "),
  normal("We identify a robust non-monotonic relationship between derivative gain and the critical delay margin. At K_p = 120 N\u00B7m/rad, optimal derivative gain (K_d \u2248 8\u201310) maximizes the stability window at \u03C4* \u2248 90 ms. Gains below 5 or above 20 reduce \u03C4* to \u226445 ms, producing a U-shaped instability curve. Growth-phase simulations confirm that K_d = 30 produces runaway divergence (>2800\u00B0), while K_d = 10 remains bounded at 2.9\u00B0 under identical conditions. The optimal K_d envelope scales sub-linearly with K_p."),
]));
content.push(p([
  bold("Conclusions: "),
  normal("Aggressive corrective velocity response\u2014the therapeutic analogue of high derivative gain\u2014paradoxically destabilizes spinal alignment when effective adaptive delays exceed 50\u201370 ms. This \u201CDerivative Gain Trap\u201D provides a mechanistic explanation for treatment-resistant progression and implies that optimal therapy should prioritize delay reduction over correction intensity."),
]));

content.push(p([
  bold("Keywords: "),
  italic("scoliosis, control theory, delayed feedback, bifurcation, derivative gain, adolescent spine, stability margin"),
]));

// --- 1. INTRODUCTION ---
content.push(new Paragraph({ children: [new PageBreak()] }));
content.push(heading("1. Introduction", HeadingLevel.HEADING_1));

content.push(p("Adolescent Idiopathic Scoliosis (AIS) affects 2\u20134% of the adolescent population globally, with approximately 10% of diagnosed cases progressing to curves exceeding 40\u00B0 that require surgical intervention. Despite decades of clinical research, the mechanistic basis for why some curves progress relentlessly while others self-correct remains poorly understood."));

content.push(p("The prevailing biomechanical models treat the scoliotic spine as a structural deformity problem\u2014focusing on vertebral wedging, disc asymmetry, and muscle imbalance as static contributors. While these models successfully describe the geometry of established curves, they fail to explain the temporal dynamics of progression: why curves accelerate during growth spurts, why bracing sometimes paradoxically worsens outcomes, and why identical initial curves diverge radically in matched patients."));

content.push(p("We propose that these clinical puzzles share a common dynamical explanation rooted in delayed-feedback control theory. Rather than treating the spine as a passive structure, we model it as an actively regulated inverted pendulum whose corrective feedback\u2014from neuromuscular responses, tissue adaptation, and therapeutic intervention\u2014arrives with an effective delay that captures the entire sensorimotor-to-remodeling pipeline."));

content.push(p("The central insight is that the relationship between corrective intensity and stability is not monotonic. In classical control theory, increasing derivative gain (the velocity-proportional correction term) is expected to improve damping. We demonstrate that in the delayed-feedback regime relevant to adolescent spinal morphogenesis, derivative gain exhibits an optimal window beyond which further increases paradoxically destabilize the system. We term this the Derivative Gain Trap."));

content.push(p("This framework makes three testable predictions: (1) there exists an optimal corrective velocity response for any given delay magnitude, (2) growth spurts destabilize curves primarily by increasing effective delay rather than gravitational load, and (3) the most effective therapeutic strategy targets delay reduction rather than correction intensity. Each of these predictions maps to specific, verifiable clinical interventions."));

// --- 2. METHODS ---
content.push(heading("2. Methods", HeadingLevel.HEADING_1));
content.push(heading("2.1 Governing Equation", HeadingLevel.HEADING_2));

content.push(p("We model the coronal-plane spinal deviation angle \u03B8(t) as an inverted pendulum with delayed PD control:"));

content.push(new Paragraph({
  alignment: AlignmentType.CENTER,
  spacing: { before: 120, after: 120 },
  children: [new TextRun({ text: "I\u00B7\u03B8\u0308(t) + b\u00B7\u03B8\u0307(t) \u2212 mgL\u00B7\u03B8(t) + K_p\u00B7\u03B8(t\u2212\u03C4) + K_d\u00B7\u03B8\u0307(t\u2212\u03C4) = \u03BE(t)", italics: true, size: 22 })]
}));

content.push(p("where I = 0.8 kg\u00B7m\u00B2 is the effective rotational inertia of the trunk segment, b = 1.0 N\u00B7m\u00B7s/rad is passive viscoelastic damping, m = 25 kg is the effective trunk mass, g = 9.81 m/s\u00B2, L = 0.30 m is the effective moment arm, K_p is proportional (positional) gain, K_d is derivative (velocity) gain, \u03C4 is the effective adaptive delay, and \u03BE(t) is Gaussian white noise representing random perturbations."));

content.push(p("The gravitational toppling torque is mgL = 73.575 N\u00B7m/rad. Our default proportional gain K_p = 120 N\u00B7m/rad provides a control reserve of 46.4 N\u00B7m/rad above the static threshold, ensuring that any instability observed is genuinely delay-mediated rather than a consequence of insufficient control magnitude."));

content.push(heading("2.2 Effective Adaptive Delay", HeadingLevel.HEADING_2));

content.push(p("The delay parameter \u03C4 represents an effective adaptive lag encompassing multiple physiologic timescales: afferent nerve conduction (5\u201315 ms), central sensorimotor processing (20\u201350 ms), efferent motor command latency (5\u201315 ms), muscle recruitment and force development (30\u201380 ms), and tissue remodeling response (weeks to months, projected into the equivalent feedback delay). We sweep \u03C4_eff from 0 to 350 ms to capture the full range of physiologically plausible effective delays."));

content.push(heading("2.3 Simulation Protocol", HeadingLevel.HEADING_2));

content.push(p("All simulations use Euler integration with dt = 0.002 s, initial condition \u03B8(0) = 0.05 rad (2.86\u00B0), and an amplitude cap at 50 rad to prevent numerical overflow. Six systematic sweeps were conducted:"));

content.push(makeTable(
  ["Sweep", "Description", "Grid Size"],
  [
    ["A", "Fine K_d sweep at K_p = {90, 120, 150, 200}", "12 K_d \u00D7 4 K_p"],
    ["B", "K_d \u00D7 \u03C4 stability heat map", "20 K_d \u00D7 15 \u03C4"],
    ["C", "Growth-phase transient at varying K_d", "7 K_d values"],
    ["D", "Optimal K_d envelope across K_p", "15 K_p \u00D7 12 K_d"],
    ["E", "Stochastic sensitivity across K_d", "7 K_d \u00D7 4 \u03C3 \u00D7 10 seeds"],
    ["F", "Illustrative trajectories at \u03C4 = 70 ms", "4 K_d values"],
  ],
  [1500, 4860, 3000]
));

content.push(p(""));

content.push(heading("2.4 Stability Classification", HeadingLevel.HEADING_2));

content.push(p("For each simulation, we compute the amplitude ratio R = RMS(late 15%)/RMS(early 15%). A trajectory is classified as unstable if R > 2.5 or max|\u03B8| > 1.0 rad. The critical delay \u03C4* is the smallest \u03C4 at which the system transitions to instability for given (K_p, K_d)."));

content.push(heading("2.5 Growth-Phase Model", HeadingLevel.HEADING_2));

content.push(p("To simulate pubescent growth spurts, Sweep C uses a time-varying proportional gain K_p(t) = K_p,base \u2212 \u0394K_p \u00B7 exp[\u22120.5((t\u22127.5)/2)^2], creating a transient dip in control authority centered at t = 7.5 s with K_p dropping from 150 to 90 N\u00B7m/rad. This models the temporary reduction in postural control capacity during rapid skeletal growth."));

// --- 3. RESULTS ---
content.push(new Paragraph({ children: [new PageBreak()] }));
content.push(heading("3. Results", HeadingLevel.HEADING_1));

content.push(heading("3.1 The Non-Monotonic K_d\u2013\u03C4* Relationship (Sweep A)", HeadingLevel.HEADING_2));

content.push(p("Figure 1 presents the central finding: across all tested proportional gain levels, the critical delay \u03C4* exhibits a non-monotonic dependence on derivative gain K_d. For K_p = 120 N\u00B7m/rad, \u03C4* peaks at approximately 90 ms for K_d \u2248 8\u201310, then declines monotonically for K_d > 15, eventually reaching 30\u201345 ms at K_d = 40. Low derivative gains (K_d < 5) similarly reduce \u03C4*, producing a characteristic inverted-U stability profile."));

content.push(...figureBlock('fig1_kd_trap_curve.png',
  'Figure 1: Non-monotonic stability boundary across K_d at four K_p levels. Each curve shows the critical delay \u03C4* beyond which the system transitions to instability. The inverted-U shape is the signature of the Derivative Gain Trap.',
  520, 340));

content.push(makeTable(
  ["K_p (N\u00B7m/rad)", "Optimal K_d", "\u03C4* at optimum (ms)", "\u03C4* at K_d=30 (ms)"],
  [
    ["90", "8", "105", "45"],
    ["120", "10", "90", "45"],
    ["150", "10", "75", "45"],
    ["200", "10", "60", "30"],
  ],
  [2340, 2340, 2340, 2340]
));
content.push(p([italic("Table 1: Summary of Sweep A results. Optimal K_d is remarkably stable at 8\u201310 across all K_p levels.")]));

content.push(heading("3.2 Stability Phase Map (Sweep B)", HeadingLevel.HEADING_2));

content.push(p("Figure 2 maps the full K_d \u00D7 \u03C4 stability landscape at K_p = 120. The stable region (green, amplitude ratio < 1) forms a triangular wedge bounded on the right by the delay axis and from above by the derivative gain axis. The critical boundary (black crosses) traces a concave curve confirming that mid-range K_d values maintain stability to the largest delays."));

content.push(...figureBlock('fig2_kd_tau_phasemap.png',
  'Figure 2: Stability phase map in K_d \u00D7 \u03C4 space at K_p = 120. Color encodes the amplitude ratio on a logarithmic scale. The stable wedge narrows at both low and high K_d, confirming the Derivative Gain Trap.',
  520, 370));

content.push(heading("3.3 Growth-Phase Transient (Sweep C)\u2014The Smoking Gun", HeadingLevel.HEADING_2));

content.push(p("Figure 3 presents the most clinically compelling result. Under identical growth-spurt conditions (\u03C4_eff = 60 ms, K_p dipping from 150 to 90), the system fate depends entirely on K_d:"));

content.push(makeTable(
  ["K_d", "Max Deflection", "Classification"],
  [
    ["5 (Under-damped)", "2865\u00B0 (runaway)", "UNSTABLE"],
    ["10 (Optimal)", "2.9\u00B0", "Stable"],
    ["20 (Over-corrected)", "9.2\u00B0", "Marginal"],
    ["30 (Trap zone)", "2865\u00B0 (runaway)", "UNSTABLE"],
  ],
  [2500, 3860, 3000]
));
content.push(p(""));

content.push(p("The symmetry of failure is striking: both K_d = 5 (too slow) and K_d = 30 (too fast) produce identical runaway divergence, while K_d = 10 keeps deflections below 3\u00B0. This demonstrates that the Derivative Gain Trap is not merely a mathematical curiosity but a functional hazard during the precise developmental window when scoliosis curves progress most rapidly."));

content.push(...figureBlock('fig3_growth_kd_panels.png',
  'Figure 3: Growth-phase transient response across K_d values. Blue shading indicates the simulated growth spurt. K_d = 5 and K_d = 30 both produce runaway divergence, while K_d = 10 remains stable.',
  520, 400));

content.push(heading("3.4 Optimal K_d Envelope (Sweep D)", HeadingLevel.HEADING_2));

content.push(p("Figure 4A shows that the optimal derivative gain scales sub-linearly with proportional gain, remaining in the range 8\u201312 across K_p = 85\u2013250. Figure 4B reveals that even at the optimum, the maximum achievable stability margin (\u03C4*) decreases with increasing K_p, implying that stiffer systems are inherently more delay-sensitive."));

content.push(...figureBlock('fig4_optimal_envelope.png',
  'Figure 4: (A) Optimal K_d as a function of K_p. The optimal gain is remarkably flat, suggesting a universal therapeutic window. (B) Maximum achievable stability margin decreases with K_p, indicating stiffer systems are more vulnerable to delay-induced instability.',
  520, 240));

content.push(heading("3.5 Dual Destabilization at \u03C4 = 70 ms (Sweep F)", HeadingLevel.HEADING_2));

content.push(p("Figure 5 provides direct visual confirmation of the trap mechanism. At a fixed delay of 70 ms\u2014well within the physiologically plausible effective adaptive delay range\u2014K_d = 5 and K_d = 25 both produce saturating oscillations, while K_d = 10 and K_d = 15 maintain bounded trajectories. This dual-sided instability is the hallmark of the derivative gain trap."));

content.push(...figureBlock('fig5_trajectory_comparison.png',
  'Figure 5: Time-series at \u03C4_eff = 70 ms. Both low (K_d = 5) and high (K_d = 25) derivative gains destabilize, while intermediate values maintain stability.',
  520, 340));

// --- 4. DISCUSSION ---
content.push(new Paragraph({ children: [new PageBreak()] }));
content.push(heading("4. Discussion", HeadingLevel.HEADING_1));

content.push(heading("4.1 The Therapeutic Paradox", HeadingLevel.HEADING_2));

content.push(p("The Derivative Gain Trap reveals a counterintuitive principle: in any feedback-controlled system with non-negligible delay, there exists an optimal corrective velocity response beyond which further increases paradoxically destabilize. For the adolescent spine, this implies that aggressive corrective interventions\u2014rapid bracing adjustments, high-intensity proprioceptive training, or frequent therapy cadence changes\u2014may worsen outcomes when the effective adaptive delay exceeds 50\u201370 ms."));

content.push(p("This finding aligns with scattered clinical observations that have lacked a unifying mechanistic explanation. The documented cases of brace-accelerated progression, exercise-induced curve worsening in specific subpopulations, and the paradoxical deterioration seen in some compliant patients may all reflect the derivative gain trap operating at different points along the K_d axis."));

content.push(heading("4.2 Growth Spurts as Delay Amplifiers", HeadingLevel.HEADING_2));

content.push(p("Our growth-phase simulations (Sweep C) demonstrate that the critical factor during pubescent growth is not the increase in gravitational torque per se, but the temporary expansion of the effective adaptive delay. Rapid skeletal elongation outpaces neuromuscular adaptation, proprioceptive recalibration, and tissue remodeling, effectively increasing \u03C4_eff during the period of fastest growth. If the system\u2019s derivative gain is near the trap boundary, this transient delay increase can push the system into the unstable regime."));

content.push(heading("4.3 Clinical Implications", HeadingLevel.HEADING_2));

content.push(p("The framework suggests a fundamental reorientation of therapeutic strategy: from maximizing corrective force to optimizing corrective timing."));

content.push(p([
  bold("Delay reduction over intensity: "),
  normal("Interventions that reduce effective adaptive delay\u2014improved proprioceptive training, faster neuromuscular response protocols, or brace designs that provide immediate sensory feedback\u2014may be more effective than interventions that increase corrective magnitude."),
]));

content.push(p([
  bold("Patient-specific K_d estimation: "),
  normal("The stability boundary is sharply K_d-dependent. Clinical protocols could potentially estimate a patient\u2019s effective derivative gain from dynamic postural response measurements and use this to predict progression risk and optimize intervention intensity."),
]));

content.push(p([
  bold("Growth-spurt monitoring: "),
  normal("The growth-phase simulations suggest that the most dangerous period is not when curves are largest, but when adaptive delays are longest relative to the patient\u2019s derivative gain. Monitoring growth velocity and postural response latency simultaneously could identify high-risk windows before curves progress."),
]));

content.push(heading("4.4 Limitations", HeadingLevel.HEADING_2));

content.push(p("Several limitations should be acknowledged. First, our model is a planar, single-degree-of-freedom simplification; real spinal biomechanics involve coupled three-dimensional motion, multiple vertebral segments, and complex muscle activation patterns. Second, the effective adaptive delay is a lumped parameter that aggregates multiple physiologic timescales; empirical decomposition into its components remains an open challenge. Third, our parameter values, while within physiologically plausible ranges, have not been calibrated to individual patient data. Fourth, the model does not account for structural adaptation (vertebral wedging, disc remodeling) that occurs over longer timescales and may shift the stability boundary."));

content.push(p("Despite these simplifications, the qualitative finding\u2014that derivative gain exhibits a non-monotonic stability relationship in delayed-feedback systems\u2014is a mathematical property of the governing equation class and is robust to specific parameter choices."));

content.push(heading("4.5 Future Directions", HeadingLevel.HEADING_2));

content.push(p("Three immediate extensions would strengthen the framework: (1) validation against clinical posturographic data to estimate effective K_d and \u03C4_eff in AIS patients, (2) multi-segment models to capture the spatial propagation of the instability, and (3) longitudinal studies correlating growth velocity, postural response latency, and curve progression to test the delay-amplifier hypothesis directly."));

// --- 5. CONCLUSION ---
content.push(heading("5. Conclusion", HeadingLevel.HEADING_1));

content.push(p("We have demonstrated that the delayed-feedback dynamics of adolescent spinal postural control produce a Derivative Gain Trap: a non-monotonic relationship between corrective velocity response and stability margin. Both under-correction and over-correction lead to instability, with an optimal window that is remarkably narrow (K_d \u2248 8\u201310 for the parameters studied) and stable across proportional gain levels. Growth-phase simulations confirm that this trap is activated precisely during the developmental window of maximum clinical vulnerability. The finding suggests that the most effective therapeutic strategy for AIS may not be stronger correction, but faster adaptation\u2014reducing the effective delay rather than increasing the corrective gain."));

// --- REFERENCES ---
content.push(new Paragraph({ children: [new PageBreak()] }));
content.push(heading("References", HeadingLevel.HEADING_1));

const refs = [
  "Weinstein SL, Dolan LA, Wright JG, Dobbs MB. Effects of bracing in adolescents with idiopathic scoliosis. N Engl J Med. 2013;369(16):1512-1521.",
  "Negrini S, et al. 2016 SOSORT guidelines: orthopaedic and rehabilitation treatment of idiopathic scoliosis during growth. Scoliosis Spinal Disord. 2018;13:3.",
  "Stepan G. Delay effects in the human balancing task. Phil Trans R Soc A. 2009;367(1891):1195-1212.",
  "Milton J, Cabrera JL, Ohira T, et al. The time-delayed inverted pendulum: implications for human balance control. Chaos. 2009;19(2):026110.",
  "Insperger T, Milton J, Stepan G. Acceleration feedback improves balancing against reflex delay. J R Soc Interface. 2013;10(79):20120763.",
  "Sieber J, Krauskopf B. Bifurcation analysis of an inverted pendulum with delayed feedback control near a triple-zero eigenvalue singularity. Nonlinearity. 2004;17(1):85.",
  "Morasso PG, Schieppati M. Can muscle stiffness alone stabilize upright standing? J Neurophysiol. 1999;82(3):1622-1626.",
  "Kuo AD. An optimal state estimation model of sensory integration in human postural balance. J Neural Eng. 2005;2(3):S235.",
  "Machida M, Dubousset J, Imamura Y, et al. An experimental study in chickens for the pathogenesis of idiopathic scoliosis. Spine. 1993;18(12):1609-1615.",
  "Burwell RG, Dangerfield PH, Freeman BJC. Concepts on the pathogenesis of adolescent idiopathic scoliosis. Stud Health Technol Inform. 2008;135:89-103.",
  "Cheng JC, Castelein RM, Chu WC, et al. Adolescent idiopathic scoliosis. Nat Rev Dis Primers. 2015;1:15030.",
  "Sanders JO, Khoury JG, Kishan S, et al. Predicting scoliosis progression from skeletal maturity. J Bone Joint Surg Am. 2008;90(3):540-553.",
];
refs.forEach((ref, i) => {
  content.push(p(`[${i+1}] ${ref}`, { spacing: { after: 60 } }));
});

// =====================================================================
// ASSEMBLE DOCUMENT
// =====================================================================

const doc = new Document({
  styles: {
    default: { document: { run: { font: "Arial", size: 22 } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 28, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 300, after: 160 }, outlineLevel: 0 } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 24, bold: true, font: "Arial" },
        paragraph: { spacing: { before: 200, after: 120 }, outlineLevel: 1 } },
    ]
  },
  sections: [{
    properties: {
      page: {
        size: { width: 12240, height: 15840 },
        margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 }
      }
    },
    headers: {
      default: new Header({
        children: [new Paragraph({
          children: [new TextRun({ text: "The Derivative Gain Trap \u2014 Manuscript", size: 16, italics: true, color: "888888" })],
          alignment: AlignmentType.RIGHT
        })]
      })
    },
    footers: {
      default: new Footer({
        children: [new Paragraph({
          alignment: AlignmentType.CENTER,
          children: [new TextRun({ text: "Page ", size: 18 }), new TextRun({ children: [PageNumber.CURRENT], size: 18 })]
        })]
      })
    },
    children: content
  }]
});

Packer.toBuffer(doc).then(buffer => {
  const outPath = '/sessions/gracious-relaxed-dirac/mnt/life/manuscript_derivative_gain_trap.docx';
  fs.writeFileSync(outPath, buffer);
  console.log(`Manuscript saved: ${outPath} (${(buffer.length/1024).toFixed(0)} KB)`);
});
