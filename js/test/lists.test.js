import assert from 'node:assert/strict';
import test from 'node:test';

import { zh } from '../src/index.js';
import { level1 as hsk2Hanzi1, all as hsk2HanziAll } from '../src/zh/hsk2/hanzi.js';
import { top1000, second1000, third1000, top10000 } from '../src/zh/subtlex-ch/words.js';

test('HSK 2.0 word counts match the 2012 syllabus', () => {
  assert.deepEqual(
    [1, 2, 3, 4, 5, 6].map((n) => zh.hsk2.words.level(n).length),
    [150, 150, 300, 600, 1300, 2500],
  );
  assert.equal(zh.hsk2.words.all.length, 5000);
});

test('HSK 2.0 hanzi is derived exclusively per level', () => {
  assert.equal(hsk2Hanzi1.length, 176);
  assert.ok(hsk2Hanzi1.includes('爱'));
  assert.ok(zh.hsk2.words.level1.includes('爱'));
  assert.equal(hsk2HanziAll.length, 2663);
  const seen = new Set();
  for (const n of [1, 2, 3, 4, 5, 6]) {
    for (const ch of zh.hsk2.hanzi.level(n)) {
      assert.equal(ch.length, 1, ch);
      assert.ok(!seen.has(ch), `duplicate hanzi ${ch}`);
      seen.add(ch);
    }
  }
});

test('HSK 3.0 hanzi bands follow the 2021 standard', () => {
  for (const n of [1, 2, 3, 4, 5, 6]) {
    assert.equal(zh.hsk3.hanzi.level(n).length, 300);
  }
  assert.equal(zh.hsk3.hanzi.level7.length, 400);
  assert.equal(zh.hsk3.hanzi.level8.length, 400);
  assert.equal(zh.hsk3.hanzi.level9.length, 400);
  assert.equal(zh.hsk3.hanzi.level7To9.length, 1200);
  assert.deepEqual(
    [...zh.hsk3.hanzi.level7, ...zh.hsk3.hanzi.level8, ...zh.hsk3.hanzi.level9],
    [...zh.hsk3.hanzi.level7To9],
  );
  assert.equal(zh.hsk3.hanzi.all.length, 3000);
  assert.ok(zh.hsk3.hanzi.level1.includes('的'));
});

test('HSK 3.0 words cover each official band', () => {
  assert.ok(zh.hsk3.words.level1.length >= 490);
  assert.ok(zh.hsk3.words.level1.includes('爱'));
  assert.equal(
    zh.hsk3.words.level7.length + zh.hsk3.words.level8.length + zh.hsk3.words.level9.length,
    zh.hsk3.words.level7To9.length,
  );
  assert.equal(zh.hsk3.words.all.length, zh.hsk3.words.level7To9.length +
    [1, 2, 3, 4, 5, 6].reduce((sum, n) => sum + zh.hsk3.words.level(n).length, 0));
});

test('SUBTLEX-CH word bands are ranked and adjacent', () => {
  assert.equal(top1000.length, 1000);
  assert.equal(second1000.length, 1000);
  assert.equal(third1000.length, 1000);
  assert.equal(top10000.length, 10000);
  assert.equal(top1000[0], '的');
  assert.deepEqual(top10000.slice(0, 1000), [...top1000]);
  assert.deepEqual(top10000.slice(1000, 2000), [...second1000]);
  assert.deepEqual(top10000.slice(2000, 3000), [...third1000]);
  assert.equal(zh.subtlexCh.hanzi.top1000[0], '我');
  assert.equal(zh.subtlexCh.hanzi.top1000.length, 1000);
});
