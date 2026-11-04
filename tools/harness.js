// Loads builders + main + engine from a directory into one vm context, with browser stubs.
const vm = require('vm'), fs = require('fs'), path = require('path');
module.exports = function load(dir) {
  const els = {};
  const document = { getElementById: (id) => els[id] || (els[id] = { value: '', style: {}, textContent: '', innerHTML: '' }) };
  const sandbox = { document, console, localStorage: { getItem: () => null, setItem() {} }, Math, JSON, Number, parseFloat, String, Array, Object, RegExp, Set }; sandbox.window = sandbox; const win = sandbox; const ctx = vm.createContext(sandbox);
  ['questionBuilders.js', 'main.js', 'question_engine.js'].forEach((f) => vm.runInContext(fs.readFileSync(path.join(dir, f), 'utf8'), ctx, { filename: f }));
  return { ctx, win, els, run: (code) => vm.runInContext(code, ctx) };
};
