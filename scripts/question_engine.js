// scripts/question_engine.js ##v7

// Convert plain text (from Google Sheets cells) to safe HTML for innerHTML:
// newlines (Alt+Enter in Sheets) become <br> tags.
function renderText(s) {
  return (s || '').replace(/\n/g, '<br>');
}

// ─────────────────────────────────────────────────────────────────────────────
//  Marking helpers — follow the Cambridge (CIE) mark-scheme conventions:
//   • B = independent mark.
//   • M = mandatory mark; if an M mark is missed the A mark cannot be awarded.
//   • C = compensatory mark (C1 lowest … C3 highest). A higher C implies the
//     lower ones, and a correct final answer (A) awards every C automatically.
//   • A = answer mark.
//  Numbers: "credit correct answers when rounded to the number of significant
//  figures given in the mark scheme" — a student's answer is accepted if it has
//  at least that many s.f. and rounds to the mark-scheme value. Standard form
//  may be typed as 6.17e-21, 6.17 x 10^-21, 6.17×10⁻²¹ etc.
// ─────────────────────────────────────────────────────────────────────────────
const SUPERSCRIPT_DIGITS = { "⁰": "0", "¹": "1", "²": "2", "³": "3", "⁴": "4", "⁵": "5", "⁶": "6", "⁷": "7", "⁸": "8", "⁹": "9", "⁻": "-", "⁺": "+" };

// Subscript characters are typed in many ways (g₀, g0, g_0), so they are turned
// into plain characters. Both the student's answer and every keyword go through
// this same function, so one keyword covers all the ways of typing it.
const SUBSCRIPT_CHARS = {
  "₀": "0", "₁": "1", "₂": "2", "₃": "3", "₄": "4", "₅": "5", "₆": "6", "₇": "7", "₈": "8", "₉": "9",
  "₊": "+", "₋": "-", "ₐ": "a", "ₑ": "e", "ₕ": "h", "ᵢ": "i", "ⱼ": "j", "ₖ": "k", "ₗ": "l", "ₘ": "m",
  "ₙ": "n", "ₒ": "o", "ₚ": "p", "ᵣ": "r", "ₛ": "s", "ₜ": "t", "ᵤ": "u", "ᵥ": "v", "ₓ": "x",
};
const SUBSCRIPT_RE = /[₀-₉₊₋ₐₑₕᵢⱼₖₗₘₙₒₚᵣₛₜᵤᵥₓ]/g;

// lower-case, unify minus/dashes, turn superscripts into ^digits, subscripts into
// plain characters, squash spaces
function normaliseText(s) {
  return String(s == null ? "" : s)
    .toLowerCase()
    .replace(SUBSCRIPT_RE, (c) => SUBSCRIPT_CHARS[c])
    .replace(/_/g, "")                       // E_k = Ek
    .replace(/×/g, "x")                      // 4× = 4x
    .replace(/[µ]/g, "μ")                    // micro sign -> Greek mu
    .replace(/[ϕφ]/g, "φ")                   // phi variants
    .replace(/[−–—]/g, "-")
    .replace(/[⁰¹²³⁴⁵⁶⁷⁸⁹⁻⁺]+/g, (m) => "^" + m.replace(/./g, (c) => SUPERSCRIPT_DIGITS[c]))
    .replace(/\s+/g, " ")
    .trim();
}

const NUM_PATTERN = "[+-]?(?:\\d+\\.?\\d*|\\.\\d+)";
const EXP_PATTERN = "(?:\\s*(?:x|×|\\*)\\s*10\\s*\\^?\\s*\\(?\\s*[+-]?\\d+\\s*\\)?|\\s*e\\s*[+-]?\\d+)";
const NUM_TOKEN_RE = () =>
  new RegExp("(" + NUM_PATTERN + ")(?:\\s*(?:x|×|\\*)\\s*10\\s*\\^?\\s*\\(?\\s*([+-]?\\d+)\\s*\\)?|\\s*e\\s*([+-]?\\d+))?", "g");
const NUMBER_ONLY_RE = new RegExp("^" + NUM_PATTERN + EXP_PATTERN + "?$");
const NUMBER_UNIT_RE = new RegExp("^(" + NUM_PATTERN + EXP_PATTERN + "?)\\s*(?:wb|kj|mj|j|kn|n|km|cm|mm|m|ms|s|hz|khz|mhz|kv|v|kw|w|pa|mol|ev|mev|kev|kg|g|k|ma|a|pf|nf|µf|μf|f|ω|ohm|t|mt)$");
const RANGE_RE = new RegExp("^(" + NUM_PATTERN + "(?:\\s*e\\s*[+-]?\\d+)?)\\s+to\\s+(" + NUM_PATTERN + "(?:\\s*e\\s*[+-]?\\d+)?)$");

function countSigFigs(mantissa) {
  const digits = mantissa.replace(/[+-]/g, "").replace(".", "").replace(/^0+/, "");
  return Math.max(1, digits.length);
}

// Every number written in a student's answer: [{ value, sf }, …]
function extractNumbers(str) {
  let s = normaliseText(String(str == null ? "" : str).replace(SUBSCRIPT_RE, ""));
  s = s.replace(/([a-zµμωΩ°%])\s*\^\s*[+-]?\d+/g, "$1");   // drop unit powers: m s^-1
  s = s.replace(/(\d),(?=\d{3}(?!\d))/g, "$1");            // 22,100 -> 22100
  const out = [];
  const re = NUM_TOKEN_RE();
  let m;
  while ((m = re.exec(s))) {
    const exp = m[2] !== undefined ? m[2] : m[3];
    const value = parseFloat(exp !== undefined ? m[1] + "e" + exp : m[1]);
    if (Number.isFinite(value)) out.push({ value, sf: countSigFigs(m[1]) });
    if (m[0].length === 0) re.lastIndex++;
  }
  return out;
}

// Drop the words "the", "a", "an" (only when they stand alone between spaces), so
// "divided by the potential difference" matches "divided by potential difference".
function stripArticles(s) {
  return String(s).replace(/(^|\s)(?:the|an|a)(?=\s|$)/g, " ").replace(/\s+/g, " ").trim();
}

function prepareInput(rawInput) {
  const norm = normaliseText(rawInput);
  let nums = null;
  return {
    norm,
    squash: norm.replace(/\s+/g, ""),
    get noArt() { return stripArticles(norm); },
    get noArtSquash() { return stripArticles(norm).replace(/\s+/g, ""); },
    get nums() { return nums || (nums = extractNumbers(rawInput)); },
  };
}

// student number t agrees with mark-scheme number e?
//  1) identical value, or
//  2) student gave at least as many s.f. as the mark scheme AND rounds to it, or
//  3) within the optional row tolerance (%), e.g. for values read from a graph.
function numbersAgree(t, e, tolPercent) {
  if (t.value === e.value) return true;
  if (t.sf >= e.sf && e.value !== 0) {
    // "rounds to the mark-scheme value": within half a unit of its last significant figure
    const unit = Math.pow(10, Math.floor(Math.log10(Math.abs(e.value))) - e.sf + 1);
    if (Math.abs(t.value - e.value) <= (unit / 2) * (1 + 1e-9)) return true;
  }
  if (tolPercent > 0 && e.value !== 0 && Math.abs(t.value - e.value) <= (Math.abs(e.value) * tolPercent) / 100) return true;
  return false;
}

function cleanKeyword(kw) {
  return normaliseText(kw).replace(/^["'“”‘’]+|["'“”‘’]+$/g, "").trim();
}

// Classify one keyword alternative:  {kind:'range'|'number'|'text', …}
function classifyKeyword(kw) {
  const k = cleanKeyword(kw);
  const r = k.match(RANGE_RE);
  if (r) {
    const lo = extractNumbers(r[1])[0], hi = extractNumbers(r[2])[0];
    if (lo && hi) return { kind: "range", k, lo: Math.min(lo.value, hi.value), hi: Math.max(lo.value, hi.value) };
  }
  // "exact:V0" means the WHOLE answer must be exactly V0 (not just contain it).
  if (k.startsWith("exact:") && k.length > 6) return { kind: "exact", k: k.slice(6).trim() };
  let numText = null;
  if (NUMBER_ONLY_RE.test(k)) numText = k;
  else { const u = k.match(NUMBER_UNIT_RE); if (u) numText = u[1]; }
  if (numText) {
    const e = extractNumbers(numText)[0];
    if (e) return { kind: "number", k, e };
  }
  return { kind: "text", k };
}

// Does the student's answer satisfy ONE keyword alternative?
function altMatches(kw, inp, tolPercent) {
  const c = classifyKeyword(kw);
  if (!c.k) return false;
  if (c.kind === "range") return inp.nums.some((t) => t.value >= c.lo && t.value <= c.hi);
  if (c.kind === "number") return inp.nums.some((t) => numbersAgree(t, c.e, tolPercent));
  if (c.kind === "exact") return inp.squash.replace(/[.\s]+$/, "") === c.k.replace(/\s+/g, "");
  if (inp.norm.includes(c.k) || inp.squash.includes(c.k.replace(/\s+/g, ""))) return true;
  // same test ignoring the words the / a / an
  const sk = stripArticles(c.k);
  const cmp = sk.length >= 4 && /^[a-z0-9]/.test(sk) ? sk : c.k;
  return inp.noArt.includes(cmp) || inp.noArtSquash.includes(cmp.replace(/\s+/g, ""));
}

// Keyword groups: flat OR list, AND-of-ORs, or OR-of-(AND-of-ORs)
function matchGroups(groups, inp, tolPercent) {
  if (!Array.isArray(groups)) return false;
  if (Array.isArray(groups[0]) && Array.isArray(groups[0][0]) && Array.isArray(groups[0][0][0])) {
    return groups.some((sub) => matchGroups(sub, inp, tolPercent));
  }
  if (groups.every((g) => typeof g === "string")) return groups.some((kw) => altMatches(kw, inp, tolPercent));
  return groups.every((grp) => grp.some((kw) => altMatches(kw, inp, tolPercent)));
}

function matchesKeywordGroups(groups, rawInput, tolPercent) {
  return matchGroups(groups, prepareInput(rawInput), tolPercent);
}

// Award marks for one typed answer using the CIE M / A / C / B rules.
function applyCieMarking(marks, rawInput) {
  const inp = prepareInput(rawInput);
  const hit = (m) => matchGroups(m.keywords, inp, m.tol);

  // M marks are mandatory: a missed M blocks the A mark.
  let aBlocked = false;
  marks.filter((m) => m.type === "M").forEach((m) => {
    if (!m.awarded && hit(m)) m.awarded = true;
    if (!m.awarded) aBlocked = true;
  });

  // A mark; a correct answer awards every C mark automatically (AFC).
  let aAwarded = false;
  const aMark = marks.find((m) => m.type === "A");
  if (aMark && !aBlocked && (aMark.awarded || hit(aMark))) {
    aMark.awarded = true;
    aAwarded = true;
    marks.forEach((m) => { if (m.type === "C") m.awarded = true; });
  }

  // C marks, highest level first; a higher C implies all the lower ones.
  if (!aAwarded) {
    marks
      .filter((m) => m.type === "C")
      .sort((a, b) => (b.level || 1) - (a.level || 1))
      .forEach((m) => {
        if (m.awarded) return;
        if (hit(m)) {
          m.awarded = true;
          marks.forEach((o) => { if (o.type === "C" && (o.level || 1) < (m.level || 1)) o.awarded = true; });
        }
      });
  }

  // B marks are independent.
  marks.filter((m) => m.type === "B").forEach((m) => {
    if (!m.awarded && hit(m)) m.awarded = true;
  });
}

// Keep the on-screen score equal to the marks actually awarded (safe to call
// after every check, so re-checking an answer can never inflate the score).
function recountMarks() {
  const parts = window.currentParts || [];
  totalMarksEarned = parts.reduce((sum, p) => sum + markEarned(p.marks), 0);
}

// Marks available / earned for one part. Normally every mark counts. When the
// sheet's "maxMarks" column is filled (e.g. "any 2 of 5 points") the builder sets
// marks.cap, the part is worth that many marks, and extra points earn nothing more.
function markTotal(marks) {
  return marks && marks.cap ? marks.cap : marks.length;
}
function markEarned(marks) {
  return Math.min(marks.filter((m) => m.awarded).length, markTotal(marks));
}


// ─────────────────────────────────────────────────────────────────────────────
//  Universal graph-drawing helper with “nice” major + minor grid lines
//  ‣ Expects spec as object with optional:
//    { xMin, xMax, yMax, xStep?, yStep?, xLabel?, yLabel?, color?, points: [[x,y], ...] }
//  ‣ You supply the exact points (include [0,0] yourself whenever physics demands it).
//  ‣ This draws y-axis on the LEFT and x-axis at the BOTTOM, with minor+major grids & labels.
// ─────────────────────────────────────────────────────────────────────────────
function drawGraph(canvas, spec) {
  const ctx = canvas.getContext("2d");
  const w = canvas.width, h = canvas.height;
  const m = 40;               // margin
  const plotW = w - 2 * m;
  const plotH = h - 2 * m;

  // Guard + defaults
  if (!spec || typeof spec !== "object") spec = {};
  const xMin = Number.isFinite(spec.xMin) ? Number(spec.xMin) : 0;
  const xMax = Number.isFinite(spec.xMax) ? Number(spec.xMax) : 1;
  const yMax = Number.isFinite(spec.yMax) ? Number(spec.yMax) : 1;

  // nice step helper
  function niceStep(raw) {
    if (!isFinite(raw) || raw <= 0) return 1;
    const exp = Math.floor(Math.log10(Math.abs(raw)));
    const base = Math.pow(10, exp);
    const frac = raw / base;
    return base * (frac <= 1 ? 1 : frac <= 2 ? 2 : frac <= 5 ? 5 : 10);
  }

  const xStep = Number.isFinite(spec.xStep) ? Number(spec.xStep) : niceStep((xMax - xMin) / 5);
  const yMin_spec = Number.isFinite(spec.yMin) ? Number(spec.yMin) : 0;
  const yStep = Number.isFinite(spec.yStep) ? Number(spec.yStep) : niceStep((yMax - yMin_spec) / 5);

  const xGraphMax = Math.ceil(xMax / xStep) * xStep;
  const xGraphMin = Math.floor(xMin / xStep) * xStep; // in case you ever set negative xMin
  const yGraphMin = Math.floor(yMin_spec / yStep) * yStep; // supports negative y (e.g. ln(I/I₀) graphs)
  const yGraphMax = Math.ceil(yMax / yStep) * yStep;

  const nX = Math.max(1, Math.round((xGraphMax - xGraphMin) / xStep));
  const nY = Math.max(1, Math.round((yGraphMax - yGraphMin) / yStep));

  // helpers to map data → canvas
  const xToPx = (x) => m + ((x - xGraphMin) / (xGraphMax - xGraphMin)) * plotW;
  const yToPx = (y) => m + plotH - ((y - yGraphMin) / (yGraphMax - yGraphMin)) * plotH;

  // BACKGROUND
  ctx.clearRect(0, 0, w, h);

  // minor grid (5 subdivisions between majors)
  ctx.strokeStyle = "#f0f0f0";
  ctx.lineWidth = 1;
  for (let i = 0; i < nX; i++) {
    for (let k = 1; k <= 5; k++) {
      const x = xToPx(xGraphMin + (i + k / 6) * xStep);
      ctx.beginPath();
      ctx.moveTo(x, m);
      ctx.lineTo(x, m + plotH);
      ctx.stroke();
    }
  }
  for (let j = 0; j < nY; j++) {
    for (let k = 1; k <= 5; k++) {
      const y = yToPx(yGraphMin + (j + k / 6) * yStep);
      ctx.beginPath();
      ctx.moveTo(m, y);
      ctx.lineTo(m + plotW, y);
      ctx.stroke();
    }
  }

  // major grid
  ctx.strokeStyle = "#e0e0e0";
  for (let i = 0; i <= nX; i++) {
    const x = xToPx(xGraphMin + i * xStep);
    ctx.beginPath();
    ctx.moveTo(x, m);
    ctx.lineTo(x, m + plotH);
    ctx.stroke();
  }
  for (let j = 0; j <= nY; j++) {
    const y = yToPx(yGraphMin + j * yStep);
    ctx.beginPath();
    ctx.moveTo(m, y);
    ctx.lineTo(m + plotW, y);
    ctx.stroke();
  }

  // axes (LEFT y-axis and BOTTOM x-axis)
  ctx.strokeStyle = "#000";
  ctx.lineWidth = 2;
  ctx.beginPath();
  // y-axis at left margin
  ctx.moveTo(m, m + plotH);
  ctx.lineTo(m, m);
  // x-axis at bottom
  ctx.moveTo(m, m + plotH);
  ctx.lineTo(m + plotW, m + plotH);
  ctx.stroke();

  // ticks & labels
  ctx.strokeStyle = "#000";
  ctx.fillStyle = "#000";
  ctx.lineWidth = 1;
  ctx.font = "12px sans-serif";
  ctx.textBaseline = "top";
  ctx.textAlign = "center";

  // tick label formatter: rounds to avoid floating-point noise like
  // 0.30000000000000004, while preserving enough precision to distinguish
  // nearby tick values (e.g. 0.1, 0.2, 0.3 on a tight microsecond axis).
  function tickLabel(val) {
    if (Math.abs(val) < 1e-12) return "0";
    // 4 significant figures is more than enough for a graph axis label
    return parseFloat(val.toPrecision(4)).toString();
  }

  // x-axis ticks & labels
  for (let i = 0; i <= nX; i++) {
    const val = xGraphMin + i * xStep;
    const x = xToPx(val);
    ctx.beginPath();
    ctx.moveTo(x, m + plotH - 5);
    ctx.lineTo(x, m + plotH + 5);
    ctx.stroke();
    ctx.fillText(tickLabel(val), x, m + plotH + 8);
  }

  // y-axis ticks & labels
  ctx.textAlign = "right";
  ctx.textBaseline = "middle";
  for (let j = 0; j <= nY; j++) {
    const val = yGraphMin + j * yStep;
    const y = yToPx(val);
    // short tick on left axis only
    ctx.beginPath();
    ctx.moveTo(m - 5, y);
    ctx.lineTo(m + 5, y);
    ctx.stroke();
    ctx.fillText(tickLabel(val), m - 8, y);
  }

  // axis titles
  if (spec.xLabel) {
    ctx.textAlign = "center";
    ctx.textBaseline = "alphabetic";
    ctx.fillText(spec.xLabel, m + plotW / 2, h - 8);
  }
  if (spec.yLabel) {
    ctx.save();
    ctx.translate(12, m + plotH / 2);
    ctx.rotate(-Math.PI / 2);
    ctx.textAlign = "center";
    ctx.textBaseline = "top";
    ctx.fillText(spec.yLabel, 0, 0);
    ctx.restore();
  }

  // plot data line(s) — either a single line (spec.points, existing behaviour)
  // or multiple labelled lines (spec.series: [{points, color, label}, ...])
  const seriesList = Array.isArray(spec.series) && spec.series.length
    ? spec.series
    : [{ points: Array.isArray(spec.points) ? spec.points : [], color: spec.color }];

  seriesList.forEach((s) => {
    const pts = Array.isArray(s.points) ? s.points : [];
    if (!pts.length) return;
    ctx.strokeStyle = s.color || "black";
    ctx.lineWidth = 2;
    ctx.beginPath();
    pts.forEach(([xv, yv], idx) => {
      const x = xToPx(Number(xv));
      const y = yToPx(Number(yv));
      if (idx === 0) ctx.moveTo(x, y);
      else ctx.lineTo(x, y);
    });
    ctx.stroke();
  });

  // series labels, drawn near the end of each line
  seriesList.forEach((s) => {
    if (!s.label || !Array.isArray(s.points) || !s.points.length) return;
    const [lx, ly] = s.points[s.points.length - 1];
    ctx.fillStyle = s.color || "black";
    ctx.font = "12px sans-serif";
    ctx.textAlign = "left";
    ctx.textBaseline = "middle";
    ctx.fillText(s.label, xToPx(Number(lx)) + 6, yToPx(Number(ly)));
  });
}

// Accept object or JSON string; coerce numeric fields (keeps old behaviour)
function normalizeGraphSpec(specLike) {
  let spec = specLike;
  if (typeof spec === "string") {
    try { spec = JSON.parse(spec); } catch { spec = {}; }
  }
  if (!spec || typeof spec !== "object") spec = {};

  const num = (v) =>
    (typeof v === "string" && v.trim() !== "" && !isNaN(v)) ? Number(v) : v;

  ["xMin", "xMax", "yMin", "yMax", "xStep", "yStep"].forEach((k) => {
    if (k in spec) spec[k] = num(spec[k]);
  });

  if (Array.isArray(spec.points)) {
    spec.points = spec.points
      .map((pt) => {
        const [x, y] = pt || [];
        return [num(x), num(y)];
      })
      .filter(([x, y]) => Number.isFinite(x) && Number.isFinite(y));
  }

  if (Array.isArray(spec.series)) {
    spec.series = spec.series.map((s) => ({
      ...s,
      points: Array.isArray(s.points)
        ? s.points
            .map((pt) => {
              const [x, y] = pt || [];
              return [num(x), num(y)];
            })
            .filter(([x, y]) => Number.isFinite(x) && Number.isFinite(y))
        : [],
    }));
  }

  return spec;
}

// ─── Weighted question selection, based on locally-saved practice history ───
// Each question's most recent score (as a percentage) is saved in
// localStorage, keyed by question id. Questions are bucketed by that score
// and drawn with different weights, so weaker/unattempted questions come up
// far more often than ones already scoring well. This is per-device
// (localStorage), not per-login-account — it survives closing the tab/
// browser, but doesn't sync across devices or distinguish students sharing
// one browser.
const SCORE_STORAGE_KEY = "physicsPracticeScores";

// Bucket boundaries are inclusive upper limits; weight = relative draw
// frequency. A question with no saved score (never attempted) is treated
// the same as a 0% score - both need attention.
const SCORE_BUCKETS = [
  { max: 0, weight: 10 },   // exactly 0%, or never attempted
  { max: 20, weight: 6 },   // 0-20%
  { max: 50, weight: 4 },   // 20-50%
  { max: 70, weight: 2 },   // 50-70%
  { max: 100, weight: 1 },  // 70-100%
];

function loadPracticeScores() {
  try {
    return JSON.parse(localStorage.getItem(SCORE_STORAGE_KEY) || "{}");
  } catch {
    return {};
  }
}

// Exposed on window so main.js's updateScoreDisplay() can call it.
window.saveScoreForQuestion = function (questionId, percent) {
  try {
    const scores = loadPracticeScores();
    scores[questionId] = percent;
    localStorage.setItem(SCORE_STORAGE_KEY, JSON.stringify(scores));
  } catch (e) {
    // localStorage can be unavailable (e.g. some private-browsing modes) -
    // fail quietly rather than break question loading/marking.
    console.warn("Could not save practice history:", e);
  }
};

function weightForPercent(percent) {
  const p = percent === undefined || percent === null ? 0 : percent;
  for (const bucket of SCORE_BUCKETS) {
    if (p <= bucket.max) return bucket.weight;
  }
  return SCORE_BUCKETS[SCORE_BUCKETS.length - 1].weight;
}

function pickWeightedQuestion() {
  const scores = loadPracticeScores();
  const weighted = window.questions.map((q) => ({
    q,
    weight: weightForPercent(scores[q.id]),
  }));
  const totalWeight = weighted.reduce((sum, w) => sum + w.weight, 0);
  let r = Math.random() * totalWeight;
  for (const w of weighted) {
    if (r < w.weight) return w.q;
    r -= w.weight;
  }
  return weighted[weighted.length - 1].q; // floating-point fallback
}

// ─── 1) Load & render a random question ───
function loadRandomQuestion() {
  const def = pickWeightedQuestion();
  window.currentQuestionId = def.id;
  const qData = window.genericBuilder(def);

  // reset scores
  resetQuestionScores();
  window.currentParts = qData.parts; // used by recountMarks()
  totalMarksPossible = qData.parts.reduce((sum, p) => sum + markTotal(p.marks), 0);
  updateScoreDisplay(); // no persistAttempt arg - this is just initial display, not a real attempt

  const container = document.getElementById("question-container");
  container.innerHTML = "";

  // main text
  const h2 = document.createElement("h2");
  h2.innerHTML = qData.mainText;
  container.appendChild(h2);

  // each part
  qData.parts.forEach((part, i) => {
    const div = document.createElement("div");
    div.classList.add("question-part");

    // prompt + score
    const p = document.createElement("p");
    p.innerHTML = part.partText + " ";
    const span = document.createElement("span");
    span.id = `score-${i}`;
    span.textContent = `(0/${markTotal(part.marks)})`;
    span.style.fontWeight = "bold";
    p.appendChild(span);
    div.appendChild(p);

    // graph if given (accepts JSON string or object; coerces numbers)
    if (part.graphSpec) {
      const canvas = document.createElement("canvas");
      canvas.width = 300;
      canvas.height = 300;
      canvas.style.border = "1px solid #000";
      canvas.style.marginRight = "10px";
      div.appendChild(canvas);
      try {
        const spec = normalizeGraphSpec(part.graphSpec);
        drawGraph(canvas, spec);
      } catch (e) {
        console.error("Graph error:", e, part.graphSpec);
        const fb = document.createElement("div");
        fb.textContent = "[graph unavailable]";
        fb.style.color = "crimson";
        div.appendChild(fb);
      }
    }

    // optional second graph, shown alongside the first (e.g. two related
    // figures the student needs to read together)
    if (part.graphSpec2) {
      const canvas2 = document.createElement("canvas");
      canvas2.width = 300;
      canvas2.height = 300;
      canvas2.style.border = "1px solid #000";
      div.appendChild(canvas2);
      try {
        const spec2 = normalizeGraphSpec(part.graphSpec2);
        drawGraph(canvas2, spec2);
      } catch (e) {
        console.error("Graph 2 error:", e, part.graphSpec2);
        const fb = document.createElement("div");
        fb.textContent = "[second graph unavailable]";
        fb.style.color = "crimson";
        div.appendChild(fb);
      }
    }

    if (part.answerType === "imageChoice") {
      // ── clickable diagram/graph options instead of a text box ──
      const grid = document.createElement("div");
      grid.style.display = "flex";
      grid.style.flexWrap = "wrap";
      grid.style.gap = "10px";
      grid.style.marginTop = "8px";

      const options = Array.isArray(part.imageOptions) ? part.imageOptions : [];
      if (!options.length) {
        const warn = document.createElement("div");
        warn.textContent = "[no image options configured for this part]";
        warn.style.color = "crimson";
        div.appendChild(warn);
      }

      options.forEach((filename, optIdx) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.style.padding = "4px";
        btn.style.border = "2px solid #999";
        btn.style.borderRadius = "6px";
        btn.style.background = "white";
        btn.style.cursor = "pointer";

        const img = document.createElement("img");
        img.src = window.resolveAssetSrc(filename);
        img.style.width = "160px";
        img.style.display = "block";
        img.onerror = () => {
          btn.style.borderColor = "crimson";
          btn.title = `Missing asset: ${filename}`;
        };
        btn.appendChild(img);

        btn.onclick = () =>
          checkImageChoice(i, optIdx, part.correctImageIndex, part.marks, grid, part.explanation);

        grid.appendChild(btn);
      });

      div.appendChild(grid);

      // feedback area (shared with the rest of the flow)
      const fb = document.createElement("div");
      fb.id = `model-${i}`;
      fb.style.display = "none";
      fb.style.marginTop = "10px";
      fb.style.padding = "10px";
      fb.style.borderRadius = "8px";
      div.appendChild(fb);
    } else if (part.answerType === "table") {
      // ── grid of inputs, row/col labelled, matching the paper's table ──
      const rows = Array.isArray(part.tableRowLabels) ? part.tableRowLabels : [];
      const cols = Array.isArray(part.tableColLabels) ? part.tableColLabels : [];

      const table = document.createElement("table");
      table.style.borderCollapse = "collapse";
      table.style.marginTop = "8px";

      const headRow = document.createElement("tr");
      headRow.appendChild(document.createElement("th"));
      cols.forEach((c) => {
        const th = document.createElement("th");
        th.textContent = c;
        th.style.border = "1px solid #999";
        th.style.padding = "6px";
        headRow.appendChild(th);
      });
      table.appendChild(headRow);

      rows.forEach((rLabel, r) => {
        const tr = document.createElement("tr");
        const th = document.createElement("th");
        th.textContent = rLabel;
        th.style.border = "1px solid #999";
        th.style.padding = "6px";
        tr.appendChild(th);

        cols.forEach((c, cIdx) => {
          const td = document.createElement("td");
          td.style.border = "1px solid #999";
          td.style.padding = "4px";
          const input = document.createElement("input");
          input.type = "text";
          input.id = `table-${i}-${r}-${cIdx}`;
          input.style.width = "160px";
          td.appendChild(input);
          tr.appendChild(td);
        });
        table.appendChild(tr);
      });

      div.appendChild(table);

      const btn = document.createElement("button");
      btn.textContent = "Check Answer";
      btn.style.marginTop = "8px";
      btn.onclick = () =>
        checkTableAnswer(i, part.marks, rows, cols, part.tableCellKeywords, part.tableCellAnswers, part.explanation);
      div.appendChild(btn);

      const fb = document.createElement("div");
      fb.id = `model-${i}`;
      fb.style.display = "none";
      fb.style.marginTop = "10px";
      fb.style.padding = "10px";
      fb.style.borderRadius = "8px";
      div.appendChild(fb);
    } else {
      // ── standard typed-answer flow (unchanged) ──
      const ta = document.createElement("textarea");
      ta.id = `answer-${i}`;
      ta.rows = 3;
      ta.cols = 60;
      ta.setAttribute("spellcheck", "true");  
      ta.setAttribute("lang", "en");
      div.appendChild(ta);

      const btn = document.createElement("button");
      btn.textContent = "Check Answer";
      btn.onclick = () =>
        checkPartAnswer(i, part.marks, part.modelAnswer, part.explanation);
      div.appendChild(btn);

      const fb = document.createElement("div");
      fb.id = `model-${i}`;
      fb.style.display = "none";
      fb.style.marginTop = "10px";
      fb.style.padding = "10px";
      fb.style.borderRadius = "8px";
      div.appendChild(fb);
    }

    container.appendChild(div);
  });

  // next question
  const nextBtn = document.createElement("button");
  nextBtn.textContent = "Next Question";
  nextBtn.style.display = "block";
  nextBtn.style.marginTop = "1rem";
  nextBtn.onclick = loadRandomQuestion;
  container.appendChild(nextBtn);

  // hide stray legacy canvas (if present)
  const stray = document.getElementById("diagram-canvas");
  if (stray) stray.style.display = "none";
}

// ─── 2) Check an imageChoice answer: single click = single attempt ───
function checkImageChoice(index, chosenIdx, correctIdx, marks, grid, explanation) {
  const buttons = grid.querySelectorAll("button");
  const correct = chosenIdx === correctIdx;

  buttons.forEach((btn, idx) => {
    btn.disabled = true;
    btn.style.cursor = "default";
    if (idx === correctIdx) btn.style.borderColor = "green";
    if (idx === chosenIdx && !correct) btn.style.borderColor = "crimson";
  });

  if (correct) {
    marks.forEach((m) => (m.awarded = true));
  }

  const earned = marks.filter((m) => m.awarded).length;
  document.getElementById(`score-${index}`).textContent = `(${earned}/${marks.length})`;

  const fb = document.getElementById(`model-${index}`);
  fb.style.display = "block";
  fb.style.border = correct ? "2px solid green" : "2px solid red";
  fb.innerHTML = correct
    ? `<strong>Correct!</strong><br><br>${renderText(explanation)}`
    : `<strong>Not quite right.</strong><br><br>${renderText(explanation)}`;

  recountMarks();
  updateScoreDisplay(true);
}


// ─── 3.5) Check a table-style answer (grid of inputs, one mark per cell) ───
function checkTableAnswer(index, marks, rowLabels, colLabels, cellKeywords, cellAnswers, explanation) {
  let earned = 0;
  let anyBlank = false;
  let markIdx = 0;

  const fb = document.getElementById(`model-${index}`);
  fb.style.display = "block";

  let feedbackRows = "";
  rowLabels.forEach((rLabel, r) => {
    colLabels.forEach((cLabel, c) => {
      const el = document.getElementById(`table-${index}-${r}-${c}`);
      const raw = (el ? el.value : "").trim();
      const kw = (cellKeywords && cellKeywords[r] && cellKeywords[r][c]) || [];
      const answer = (cellAnswers && cellAnswers[r] && cellAnswers[r][c]) || "";
      const mark = marks[markIdx];
      markIdx++;

      if (raw === "") anyBlank = true;

      const correct = raw !== "" && matchesKeywordGroups(kw, raw);
      if (mark) mark.awarded = correct;
      if (correct) earned++;

      if (el) el.style.border = raw === "" ? "1px solid #999" : correct ? "2px solid green" : "2px solid crimson";

      const icon = correct ? "&#10003;" : "&#10007;";
      const iconColor = correct ? "green" : "crimson";
      feedbackRows += `<tr><td style="padding:2px 8px 2px 0;color:${iconColor};">${icon} ${rLabel} &ndash; ${cLabel}:</td><td>${answer}</td></tr>`;
    });
  });

  recountMarks();
  const tableFull = markEarned(marks) === markTotal(marks);   // honours the maxMarks cap
  document.getElementById(`score-${index}`).textContent = `(${markEarned(marks)}/${markTotal(marks)})`;

  // per-cell keyword breakdown, for reporting suspected marking issues during beta testing
  let breakdownRows = "";
  markIdx = 0;
  rowLabels.forEach((rLabel, r) => {
    colLabels.forEach((cLabel, c) => {
      const kw = (cellKeywords && cellKeywords[r] && cellKeywords[r][c]) || [];
      const mark = marks[markIdx];
      markIdx++;
      const icon = mark && mark.awarded ? "&#10003;" : "&#10007;";
      const color = mark && mark.awarded ? "green" : "crimson";
      breakdownRows += `<div style="color:${color};">${icon} ${rLabel} &ndash; ${cLabel}: needed ${describeKeywordRequirement(kw)}</div>`;
    });
  });

  fb.style.border = tableFull ? "2px solid green" : earned > 0 ? "2px solid orange" : "2px solid red";
  fb.innerHTML =
    (anyBlank && !tableFull ? `<strong>Try to fill in every cell.</strong><br><br>` : tableFull ? `<strong>Correct!</strong><br><br>` : `<strong>Not quite right yet.</strong><br><br>`) +
    `<em>Model answers:</em><table>${feedbackRows}</table>` +
    (explanation ? `<br>${renderText(explanation)}` : "") +
    `<div style="margin-top:10px;font-size:0.9em;border-top:1px solid #ccc;padding-top:6px;">` +
    `<em>Marking breakdown (for reporting issues during beta testing):</em><br>${breakdownRows}</div>`;

  updateScoreDisplay(true);
}

// Human-readable description of what a keyword group needs — shown in the
// marking breakdown after an answer is checked.
function describeAlternative(kw, tolPercent) {
  const c = classifyKeyword(kw);
  if (c.kind === "range") return `any value from ${c.lo} to ${c.hi}`;
  if (c.kind === "number") {
    return `&ldquo;${c.k}&rdquo; (at least ${c.e.sf} s.f.${tolPercent > 0 ? `, or within ±${tolPercent}%` : ""})`;
  }
  if (c.kind === "exact") return `exactly &ldquo;${c.k}&rdquo;`;
  return `&ldquo;${c.k}&rdquo;`;
}

function describeKeywordRequirement(groups, tolPercent) {
  if (!Array.isArray(groups) || groups.length === 0) return "any reasonable answer";
  // OR-of-(AND-of-OR): rare, deepest nesting case
  if (Array.isArray(groups[0]) && Array.isArray(groups[0][0]) && Array.isArray(groups[0][0][0])) {
    return groups.map((g) => describeKeywordRequirement(g, tolPercent)).join(" &nbsp;OR&nbsp; ");
  }
  // flat OR: array of strings
  if (groups.every((g) => typeof g === "string")) {
    return groups.map((g) => describeAlternative(g, tolPercent)).join(" or ");
  }
  // AND-of-OR: array of arrays of strings
  return groups.map((grp) => "(" + grp.map((kw) => describeAlternative(kw, tolPercent)).join(" or ") + ")").join(" and ");
}

// Builds the "Marking breakdown" block: one line per mark, showing whether
// it was awarded and what wording/answer was needed for it. Shown for every
// outcome (correct, partial, wrong) so a screenshot always shows the full
// picture, not just the final score.
// Full keyword detail is for testing/teachers only: add ?beta=1 to the page address
// (or set localStorage physicsBeta = "1"). Students see a tick or cross per mark point.
function betaMarkingDetail() {
  try {
    if (/[?&]beta=1\b/.test(window.location.search)) return true;
    return localStorage.getItem("physicsBeta") === "1";
  } catch (e) { return false; }
}

function buildMarkingBreakdown(marks) {
  if (!marks || !marks.length) return "";
  const detail = betaMarkingDetail();
  const rows = marks.map((m, i) => {
    const icon = m.awarded ? "&#10003;" : "&#10007;";
    const color = m.awarded ? "green" : "crimson";
    if (!detail) return `<div style="color:${color};">${icon} Mark ${i + 1}</div>`;
    const req = m.keywords ? describeKeywordRequirement(m.keywords, m.tol) : "correct final answer";
    return `<div style="color:${color};">${icon} Mark ${i + 1} (${m.type}): needed ${req}</div>`;
  });
  if (marks.cap) rows.unshift(`<div>This part is worth ${marks.cap} mark${marks.cap > 1 ? "s" : ""}: any ${marks.cap} of the points below.</div>`);
  const title = detail ? "Marking breakdown (for reporting issues during beta testing):" : "Marks awarded:";
  return `<div style="margin-top:10px;font-size:0.9em;border-top:1px solid #ccc;padding-top:6px;">` +
    `<em>${title}</em><br>${rows.join("")}</div>`;
}

function checkPartAnswer(index, marks, modelAnswer, explanation) {
  const raw = document.getElementById(`answer-${index}`).value.trim();
  const fb = document.getElementById(`model-${index}`);

  // blank-guard
  if (raw === "") {
    fb.style.display = "block";
    fb.style.border = "2px solid red";
    fb.innerHTML =
      `<strong>Try to always put something down.</strong><br><br>` +
      `<em>Key Idea:</em><br>${renderText(explanation)}`;
    return;
  }

  fb.style.display = "block";

  // No mark scheme encoded for this part: nothing to score, just show the answer.
  if (!marks.length) {
    fb.style.border = "2px solid #999";
    fb.innerHTML =
      `<strong>Compare with the model answer.</strong><br><br>Model Answer:<br>${renderText(modelAnswer)}` +
      (explanation ? `<br><br><em>Key Idea:</em><br>${renderText(explanation)}` : "");
    return;
  }

  applyCieMarking(marks, raw);
  recountMarks();

  const earned = markEarned(marks);
  const possible = markTotal(marks);
  document.getElementById(`score-${index}`).textContent = `(${earned}/${possible})`;

  if (earned === possible) {
    fb.innerHTML = `<strong>Correct!</strong><br><br>Model Answer:<br>${renderText(modelAnswer)}` + buildMarkingBreakdown(marks);
    fb.style.border = "2px solid green";
  } else if (earned > 0) {
    fb.innerHTML =
      `<strong>You're nearly there!</strong><br><br><em>Key Idea:</em><br>${renderText(explanation)}` +
      `<br><br><strong>Model Answer:</strong><br>${renderText(modelAnswer)}` + buildMarkingBreakdown(marks);
    fb.style.border = "2px solid orange";
  } else {
    fb.innerHTML =
      `<strong>Not quite right.</strong><br><br><em>Key Idea:</em><br>${renderText(explanation)}` +
      `<br><br><strong>Model Answer:</strong><br>${renderText(modelAnswer)}` + buildMarkingBreakdown(marks);
    fb.style.border = "2px solid red";
  }

  updateScoreDisplay(true);
}


// expose globally
window.loadRandomQuestion = loadRandomQuestion;
