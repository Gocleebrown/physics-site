// scripts/questionLoader.js

const SHEET_CSV_URL =
  "https://docs.google.com/spreadsheets/d/1mspkPndqlydcum52DiVx_oq0cbmV8F06igR8kISehTI/export?format=csv&gid=0";

async function loadQuestionsFromSheet() {
  console.log("[Loader] fetching CSV…");
  const res = await fetch(SHEET_CSV_URL);
  const csv = await res.text();

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
        type: r.type?.trim() || "general",
        params: JSON.parse(r.params || "{}"),
        parts: [],
      };
    }
    byId[id].parts.push(r);
  });

  const definitions = Object.values(byId);
  // Expose definitions for fresh builds on each Next Question
  window.questions = definitions;
  console.log("[Loader] stored question definitions:", definitions);
  return definitions;
}
 
