// scripts/questionLoader.js ##v2

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
  // Google Sheets prepends a "## Sheet name: …" line — strip it before parsing
  const csv = rawCsv.replace(/^##[^\n]*\n/, '');

  const { data: rows } = Papa.parse(csv, {
    header: true,
    skipEmptyLines: true,
  });

  // Build raw definitions (params + parts), but do not call genericBuilder yet
  const byId = {};
  rows.forEach((r) => {
    const id = r.id?.trim();
    if (!id) return;
    if (!byId[id]) {
      byId[id] = {
        id,
        type:   r.type?.trim()  || "general",
        level:  r.level?.trim() || "A2",       // NEW: defaults A2 for existing rows
        tags:   parseTags(r.tags),              // NEW: tags as a clean array
        params: JSON.parse(r.params || "{}"),
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
