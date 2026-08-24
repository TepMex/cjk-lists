# cjk-lists (Rust)

```toml
[dependencies]
cjk-lists = "0.1"
```

```rust
use cjk_lists::zh::hsk2::hanzi::LEVEL_1;
use cjk_lists::zh::subtlex_ch::TOP_1000;

assert_eq!(TOP_1000[0], "的");
println!("{}", LEVEL_1.len());
```

`no_std`, no dependencies. See the
[repository README](https://github.com/TepMex/cjk-lists) for the full API,
sources, and JavaScript / Python packages.
