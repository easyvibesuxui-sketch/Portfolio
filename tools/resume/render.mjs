// node tools/resume/render.mjs <in.html> <out.pdf> [landscape]
import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import { pathToFileURL } from 'node:url';
import path from 'node:path';
const [,, src, out, mode] = process.argv;
const b = await chromium.launch();
const p = await b.newPage();
await p.goto(pathToFileURL(path.resolve(src)).href, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: out, preferCSSPageSize: true, printBackground: true, tagged: true, outline: true });
await b.close();
console.log('wrote', out);
