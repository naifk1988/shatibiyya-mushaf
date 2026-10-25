# Farsh audit A: al-Fatiha + al-Baqarah 1–141

Scope: `data/s/1.json` (all of it) and `data/s/2.json` (2:1–2:141). I compared every card with al-Wafi (book 38075, pp. 50–52 and 199–211, plus p. 230 for the ya'at al-idafa). I spot-checked against the qira'at tools (Tafsir MCP `get_qeraat_variants` for 2:7, 2:38, 2:85 and 2:105, and `list_verse_qiraat` for 2:61). Those tools cover the ten readers, so I used only the seven. Usul differences (madd, imala, hamz, naql, صلة ميم الجمع, idgham) are ignored.

How I checked for missing places: al-Wafi's Baqarah farsh for these ayahs is the continuous run of bayts 445–487 plus the ya'at bayt 545. I matched every rule in that run against the ayah text (`text_preview.json`), including every recurring rule (قيل، هو/هي، النبيء، ينزل، يأمركم، إبراهام، جبريل…). App behaviour: `alignCue` in `index.html` marks only the **first** match of a cue in an ayah, unless the cue carries an ordinal such as «(الثانية)».

## Findings

| # | Ayah | Word | Problem | Correct value | Source |
|---|------|------|---------|---------------|--------|
| 1 | 2:105 | يُنَزَّلَ | **Wrong vowel in w.** The card copies 2:90's active forms (`يُنْزِلَ` / `يُنَزِّلَ`). Here the verb is passive («أَنْ يُنَزَّلَ عَلَيْكُمْ»), as the card's own note says. | Ibn Kathir and Abu 'Amr (bazzi, qunbul, duri_a, susi): **يُنْزَلَ**. The rest: **يُنَزَّلَ**. | al-Wafi p206 (gives «أَنْ يُنَزَّلَ عَلَيْكُمْ» as the passive example); Tafsir MCP 2:105 |
| 2 | 2:6, 2:20, 2:38, 2:61, 2:62, 2:85, 2:112, 2:129 | عليهم | **Missing places.** Bayt 110 (Hamza: ضم هاء عليهم/إليهم/لديهم) applies to the whole Quran, in both pause and continuous reading. Here it has `all:false` and cards only in al-Fatiha, and `usul_rules.json` has no rule for it (the `mim` rule covers only صلة الميم and the ضم/كسر before a sakin). Every Hamza «عليهم» in 2:1–141 has no marking. This is also inconsistent with bayt 108 (صراط), which is handled with `all:true`. | Hamza (khalaf, khallad): **عَلَيْهُمْ**. The rest: **عَلَيْهِمْ**. At 2:61 «عليهمُ الذلة»: Hamza **عَلَيْهُمُ** (and al-Kisa'i also ضم in continuous reading, by the usul mim rule). Hamza keeps the ضم when pausing too. | al-Wafi p51: «في جميع القرآن الكريم … وأخذ هذا التعميم من الإطلاق»; Tafsir MCP 2:38 w14, 2:85 w12 (يعقوب وحمزة بضم الهاء); 2:61 w38 |
| 3 | 2:125 | إبراهيم (الثانية) «وَعَهِدْنَا إِلَى إِبْرَاهِيمَ» | **Missing place.** The ayah has two «إبراهيم» and the one card (cue `إبراهيم`) marks only the first («مَقَامِ إِبْرَاهِيمَ»). | Add a second card with cue `إبراهيم (الثانية)`: hisham إِبْرَاهَام; ibn_dhakwan both forms; the rest إِبْرَاهِيم. | al-Wafi p210 («جميع المواضع في سورة البقرة»); ayah text |
| 4 | 2:54 | بارئكم (الثانية) «عِنْدَ بَارِئِكُمْ» | **Missing place.** There are two places in this one ayah, and the card's ma3na says so itself, but there is one card with cue `بارئكم`, so only the first is marked. | Add a card with cue `بارئكم (الثانية)` and the same readings: susi بَارِئْكُمْ; duri_a إسكان + اختلاس; the rest بَارِئِكُمْ. | al-Wafi p202–203 («في الموضعين هنا») |
| 5 | 2:124–2:140 (all 10 إبراهيم cards) | إبراهيم | **Data defect in how the two-way rawi is stored.** The reading labelled «هشام» has `q:[hisham, ibn_dhakwan]`. Then a reading «ابن ذكوان» has `q:[]` and `w:""`, which shows as an empty row. ibn_dhakwan also appears in «الباقون». The content is right (Ibn Dhakwan has both forms in al-Baqarah only), but the structure is not. | Use the pattern of the 2:54 card: label the first reading «هشام وابن ذكوان (بخلف)», or drop the empty entry. | al-Wafi p210 («ووجهان فيه لابن ذكوان ههنا») |
| 6 | 1:7 (both cards for bayt 111) | عليهم | **Same defect.** The reading labelled «ابن كثير (البزي، قنبل)» has qalun in q, and the reading «نافع من رواية قالون» has `q:[]`, `w:""`. Also, صلة ميم الجمع is usul, and `usul_rules.json` (`mim`) already covers it, so these two farsh cards duplicate an usul rule. | Either remove them (it is usul), or fix the labels (e.g. «ابن كثير، وقالون بخلف») and drop the empty entry. | al-Wafi p51; usul_rules.json `mim` |

## Checked and found correct (no action)

- **al-Fatiha:**
  - مالك 1:4.
  - الصراط 1:6 and صراط 1:7 (قنبل سين; خلف إشمام; خلاد إشمام في الأول فقط). The note correctly records the footnote that Khallad also has الصاد الخالصة there.
  - عليهم ×2 in 1:7 (bayt 110).
- **Baqarah, by bayt:**
  - 445 يخدعون 2:9.
  - 446 يكذبون 2:10.
  - 447 قيل 2:11, 2:13, 2:59, 2:91 (all the فعل places in range).
  - 449 وهو/فهي 2:29, 2:74, 2:85, 2:91, 2:112, 2:137, 2:139 (complete).
  - 451 فأزلهما 2:36.
  - 452 آدم/كلمات 2:37.
  - 453 يقبل 2:48 (the first one only; 2:123 is correctly left out) and واعدنا 2:51.
  - 454–455 بارئكم/يأمركم 2:54, 2:67, 2:93 (Susi إسكان only; Duri إسكان + اختلاس).
  - 456–457 نغفر 2:58.
  - 458 النبيين/أنبياء/النبيون 2:61, 2:91, 2:136.
  - 460 الصابئين 2:62.
  - 460–461 هزوا 2:67 (Hafs هُزُوًا, Hamza هُزْءًا, the rest هُزُؤًا).
  - 462 تعملون 2:74 (Ibn Kathir) and 2:85 (Nafi', Ibn Kathir, Shu'ba).
  - 463 خطيئته 2:81 and تعبدون 2:83.
  - 464 حسنا 2:83.
  - 465 تظاهرون 2:85.
  - 466 أسارى/تفادوهم 2:85.
  - 467 القدس 2:87.
  - 468 ينزل 2:90.
  - 471–472 جبريل 2:97, 2:98 (Shu'ba جَبْرَئِل).
  - 473 ميكال 2:98.
  - 474 ولكن الشياطين 2:102.
  - 475 ننسخ/ننسها 2:106.
  - 476 وقالوا 2:116 and فيكون 2:117.
  - 479 تسأل 2:119.
  - 480–484 إبراهيم (q/w content).
  - 484 واتخذوا 2:125.
  - 485–486 أرنا 2:128 (Duri اختلاس only), فأمتعه 2:126 and ووصى 2:132.
  - 487 تقولون 2:140.
  - 545 ya'at in range: إني أعلم 2:30 (the second إني) and 2:33, عهدي 2:124, بيتي 2:125. These are 4 of the 8 ya'at listed for al-Baqarah on p230; the other 4 fall after 2:141.
- **No wrong cards found:** no card sits on an ayah where its rule does not apply.
