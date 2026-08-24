# Data sources

Lists in this repository are transcriptions of public standards and
open-access frequency data. The code that packages them is MIT-licensed;
the lists themselves remain subject to their original terms.

## HSK 2.0 (2012)

Official *Hanyu Shuiping Kaoshi* vocabulary syllabus (levels 1–6).

- Primary file: [HSK-2012.xls](https://www.chinesetest.cn/userfiles/file/HSK/HSK-2012.xls)
- Machine-readable transcription used here: [leonsilicon/hsk2.0](https://github.com/leonsilicon/hsk2.0)
  (`data/HSK2.0`, itself based on [becky82/mteh](https://github.com/becky82/mteh))

Hanzi lists are **not published separately** for HSK 2.0. Characters are
assigned to the first level in which they appear in the official word list.

Counts after de-duplication within each level:

| Level | Words | Hanzi |
| ----- | ----- | ----- |
| 1     | 150   | 176   |
| 2     | 150   | 176   |
| 3     | 300   | 269   |
| 4     | 600   | 446   |
| 5     | 1300  | 620   |
| 6     | 2500  | 976   |
| total | 5000  | 2663  |

## HSK 3.0 (2021)

Official *Chinese Proficiency Grading Standards for International Chinese
Language Education* (GF 0025-2021).

- Standard (PDF): [Ministry of Education, 2021-03-31](http://www.moe.gov.cn/jyb_xwfb/gzdt_gzdt/s5987/202103/W020210329527301787356.pdf)
- Machine-readable transcription used here: [leonsilicon/hsk3.0](https://github.com/leonsilicon/hsk3.0)
  (`data/HSK3.0`, cross-checked community OCR of the official PDF)

Hanzi levels 1–6 are official 300-character bands. Levels **7–9 are one
official band** (1200 characters / ~5600 words). This package also exposes
`level7`, `level8`, and `level9` as equal sequential thirds of that band so
callers can import nine lists; use `level7To9` / `level7_9` / `LEVEL_7_9`
when you need the official combined list.

Word lists keep official forms, including variants such as `爸爸|爸` and
example-marked suffixes. Duplicate surface forms *inside a single level*
are dropped (first occurrence kept), so some word counts are a few items
below the published syllabus totals.

## SUBTLEX-CH

Cai, Q., & Brysbaert, M. (2010). SUBTLEX-CH: Chinese Word and Character
Frequencies Based on Film Subtitles. *PLOS ONE, 5*(6), e10729.
https://doi.org/10.1371/journal.pone.0010729

The article and supplementary files are under the Creative Commons
Attribution License. Please cite Cai & Brysbaert (2010) if you use these
ranks.

- Word frequencies: `SUBTLEX-CH-WF` from
  [PLOS ONE File S1 / s002](https://doi.org/10.1371/journal.pone.0010729.s002)
  (GBK-encoded, ranked by descending `WCount`)
- Character frequencies: Unicode conversion of `SUBTLEX-CH-CHR` from
  [becky82/mteh](https://github.com/becky82/mteh/blob/main/sources/SUBTLEX/SUBTLEX-CH-CHR_converted_to_unicode.txt)
  (ranked by descending character count)

The published character list has fewer than 10,000 types, so character
bands stop at top 1000 / 1001–2000 / 2001–3000 / top 5000. Word bands
include top 10,000 as requested.

## Regenerating

```bash
python3 scripts/generate.py
```

Sources are read from `/tmp/cjk-src` when present, otherwise downloaded
into `.cache/sources`.
