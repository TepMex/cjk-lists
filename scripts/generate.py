#!/usr/bin/env python3
"""Build canonical JSON lists and JS / Python / Rust package bindings."""

from __future__ import annotations

import json
import sys
import urllib.request
import zipfile
from io import BytesIO
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
JS_SRC = ROOT / "js" / "src"
PY_SRC = ROOT / "python" / "src" / "cjk_lists"
RS_SRC = ROOT / "rust" / "src"
CACHE = ROOT / ".cache" / "sources"

HSK2_BASE = "https://raw.githubusercontent.com/leonsilicon/hsk2.0/main/data/HSK2.0"
HSK3_BASE = "https://raw.githubusercontent.com/leonsilicon/hsk3.0/main/data/HSK3.0"
SUBTLEX_ZIP = (
    "https://journals.plos.org/plosone/article/file"
    "?id=10.1371/journal.pone.0010729.s002&type=supplementary"
)
SUBTLEX_CHR_UNICODE = (
    "https://raw.githubusercontent.com/becky82/mteh/main/sources/SUBTLEX/"
    "SUBTLEX-CH-CHR_converted_to_unicode.txt"
)

LOCAL_HSK2 = Path("/tmp/cjk-src/hsk2")
LOCAL_HSK3 = Path("/tmp/cjk-src/hsk3")
LOCAL_WF = Path("/tmp/cjk-src/subtlex/SUBTLEX-CH-WF")
LOCAL_CHR = Path("/tmp/cjk-src/subtlex/SUBTLEX-CH-CHR_unicode.txt")


def fetch(url: str) -> bytes:
    req = urllib.request.Request(url, headers={"User-Agent": "cjk-lists-generator/0.1"})
    with urllib.request.urlopen(req, timeout=60) as resp:
        return resp.read()


def write_text(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not content.endswith("\n"):
        content += "\n"
    path.write_text(content, encoding="utf-8")


def write_json(path: Path, payload: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def parse_lines(text: str) -> list[str]:
    items: list[str] = []
    seen: set[str] = set()
    for raw in text.splitlines():
        line = raw.strip()
        if not line or line.startswith("#"):
            continue
        if line not in seen:
            items.append(line)
            seen.add(line)
    return items


def split_three(items: list[str]) -> tuple[list[str], list[str], list[str]]:
    third = len(items) // 3
    return items[:third], items[third : 2 * third], items[2 * third :]


def rust_str(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def load_txt(path: Path) -> list[str]:
    return parse_lines(path.read_text(encoding="utf-8"))


def download_text(url: str, dest: Path) -> str:
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists():
        return dest.read_text(encoding="utf-8")
    text = fetch(url).decode("utf-8")
    dest.write_text(text, encoding="utf-8")
    return text


def hsk_items(version: str, filename: str) -> list[str]:
    local_dir = LOCAL_HSK2 if version == "2.0" else LOCAL_HSK3
    local = local_dir / filename
    if local.exists():
        return load_txt(local)
    base = HSK2_BASE if version == "2.0" else HSK3_BASE
    text = download_text(f"{base}/{filename}", CACHE / version / filename)
    return parse_lines(text)


def load_subtlex() -> tuple[list[str], list[str]]:
    wf_dest = CACHE / "SUBTLEX-CH-WF.gbk"
    chr_dest = CACHE / "SUBTLEX-CH-CHR_unicode.txt"
    wf_dest.parent.mkdir(parents=True, exist_ok=True)

    if LOCAL_WF.exists():
        wf_bytes = LOCAL_WF.read_bytes()
        wf_dest.write_bytes(wf_bytes)
    elif wf_dest.exists():
        wf_bytes = wf_dest.read_bytes()
    else:
        blob = fetch(SUBTLEX_ZIP)
        with zipfile.ZipFile(BytesIO(blob)) as zf:
            wf_bytes = zf.read("SUBTLEX-CH-WF")
        wf_dest.write_bytes(wf_bytes)

    if LOCAL_CHR.exists():
        chr_text = LOCAL_CHR.read_text(encoding="utf-8")
        chr_dest.write_text(chr_text, encoding="utf-8")
    elif chr_dest.exists():
        chr_text = chr_dest.read_text(encoding="utf-8")
    else:
        chr_text = fetch(SUBTLEX_CHR_UNICODE).decode("utf-8")
        chr_dest.write_text(chr_text, encoding="utf-8")

    words: list[str] = []
    for line in wf_bytes.decode("gbk").splitlines()[3:]:
        if not line.strip():
            continue
        word = line.split("\t", 1)[0].strip()
        if word:
            words.append(word)

    hanzi: list[str] = []
    header_seen = False
    for line in chr_text.splitlines():
        if not header_seen:
            if line.startswith("Character"):
                header_seen = True
            continue
        if not line.strip():
            continue
        char = line.split()[0]
        if len(char) == 1:
            hanzi.append(char)
    return words, hanzi


def emit_js_array(name: str, items: list[str], doc: str | None = None) -> str:
    dumped = ",\n".join("  " + json.dumps(item, ensure_ascii=False) for item in items)
    header = f"/** {doc} */\n" if doc else ""
    return (
        f"{header}/** @type {{readonly string[]}} */\n"
        f"export const {name} = Object.freeze([\n{dumped}\n]);\n"
    )


def emit_dts_array(name: str, doc: str) -> str:
    return f"/** {doc} */\nexport declare const {name}: readonly string[];\n"


def emit_py_tuple(name: str, items: list[str]) -> str:
    dumped = ",\n".join("    " + json.dumps(item, ensure_ascii=False) for item in items)
    if not items:
        return f"{name}: tuple[str, ...] = ()\n"
    return f"{name}: tuple[str, ...] = (\n{dumped},\n)\n"


def emit_rs_static(name: str, items: list[str], doc: str) -> str:
    dumped = ",\n".join("    " + rust_str(item) for item in items)
    return f"/// {doc}\npub static {name}: &[&str] = &[\n{dumped}\n];\n\n"


def write_js_level_module(
    js_path: Path,
    dts_path: Path,
    levels: dict[int, list[str]],
    extra: dict[str, tuple[str, list[str]]],
    title: str,
    unofficial: set[int] | None = None,
) -> None:
    unofficial = unofficial or set()
    js_parts = [f"/** {title} */\n"]
    dts_parts = [f"/** {title} */\n"]
    names: list[str] = []
    for n in sorted(levels):
        ident = f"level{n}"
        doc = f"{title} level {n}."
        if n in unofficial:
            doc += " Unofficial sequential third of the official 7–9 band."
        js_parts.append(emit_js_array(ident, levels[n], doc))
        dts_parts.append(emit_dts_array(ident, doc))
        names.append(ident)
    for ident, (doc, items) in extra.items():
        js_parts.append(emit_js_array(ident, items, doc))
        dts_parts.append(emit_dts_array(ident, doc))
    level_entries = ",\n".join(f"  {n}: {f'level{n}'}" for n in sorted(levels))
    concat = ", ".join(names)
    js_parts.append(
        f"export const levels = Object.freeze({{\n{level_entries}\n}});\n\n"
        f"export const all = Object.freeze([{concat}].flat());\n\n"
        "/** @param {number} n */\n"
        "export function level(n) {\n"
        "  return levels[n];\n"
        "}\n"
    )
    dts_parts.append(
        "export declare const levels: Readonly<Record<number, readonly string[]>>;\n"
        "export declare const all: readonly string[];\n"
        "export declare function level(n: number): readonly string[] | undefined;\n"
    )
    write_text(js_path, "\n".join(js_parts))
    write_text(dts_path, "\n".join(dts_parts))


def write_py_level_module(
    path: Path,
    levels: dict[int, list[str]],
    extra: dict[str, tuple[str, list[str]]],
    title: str,
    unofficial: set[int] | None = None,
) -> None:
    unofficial = unofficial or set()
    chunks = [f'"""{title}"""\n\nfrom __future__ import annotations\n\n']
    names: list[str] = []
    for n in sorted(levels):
        ident = f"level{n}"
        if n in unofficial:
            chunks.append(
                "# Unofficial sequential third of the official HSK 3.0 7-9 band.\n"
            )
        chunks.append(emit_py_tuple(ident, levels[n]))
        chunks.append("\n")
        names.append(ident)
    extra_names: list[str] = []
    for ident, (_doc, items) in extra.items():
        chunks.append(emit_py_tuple(ident, items))
        chunks.append("\n")
        extra_names.append(ident)
    dict_entries = ", ".join(f"{n}: {name}" for n, name in zip(sorted(levels), names))
    chunks.append(f"levels: dict[int, tuple[str, ...]] = {{{dict_entries}}}\n\n")
    chunks.append("all: tuple[str, ...] = " + " + ".join(names) + "\n\n")
    chunks.append(
        "def level(n: int) -> tuple[str, ...]:\n"
        "    try:\n"
        "        return levels[n]\n"
        "    except KeyError as exc:\n"
        '        raise KeyError(f"unknown level {n}") from exc\n'
    )
    public = names + extra_names + ["levels", "all", "level"]
    chunks.append(f"\n__all__ = {public!r}\n")
    write_text(path, "".join(chunks))


def write_rs_level_module(
    path: Path,
    levels: dict[int, list[str]],
    extra: dict[str, tuple[str, list[str]]],
    title: str,
    unofficial: set[int] | None = None,
) -> None:
    unofficial = unofficial or set()
    chunks = [f"//! {title}\n\n"]
    for n in sorted(levels):
        doc = f"{title} level {n}."
        if n in unofficial:
            doc += " Unofficial sequential third of the official 7-9 band."
        chunks.append(emit_rs_static(f"LEVEL_{n}", levels[n], doc))
    for ident, (doc, items) in extra.items():
        chunks.append(emit_rs_static(ident, items, doc))
    all_items: list[str] = []
    for n in sorted(levels):
        all_items.extend(levels[n])
    chunks.append(emit_rs_static("ALL", all_items, f"All {title} items in level order."))
    match_arms = "\n".join(f"        {n} => Some(LEVEL_{n})," for n in sorted(levels))
    chunks.append(
        "/// Exclusive items introduced at `n`, if that level exists.\n"
        "pub fn level(n: u8) -> Option<&'static [&'static str]> {\n"
        "    match n {\n"
        f"{match_arms}\n"
        "        _ => None,\n"
        "    }\n"
        "}\n"
    )
    write_text(path, "".join(chunks))


def write_js_band_module(
    js_path: Path, dts_path: Path, bands: dict[str, list[str]], title: str
) -> None:
    js_parts = [f"/** {title} */\n"]
    dts_parts = [f"/** {title} */\n"]
    for ident, items in bands.items():
        js_parts.append(emit_js_array(ident, items, f"{title}: {ident}."))
        dts_parts.append(emit_dts_array(ident, f"{title}: {ident}."))
    write_text(js_path, "\n".join(js_parts))
    write_text(dts_path, "\n".join(dts_parts))


def write_py_band_module(path: Path, bands: dict[str, list[str]], title: str) -> None:
    chunks = [f'"""{title}"""\n\nfrom __future__ import annotations\n\n']
    for ident, items in bands.items():
        chunks.append(emit_py_tuple(ident, items))
        chunks.append("\n")
    chunks.append(f"__all__ = {list(bands)!r}\n")
    write_text(path, "".join(chunks))


def write_rs_band_module(path: Path, bands: dict[str, list[str]], title: str) -> None:
    chunks = [f"//! {title}\n\n"]
    for ident, items in bands.items():
        chunks.append(emit_rs_static(ident, items, f"{title}: {ident}."))
    write_text(path, "".join(chunks))


def build_hsk2() -> dict[str, dict[int, list[str]]]:
    return {
        "hanzi": {
            n: hsk_items("2.0", f"HSK2.0_chars_level{n}.txt") for n in range(1, 7)
        },
        "words": {
            n: hsk_items("2.0", f"HSK2.0_words_level{n}.txt") for n in range(1, 7)
        },
    }


def build_hsk3() -> dict:
    hanzi = {n: hsk_items("3.0", f"HSK3.0_chars_level{n}.txt") for n in range(1, 7)}
    words = {n: hsk_items("3.0", f"HSK3.0_words_level{n}.txt") for n in range(1, 7)}
    hanzi_79 = hsk_items("3.0", "HSK3.0_chars_level7-9.txt")
    words_79 = hsk_items("3.0", "HSK3.0_words_level7-9.txt")
    h7, h8, h9 = split_three(hanzi_79)
    w7, w8, w9 = split_three(words_79)
    hanzi[7], hanzi[8], hanzi[9] = h7, h8, h9
    words[7], words[8], words[9] = w7, w8, w9
    return {
        "hanzi": hanzi,
        "words": words,
        "hanzi_7_9": hanzi_79,
        "words_7_9": words_79,
    }


def write_canonical(
    hsk2: dict, hsk3: dict, subtlex_words: list[str], subtlex_hanzi: list[str]
) -> None:
    catalog: dict = {
        "zh": {
            "hsk2": {"hanzi": {}, "words": {}},
            "hsk3": {"hanzi": {}, "words": {}},
            "subtlex_ch": {"hanzi": {}, "words": {}},
        }
    }

    def dump_numbered(series: str, kind: str, mapping: dict[int, list[str]]) -> list[str]:
        all_items: list[str] = []
        for n, items in mapping.items():
            write_json(DATA / "zh" / series / kind / f"{n}.json", items)
            catalog["zh"][series][kind][str(n)] = len(items)
            all_items.extend(items)
        write_json(DATA / "zh" / series / kind / "all.json", all_items)
        catalog["zh"][series][kind]["all"] = len(all_items)
        return all_items

    dump_numbered("hsk2", "hanzi", hsk2["hanzi"])
    dump_numbered("hsk2", "words", hsk2["words"])
    dump_numbered("hsk3", "hanzi", {n: hsk3["hanzi"][n] for n in range(1, 10)})
    dump_numbered("hsk3", "words", {n: hsk3["words"][n] for n in range(1, 10)})
    write_json(DATA / "zh" / "hsk3" / "hanzi" / "7-9.json", hsk3["hanzi_7_9"])
    write_json(DATA / "zh" / "hsk3" / "words" / "7-9.json", hsk3["words_7_9"])
    catalog["zh"]["hsk3"]["hanzi"]["7-9"] = len(hsk3["hanzi_7_9"])
    catalog["zh"]["hsk3"]["words"]["7-9"] = len(hsk3["words_7_9"])

    word_bands = {
        "top-1000": subtlex_words[:1000],
        "1001-2000": subtlex_words[1000:2000],
        "2001-3000": subtlex_words[2000:3000],
        "top-10000": subtlex_words[:10000],
    }
    for key, items in word_bands.items():
        write_json(DATA / "zh" / "subtlex-ch" / "words" / f"{key}.json", items)
        catalog["zh"]["subtlex_ch"]["words"][key] = len(items)

    hanzi_bands = {
        "top-1000": subtlex_hanzi[:1000],
        "1001-2000": subtlex_hanzi[1000:2000],
        "2001-3000": subtlex_hanzi[2000:3000],
        "top-5000": subtlex_hanzi[:5000],
    }
    for key, items in hanzi_bands.items():
        write_json(DATA / "zh" / "subtlex-ch" / "hanzi" / f"{key}.json", items)
        catalog["zh"]["subtlex_ch"]["hanzi"][key] = len(items)

    write_json(DATA / "catalog.json", catalog)


def write_bindings(
    hsk2: dict, hsk3: dict, subtlex_words: list[str], subtlex_hanzi: list[str]
) -> None:
    unofficial = {7, 8, 9}
    write_js_level_module(
        JS_SRC / "zh" / "hsk2" / "hanzi.js",
        JS_SRC / "zh" / "hsk2" / "hanzi.d.ts",
        hsk2["hanzi"],
        {},
        "HSK 2.0 hanzi (exclusive per level; derived from the official word list).",
    )
    write_js_level_module(
        JS_SRC / "zh" / "hsk2" / "words.js",
        JS_SRC / "zh" / "hsk2" / "words.d.ts",
        hsk2["words"],
        {},
        "HSK 2.0 words (exclusive per level; official 2012 syllabus).",
    )
    write_js_level_module(
        JS_SRC / "zh" / "hsk3" / "hanzi.js",
        JS_SRC / "zh" / "hsk3" / "hanzi.d.ts",
        {n: hsk3["hanzi"][n] for n in range(1, 10)},
        {
            "level7To9": (
                "Official combined HSK 3.0 levels 7-9 hanzi (not split by Hanban).",
                hsk3["hanzi_7_9"],
            )
        },
        "HSK 3.0 hanzi (exclusive per level; official 2021 character lists).",
        unofficial=unofficial,
    )
    write_js_level_module(
        JS_SRC / "zh" / "hsk3" / "words.js",
        JS_SRC / "zh" / "hsk3" / "words.d.ts",
        {n: hsk3["words"][n] for n in range(1, 10)},
        {
            "level7To9": (
                "Official combined HSK 3.0 levels 7-9 words (not split by Hanban).",
                hsk3["words_7_9"],
            )
        },
        "HSK 3.0 words (exclusive per level; official 2021 word lists).",
        unofficial=unofficial,
    )
    write_js_band_module(
        JS_SRC / "zh" / "subtlex-ch" / "words.js",
        JS_SRC / "zh" / "subtlex-ch" / "words.d.ts",
        {
            "top1000": subtlex_words[:1000],
            "second1000": subtlex_words[1000:2000],
            "third1000": subtlex_words[2000:3000],
            "top10000": subtlex_words[:10000],
        },
        "SUBTLEX-CH word frequency ranks (Cai & Brysbaert, 2010).",
    )
    write_js_band_module(
        JS_SRC / "zh" / "subtlex-ch" / "hanzi.js",
        JS_SRC / "zh" / "subtlex-ch" / "hanzi.d.ts",
        {
            "top1000": subtlex_hanzi[:1000],
            "second1000": subtlex_hanzi[1000:2000],
            "third1000": subtlex_hanzi[2000:3000],
            "top5000": subtlex_hanzi[:5000],
        },
        "SUBTLEX-CH character frequency ranks (Cai & Brysbaert, 2010).",
    )
    write_text(
        JS_SRC / "zh" / "hsk2" / "index.js",
        "export * as hanzi from './hanzi.js';\nexport * as words from './words.js';\n",
    )
    write_text(
        JS_SRC / "zh" / "hsk2" / "index.d.ts",
        "export * as hanzi from './hanzi.js';\nexport * as words from './words.js';\n",
    )
    write_text(
        JS_SRC / "zh" / "hsk3" / "index.js",
        "export * as hanzi from './hanzi.js';\nexport * as words from './words.js';\n",
    )
    write_text(
        JS_SRC / "zh" / "hsk3" / "index.d.ts",
        "export * as hanzi from './hanzi.js';\nexport * as words from './words.js';\n",
    )
    write_text(
        JS_SRC / "zh" / "subtlex-ch" / "index.js",
        "export * as hanzi from './hanzi.js';\n"
        "export * as words from './words.js';\n"
        "export { top1000, second1000, third1000, top10000 } from './words.js';\n",
    )
    write_text(
        JS_SRC / "zh" / "subtlex-ch" / "index.d.ts",
        "export * as hanzi from './hanzi.js';\n"
        "export * as words from './words.js';\n"
        "export { top1000, second1000, third1000, top10000 } from './words.js';\n",
    )
    write_text(
        JS_SRC / "zh" / "index.js",
        "export * as hsk2 from './hsk2/index.js';\n"
        "export * as hsk3 from './hsk3/index.js';\n"
        "export * as subtlexCh from './subtlex-ch/index.js';\n",
    )
    write_text(
        JS_SRC / "zh" / "index.d.ts",
        "export * as hsk2 from './hsk2/index.js';\n"
        "export * as hsk3 from './hsk3/index.js';\n"
        "export * as subtlexCh from './subtlex-ch/index.js';\n",
    )
    write_text(JS_SRC / "index.js", "export * as zh from './zh/index.js';\n")
    write_text(JS_SRC / "index.d.ts", "export * as zh from './zh/index.js';\n")

    write_py_level_module(
        PY_SRC / "zh" / "hsk2" / "hanzi.py",
        hsk2["hanzi"],
        {},
        "HSK 2.0 hanzi (exclusive per level; derived from the official word list).",
    )
    write_py_level_module(
        PY_SRC / "zh" / "hsk2" / "words.py",
        hsk2["words"],
        {},
        "HSK 2.0 words (exclusive per level; official 2012 syllabus).",
    )
    write_py_level_module(
        PY_SRC / "zh" / "hsk3" / "hanzi.py",
        {n: hsk3["hanzi"][n] for n in range(1, 10)},
        {"level7_9": ("Official combined HSK 3.0 levels 7-9 hanzi.", hsk3["hanzi_7_9"])},
        "HSK 3.0 hanzi (exclusive per level; official 2021 character lists).",
        unofficial=unofficial,
    )
    write_py_level_module(
        PY_SRC / "zh" / "hsk3" / "words.py",
        {n: hsk3["words"][n] for n in range(1, 10)},
        {"level7_9": ("Official combined HSK 3.0 levels 7-9 words.", hsk3["words_7_9"])},
        "HSK 3.0 words (exclusive per level; official 2021 word lists).",
        unofficial=unofficial,
    )
    write_py_band_module(
        PY_SRC / "zh" / "subtlex_ch" / "words.py",
        {
            "top_1000": subtlex_words[:1000],
            "second_1000": subtlex_words[1000:2000],
            "third_1000": subtlex_words[2000:3000],
            "top_10000": subtlex_words[:10000],
        },
        "SUBTLEX-CH word frequency ranks (Cai & Brysbaert, 2010).",
    )
    write_py_band_module(
        PY_SRC / "zh" / "subtlex_ch" / "hanzi.py",
        {
            "top_1000": subtlex_hanzi[:1000],
            "second_1000": subtlex_hanzi[1000:2000],
            "third_1000": subtlex_hanzi[2000:3000],
            "top_5000": subtlex_hanzi[:5000],
        },
        "SUBTLEX-CH character frequency ranks (Cai & Brysbaert, 2010).",
    )
    write_text(
        PY_SRC / "zh" / "hsk2" / "__init__.py",
        "from . import hanzi, words\n\n__all__ = ['hanzi', 'words']\n",
    )
    write_text(
        PY_SRC / "zh" / "hsk3" / "__init__.py",
        "from . import hanzi, words\n\n__all__ = ['hanzi', 'words']\n",
    )
    write_text(
        PY_SRC / "zh" / "subtlex_ch" / "__init__.py",
        "from . import hanzi, words\n"
        "from .words import second_1000, third_1000, top_1000, top_10000\n\n"
        "__all__ = ['hanzi', 'words', 'top_1000', 'second_1000', 'third_1000', 'top_10000']\n",
    )
    write_text(
        PY_SRC / "zh" / "__init__.py",
        "from . import hsk2, hsk3, subtlex_ch\n\n__all__ = ['hsk2', 'hsk3', 'subtlex_ch']\n",
    )
    write_text(
        PY_SRC / "__init__.py",
        '"""Convenient official CJK character and word lists."""\n\n'
        "from . import zh\n\n"
        '__version__ = "0.1.0"\n'
        "__all__ = ['zh']\n",
    )
    write_text(PY_SRC / "py.typed", "")

    write_rs_level_module(
        RS_SRC / "zh" / "hsk2" / "hanzi.rs",
        hsk2["hanzi"],
        {},
        "HSK 2.0 hanzi (exclusive per level; derived from the official word list).",
    )
    write_rs_level_module(
        RS_SRC / "zh" / "hsk2" / "words.rs",
        hsk2["words"],
        {},
        "HSK 2.0 words (exclusive per level; official 2012 syllabus).",
    )
    write_rs_level_module(
        RS_SRC / "zh" / "hsk3" / "hanzi.rs",
        {n: hsk3["hanzi"][n] for n in range(1, 10)},
        {"LEVEL_7_9": ("Official combined HSK 3.0 levels 7-9 hanzi.", hsk3["hanzi_7_9"])},
        "HSK 3.0 hanzi (exclusive per level; official 2021 character lists).",
        unofficial=unofficial,
    )
    write_rs_level_module(
        RS_SRC / "zh" / "hsk3" / "words.rs",
        {n: hsk3["words"][n] for n in range(1, 10)},
        {"LEVEL_7_9": ("Official combined HSK 3.0 levels 7-9 words.", hsk3["words_7_9"])},
        "HSK 3.0 words (exclusive per level; official 2021 word lists).",
        unofficial=unofficial,
    )
    write_rs_band_module(
        RS_SRC / "zh" / "subtlex_ch" / "words.rs",
        {
            "TOP_1000": subtlex_words[:1000],
            "SECOND_1000": subtlex_words[1000:2000],
            "THIRD_1000": subtlex_words[2000:3000],
            "TOP_10000": subtlex_words[:10000],
        },
        "SUBTLEX-CH word frequency ranks (Cai & Brysbaert, 2010).",
    )
    write_rs_band_module(
        RS_SRC / "zh" / "subtlex_ch" / "hanzi.rs",
        {
            "TOP_1000": subtlex_hanzi[:1000],
            "SECOND_1000": subtlex_hanzi[1000:2000],
            "THIRD_1000": subtlex_hanzi[2000:3000],
            "TOP_5000": subtlex_hanzi[:5000],
        },
        "SUBTLEX-CH character frequency ranks (Cai & Brysbaert, 2010).",
    )
    write_text(RS_SRC / "zh" / "hsk2" / "mod.rs", "pub mod hanzi;\npub mod words;\n")
    write_text(RS_SRC / "zh" / "hsk3" / "mod.rs", "pub mod hanzi;\npub mod words;\n")
    write_text(
        RS_SRC / "zh" / "subtlex_ch" / "mod.rs",
        "pub mod hanzi;\npub mod words;\n"
        "pub use words::{SECOND_1000, THIRD_1000, TOP_1000, TOP_10000};\n",
    )
    write_text(RS_SRC / "zh" / "mod.rs", "pub mod hsk2;\npub mod hsk3;\npub mod subtlex_ch;\n")
    write_text(
        RS_SRC / "lib.rs",
        "//! Convenient official CJK character and word lists.\n\n"
        "#![no_std]\n\n"
        "pub mod zh;\n",
    )


def main() -> int:
    print("Loading HSK 2.0…", file=sys.stderr)
    hsk2 = build_hsk2()
    print("Loading HSK 3.0…", file=sys.stderr)
    hsk3 = build_hsk3()
    print("Loading SUBTLEX-CH…", file=sys.stderr)
    words, hanzi = load_subtlex()
    print(f"SUBTLEX-CH words={len(words)} hanzi={len(hanzi)}", file=sys.stderr)
    write_canonical(hsk2, hsk3, words, hanzi)
    write_bindings(hsk2, hsk3, words, hanzi)
    print("Wrote data/ and language bindings.", file=sys.stderr)
    return 0


if __name__ == "__main__":
    sys.exit(main())
