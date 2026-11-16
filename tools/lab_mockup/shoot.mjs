import { chromium } from '/opt/node-tools/node_modules/playwright/index.mjs';
import fs from 'node:fs';
const [,, list, out] = process.argv;
const rows = fs.readFileSync(list, 'utf8').trim().split('\n').map(l => l.split(' '));
const b = await chromium.launch({ args: ['--use-gl=angle','--use-angle=swiftshader','--enable-unsafe-swiftshader','--ignore-gpu-blocklist','--autoplay-policy=no-user-gesture-required'] });
const slow = /space|horror|risk|shoprider|poker|minigame|ink-gallery|lust/i;
let i = 0;
async function one([slug, url]) {
  const ctx = await b.newContext({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1.5 });
  const p = await ctx.newPage();
  try {
    await p.goto(url, { waitUntil: 'load', timeout: 60000 });
    await p.waitForTimeout(slow.test(url) ? 12000 : 6000);
    await p.screenshot({ timeout: 90000, path: `${out}/${slug}.png` });
    console.log('ok', slug);
  } catch (e) { console.log('FAIL', slug, e.message.slice(0, 90)); }
  await ctx.close();
}
const queue = [...rows];
await Promise.all([0,1,2,3].map(async () => { while (queue.length) await one(queue.shift()); }));
await b.close();
