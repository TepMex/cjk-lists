/** HSK 2.0 words (exclusive per level; official 2012 syllabus). */

/** HSK 2.0 words (exclusive per level; official 2012 syllabus). level 1. */
export declare const level1: readonly string[];

/** HSK 2.0 words (exclusive per level; official 2012 syllabus). level 2. */
export declare const level2: readonly string[];

/** HSK 2.0 words (exclusive per level; official 2012 syllabus). level 3. */
export declare const level3: readonly string[];

/** HSK 2.0 words (exclusive per level; official 2012 syllabus). level 4. */
export declare const level4: readonly string[];

/** HSK 2.0 words (exclusive per level; official 2012 syllabus). level 5. */
export declare const level5: readonly string[];

/** HSK 2.0 words (exclusive per level; official 2012 syllabus). level 6. */
export declare const level6: readonly string[];

export declare const levels: Readonly<Record<number, readonly string[]>>;
export declare const all: readonly string[];
export declare function level(n: number): readonly string[] | undefined;
