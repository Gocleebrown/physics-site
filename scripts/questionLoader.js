// scripts/questionLoader.js ##v4

const SHEET_CSV_URL =
  "https://docs.google.com/spreadsheets/d/1mspkPndqlydcum52DiVx_oq0cbmV8F06igR8kISehTI/export?format=csv&gid=0";

// Parse a comma-separated tags string into a clean array.
// e.g. "Circular motion, Gravitation" → ["Circular motion", "Gravitation"]
function parseTags(tagsStr) {
  if (!tagsStr || !tagsStr.trim()) return [];
  return tagsStr.split(',').map(t => t.trim()).filter(Boolean);
}

async function loadQuestionsFromSheet() {
  console.log("[Loader] fetching CSV…");
  const res = await fetch(SHEET_CSV_URL);
  if (!res.ok) {
    throw new Error(`[Loader] CSV fetch failed: ${res.status} ${res.statusText}`);
  }
  const rawCsv = await res.text();
  // Google Sheets may prepend a UTF-8 BOM and/or one or more "## …" comment lines.
  // Strip them all so PapaParse sees a clean CSV header on line 1.
  const rawNoBom = rawCsv.replace(/^﻿/, '');
  const lines = rawNoBom.split(/\r?\n/);
  const dataStart = lines.findIndex(l => l.trim().length > 0 && !l.trim().startsWith('#'));
  const csv = dataStart > 0 ? lines.slice(dataStart).join('\n') : rawNoBom;

  const { data: rows } = Papa.parse(csv, {
    header: true,
    skipEmptyLines: true,
  });

  // Build raw definitions (params + parts), but do not call genericBuilder yet
  const byId = {};
  rows.forEach((r) => {
    const id = r.id?.trim();
    // Skip blank ids and any header row that slipped through as data
    if (!id || id === 'id') return;
    if (!byId[id]) {
      let parsedParams = {};
      try {
        parsedParams = JSON.parse(r.params || "{}");
      } catch (e) {
        console.warn("[Loader] bad params for id=" + id + ":", r.params);
      }
      byId[id] = {
        id,
        type:   r.type?.trim()  || "general",
        level:  r.level?.trim() || "A2",
        tags:   parseTags(r.tags),
        params: parsedParams,
        parts:  [],
      };
    }
    byId[id].parts.push(r);
  });

  const definitions = Object.values(byId);

  // Store unfiltered dataset separately so the selection page can filter it.
  // window.questions is kept in sync as the *active* filtered set.
  window.allDefinitions = definitions;
  window.questions = definitions; // default: all questions (backward-compatible)

  console.log("[Loader] stored", definitions.length, "question definitions");
  return definitions;
}

// Return sorted unique topic tags for a given level, drawn from window.allDefinitions.
// Pass level=null to get tags across all levels.
function getTopicsForLevel(level) {
  const defs = window.allDefinitions || window.questions || [];
  const tagSet = new Set();
  defs.forEach(q => {
    if (!level || q.level === level) {
      (q.tags || []).forEach(t => tagSet.add(t));
    }
  });
  return Array.from(tagSet).sort();
}

// Return definitions matching a level, optionally filtered by a Set of topic strings.
// topicSet=null or empty Set → return all questions for that level.
function filterQuestionsByLevelAndTopics(level, topicSet) {
  const defs = window.allDefinitions || window.questions || [];
  return defs.filter(q => {
    if (q.level !== level) return false;
    if (!topicSet || topicSet.size === 0) return true;
    return (q.tags || []).some(t => topicSet.has(t));
  });
}
