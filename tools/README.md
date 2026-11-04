# /tools — build and test scripts (no answer data)

These run in Node/Python and are NOT served by the site. They test sheet rows against the real engine in `/scripts`.

1. Export the sheet tab "read from here" as CSV (Drive export), then:
   `python3 tools/csv_to_json.py sheet.csv sheet.json`
2. Build test — builds every question 60 times, fails on NaN/undefined/`${`, and marks the model answer of every part:
   `node tools/build_test.js scripts sheet.json 189 result.json`
   (args: scripts dir, sheet json, first row to test, output file). Prints question count, build failures, bad-text count, and the number of rows that do not score full marks on their own model answer.
3. `example_marking_test.js` shows how to write a student-simulation test (right answer, wrong answer, blank) for one question. Copy and edit the id. Reset `marks[i].awarded=false` before every `applyCieMarking(marks, studentText)` call.
4. `harness.js` loads the three engine files plus main.js into a vm with browser stubs.

Read `HANDOVER.md` first: it holds all the rules.
