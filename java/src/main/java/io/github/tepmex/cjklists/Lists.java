package io.github.tepmex.cjklists;

import java.util.List;

/** Helpers for assembling generated list constants. */
public final class Lists {
  private Lists() {}

  /**
   * Concatenate list fragments into one unmodifiable list.
   *
   * <p>Used by generated sources so large HSK / SUBTLEX arrays stay under the JVM 64 KiB method
   * size limit.
   */
  @SafeVarargs
  public static List<String> concat(List<String>... parts) {
    int size = 0;
    for (List<String> part : parts) {
      size += part.size();
    }
    String[] items = new String[size];
    int i = 0;
    for (List<String> part : parts) {
      for (String item : part) {
        items[i++] = item;
      }
    }
    return List.of(items);
  }
}
