# cjk-lists

Public packages that expose official CJK character and word lists as
plain, importable data. One folder per programming language:

| Folder   | Registry | Install |
| -------- | -------- | ------- |
| `js/`    | npm / bun | `npm install cjk-lists` / `bun add cjk-lists` |
| `python/` | PyPI    | `pip install cjk-lists` |
| `rust/`  | crates.io | `cjk-lists` in `Cargo.toml` |

Canonical JSON lives in [`data/`](data/). Language bindings are generated
from those files by [`scripts/generate.py`](scripts/generate.py).

Japanese and Korean lists will follow the same layout. This release starts
with **Mandarin Chinese (simplified hanzi)**.

## Mandarin Chinese

```text
zh
├── hsk2.hanzi / hsk2.words     levels 1–6 (exclusive)
├── hsk3.hanzi / hsk3.words     levels 1–9 (exclusive)
└── subtlexCh                   frequency bands
```

Levels are **exclusive**: level 4 is the items introduced at 4, not the
union of 1–4. Use `all` when you want every item in order.

HSK 3.0 does **not** officially split levels 7–9. `level7` / `level8` /
`level9` are equal sequential thirds of that official band. Prefer
`level7To9` (JS), `level7_9` (Python), or `LEVEL_7_9` (Rust) when you need
the combined syllabus list.

Provenance, licenses, and exact counts: [`data/SOURCES.md`](data/SOURCES.md).

### JavaScript / TypeScript (npm, bun)

```js
import { zh } from 'cjk-lists';
import { level1 as hsk2Hanzi1 } from 'cjk-lists/zh/hsk2/hanzi';
import { top1000, second1000, third1000, top10000 } from 'cjk-lists/zh/subtlex-ch';

zh.hsk2.hanzi.level1;          // HSK 2.0 hanzi, level 1
zh.hsk2.words.level(3);        // HSK 2.0 words, level 3
zh.hsk3.hanzi.level7To9;       // official HSK 3.0 hanzi 7–9
zh.subtlexCh.top1000;          // SUBTLEX-CH words, ranks 1–1000
zh.subtlexCh.hanzi.top1000;    // SUBTLEX-CH characters, ranks 1–1000
```

Works with Node.js 18+ (`type: module`) and Bun.

### Python (pip)

```python
from cjk_lists import zh

zh.hsk2.hanzi.level1
zh.hsk2.words.level(3)
zh.hsk3.hanzi.level7_9
zh.subtlex_ch.top_1000
zh.subtlex_ch.hanzi.top_1000
```

```python
from cjk_lists.zh.hsk3.hanzi import level1, level9, all
from cjk_lists.zh.subtlex_ch.words import second_1000, third_1000, top_10000
```

### Rust (cargo)

```rust
use cjk_lists::zh::hsk2::hanzi::LEVEL_1;
use cjk_lists::zh::hsk3::hanzi::{LEVEL_7_9, level};
use cjk_lists::zh::subtlex_ch::{TOP_1000, SECOND_1000, THIRD_1000, TOP_10000};

assert!(LEVEL_1.contains(&"爱"));
assert_eq!(level(1).unwrap().len(), 300);
assert_eq!(TOP_1000[0], "的");
```

The crate is `no_std` and has no dependencies.

## Install from this repo

Until the packages are published to npm / PyPI / crates.io:

```bash
# JavaScript (npm or bun)
npm install ./js
bun add ./js

# Python
pip install ./python

# Rust — from a sibling crate, after cloning this repo:
# cjk-lists = { path = "../cjk-lists/rust" }
# or, once pushed:
# cjk-lists = { git = "https://github.com/TepMex/cjk-lists" }
```

## Regenerating lists

```bash
python3 scripts/generate.py
```

## License

Package code is [MIT](LICENSE). HSK lists are transcriptions of public
exam syllabi. SUBTLEX-CH is CC BY 4.0; cite Cai & Brysbaert (2010) if you
use those ranks. See [`data/SOURCES.md`](data/SOURCES.md).
