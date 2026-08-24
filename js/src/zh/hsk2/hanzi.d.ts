/** HSK 2.0 hanzi (exclusive per level; derived from the official word list). */

/** HSK 2.0 hanzi (exclusive per level; derived from the official word list). level 1. */
export declare const level1: readonly string[];

/** HSK 2.0 hanzi (exclusive per level; derived from the official word list). level 2. */
export declare const level2: readonly string[];

/** HSK 2.0 hanzi (exclusive per level; derived from the official word list). level 3. */
export declare const level3: readonly string[];

/** HSK 2.0 hanzi (exclusive per level; derived from the official word list). level 4. */
export declare const level4: readonly string[];

/** HSK 2.0 hanzi (exclusive per level; derived from the official word list). level 5. */
export declare const level5: readonly string[];

/** HSK 2.0 hanzi (exclusive per level; derived from the official word list). level 6. */
export declare const level6: readonly string[];

export declare const levels: Readonly<Record<number, readonly string[]>>;
export declare const all: readonly string[];
export declare function level(n: number): readonly string[] | undefined;
