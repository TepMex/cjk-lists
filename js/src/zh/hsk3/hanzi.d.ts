/** HSK 3.0 hanzi (exclusive per level; official 2021 character lists). */

/** HSK 3.0 hanzi (exclusive per level; official 2021 character lists). level 1. */
export declare const level1: readonly string[];

/** HSK 3.0 hanzi (exclusive per level; official 2021 character lists). level 2. */
export declare const level2: readonly string[];

/** HSK 3.0 hanzi (exclusive per level; official 2021 character lists). level 3. */
export declare const level3: readonly string[];

/** HSK 3.0 hanzi (exclusive per level; official 2021 character lists). level 4. */
export declare const level4: readonly string[];

/** HSK 3.0 hanzi (exclusive per level; official 2021 character lists). level 5. */
export declare const level5: readonly string[];

/** HSK 3.0 hanzi (exclusive per level; official 2021 character lists). level 6. */
export declare const level6: readonly string[];

/** HSK 3.0 hanzi (exclusive per level; official 2021 character lists). level 7. Unofficial sequential third of the official 7–9 band. */
export declare const level7: readonly string[];

/** HSK 3.0 hanzi (exclusive per level; official 2021 character lists). level 8. Unofficial sequential third of the official 7–9 band. */
export declare const level8: readonly string[];

/** HSK 3.0 hanzi (exclusive per level; official 2021 character lists). level 9. Unofficial sequential third of the official 7–9 band. */
export declare const level9: readonly string[];

/** Official combined HSK 3.0 levels 7-9 hanzi (not split by Hanban). */
export declare const level7To9: readonly string[];

export declare const levels: Readonly<Record<number, readonly string[]>>;
export declare const all: readonly string[];
export declare function level(n: number): readonly string[] | undefined;
