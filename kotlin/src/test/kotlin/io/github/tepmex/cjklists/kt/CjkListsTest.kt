package io.github.tepmex.cjklists.kt

import io.github.tepmex.cjklists.kt.zh.hsk2.Hanzi
import io.github.tepmex.cjklists.kt.zh.hsk2.Words
import io.github.tepmex.cjklists.kt.zh.hsk3.Hanzi as Hsk3Hanzi
import io.github.tepmex.cjklists.kt.zh.hsk3.Words as Hsk3Words
import io.github.tepmex.cjklists.kt.zh.subtlexch.Hanzi as SubtlexHanzi
import io.github.tepmex.cjklists.kt.zh.subtlexch.second1000
import io.github.tepmex.cjklists.kt.zh.subtlexch.third1000
import io.github.tepmex.cjklists.kt.zh.subtlexch.top1000
import io.github.tepmex.cjklists.kt.zh.subtlexch.top10000
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertTrue

class CjkListsTest {
    @Test
    fun hsk2WordCounts() {
        assertEquals(
            listOf(150, 150, 300, 600, 1300, 2500),
            (1..6).map { Words.level(it).size },
        )
        assertEquals(5000, Words.all.size)
        assertTrue("爱" in Words.level1)
    }

    @Test
    fun hsk2HanziExclusive() {
        assertEquals(176, Hanzi.level1.size)
        assertTrue("爱" in Hanzi.level1)
        assertEquals(2663, Hanzi.all.size)
        val seen = HashSet<String>()
        for (n in 1..6) {
            for (ch in Hanzi.level(n)) {
                assertEquals(1, ch.length, ch)
                assertTrue(seen.add(ch), "duplicate hanzi $ch")
            }
        }
        assertEquals(2663, seen.size)
    }

    @Test
    fun hsk3HanziBands() {
        for (n in 1..6) {
            assertEquals(300, Hsk3Hanzi.level(n).size)
        }
        assertEquals(400, Hsk3Hanzi.level7.size)
        assertEquals(400, Hsk3Hanzi.level8.size)
        assertEquals(400, Hsk3Hanzi.level9.size)
        assertEquals(1200, Hsk3Hanzi.level7To9.size)
        assertEquals(Hsk3Hanzi.level7 + Hsk3Hanzi.level8 + Hsk3Hanzi.level9, Hsk3Hanzi.level7To9)
        assertEquals(3000, Hsk3Hanzi.all.size)
        assertTrue("的" in Hsk3Hanzi.level1)
    }

    @Test
    fun hsk3WordsCoverBands() {
        assertTrue(Hsk3Words.level1.size >= 490)
        assertTrue("爱" in Hsk3Words.level1)
        assertEquals(
            Hsk3Words.level7To9.size,
            Hsk3Words.level7.size + Hsk3Words.level8.size + Hsk3Words.level9.size,
        )
    }

    @Test
    fun subtlexWordBands() {
        assertEquals(1000, top1000.size)
        assertEquals(1000, second1000.size)
        assertEquals(1000, third1000.size)
        assertEquals(10000, top10000.size)
        assertEquals("的", top1000[0])
        assertEquals(top1000, top10000.subList(0, 1000))
        assertEquals(second1000, top10000.subList(1000, 2000))
        assertEquals(third1000, top10000.subList(2000, 3000))
        assertEquals("我", SubtlexHanzi.top1000[0])
        assertEquals(1000, SubtlexHanzi.top1000.size)
    }
}
