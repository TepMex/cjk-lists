use cjk_lists::zh::hsk2;
use cjk_lists::zh::hsk3;
use cjk_lists::zh::subtlex_ch;

#[test]
fn hsk2_word_counts() {
    assert_eq!(hsk2::words::LEVEL_1.len(), 150);
    assert_eq!(hsk2::words::LEVEL_2.len(), 150);
    assert_eq!(hsk2::words::LEVEL_3.len(), 300);
    assert_eq!(hsk2::words::LEVEL_4.len(), 600);
    assert_eq!(hsk2::words::LEVEL_5.len(), 1300);
    assert_eq!(hsk2::words::LEVEL_6.len(), 2500);
    assert_eq!(hsk2::words::ALL.len(), 5000);
    assert!(hsk2::words::LEVEL_1.contains(&"爱"));
}

#[test]
fn hsk2_hanzi_exclusive() {
    assert_eq!(hsk2::hanzi::LEVEL_1.len(), 176);
    assert!(hsk2::hanzi::LEVEL_1.contains(&"爱"));
    assert_eq!(hsk2::hanzi::ALL.len(), 2663);
}

#[test]
fn hsk3_hanzi_bands() {
    for n in 1..=6 {
        assert_eq!(hsk3::hanzi::level(n).unwrap().len(), 300);
    }
    assert_eq!(hsk3::hanzi::LEVEL_7.len(), 400);
    assert_eq!(hsk3::hanzi::LEVEL_8.len(), 400);
    assert_eq!(hsk3::hanzi::LEVEL_9.len(), 400);
    assert_eq!(hsk3::hanzi::LEVEL_7_9.len(), 1200);
    assert_eq!(hsk3::hanzi::ALL.len(), 3000);
    assert!(hsk3::hanzi::LEVEL_1.contains(&"的"));
}

#[test]
fn hsk3_words_cover_bands() {
    assert!(hsk3::words::LEVEL_1.len() >= 490);
    assert!(hsk3::words::LEVEL_1.contains(&"爱"));
    assert_eq!(
        hsk3::words::LEVEL_7.len() + hsk3::words::LEVEL_8.len() + hsk3::words::LEVEL_9.len(),
        hsk3::words::LEVEL_7_9.len()
    );
}

#[test]
fn subtlex_word_bands() {
    assert_eq!(subtlex_ch::TOP_1000.len(), 1000);
    assert_eq!(subtlex_ch::SECOND_1000.len(), 1000);
    assert_eq!(subtlex_ch::THIRD_1000.len(), 1000);
    assert_eq!(subtlex_ch::TOP_10000.len(), 10000);
    assert_eq!(subtlex_ch::TOP_1000[0], "的");
    assert_eq!(&subtlex_ch::TOP_10000[..1000], subtlex_ch::TOP_1000);
    assert_eq!(subtlex_ch::hanzi::TOP_1000[0], "我");
}
