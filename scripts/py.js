#!/usr/bin/env node
/**
 * Cross-platform Python launcher.
 *
 * Windows ships `python` or `py`, macOS/Linux ship `python3`. Hard-coding either one
 * breaks npm scripts on the other platform, so this finds whichever exists and runs it.
 *
 *   node scripts/py.js scripts/gen_data.py
 */
const { spawnSync } = require('child_process');

const CANDIDATES = process.platform === 'win32'
  ? ['py -3', 'python', 'python3']
  : ['python3', 'python'];

function resolvePython() {
  for (const cmd of CANDIDATES) {
    const [bin, ...pre] = cmd.split(' ');
    const probe = spawnSync(bin, [...pre, '--version'], { stdio: 'ignore', shell: false });
    if (!probe.error && probe.status === 0) return [bin, pre];
  }
  return null;
}

const found = resolvePython();
if (!found) {
  console.error(
    'No Python interpreter found.\n' +
    `Tried: ${CANDIDATES.join(', ')}\n` +
    'Install Python 3 from https://www.python.org/downloads/ and make sure it is on PATH,\n' +
    'then run:  pip install openpyxl'
  );
  process.exit(1);
}

const [bin, pre] = found;
const r = spawnSync(bin, [...pre, ...process.argv.slice(2)], { stdio: 'inherit', shell: false });
if (r.error) { console.error(r.error.message); process.exit(1); }
process.exit(r.status === null ? 1 : r.status);
