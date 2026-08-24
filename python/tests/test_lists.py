import unittest

from cjk_lists import zh


class Hsk2Tests(unittest.TestCase):
    def test_word_counts(self) -> None:
        self.assertEqual(
            [len(zh.hsk2.words.level(n)) for n in range(1, 7)],
            [150, 150, 300, 600, 1300, 2500],
        )
        self.assertEqual(len(zh.hsk2.words.all), 5000)

    def test_hanzi_exclusive(self) -> None:
        self.assertEqual(len(zh.hsk2.hanzi.level1), 176)
        self.assertIn("爱", zh.hsk2.hanzi.level1)
        self.assertIn("爱", zh.hsk2.words.level1)
        seen: set[str] = set()
        for n in range(1, 7):
            for ch in zh.hsk2.hanzi.level(n):
                self.assertEqual(len(ch), 1, ch)
                self.assertNotIn(ch, seen)
                seen.add(ch)
        self.assertEqual(len(seen), 2663)


class Hsk3Tests(unittest.TestCase):
    def test_hanzi_bands(self) -> None:
        for n in range(1, 7):
            self.assertEqual(len(zh.hsk3.hanzi.level(n)), 300)
        self.assertEqual(len(zh.hsk3.hanzi.level7), 400)
        self.assertEqual(len(zh.hsk3.hanzi.level8), 400)
        self.assertEqual(len(zh.hsk3.hanzi.level9), 400)
        self.assertEqual(len(zh.hsk3.hanzi.level7_9), 1200)
        self.assertEqual(
            zh.hsk3.hanzi.level7 + zh.hsk3.hanzi.level8 + zh.hsk3.hanzi.level9,
            zh.hsk3.hanzi.level7_9,
        )
        self.assertEqual(len(zh.hsk3.hanzi.all), 3000)
        self.assertIn("的", zh.hsk3.hanzi.level1)

    def test_word_bands(self) -> None:
        self.assertGreaterEqual(len(zh.hsk3.words.level1), 490)
        self.assertIn("爱", zh.hsk3.words.level1)
        self.assertEqual(
            len(zh.hsk3.words.level7)
            + len(zh.hsk3.words.level8)
            + len(zh.hsk3.words.level9),
            len(zh.hsk3.words.level7_9),
        )


class SubtlexTests(unittest.TestCase):
    def test_word_bands(self) -> None:
        self.assertEqual(len(zh.subtlex_ch.top_1000), 1000)
        self.assertEqual(len(zh.subtlex_ch.second_1000), 1000)
        self.assertEqual(len(zh.subtlex_ch.third_1000), 1000)
        self.assertEqual(len(zh.subtlex_ch.top_10000), 10000)
        self.assertEqual(zh.subtlex_ch.top_1000[0], "的")
        self.assertEqual(zh.subtlex_ch.top_10000[:1000], zh.subtlex_ch.top_1000)
        self.assertEqual(zh.subtlex_ch.top_10000[1000:2000], zh.subtlex_ch.second_1000)
        self.assertEqual(zh.subtlex_ch.top_10000[2000:3000], zh.subtlex_ch.third_1000)

    def test_hanzi_bands(self) -> None:
        self.assertEqual(zh.subtlex_ch.hanzi.top_1000[0], "我")
        self.assertEqual(len(zh.subtlex_ch.hanzi.top_1000), 1000)
        self.assertEqual(len(zh.subtlex_ch.hanzi.top_5000), 5000)


if __name__ == "__main__":
    unittest.main()
