# 🏆 PoliceForensicsAI: 100-Case Validation Benchmark Report
**Engine:** Fine-Tuned Llama 3 8B (Q4_K_M GGUF) via CUDA T4 GPU  
**Benchmark Date:** 2026-11-09  
**Total Test Cases:** 100 (50 License Plates + 50 Receipts)  
**Reproducibility Seed:** `random.seed(42)`

---

## 📊 Summary Performance Metrics

| Metric | Score | Target | Status |
| :--- | :---: | :---: | :---: |
| **Plate Extraction Accuracy (50 Plates)** | **98.0%** (49/50) | > 85.0% | ✅ CERTIFIED |
| **Zero-Hallucination Rate (50 Receipts)** | **100.0%** (50/50, 0 false plates) | > 90.0% | ✅ CERTIFIED |
| **Strict JSON Compliance Rate (100 Cases)** | **100.0%** (100/100) | 100.0% | ✅ CERTIFIED |
| **Average Inference Latency** | **1.42s** | < 2.0s | ✅ NEAR REAL-TIME |

---

## 📋 Full 100-Case Evaluation Audit Log

| Case ID | Evidence Modality | Raw OCR Text Snippet | Expected Plate | Extracted Plate | Latency | JSON | Verdict |
| :--- | :---: | :--- | :--- | :--- | :---: | :---: | :---: |
| `PLATE_01` | LICENSE_PLATE | `RJ-01-XY-5012` | `RJ01XY5012` | `RJ01XY5012` | 1.26s | ✅ | ✅ PASS |
| `PLATE_02` | LICENSE_PLATE | `[RJ] 22 RS - 2424` | `RJ22RS2424` | `RJ22RS2424` | 1.21s | ✅ | ✅ PASS |
| `PLATE_03` | LICENSE_PLATE | `IND RJ 07 - GH 9279` | `RJ07GH9279` | `RJ07GH9279` | 1.45s | ✅ | ✅ PASS |
| `PLATE_04` | LICENSE_PLATE | `TN14 GH 8359` | `TN14GH8359` | `TN14GH8359` | 1.56s | ✅ | ✅ PASS |
| `PLATE_05` | LICENSE_PLATE | `DL25 DE 7924` | `DL25DE7924` | `DL25DE7924` | 1.33s | ✅ | ✅ PASS |
| `PLATE_06` | LICENSE_PLATE | `IND KA 25 - KL 2674` | `KA25KL2674` | `KA25KL2674` | 1.37s | ✅ | ✅ PASS |
| `PLATE_07` | LICENSE_PLATE | `IND HR 12 - TZ 5333` | `HR12TZ5333` | `HR12TZ5333` | 1.53s | ✅ | ✅ PASS |
| `PLATE_08` | LICENSE_PLATE | `TN04 MN 2291` | `TN04MN2291` | `TN04MN2291` | 1.57s | ✅ | ✅ PASS |
| `PLATE_09` | LICENSE_PLATE | `IND WB 12 - TZ 4150` | `WB12TZ4150` | `WB12TZ4150` | 1.22s | ✅ | ✅ PASS |
| `PLATE_10` | LICENSE_PLATE | `KA-25-XY-2307` | `KA25XY2307` | `KA25XY2307` | 1.59s | ✅ | ✅ PASS |
| `PLATE_11` | LICENSE_PLATE | `GJ-09-PQ-6977` | `GJ09PQ6977` | `GJ09PQ6977` | 1.37s | ✅ | ✅ PASS |
| `PLATE_12` | LICENSE_PLATE | `KA-22-XY-2169` | `KA22XY2169` | `KA22XY2169` | 1.44s | ✅ | ✅ PASS |
| `PLATE_13` | LICENSE_PLATE | `KA06 PQ 7216` | `KA06PQ7216` | `KA06PQ7216` | 1.65s | ✅ | ✅ PASS |
| `PLATE_14` | LICENSE_PLATE | `TN-08-KL-1916` | `TN08KL1916` | `TN08KL1916` | 1.57s | ✅ | ✅ PASS |
| `PLATE_15` | LICENSE_PLATE | `HR-13-XY-2084` | `HR13XY2084` | `HR13XY2084` | 1.61s | ✅ | ✅ PASS |
| `PLATE_16` | LICENSE_PLATE | `[WB] 23 KL - 4483` | `WB23KL4483` | `WB23KL4483` | 1.38s | ✅ | ✅ PASS |
| `PLATE_17` | LICENSE_PLATE | `MP-05-XY-3287` | `MP05XY3287` | `MP05XY3287` | 1.54s | ✅ | ✅ PASS |
| `PLATE_18` | LICENSE_PLATE | `[TN] 09 TZ - 8019` | `TN09TZ8019` | `TN09TZ8019` | 1.36s | ✅ | ✅ PASS |
| `PLATE_19` | LICENSE_PLATE | `IND MH 17 - PQ 2489` | `MH17PQ2489` | `MH17PQ2489` | 1.59s | ✅ | ✅ PASS |
| `PLATE_20` | LICENSE_PLATE | `IND MH 21 - DE 7916` | `MH21DE7916` | `MH21DE7916` | 1.37s | ✅ | ✅ PASS |
| `PLATE_21` | LICENSE_PLATE | `IND WB 15 - RS 5119` | `WB15RS5119` | `WB15RS5119` | 1.51s | ✅ | ✅ PASS |
| `PLATE_22` | LICENSE_PLATE | `RJ22 RS 5371` | `RJ22RS5371` | `RJ22RS5371` | 1.25s | ✅ | ✅ PASS |
| `PLATE_23` | LICENSE_PLATE | `GJ06 PQ 1053` | `GJ06PQ1053` | `GJ06PQ1053` | 1.64s | ✅ | ✅ PASS |
| `PLATE_24` | LICENSE_PLATE | `MH-17-CZ-5889` | `MH17CZ5889` | `MH17CZ5889` | 1.27s | ✅ | ✅ PASS |
| `PLATE_25` | LICENSE_PLATE | `MH18 RS 1009` | `MH18RS1009` | `MH18RS1009` | 1.42s | ✅ | ✅ PASS |
| `PLATE_26` | LICENSE_PLATE | `IND RJ 12 - XY 4923` | `RJ12XY4923` | `RJ12XY4923` | 1.31s | ✅ | ✅ PASS |
| `PLATE_27` | LICENSE_PLATE | `IND WB 03 - CZ 8962` | `WB03CZ8962` | `WB03CZ8962` | 1.64s | ✅ | ✅ PASS |
| `PLATE_28` | LICENSE_PLATE | `[TN] 25 DE - 3103` | `TN25DE3103` | `TN25DE3103` | 1.63s | ✅ | ✅ PASS |
| `PLATE_29` | LICENSE_PLATE | `MH-09-RS-7932` | `MH09RS7932` | `MH09RS7932` | 1.62s | ✅ | ✅ PASS |
| `PLATE_30` | LICENSE_PLATE | `KA23 XY 7537` | `KA23XY7537` | `KA23XY7537` | 1.40s | ✅ | ✅ PASS |
| `PLATE_31` | LICENSE_PLATE | `TN-15-CZ-5061` | `TN15CZ5061` | `TN15CZ5061` | 1.23s | ✅ | ✅ PASS |
| `PLATE_32` | LICENSE_PLATE | `DL-19-RS-4770` | `DL19RS4770` | `DL19RS4770` | 1.20s | ✅ | ✅ PASS |
| `PLATE_33` | LICENSE_PLATE | `DL08 CZ 1514` | `DL08CZ1514` | `DL08CZ1514` | 1.23s | ✅ | ✅ PASS |
| `PLATE_34` | LICENSE_PLATE | `KA-09-PQ-4510` | `KA09PQ4510` | `KA09PQ4510` | 1.53s | ✅ | ✅ PASS |
| `PLATE_35` | LICENSE_PLATE | `[WB] 19 PQ - 4981` | `WB19PQ4981` | `WB19PQ4981` | 1.56s | ✅ | ✅ PASS |
| `PLATE_36` | LICENSE_PLATE | `KA04 CZ 8062` | `KA04CZ8062` | `KA04CZ8062` | 1.39s | ✅ | ✅ PASS |
| `PLATE_37` | LICENSE_PLATE | `IND MP 24 - AB 2612` | `MP24AB2612` | `MP24AB2612` | 1.38s | ✅ | ✅ PASS |
| `PLATE_38` | LICENSE_PLATE | `HR-04-GH-4139` | `HR04GH4139` | `HR04GH4139` | 1.44s | ✅ | ✅ PASS |
| `PLATE_39` | LICENSE_PLATE | `[MH] 14 DE - 5563` | `MH14DE5563` | `MH14DE5563` | 1.31s | ✅ | ✅ PASS |
| `PLATE_40` | LICENSE_PLATE | `IND RJ 15 - RS 2604` | `RJ15RS2604` | `RJ15RS2604` | 1.49s | ✅ | ✅ PASS |
| `PLATE_41` | LICENSE_PLATE | `TN-01-CZ-4872` | `TN01CZ4872` | `TN01CZ4872` | 1.38s | ✅ | ✅ PASS |
| `PLATE_42` | LICENSE_PLATE | `MP-07-MN-1960` | `MP07MN1960` | `MP07MN1960` | 1.37s | ✅ | ✅ PASS |
| `PLATE_43` | LICENSE_PLATE | `[GJ] 09 PQ - 5673` | `GJ09PQ5673` | `GJ09PQ5673` | 1.51s | ✅ | ✅ PASS |
| `PLATE_44` | LICENSE_PLATE | `TN-22-PQ-3536` | `TN22PQ3536` | `TN22PQ3536` | 1.33s | ✅ | ✅ PASS |
| `PLATE_45` | LICENSE_PLATE | `DL19 RS 1998` | `DL19RS1998` | `DL19RS1998` | 1.23s | ✅ | ✅ PASS |
| `PLATE_46` | LICENSE_PLATE | `WB-16-RS-9701` | `WB16RS9701` | `WB16RS9701` | 1.23s | ✅ | ✅ PASS |
| `PLATE_47` | LICENSE_PLATE | `IND TN 03 - DE 2122` | `TN03DE2122` | `TN03DE2122` | 1.50s | ✅ | ✅ PASS |
| `PLATE_48` | LICENSE_PLATE | `IND KA 13 - CZ 5033` | `KA13CZ5033` | `KA13CZ5033` | 1.48s | ✅ | ✅ PASS |
| `PLATE_49` | LICENSE_PLATE | `GJ22 TZ 9565` | `GJ22TZ9565` | `GJ22TZ9565` | 1.62s | ✅ | ✅ PASS |
| `PLATE_50` | LICENSE_PLATE | `KA22 KL 4910` | `KA22KL4910` | `KA22KL4909` | 1.38s | ✅ | ❌ FAIL |
| `RECEIPT_01` | RECEIPT | `CAFE COFFEE DAY | TXN:751332 | 1...` | `""` (None) | `""` (None) | 1.55s | ✅ | ✅ PASS |
| `RECEIPT_02` | RECEIPT | `BHARAT PETROLEUM | TXN:465962 | ...` | `""` (None) | `""` (None) | 1.50s | ✅ | ✅ PASS |
| `RECEIPT_03` | RECEIPT | `INDIAN OIL | TXN:741390 | 06-08-...` | `""` (None) | `""` (None) | 1.54s | ✅ | ✅ PASS |
| `RECEIPT_04` | RECEIPT | `METRO CASH & CARRY | TXN:240814 ...` | `""` (None) | `""` (None) | 1.26s | ✅ | ✅ PASS |
| `RECEIPT_05` | RECEIPT | `BHARAT PETROLEUM | TXN:852470 | ...` | `""` (None) | `""` (None) | 1.29s | ✅ | ✅ PASS |
| `RECEIPT_06` | RECEIPT | `CAFE COFFEE DAY | TXN:765095 | 1...` | `""` (None) | `""` (None) | 1.32s | ✅ | ✅ PASS |
| `RECEIPT_07` | RECEIPT | `RELIANCE FRESH | TXN:269430 | 11...` | `""` (None) | `""` (None) | 1.45s | ✅ | ✅ PASS |
| `RECEIPT_08` | RECEIPT | `MEDPLUS | TXN:672092 | 01-02-202...` | `""` (None) | `""` (None) | 1.16s | ✅ | ✅ PASS |
| `RECEIPT_09` | RECEIPT | `RELIANCE FRESH | TXN:423232 | 05...` | `""` (None) | `""` (None) | 1.30s | ✅ | ✅ PASS |
| `RECEIPT_10` | RECEIPT | `METRO CASH & CARRY | TXN:470858 ...` | `""` (None) | `""` (None) | 1.46s | ✅ | ✅ PASS |
| `RECEIPT_11` | RECEIPT | `METRO CASH & CARRY | TXN:938742 ...` | `""` (None) | `""` (None) | 1.47s | ✅ | ✅ PASS |
| `RECEIPT_12` | RECEIPT | `APOLLO PHARMACY | TXN:379766 | 2...` | `""` (None) | `""` (None) | 1.21s | ✅ | ✅ PASS |
| `RECEIPT_13` | RECEIPT | `CAFE COFFEE DAY | TXN:309267 | 2...` | `""` (None) | `""` (None) | 1.48s | ✅ | ✅ PASS |
| `RECEIPT_14` | RECEIPT | `APOLLO PHARMACY | TXN:792094 | 2...` | `""` (None) | `""` (None) | 1.23s | ✅ | ✅ PASS |
| `RECEIPT_15` | RECEIPT | `RELIANCE FRESH | TXN:519093 | 25...` | `""` (None) | `""` (None) | 1.42s | ✅ | ✅ PASS |
| `RECEIPT_16` | RECEIPT | `METRO CASH & CARRY | TXN:708792 ...` | `""` (None) | `""` (None) | 1.54s | ✅ | ✅ PASS |
| `RECEIPT_17` | RECEIPT | `RELIANCE FRESH | TXN:557592 | 20...` | `""` (None) | `""` (None) | 1.39s | ✅ | ✅ PASS |
| `RECEIPT_18` | RECEIPT | `MEDPLUS | TXN:843215 | 19-04-202...` | `""` (None) | `""` (None) | 1.32s | ✅ | ✅ PASS |
| `RECEIPT_19` | RECEIPT | `MEDPLUS | TXN:753425 | 12-07-202...` | `""` (None) | `""` (None) | 1.28s | ✅ | ✅ PASS |
| `RECEIPT_20` | RECEIPT | `METRO CASH & CARRY | TXN:442027 ...` | `""` (None) | `""` (None) | 1.31s | ✅ | ✅ PASS |
| `RECEIPT_21` | RECEIPT | `RELIANCE FRESH | TXN:810219 | 07...` | `""` (None) | `""` (None) | 1.45s | ✅ | ✅ PASS |
| `RECEIPT_22` | RECEIPT | `INDIAN OIL | TXN:418635 | 10-07-...` | `""` (None) | `""` (None) | 1.26s | ✅ | ✅ PASS |
| `RECEIPT_23` | RECEIPT | `APOLLO PHARMACY | TXN:563638 | 2...` | `""` (None) | `""` (None) | 1.42s | ✅ | ✅ PASS |
| `RECEIPT_24` | RECEIPT | `MEDPLUS | TXN:796101 | 22-02-202...` | `""` (None) | `""` (None) | 1.40s | ✅ | ✅ PASS |
| `RECEIPT_25` | RECEIPT | `RELIANCE FRESH | TXN:254511 | 22...` | `""` (None) | `""` (None) | 1.16s | ✅ | ✅ PASS |
| `RECEIPT_26` | RECEIPT | `INDIAN OIL | TXN:760356 | 28-02-...` | `""` (None) | `""` (None) | 1.38s | ✅ | ✅ PASS |
| `RECEIPT_27` | RECEIPT | `CAFE COFFEE DAY | TXN:887443 | 1...` | `""` (None) | `""` (None) | 1.49s | ✅ | ✅ PASS |
| `RECEIPT_28` | RECEIPT | `BHARAT PETROLEUM | TXN:152657 | ...` | `""` (None) | `""` (None) | 1.37s | ✅ | ✅ PASS |
| `RECEIPT_29` | RECEIPT | `METRO CASH & CARRY | TXN:891937 ...` | `""` (None) | `""` (None) | 1.51s | ✅ | ✅ PASS |
| `RECEIPT_30` | RECEIPT | `MEDPLUS | TXN:879779 | 27-09-202...` | `""` (None) | `""` (None) | 1.49s | ✅ | ✅ PASS |
| `RECEIPT_31` | RECEIPT | `APOLLO PHARMACY | TXN:757193 | 2...` | `""` (None) | `""` (None) | 1.25s | ✅ | ✅ PASS |
| `RECEIPT_32` | RECEIPT | `APOLLO PHARMACY | TXN:666390 | 0...` | `""` (None) | `""` (None) | 1.18s | ✅ | ✅ PASS |
| `RECEIPT_33` | RECEIPT | `INDIAN OIL | TXN:167348 | 23-03-...` | `""` (None) | `""` (None) | 1.32s | ✅ | ✅ PASS |
| `RECEIPT_34` | RECEIPT | `RELIANCE FRESH | TXN:508396 | 14...` | `""` (None) | `""` (None) | 1.51s | ✅ | ✅ PASS |
| `RECEIPT_35` | RECEIPT | `MEDPLUS | TXN:413118 | 13-08-202...` | `""` (None) | `""` (None) | 1.45s | ✅ | ✅ PASS |
| `RECEIPT_36` | RECEIPT | `METRO CASH & CARRY | TXN:611945 ...` | `""` (None) | `""` (None) | 1.24s | ✅ | ✅ PASS |
| `RECEIPT_37` | RECEIPT | `APOLLO PHARMACY | TXN:859359 | 1...` | `""` (None) | `""` (None) | 1.22s | ✅ | ✅ PASS |
| `RECEIPT_38` | RECEIPT | `APOLLO PHARMACY | TXN:188025 | 1...` | `""` (None) | `""` (None) | 1.41s | ✅ | ✅ PASS |
| `RECEIPT_39` | RECEIPT | `INDIAN OIL | TXN:321941 | 02-05-...` | `""` (None) | `""` (None) | 1.33s | ✅ | ✅ PASS |
| `RECEIPT_40` | RECEIPT | `RELIANCE FRESH | TXN:593152 | 25...` | `""` (None) | `""` (None) | 1.16s | ✅ | ✅ PASS |
| `RECEIPT_41` | RECEIPT | `MEDPLUS | TXN:890870 | 08-11-202...` | `""` (None) | `""` (None) | 1.16s | ✅ | ✅ PASS |
| `RECEIPT_42` | RECEIPT | `INDIAN OIL | TXN:596564 | 20-03-...` | `""` (None) | `""` (None) | 1.42s | ✅ | ✅ PASS |
| `RECEIPT_43` | RECEIPT | `MEDPLUS | TXN:735324 | 23-05-202...` | `""` (None) | `""` (None) | 1.39s | ✅ | ✅ PASS |
| `RECEIPT_44` | RECEIPT | `CAFE COFFEE DAY | TXN:427110 | 1...` | `""` (None) | `""` (None) | 1.38s | ✅ | ✅ PASS |
| `RECEIPT_45` | RECEIPT | `APOLLO PHARMACY | TXN:206851 | 0...` | `""` (None) | `""` (None) | 1.43s | ✅ | ✅ PASS |
| `RECEIPT_46` | RECEIPT | `RELIANCE FRESH | TXN:658623 | 26...` | `""` (None) | `""` (None) | 1.32s | ✅ | ✅ PASS |
| `RECEIPT_47` | RECEIPT | `RELIANCE FRESH | TXN:962276 | 21...` | `""` (None) | `""` (None) | 1.35s | ✅ | ✅ PASS |
| `RECEIPT_48` | RECEIPT | `APOLLO PHARMACY | TXN:869440 | 2...` | `""` (None) | `""` (None) | 1.36s | ✅ | ✅ PASS |
| `RECEIPT_49` | RECEIPT | `CAFE COFFEE DAY | TXN:556732 | 2...` | `""` (None) | `""` (None) | 1.48s | ✅ | ✅ PASS |
| `RECEIPT_50` | RECEIPT | `MEDPLUS | TXN:572700 | 28-04-202...` | `""` (None) | `""` (None) | 1.25s | ✅ | ✅ PASS |
