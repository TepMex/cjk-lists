# cjk-lists (Java)

```xml
<dependency>
  <groupId>io.github.tepmex</groupId>
  <artifactId>cjk-lists</artifactId>
  <version>0.1.0</version>
</dependency>
```

```java
import io.github.tepmex.cjklists.zh.hsk2.Hanzi;
import io.github.tepmex.cjklists.zh.subtlexch.Words;

System.out.println(Hanzi.LEVEL_1.size());
System.out.println(Words.TOP_1000.get(0)); // 的
```

Requires Java 11+. See the [repository README](https://github.com/TepMex/cjk-lists) for the
full API, sources, and other language packages.
