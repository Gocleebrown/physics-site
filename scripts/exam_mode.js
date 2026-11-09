// scripts/exam_mode.js ##v2
//
// "Whole paper" exam mode. Separate from the practice flow in question_engine.js so
// that nothing in normal practice can be affected by it.
//
//  - A paper is picked at random (the student never chooses it).
//  - Questions run in paper order on one page. No hints, key ideas, model answers or
//    per-part feedback are shown while sitting the paper.
//  - Numbers are random but FIXED for the sitting (seeded), so a refresh or resume
//    shows exactly the same paper, and the review matches what the student answered.
//  - Answers autosave in this browser; a sitting can be resumed after a refresh.
//  - Optional timer with extra-time settings. Time up = paper is submitted.
//  - On finishing, every part is marked with the normal CIE marking engine and the
//    student sees their answers, marks, model answers, key ideas and a topic summary.
//
// Relies on globals from the other scripts: genericBuilder, applyCieMarking,
// matchesKeywordGroups, markTotal, markEarned, buildMarkingBreakdown, renderText,
// normalizeGraphSpec, drawGraph, resolveAssetSrc, showPage.

(function () {
  const SITTING_KEY = "physicsExamSitting";
  const HISTORY_KEY = "physicsExamHistory";
  const LASTPAPER_KEY = "physicsExamLastPaper";

  // ── tiny helpers ──────────────────────────────────────────────────────────
  const $ = (id) => document.getElementById(id);
  const esc = (s) =>
    String(s == null ? "" : s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));

  function lsGet(k) {
    try { return JSON.parse(localStorage.getItem(k)); } catch (e) { return null; }
  }
  function lsSet(k, v) {
    try { localStorage.setItem(k, JSON.stringify(v)); return true; }
    catch (e) { console.warn("[Exam] could not save to this browser:", e); return false; }
  }
  function lsDel(k) { try { localStorage.removeItem(k); } catch (e) { /* ignore */ } }

  // Seeded random numbers so a sitting always rebuilds to the same numbers.
  function hashStr(s) {
    let h = 2166136261;
    for (let i = 0; i < s.length; i++) { h ^= s.charCodeAt(i); h = Math.imul(h, 16777619); }
    return h >>> 0;
  }
  function mulberry32(a) {
    return function () {
      a |= 0; a = (a + 0x6d2b79f5) | 0;
      let t = Math.imul(a ^ (a >>> 15), 1 | a);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }
  function buildSeeded(def, seed) {
    const orig = Math.random;
    Math.random = mulberry32(hashStr(seed + "|" + def.id));
    try { return window.genericBuilder(def); }
    finally { Math.random = orig; }
  }

  function qNumber(id) {
    const m = /[-_][Qq](\d+)$/.exec(id || "");
    return m ? parseInt(m[1], 10) : 0;
  }

  // ── papers ────────────────────────────────────────────────────────────────
  // Every paper (level + tier) that has at least one question, as [{paper, defs}].
  function papersFor(level, tier) {
    const defs = window.allDefinitions || [];
    const byPaper = {};
    defs.forEach((q) => {
      if (q.level !== level) return;
      if (tier && q.tier !== tier) return;
      const p = (q.paper || "").trim();
      if (!p) return;
      (byPaper[p] = byPaper[p] || []).push(q);
    });
    return Object.keys(byPaper).map((p) => ({
      paper: p,
      defs: byPaper[p].slice().sort((a, b) => qNumber(a.id) - qNumber(b.id)),
    }));
  }
  window.examPapersFor = papersFor;

  // Official length and mark total of the real paper, used to set the time allowed.
  function officialSpec(level, paper) {
    const m = /_p(\d)\d/i.exec(paper || "");
    const comp = m ? m[1] : "";
    if (level === "IGCSE" && (comp === "3" || comp === "4")) return { minutes: 75, marks: 80 };
    if (level === "AS" && comp === "2") return { minutes: 75, marks: 60 };
    if (level === "A2" && comp === "4") return { minutes: 120, marks: 100 };
    return null;
  }
  function allowedSeconds(level, paper, totalMarks) {
    const spec = officialSpec(level, paper);
    const raw = spec ? spec.minutes * 60 * (totalMarks / spec.marks) : totalMarks * 60;
    return Math.max(60, Math.round(raw / 60) * 60);
  }
  function fmtDuration(sec) {
    sec = Math.max(0, Math.round(sec));
    const h = Math.floor(sec / 3600), m = Math.floor((sec % 3600) / 60), s = sec % 60;
    const p2 = (n) => String(n).padStart(2, "0");
    return h > 0 ? h + ":" + p2(m) + ":" + p2(s) : p2(m) + ":" + p2(s);
  }
  function fmtMinutes(sec) {
    const m = Math.round(sec / 60);
    return m >= 60 ? Math.floor(m / 60) + " h " + (m % 60 ? (m % 60) + " min" : "") : m + " min";
  }

  function totalMarksOf(built) {
    return built.reduce((s, q) => s + q.parts.reduce((a, p) => a + markTotal(p.marks), 0), 0);
  }

  // ── state ─────────────────────────────────────────────────────────────────
  let state = null;       // current sitting (also mirrored in localStorage)
  let built = [];         // built questions for the sitting
  let timerHandle = null;
  let saveHandle = null;
  let snapHandle = null;
  let savedScoreDisplay = null;

  function saveState() {
    if (state) lsSet(SITTING_KEY, state);
  }

  function defsForState(s) {
    const all = window.allDefinitions || [];
    const byId = {};
    all.forEach((d) => { byId[d.id] = d; });
    return s.qids.map((id) => byId[id]).filter(Boolean);
  }

  // ── start dialog ──────────────────────────────────────────────────────────
  function startExamFlow(level, tier) {
    if (!window.allDefinitions) {
      alert("Questions are still loading — please wait a moment.");
      return;
    }
    const existing = lsGet(SITTING_KEY);
    if (existing && !existing.finished) {
      if (!confirm("You already have a paper in progress. Starting a new one will throw it away. Continue?")) return;
    }
    const papers = papersFor(level, tier);
    if (!papers.length) {
      alert("No whole papers are available for " + level + (tier ? " " + tier : "") + " yet.");
      return;
    }
    // Random paper, avoiding the one sat last time when there is a choice.
    const last = lsGet(LASTPAPER_KEY);
    let pool = papers.filter((p) => p.paper !== last);
    if (!pool.length) pool = papers;
    const pick = pool[Math.floor(Math.random() * pool.length)];
    const seed = String(Date.now()) + "-" + Math.floor(Math.random() * 1e9);

    let preview;
    try { preview = pick.defs.map((d) => buildSeeded(d, seed)); }
    catch (e) { alert("Sorry, this paper could not be built: " + e.message); return; }
    const marks = totalMarksOf(preview);
    const baseSec = allowedSeconds(level, pick.paper, marks);
    openDialog({ level, tier, pick, seed, marks, baseSec, nq: pick.defs.length });
  }

  function openDialog(o) {
    closeDialog();
    const wrap = document.createElement("div");
    wrap.id = "exam-dialog";
    wrap.className = "exam-overlay";
    wrap.innerHTML =
      '<div class="exam-modal" role="dialog" aria-modal="true" aria-labelledby="exam-dlg-title">' +
      '<h3 id="exam-dlg-title">Whole paper &ndash; ' + esc(o.level + (o.tier ? " " + o.tier : "")) + "</h3>" +
      "<p><b>" + o.nq + " questions &middot; " + o.marks + " marks</b></p>" +
      "<ul>" +
      "<li>A paper is chosen at random.</li>" +
      "<li>Questions are in paper order. No hints, key ideas or model answers are shown until you finish.</li>" +
      "<li>Your answers save in this browser, so you can refresh and carry on.</li>" +
      "<li>When you finish, every answer is marked and you can review it all.</li>" +
      "</ul>" +
      '<div class="exam-opt"><label><input type="radio" name="exm-t" value="untimed" checked> Untimed</label> ' +
      '<label><input type="radio" name="exm-t" value="timed"> Timed</label></div>' +
      '<div class="exam-opt" id="exm-extra-row" style="display:none">Extra time: ' +
      '<select id="exm-extra"><option value="0">None</option><option value="0.25">+25%</option>' +
      '<option value="0.5">+50%</option><option value="1">+100%</option></select></div>' +
      '<p id="exm-time-note" style="display:none"></p>' +
      '<div class="exam-actions"><button type="button" id="exm-cancel">Cancel</button>' +
      '<button type="button" class="primary" id="exm-start">Start paper</button></div>' +
      "</div>";
    document.body.appendChild(wrap);

    const timedEls = wrap.querySelectorAll('input[name="exm-t"]');
    const extraSel = $("exm-extra");
    function refresh() {
      const timed = wrap.querySelector('input[name="exm-t"]:checked').value === "timed";
      $("exm-extra-row").style.display = timed ? "block" : "none";
      const note = $("exm-time-note");
      note.style.display = timed ? "block" : "none";
      const sec = Math.round((o.baseSec * (1 + parseFloat(extraSel.value))) / 60) * 60;
      note.textContent = "Time allowed: " + fmtMinutes(sec) + ". The paper is submitted automatically when time runs out.";
    }
    timedEls.forEach((r) => r.addEventListener("change", refresh));
    extraSel.addEventListener("change", refresh);
    refresh();

    $("exm-cancel").addEventListener("click", closeDialog);
    $("exm-start").addEventListener("click", () => {
      const timed = wrap.querySelector('input[name="exm-t"]:checked').value === "timed";
      const extra = parseFloat(extraSel.value) || 0;
      const allowed = Math.round((o.baseSec * (1 + extra)) / 60) * 60;
      const now = Date.now();
      state = {
        v: 1,
        seed: o.seed,
        level: o.level,
        tier: o.tier || "",
        paper: o.pick.paper,
        qids: o.pick.defs.map((d) => d.id),
        timed,
        extra,
        allowedSec: allowed,
        startedAt: now,
        endsAt: timed ? now + allowed * 1000 : null,
        answers: {},
        finished: false,
        finishedAt: null,
        autoSubmitted: false,
      };
      lsSet(LASTPAPER_KEY, o.pick.paper);
      saveState();
      closeDialog();
      enterExam();
    });
  }
  function closeDialog() {
    const d = $("exam-dialog");
    if (d) d.remove();
  }

  // ── entering / leaving the exam page ───────────────────────────────────────
  function enterExam() {
    if (!state) return;
    const defs = defsForState(state);
    if (defs.length !== state.qids.length) {
      alert("Some questions in this saved paper are no longer available, so it can't be resumed.");
      lsDel(SITTING_KEY);
      state = null;
      refreshBanner();
      return;
    }
    built = defs.map((d) => buildSeeded(d, state.seed));
    const sd = $("score-display");
    if (sd && savedScoreDisplay === null) savedScoreDisplay = sd.style.display;
    if (sd) sd.style.display = "none";
    showPage("practice-page");
    window.scrollTo(0, 0);
    if (state.finished) { renderReview(); return; }
    if (state.timed && Date.now() >= state.endsAt) { finishExam(true); return; }
    renderExam();
    startTimer();
  }

  function leaveExam() {
    stopTimer();
    if (saveHandle) { clearTimeout(saveHandle); saveHandle = null; }
    const sd = $("score-display");
    if (sd && savedScoreDisplay !== null) sd.style.display = savedScoreDisplay;
    savedScoreDisplay = null;
    $("question-container").innerHTML = "";
    built = [];
    showPage("selection-page");
    refreshBanner();
  }

  // ── rendering the paper (no feedback) ──────────────────────────────────────
  function renderExam() {
    const container = $("question-container");
    container.innerHTML = "";

    const bar = document.createElement("div");
    bar.className = "exam-bar";
    bar.innerHTML =
      '<span class="exam-bar-title">Whole paper &ndash; ' + esc(state.level + (state.tier ? " " + state.tier : "")) + "</span>" +
      '<span class="exam-bar-timer" id="exam-timer"></span>' +
      '<button type="button" class="exam-finish" id="exam-finish-top">Finish &amp; mark paper</button>';
    container.appendChild(bar);

    built.forEach((qData, qi) => {
      const sec = document.createElement("section");
      sec.className = "exam-question";
      const h2 = document.createElement("h2");
      h2.innerHTML = qData.mainText;
      sec.appendChild(h2);
      qData.parts.forEach((part, pi) => sec.appendChild(renderPart(part, qi, pi)));
      container.appendChild(sec);
    });

    const end = document.createElement("div");
    end.className = "exam-end";
    end.innerHTML =
      '<p>When you have answered everything you can, finish the paper to see your marks.</p>' +
      '<button type="button" class="exam-finish" id="exam-finish-bottom">Finish &amp; mark paper</button>';
    container.appendChild(end);

    $("exam-finish-top").addEventListener("click", () => tryFinish());
    $("exam-finish-bottom").addEventListener("click", () => tryFinish());

    container.addEventListener("input", scheduleSave);
    container.addEventListener("focusout", scheduleSave);
    updateTimerText();
  }

  function renderPart(part, qi, pi) {
    const div = document.createElement("div");
    div.classList.add("question-part");

    const p = document.createElement("p");
    p.innerHTML = part.partText + ' <span class="exam-marks">[' + markTotal(part.marks) + "]</span>";
    div.appendChild(p);

    [part.graphSpec, part.graphSpec2].forEach((gs) => {
      if (!gs) return;
      const canvas = document.createElement("canvas");
      canvas.width = 300; canvas.height = 300;
      canvas.style.border = "1px solid #000";
      canvas.style.marginRight = "10px";
      div.appendChild(canvas);
      try { drawGraph(canvas, normalizeGraphSpec(gs)); }
      catch (e) { canvas.replaceWith(Object.assign(document.createElement("div"), { textContent: "[graph unavailable]" })); }
    });

    const key = qi + "-" + pi;

    if (part.answerType === "imageChoice") {
      const grid = document.createElement("div");
      grid.className = "exam-imgchoice";
      (part.imageOptions || []).forEach((filename, optIdx) => {
        const btn = document.createElement("button");
        btn.type = "button";
        btn.className = "exam-imgopt";
        const img = document.createElement("img");
        img.src = window.resolveAssetSrc(filename);
        img.style.width = "160px";
        img.style.display = "block";
        btn.appendChild(img);
        if (state.answers["i-" + key] === optIdx) btn.classList.add("selected");
        btn.addEventListener("click", () => {
          state.answers["i-" + key] = optIdx;
          grid.querySelectorAll("button").forEach((b, k) => b.classList.toggle("selected", k === optIdx));
          saveState();
        });
        grid.appendChild(btn);
      });
      div.appendChild(grid);
    } else if (part.answerType === "table") {
      const rows = part.tableRowLabels || [], cols = part.tableColLabels || [];
      const table = document.createElement("table");
      table.style.borderCollapse = "collapse";
      table.style.marginTop = "8px";
      const head = document.createElement("tr");
      head.appendChild(document.createElement("th"));
      cols.forEach((c) => {
        const th = document.createElement("th");
        th.textContent = c; th.style.border = "1px solid #999"; th.style.padding = "6px";
        head.appendChild(th);
      });
      table.appendChild(head);
      rows.forEach((rl, r) => {
        const tr = document.createElement("tr");
        const th = document.createElement("th");
        th.textContent = rl; th.style.border = "1px solid #999"; th.style.padding = "6px";
        tr.appendChild(th);
        cols.forEach((cl, c) => {
          const td = document.createElement("td");
          td.style.border = "1px solid #999"; td.style.padding = "4px";
          const input = document.createElement("input");
          input.type = "text";
          input.className = "ex-input";
          input.dataset.key = "t-" + key + "-" + r + "-" + c;
          input.style.width = "160px";
          input.value = state.answers[input.dataset.key] || "";
          td.appendChild(input);
          tr.appendChild(td);
        });
        table.appendChild(tr);
      });
      div.appendChild(table);
    } else {
      const ta = document.createElement("textarea");
      ta.rows = 3; ta.cols = 60;
      ta.className = "ex-input";
      ta.dataset.key = "a-" + key;
      ta.setAttribute("spellcheck", "true");
      ta.setAttribute("lang", "en");
      ta.value = state.answers[ta.dataset.key] || "";
      div.appendChild(ta);
    }
    return div;
  }

  // ── autosave ───────────────────────────────────────────────────────────────
  function collectAnswers() {
    if (!state || state.finished) return;
    document.querySelectorAll("#question-container .ex-input").forEach((el) => {
      state.answers[el.dataset.key] = el.value;
    });
  }
  function scheduleSave() {
    if (saveHandle) clearTimeout(saveHandle);
    saveHandle = setTimeout(() => { collectAnswers(); saveState(); saveHandle = null; }, 300);
  }

  // ── timer ──────────────────────────────────────────────────────────────────
  function startTimer() {
    stopTimer();
    timerHandle = setInterval(tick, 1000);
    // shortcut buttons insert text without an input event, so also snapshot regularly
    snapHandle = setInterval(() => { collectAnswers(); saveState(); }, 5000);
  }
  function stopTimer() {
    if (timerHandle) { clearInterval(timerHandle); timerHandle = null; }
    if (snapHandle) { clearInterval(snapHandle); snapHandle = null; }
  }
  function tick() {
    if (!state || state.finished) return;
    updateTimerText();
    if (state.timed && Date.now() >= state.endsAt) finishExam(true);
  }
  function updateTimerText() {
    const el = $("exam-timer");
    if (!el || !state) return;
    if (state.timed) {
      const left = Math.max(0, Math.round((state.endsAt - Date.now()) / 1000));
      el.textContent = "Time left: " + fmtDuration(left);
      el.classList.toggle("low", left <= 300);
    } else {
      el.textContent = "Time taken: " + fmtDuration((Date.now() - state.startedAt) / 1000);
    }
  }

  // ── finishing and marking ──────────────────────────────────────────────────
  function unansweredCount() {
    collectAnswers();
    let blank = 0, total = 0;
    built.forEach((q, qi) => q.parts.forEach((part, pi) => {
      total++;
      const k = qi + "-" + pi;
      let has = false;
      if (part.answerType === "imageChoice") has = state.answers["i-" + k] !== undefined;
      else if (part.answerType === "table") {
        has = Object.keys(state.answers).some((a) => a.indexOf("t-" + k + "-") === 0 && String(state.answers[a]).trim() !== "");
      } else has = String(state.answers["a-" + k] || "").trim() !== "";
      if (!has) blank++;
    }));
    return { blank, total };
  }

  function tryFinish() {
    const { blank, total } = unansweredCount();
    const msg =
      (blank ? blank + " of " + total + " parts have no answer. " : "") +
      "Finish and mark the paper? You will not be able to change your answers.";
    if (confirm(msg)) finishExam(false);
  }

  // Mark every part of every question from the saved answers.
  function markSitting() {
    return built.map((q, qi) => ({
      id: state.qids[qi],
      parts: q.parts.map((part, pi) => markPart(part, qi, pi)),
    }));
  }

  function markPart(part, qi, pi) {
    const k = qi + "-" + pi;
    const marks = part.marks;
    const out = { answer: "", cells: null, chosen: null, hasMarks: marks.length > 0 };
    if (part.answerType === "imageChoice") {
      const chosen = state.answers["i-" + k];
      out.chosen = chosen === undefined ? null : chosen;
      if (chosen !== undefined && chosen === part.correctImageIndex) marks.forEach((m) => { m.awarded = true; });
    } else if (part.answerType === "table") {
      const rows = part.tableRowLabels || [], cols = part.tableColLabels || [];
      out.cells = [];
      let idx = 0;
      rows.forEach((rl, r) => cols.forEach((cl, c) => {
        const raw = String(state.answers["t-" + k + "-" + r + "-" + c] || "").trim();
        const kw = (part.tableCellKeywords && part.tableCellKeywords[r] && part.tableCellKeywords[r][c]) || [];
        const answer = (part.tableCellAnswers && part.tableCellAnswers[r] && part.tableCellAnswers[r][c]) || "";
        const ok = raw !== "" && matchesKeywordGroups(kw, raw);
        if (marks[idx]) marks[idx].awarded = ok;
        idx++;
        out.cells.push({ label: rl + " – " + cl, raw, ok, answer });
      }));
    } else {
      const raw = String(state.answers["a-" + k] || "").trim();
      out.answer = raw;
      if (raw !== "" && marks.length) applyCieMarking(marks, raw);
    }
    out.earned = markEarned(marks);
    out.possible = markTotal(marks);
    return out;
  }

  function finishExam(auto) {
    if (!state || state.finished) return;
    collectAnswers();
    stopTimer();
    state.finished = true;
    state.finishedAt = Date.now();
    state.autoSubmitted = !!auto;
    saveState();
    recordHistory();
    window.scrollTo(0, 0);
    renderReview();
  }

  function recordHistory() {
    try {
      const results = markSitting();
      let earned = 0, possible = 0;
      const per = results.map((q) => {
        const e = q.parts.reduce((s, p) => s + p.earned, 0);
        const p = q.parts.reduce((s, x) => s + x.possible, 0);
        earned += e; possible += p;
        if (p > 0 && window.saveScoreForQuestion) window.saveScoreForQuestion(q.id, (e / p) * 100);
        return { id: q.id, e, p };
      });
      const hist = lsGet(HISTORY_KEY) || [];
      hist.push({
        at: state.finishedAt, level: state.level, tier: state.tier, paper: state.paper,
        earned, possible, seconds: Math.round((state.finishedAt - state.startedAt) / 1000),
        timed: state.timed, extra: state.extra, questions: per,
      });
      lsSet(HISTORY_KEY, hist.slice(-200));
    } catch (e) {
      console.warn("[Exam] could not record history:", e);
    }
  }

  // ── review ─────────────────────────────────────────────────────────────────
  function renderReview() {
    stopTimer();
    // rebuild so marks are applied exactly once to fresh mark objects
    built = defsForState(state).map((d) => buildSeeded(d, state.seed));
    const results = markSitting();
    const defs = defsForState(state);

    let earned = 0, possible = 0;
    const qTotals = results.map((q) => {
      const e = q.parts.reduce((s, p) => s + p.earned, 0);
      const p = q.parts.reduce((s, x) => s + x.possible, 0);
      earned += e; possible += p;
      return { e, p };
    });
    const pct = possible ? Math.round((earned / possible) * 100) : 0;
    const secs = Math.round(((state.finishedAt || Date.now()) - state.startedAt) / 1000);

    // topic summary
    const topics = {};
    defs.forEach((d, i) => {
      const tags = d.tags && d.tags.length ? d.tags : ["Untagged"];
      tags.forEach((t) => {
        topics[t] = topics[t] || { e: 0, p: 0 };
        topics[t].e += qTotals[i].e; topics[t].p += qTotals[i].p;
      });
    });
    const topicRows = Object.keys(topics)
      .map((t) => ({ t, e: topics[t].e, p: topics[t].p, pc: topics[t].p ? topics[t].e / topics[t].p : 0 }))
      .sort((a, b) => a.pc - b.pc)
      .map((r) => "<tr><td>" + esc(r.t) + "</td><td>" + r.e + " / " + r.p + "</td><td>" + Math.round(r.pc * 100) + "%</td></tr>")
      .join("");

    const container = $("question-container");
    container.innerHTML = "";
    const head = document.createElement("div");
    head.className = "exam-summary";
    head.innerHTML =
      "<h2>Paper complete</h2>" +
      '<p class="exam-bigmark">' + earned + " / " + possible + " <span>(" + pct + "%)</span></p>" +
      "<p>" + esc(state.level + (state.tier ? " " + state.tier : "")) + " &middot; " + results.length + " questions &middot; time " +
      fmtDuration(secs) + (state.timed ? " of " + fmtMinutes(state.allowedSec) + " allowed" : " (untimed)") +
      (state.autoSubmitted ? " &middot; <b>submitted automatically when time ran out</b>" : "") + "</p>" +
      '<p class="exam-source">Source paper: ' + esc(state.paper) + "</p>" +
      "<h3>Marks by topic (weakest first)</h3>" +
      '<table class="exam-topics"><tr><th>Topic</th><th>Marks</th><th>%</th></tr>' + topicRows + "</table>" +
      '<div class="exam-actions"><button type="button" id="exam-back">Back to menu</button></div>';
    container.appendChild(head);

    built.forEach((qData, qi) => {
      const sec = document.createElement("section");
      sec.className = "exam-question";
      const h2 = document.createElement("h2");
      h2.innerHTML = qData.mainText;
      sec.appendChild(h2);
      const qt = document.createElement("p");
      qt.className = "exam-qtotal";
      qt.textContent = "Question mark: " + qTotals[qi].e + " / " + qTotals[qi].p;
      sec.appendChild(qt);

      qData.parts.forEach((part, pi) => {
        const r = results[qi].parts[pi];
        const box = document.createElement("div");
        box.className = "question-part exam-review-part";
        const full = r.possible > 0 && r.earned === r.possible;
        box.style.borderLeft = "5px solid " + (!r.hasMarks ? "#999" : full ? "green" : r.earned > 0 ? "orange" : "crimson");

        let html = "<p>" + part.partText + ' <b>(' + r.earned + "/" + r.possible + ")</b></p>";
        if (part.answerType === "imageChoice") {
          const opts = part.imageOptions || [];
          html += "<p><em>Your choice:</em> " + (r.chosen === null ? "no answer" : "option " + (r.chosen + 1)) +
            " &mdash; correct: option " + (part.correctImageIndex + 1) + "</p>";
          if (opts.length) {
            html += '<div class="exam-imgchoice">' + opts.map((f, k) =>
              '<span class="exam-imgopt' + (k === part.correctImageIndex ? " right" : k === r.chosen ? " wrong" : "") + '"><img src="' +
              window.resolveAssetSrc(f) + '" style="width:120px;display:block"></span>').join("") + "</div>";
          }
        } else if (part.answerType === "table") {
          html += "<table><tr><th>Cell</th><th>Your answer</th><th>Model answer</th></tr>" + (r.cells || []).map((c) =>
            '<tr style="color:' + (c.ok ? "green" : "crimson") + '"><td>' + (c.ok ? "&#10003; " : "&#10007; ") + esc(c.label) + "</td><td>" +
            (c.raw ? esc(c.raw) : "<i>blank</i>") + "</td><td>" + c.answer + "</td></tr>").join("") + "</table>";
        } else {
          html += '<p><em>Your answer:</em></p><div class="exam-youranswer">' + (r.answer ? esc(r.answer).replace(/\n/g, "<br>") : "<i>no answer</i>") + "</div>";
        }
        if (part.answerType !== "table" && part.modelAnswer) html += "<p><strong>Model answer:</strong><br>" + renderText(part.modelAnswer) + "</p>";
        if (part.explanation) html += "<p><em>Key idea:</em><br>" + renderText(part.explanation) + "</p>";
        if (r.hasMarks && part.answerType !== "imageChoice") html += buildMarkingBreakdown(part.marks, (part.modelAnswer || "") + " " + (part.explanation || "") + " " + (part.partText || ""));
        if (!r.hasMarks) html += "<p><em>This part is not auto-marked &mdash; compare your answer with the model answer.</em></p>";
        box.innerHTML = html;
        sec.appendChild(box);
      });
      container.appendChild(sec);
    });

    const end = document.createElement("div");
    end.className = "exam-end";
    end.innerHTML = '<button type="button" id="exam-back-bottom">Back to menu</button>';
    container.appendChild(end);
    $("exam-back").addEventListener("click", leaveExam);
    $("exam-back-bottom").addEventListener("click", leaveExam);
  }

  // ── resume banner on the selection page ────────────────────────────────────
  function refreshBanner() {
    const el = $("exam-resume");
    if (!el) return;
    const s = lsGet(SITTING_KEY);
    if (!s) { el.style.display = "none"; el.innerHTML = ""; return; }
    const label = esc(s.level + (s.tier ? " " + s.tier : ""));
    if (!s.finished) {
      el.innerHTML = "<b>Paper in progress</b> (" + label + ", " + s.qids.length + " questions). " +
        '<button type="button" id="exm-resume">Resume</button> <button type="button" id="exm-discard">Discard</button>';
    } else {
      el.innerHTML = "<b>Your last paper is finished</b> (" + label + "). " +
        '<button type="button" id="exm-view">View results</button> <button type="button" id="exm-dismiss">Dismiss</button>';
    }
    el.style.display = "block";
    const on = (id, fn) => { const b = $(id); if (b) b.addEventListener("click", fn); };
    const needLoaded = () => {
      if (!window.allDefinitions) { alert("Questions are still loading — please wait a moment."); return false; }
      return true;
    };
    on("exm-resume", () => { if (!needLoaded()) return; state = s; enterExam(); });
    on("exm-view", () => { if (!needLoaded()) return; state = s; enterExam(); });
    on("exm-discard", () => {
      if (!confirm("Discard this paper and your answers?")) return;
      lsDel(SITTING_KEY); state = null; refreshBanner();
    });
    on("exm-dismiss", () => { lsDel(SITTING_KEY); state = null; refreshBanner(); });
  }

  // ── tooltip toggle for touch screens ───────────────────────────────────────
  document.addEventListener("click", (e) => {
    const tip = e.target.closest && e.target.closest(".info-tip");
    document.querySelectorAll(".exam-wrap.open").forEach((w) => { if (!tip || !w.contains(tip)) w.classList.remove("open"); });
    if (tip) tip.closest(".exam-wrap").classList.toggle("open");
  });

  // ── public hooks used by index.html ────────────────────────────────────────
  window.startExamFlow = startExamFlow;
  window.refreshExamBanner = refreshBanner;
  window.examDebug = () => ({ state, built });   // for automated tests
  document.addEventListener("DOMContentLoaded", refreshBanner);
})();
