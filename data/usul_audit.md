# Usul places audit: al-Fatiha and al-Baqarah

Independent review of `data/usul_places_review.txt` (891 lines: mim 531, naql 177, imala 128, idgham 54), checked against `data/usul_rules.json` and the Hafs words in `data/q4`.

**Coverage**
- Every idgham, imala and naql line was checked by hand.
- All 531 mim lines were checked by script for word form, next word and the h flag, and about 150 were read by hand.
- False negatives were found with a script over every word pair: identical last and first letter for idgham, a hamza-initial next word for naql, words with ى or a final alif (with or without an attached pronoun) for imala, and words ending in م for mim.

## A. False positives (remove)

| rule | key | word | problem | fix |
|---|---|---|---|---|
| idgham | 2:282 | كَاتِبُ → بِالْعَدْلِ | The Mushaf has «كَاتِبٌ بِالْعَدْلِ» with tanwin (iqlab). This text writes tanwin before ب as a single haraka (compare «بَصِيرُ بِمَا» 2:96). Tanwin blocks idgham (المانع 3). | remove |
| mim | 2:211 | كَمْ → ءَاتَيْنَاهُم (h) | «كم» is an interrogative particle, not a plural mim. | remove; add naql (see B) |
| mim | 2:249 | كَم → مِّن | «كم» is a khabariyya particle, not a plural mim. | remove |
| mim | 2:259 | كَمْ → لَبِثْتَ | «كم» is an interrogative particle, not a plural mim. | remove |

No other false positives were found. The remaining 53 idgham, 128 imala, 177 naql and 528 mim lines are correct.

## B. False negatives (add)

### naql (26)
| rule | key | word | problem | fix |
|---|---|---|---|---|
| naql | 2:4 | وَبِالْأخِرَةِ | Lam al-ta'rif after two prefixes (وَ + بِ); `naql_inside` allows only one. | add |
| naql | 2:71 | الْـئَانَ | Written with tatweel and a ئ seat, so the `ال[أإآء]` regex misses it. | add |
| naql | 2:187 | فَالْـئَانَ | Same as 2:71. | add |
| naql | 2:178 | وَأَدَاءٌ → إِلَيْهِ | Tanwin on a final hamza; the detector rejects every word ending in a hamza letter. | add |
| naql | 2:211 | كَمْ → ءَاتَيْنَاهُم | Was hidden by the wrong mim («كَمَ اتيناهم» for Warsh). | add |
| naql | 2:90 | بَغْيًا → أَن | Fatha tanwin is written with an alif, and the alif is treated as a madd letter. | add |
| naql | 2:111, 2:135, 2:140 | هُودًا → أَوْ | Same (fatha tanwin with alif). | add ×3 |
| naql | 2:126 | بَلَدًا → ءَامِنا | Same. | add |
| naql | 2:148 | جَمِيعًا → إِنَّ | Same. | add |
| naql | 2:174 | قَلِيلًا → أُوْلَئِكَ | Same. | add |
| naql | 2:182 | جَنَفًا → أَوْ | Same. | add |
| naql | 2:184, 2:185, 2:196 | مَرِيضًا → أَوْ | Same. | add ×3 |
| naql | 2:229 | شَيْ‍ئًا → إِلَّا | Same. | add |
| naql | 2:235 | سِرًّا → إِلَّا | Same. | add |
| naql | 2:239 | فَرِجَالًا → أَوْ | Same. | add |
| naql | 2:240 | مَّتَاعًا → إِلَى | Same. | add |
| naql | 2:259 | يَوْمًا → أَوْ | Same. | add |
| naql | 2:282 | سَفِيهًا → أَوْ، ضَعِيفًا → أَوْ، صَغِيرًا → أَوْ، كَبِيرًا → إِلَى | Same. | add ×4 |
| naql | 2:286 | نَفْسًا → إِلَّا | Same. | add |

These were correctly left out and are not naql: «ظَنَّا أَن» 2:230 and «يَخَافَا أَلَّا» 2:229 (dual alif), and «أَنَا أُحْيِ» 2:258 (a written alif).

### imala (7)
| rule | key | word | problem | fix |
|---|---|---|---|---|
| imala | 2:29 | فَسَوَّىهُنَّ | The pronoun regex has no «هن». | add (both readers, no flag) |
| imala | 2:273 | بِسِيمَاهُمْ | Written with alif and missing from `ALIF_WORDS`. The card lists «سيماهم». | add |
| imala | 2:275 ×3 | الرِّبَوااْ (يأكلون الربا، مثل الربا، وحرم الربا) | `ALIF_WORDS` has «الربا», but this text's bare form is «الربواا». | add ×3 |
| imala | 2:276 | الرِّبَوااْ → وَيُرْبِي | Same. | add |
| imala | 2:278 | الرِّبَوااْ → إِن | Same. | add |

No flag is needed on any of these: none is followed by a sakin.

### idgham and mim
- **idgham:** none missing. All 214 same-letter pairs were checked. The rest are sakin first letters (small idgham), tanwin (dropped or explicit), shadda («أُحِلَّ لَكُمْ»، «يَحِلُّ»، «إِنَّ نَصْرَ»), madd letters («فِي يَوْمَيْنِ»، «الَّذِي يَ…»), plural waw («فَوَلُّوا وُجُوهَكُمْ»), or hamzat al-wasl as the second word.
- **mim:** none missing.

## C. Flags

| rule | flag | finding |
|---|---|---|
| mim | h | 528 of 528 are consistent: h exactly when the next word starts with hamzat qat'. |
| idgham | x | 3 places, all correct: «ونحنْ نسبح» 2:30, «العلمْ ما» 2:120, «شهرْ رمضان» 2:185. The lin cases («حيث ثقفتموهم» 2:191) and madd cases («إسرائيل لا»، «الرحيم ملك») are correctly left without x. |
| idgham | across ayah | 1:3→1:4, 2:105→2:106 and 2:222→2:223 apply only when the ayahs are joined. Consider a wasl-only marker in the UI. |
| imala | w | All 23 are correct: 11 tanwin cases (هدى ×5 including وهدى، أذى ×4، مصلى، مسمى) and 12 before a sakin (موسى الكتاب ×2، عيسى ابن ×2، نرى الله، يرى الذين، هدى الله 2:120، هدى الله 2:143، فهدى الله، وآتى المال، وآتى الزكاة، القتلى الحر). |
| imala | k | All correct: فأحياكم، فأحيا، أحياهم (أحيا without waw), خطاياكم، مرضات ×2. |
| imala | dk | Correct: هداي 2:38. |

## D. Patterns to fix in `build_usul.py`

1. **How this text writes tanwin.** Before an izhar letter or hamza it is written explicitly. Before idgham or ikhfa letters it is dropped (هُدى، مَرَضا، حَسَنَة). Before ب it becomes a **single haraka** (كَاتِبُ، بَصِيرُ). So `moving()` reads iqlab tanwin as a voweled letter.
   - Fix: get tanwin from an Uthmani source (the small mim ۢ) or flag it before ب.
   - Note: «طَعَامُ مِسْكِينٍ» 2:184 is a genuine place: Abu Amr reads «فديةٌ طعامُ مسكينٍ».
2. **mim:** add «كم» (and any prefixed form) to the exclusions next to ثم/لم/أم/يوم. This also releases the naql at 2:211.
3. **naql_between:**
   - Treat a final ا preceded by ً (ـًا/ـًّا) as tanwin, not madd.
   - Accept a final hamza (ء/أ/ؤ/ئ) when it carries tanwin.
4. **naql_inside:**
   - Strip ZWJ and tatweel first.
   - Allow stacked prefixes: `^[وف]?[بكل]?(ال|لل)`.
   - Accept ئ/ؤ as hamza seats (الْـئَانَ).
5. **imala:**
   - Pronoun regex: add «هن» (and «هما» is already there). Better: strip any pronoun suffix and test the stem.
   - Write `ALIF_WORDS` keys in this text's own rasm («الربواا»), not standard spelling, or normalize both sides.
   - Add «سيماهم» with prefix stripping (بـ).
   - The keys «هداهم», «اشتراه» never match because the text uses ى; they are harmless but dead.

## Net change

| rule | before | after |
|---|---|---|
| idgham | 54 | 53 |
| mim | 531 | 528 |
| naql | 177 | 203 |
| imala | 128 | 135 |
