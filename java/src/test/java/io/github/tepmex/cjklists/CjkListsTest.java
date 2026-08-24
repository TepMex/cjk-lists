package io.github.tepmex.cjklists;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertTrue;

import io.github.tepmex.cjklists.zh.hsk2.Hanzi;
import io.github.tepmex.cjklists.zh.hsk2.Words;
import java.util.ArrayList;
import java.util.HashSet;
import java.util.List;
import java.util.Set;
import org.junit.jupiter.api.Test;

class CjkListsTest {
  @Test
  void hsk2WordCounts() {
    assertEquals(
        List.of(150, 150, 300, 600, 1300, 2500),
        List.of(
            Words.level(1).size(),
            Words.level(2).size(),
            Words.level(3).size(),
            Words.level(4).size(),
            Words.level(5).size(),
            Words.level(6).size()));
    assertEquals(5000, Words.ALL.size());
    assertTrue(Words.LEVEL_1.contains("爱"));
  }

  @Test
  void hsk2HanziExclusive() {
    assertEquals(176, Hanzi.LEVEL_1.size());
    assertTrue(Hanzi.LEVEL_1.contains("爱"));
    assertEquals(2663, Hanzi.ALL.size());
    Set<String> seen = new HashSet<>();
    for (int n = 1; n <= 6; n++) {
      for (String ch : Hanzi.level(n)) {
        assertEquals(1, ch.length(), ch);
        assertTrue(seen.add(ch), () -> "duplicate hanzi " + ch);
      }
    }
    assertEquals(2663, seen.size());
  }

  @Test
  void hsk3HanziBands() {
    var hanzi = io.github.tepmex.cjklists.zh.hsk3.Hanzi.class;
    for (int n = 1; n <= 6; n++) {
      assertEquals(300, io.github.tepmex.cjklists.zh.hsk3.Hanzi.level(n).size());
    }
    assertEquals(400, io.github.tepmex.cjklists.zh.hsk3.Hanzi.LEVEL_7.size());
    assertEquals(400, io.github.tepmex.cjklists.zh.hsk3.Hanzi.LEVEL_8.size());
    assertEquals(400, io.github.tepmex.cjklists.zh.hsk3.Hanzi.LEVEL_9.size());
    assertEquals(1200, io.github.tepmex.cjklists.zh.hsk3.Hanzi.LEVEL_7_9.size());
    List<String> combined = new ArrayList<>();
    combined.addAll(io.github.tepmex.cjklists.zh.hsk3.Hanzi.LEVEL_7);
    combined.addAll(io.github.tepmex.cjklists.zh.hsk3.Hanzi.LEVEL_8);
    combined.addAll(io.github.tepmex.cjklists.zh.hsk3.Hanzi.LEVEL_9);
    assertEquals(io.github.tepmex.cjklists.zh.hsk3.Hanzi.LEVEL_7_9, combined);
    assertEquals(3000, io.github.tepmex.cjklists.zh.hsk3.Hanzi.ALL.size());
    assertTrue(io.github.tepmex.cjklists.zh.hsk3.Hanzi.LEVEL_1.contains("的"));
    assertEquals("Hanzi", hanzi.getSimpleName());
  }

  @Test
  void hsk3WordsCoverBands() {
    assertTrue(io.github.tepmex.cjklists.zh.hsk3.Words.LEVEL_1.size() >= 490);
    assertTrue(io.github.tepmex.cjklists.zh.hsk3.Words.LEVEL_1.contains("爱"));
    assertEquals(
        io.github.tepmex.cjklists.zh.hsk3.Words.LEVEL_7_9.size(),
        io.github.tepmex.cjklists.zh.hsk3.Words.LEVEL_7.size()
            + io.github.tepmex.cjklists.zh.hsk3.Words.LEVEL_8.size()
            + io.github.tepmex.cjklists.zh.hsk3.Words.LEVEL_9.size());
  }

  @Test
  void subtlexWordBands() {
    assertEquals(1000, io.github.tepmex.cjklists.zh.subtlexch.Words.TOP_1000.size());
    assertEquals(1000, io.github.tepmex.cjklists.zh.subtlexch.Words.SECOND_1000.size());
    assertEquals(1000, io.github.tepmex.cjklists.zh.subtlexch.Words.THIRD_1000.size());
    assertEquals(10000, io.github.tepmex.cjklists.zh.subtlexch.Words.TOP_10000.size());
    assertEquals("的", io.github.tepmex.cjklists.zh.subtlexch.Words.TOP_1000.get(0));
    assertEquals(
        io.github.tepmex.cjklists.zh.subtlexch.Words.TOP_1000,
        io.github.tepmex.cjklists.zh.subtlexch.Words.TOP_10000.subList(0, 1000));
    assertEquals(
        io.github.tepmex.cjklists.zh.subtlexch.Words.SECOND_1000,
        io.github.tepmex.cjklists.zh.subtlexch.Words.TOP_10000.subList(1000, 2000));
    assertEquals(
        io.github.tepmex.cjklists.zh.subtlexch.Words.THIRD_1000,
        io.github.tepmex.cjklists.zh.subtlexch.Words.TOP_10000.subList(2000, 3000));
    assertEquals("我", io.github.tepmex.cjklists.zh.subtlexch.Hanzi.TOP_1000.get(0));
    assertEquals(1000, io.github.tepmex.cjklists.zh.subtlexch.Hanzi.TOP_1000.size());
  }
}
