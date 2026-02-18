# Bolt-BioFold Analysis Report

**Date:** 2026-02-18 03:50:05
**Source:** Local AlphaFold Predictions (Default Seed List)
**Code Version:** Bolt-BioFold 2.0 (Surface Metrics Added)

## Results Summary

| Protein | Anisotropy | Rg (A) | Curvature | pLDDT | Domains | Surface (Exposed) | Charge Score |
|---|---|---|---|---|---|---|---|
| Q92508 | 15.18 | 58.9 | 0.135 | 72.0 | 35 | 1094 | 0.22 |
| Q9H5I5 | 19.72 | 43.4 | 0.132 | 79.4 | 7 | 459 | 0.22 |
| P02452 | 7.82 | 23.5 | 0.226 | 52.7 | 3 | 181 | 0.30 |
| COL2A1 | 7.02 | 25.0 | 0.226 | 52.1 | 3 | 187 | 0.30 |
| P46937 | 3.96 | 23.6 | 0.219 | 57.4 | 5 | 124 | 0.27 |
| TRPV4 | 8.61 | 35.4 | 0.163 | 71.6 | 8 | 413 | 0.26 |
| RUNX2 | 10.04 | 22.4 | 0.181 | 59.5 | 2 | 117 | 0.24 |
| SOX9 | 4.79 | 16.6 | 0.121 | 56.0 | 1 | 70 | 0.46 |
| VINCULIN | 3.03 | 33.2 | 0.138 | 86.6 | 6 | 578 | 0.38 |
| TALIN1 | 4.18 | 56.9 | 0.133 | 75.9 | 51 | 950 | 0.36 |
| NOTCH1 | 4.18 | 51.4 | 0.213 | 59.6 | 12 | 460 | 0.28 |
| FIBRONECTIN | 5.98 | 55.1 | 0.182 | 69.7 | 49 | 1034 | 0.25 |
| Q9UBK2 | 4.77 | 31.2 | 0.148 | 52.7 | 4 | 147 | 0.47 |
| P08069 | 2.04 | 43.2 | 0.180 | 78.0 | 16 | 614 | 0.31 |
| P10912 | 26.34 | 31.4 | 0.181 | 58.7 | 3 | 159 | 0.24 |
| O00327 | 11.02 | 32.1 | 0.166 | 65.5 | 7 | 224 | 0.36 |
| P11532 | 1.73 | 22.8 | 0.174 | 76.3 | 2 | 239 | 0.35 |
| Q15746 | 2.14 | 41.5 | 0.184 | 65.8 | 28 | 819 | 0.31 |

## Interpretation

### Q92508
**Date:** 2026-02-17 19:28:30
**Source:** AlphaFold DB (Default Seed List)
**Code Version:** Bolt-BioFold 2.1 (PAE Integration)

## Results Summary

| Gene | Anisotropy | Rg (A) | Curvature | pLDDT | Domains | PAE Blockiness | Surface | Charge |
|---|---|---|---|---|---|---|---|---|
| PIEZO1 | 15.18 | 58.9 | 0.135 | 72.0 | 24 | 14.6 | 1094 | 0.22 |
| PIEZO2 | 19.72 | 43.4 | 0.132 | 79.4 | 5 | 9.5 | 459 | 0.22 |
| LBX1 | 5.14 | 22.7 | 0.121 | 66.9 | 1 | 0.0 | 107 | 0.35 |
| YAP1 | 3.96 | 23.6 | 0.219 | 57.4 | 3 | 22.1 | 124 | 0.27 |
| IFT88 | 7.86 | 38.3 | 0.185 | 76.3 | 3 | 8.2 | 360 | 0.40 |
| ITGB1 | 10.43 | 45.8 | 0.192 | 85.9 | 9 | 15.9 | 433 | 0.32 |

## Interpretation

### PIEZO1 (Q92508)
**What we see:**
- Geometry: Anisotropy 15.18, Rg 58.9A.
- Curvature: High mean curvature (0.135) with hotspots at 2217-2217 (k=3.16); 2312-2312 (k=3.09); 2364-2364 (k=1.89).
- Surface: 1094 exposed residues with charge score 0.22.
- PAE: Mean 22.7, Blockiness 14.6.
- Flexibility: Potential hinges at 2-7; 9-11; 23-30; 47-53; 55-58; 75-78; 81-88; 90-95; 98-104; 110-115; 118-120; 233-242; 266-272; 294-299; 306-309; 413-416; 430-432; 434-440; 453-460; 462-464; 486-488; 493-500; 509-513; 515-517; 560-563; 566-573; 593-596; 616-620; 648-654; 674-682; 684-686; 697-699; 707-709; 787-789; 875-877; 887-895; 922-925; 953-957; 1071-1075; 1133-1141; 1239-1245; 1259-1263; 1266-1273; 1445-1455; 1505-1517; 1554-1558; 1567-1570; 1721-1723; 1759-1761; 1763-1765; 1777-1780; 1920-1922; 1981-1984; 1987-1995; 2053-2055; 2289-2291; 2293-2295; 2311-2314; 2330-2344; 2395-2397; 2409-2414.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** HIGH. (Reliable backbone geometry).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### Q9H5I5
### PIEZO2 (Q9H5I5)
**What we see:**
- Geometry: Anisotropy 19.72, Rg 43.4A.
- Curvature: High mean curvature (0.132) with hotspots at 403-403 (k=2.78); 498-498 (k=2.62); 551-552 (k=1.73).
- Surface: 459 exposed residues with charge score 0.22.
- PAE: Mean 17.0, Blockiness 9.5.
- Flexibility: Potential hinges at 100-103; 173-183; 378-381; 498-500; 528-532; 578-582; 593-602; 616-618.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** HIGH. (Reliable backbone geometry).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### P02452
### LBX1 (P52954)
**What we see:**
- Geometry: Anisotropy 5.14, Rg 22.7A.
- Curvature: High mean curvature (0.121) with hotspots at 159-159 (k=0.85); 195-195 (k=0.26); 143-144 (k=0.26).
- Surface: 107 exposed residues with charge score 0.35.
- PAE: Mean 25.1, Blockiness 0.0.
- Flexibility: Potential hinges at 105-107; 197-199.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### COL2A1
**What we see:**
- Geometry: Anisotropy 7.02, Rg 25.0A.
- Curvature: High mean curvature (0.226) with hotspots at 58-58 (k=2.97); 36-36 (k=2.75); 1317-1317 (k=2.58).
- Surface: 187 exposed residues with charge score 0.30.
- Flexibility: Potential hinges at 29-31; 71-78; 80-82; 1340-1342; 1364-1367.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
- ECM component defining tissue stiffness and elasticity.
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### P46937
### YAP1 (P46937)
**What we see:**
- Geometry: Anisotropy 3.96, Rg 23.6A.
- Curvature: High mean curvature (0.219) with hotspots at 251-251 (k=2.60); 192-192 (k=2.53); 241-242 (k=1.79).
- Surface: 124 exposed residues with charge score 0.27.
- PAE: Mean 27.5, Blockiness 22.1.
- Flexibility: Potential hinges at 49-51; 66-68; 70-78; 266-268; 330-332; 336-338.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### TRPV4
**What we see:**
- Geometry: Anisotropy 8.61, Rg 35.4A.
- Curvature: High mean curvature (0.163) with hotspots at 410-411 (k=1.95); 233-233 (k=1.69); 397-397 (k=1.55).
- Surface: 413 exposed residues with charge score 0.26.
- Flexibility: Potential hinges at 103-105; 202-204; 394-398; 425-430; 439-441; 493-496; 541-545; 593-597; 603-611; 660-664; 685-689; 715-722; 724-726; 745-750; 765-770; 785-788; 790-792.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
- Ion channel architecture critical for mechanotransduction.
**Confidence:** HIGH. (Reliable backbone geometry).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### RUNX2
**What we see:**
- Geometry: Anisotropy 10.04, Rg 22.4A.
- Curvature: High mean curvature (0.181) with hotspots at 103-103 (k=2.76); 190-190 (k=1.97); 162-162 (k=1.43).
- Surface: 117 exposed residues with charge score 0.24.
- Flexibility: Potential hinges at 59-61; 91-95; 226-230.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
- Nuclear factor whose transport/activity is regulated by mechanical signals.
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### IFT88 (Q13099)
**What we see:**
- Geometry: Anisotropy 7.86, Rg 38.3A.
- Curvature: High mean curvature (0.185) with hotspots at 391-391 (k=1.48); 445-445 (k=0.70); 650-650 (k=0.65).
- Surface: 360 exposed residues with charge score 0.40.
- PAE: Mean 19.4, Blockiness 8.2.
- Flexibility: Potential hinges at 28-34; 41-43; 183-186; 226-230; 347-353; 355-357.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** HIGH. (Reliable backbone geometry).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### ITGB1 (P05556)
**What we see:**
- Geometry: Anisotropy 10.43, Rg 45.8A.
- Curvature: High mean curvature (0.192) with hotspots at 614-614 (k=2.81); 532-532 (k=2.71); 448-448 (k=2.69).
- Surface: 433 exposed residues with charge score 0.32.
- PAE: Mean 18.2, Blockiness 15.9.
- Flexibility: Potential hinges at 54-57; 97-106; 207-209; 361-363; 505-509; 531-533; 540-544; 600-603; 680-685; 695-697; 707-710.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** HIGH. (Reliable backbone geometry).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### NOTCH1
**What we see:**
- Geometry: Anisotropy 4.18, Rg 51.4A.
- Curvature: High mean curvature (0.213) with hotspots at 198-198 (k=2.27); 1423-1423 (k=2.04); 96-96 (k=1.72).
- Surface: 460 exposed residues with charge score 0.28.
- Flexibility: Potential hinges at 29-35; 47-52; 54-57; 66-71; 77-81; 88-93; 95-97; 109-115; 119-122; 128-133; 135-138; 146-153; 155-160; 165-168; 172-174; 186-192; 196-199; 205-214; 225-231; 235-238; 244-249; 251-253; 263-270; 273-277; 282-287; 289-291; 303-309; 313-316; 322-326; 329-331; 341-347; 351-354; 360-370; 378-384; 389-393; 399-404; 406-408; 420-426; 430-434; 439-444; 446-448; 458-465; 468-472; 477-482; 484-486; 496-502; 506-509; 515-520; 522-524; 534-540; 544-548; 553-558; 560-562; 572-578; 581-584; 590-595; 597-599; 610-614; 619-622; 629-633; 635-637; 647-653; 656-660; 665-674; 685-690; 694-697; 703-708; 710-712; 722-728; 731-735; 740-745; 747-749; 759-765; 769-773; 778-783; 785-787; 798-803; 807-810; 823-825; 836-841; 857-861; 863-865; 875-882; 885-889; 894-899; 901-903; 913-919; 923-927; 932-937; 939-941; 951-957; 961-965; 970-975; 977-979; 989-996; 999-1002; 1008-1017; 1028-1033; 1046-1048; 1053-1055; 1066-1071; 1075-1079; 1084-1089; 1091-1094; 1099-1101; 1104-1106; 1112-1114; 1123-1127; 1132-1137; 1139-1141; 1151-1157; 1161-1165; 1170-1179; 1189-1196; 1199-1203; 1208-1213; 1215-1217; 1228-1242; 1245-1249; 1254-1259; 1261-1263; 1274-1280; 1285-1289; 1294-1296; 1301-1303; 1313-1319; 1326-1328; 1334-1337; 1339-1344; 1355-1361; 1365-1367; 1373-1382; 1394-1400; 1406-1409; 1414-1420; 1427-1433; 1435-1437; 1454-1466; 1468-1472; 1488-1491; 1500-1508; 1510-1512; 1536-1538; 1540-1544; 1549-1554; 1560-1563; 1608-1612; 1685-1689; 1708-1712; 1876-1881; 1886-1888; 1909-1917; 1923-1926.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### FIBRONECTIN
**What we see:**
- Geometry: Anisotropy 5.98, Rg 55.1A.
- Curvature: High mean curvature (0.182) with hotspots at 1099-1099 (k=2.89); 1942-1942 (k=2.85); 2267-2267 (k=2.83).
- Surface: 1034 exposed residues with charge score 0.25.
- Flexibility: Potential hinges at 53-55; 58-62; 81-83; 98-101; 105-109; 114-118; 139-144; 148-151; 157-159; 180-182; 188-190; 194-198; 232-235; 239-243; 249-252; 309-311; 316-318; 324-326; 335-338; 351-353; 370-372; 377-383; 392-394; 411-415; 430-432; 437-440; 516-521; 524-528; 534-537; 562-565; 569-573; 578-582; 647-649; 660-663; 671-675; 684-687; 743-746; 756-759; 769-771; 793-797; 822-824; 846-848; 870-873; 884-886; 928-933; 943-946; 955-958; 980-983; 1007-1010; 1032-1034; 1056-1059; 1070-1072; 1097-1100; 1108-1112; 1121-1124; 1131-1136; 1142-1147; 1155-1159; 1184-1187; 1197-1201; 1212-1215; 1235-1240; 1251-1253; 1289-1294; 1303-1307; 1328-1332; 1341-1344; 1380-1384; 1396-1398; 1407-1410; 1432-1435; 1485-1488; 1509-1511; 1523-1525; 1549-1551; 1560-1565; 1575-1578; 1599-1601; 1613-1615; 1655-1659; 1669-1672; 1693-1696; 1706-1709; 1745-1749; 1759-1761; 1796-1799; 1823-1825; 1849-1851; 1873-1876; 1887-1889; 1926-1931; 1941-1943; 1952-1954; 1964-1966; 1976-1980; 2030-2032; 2067-2070; 2214-2220; 2229-2232; 2241-2245; 2251-2257; 2266-2269; 2305-2309; 2315-2318; 2340-2345; 2348-2352; 2387-2389; 2392-2396; 2401-2403; 2412-2416.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
- ECM component defining tissue stiffness and elasticity.
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### Q9UBK2
**What we see:**
- Geometry: Anisotropy 4.77, Rg 31.2A.
- Curvature: High mean curvature (0.148) with hotspots at 711-711 (k=1.92); 103-103 (k=0.44); 697-698 (k=0.43).
- Surface: 147 exposed residues with charge score 0.47.
- Flexibility: Potential hinges at 44-47; 100-105; 142-144; 381-385; 711-713; 736-742; 750-752.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
- High surface charge density suggests strong electrostatic interaction potential (e.g., with charged ECM components or DNA).
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### P08069
**What we see:**
- Geometry: Anisotropy 2.04, Rg 43.2A.
- Curvature: High mean curvature (0.180) with hotspots at 1071-1071 (k=3.03); 871-871 (k=2.88); 501-501 (k=2.84).
- Surface: 614 exposed residues with charge score 0.31.
- Flexibility: Potential hinges at 64-68; 184-188; 196-199; 287-290; 314-316; 333-335; 342-344; 364-371; 513-517; 539-542; 586-591; 708-710; 723-725; 871-873; 954-956; 1005-1009; 1037-1041; 1095-1100; 1184-1186.
**Why it matters:**
- Mixed geometry suggests a multifunctional role.
**Confidence:** HIGH. (Reliable backbone geometry).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### P10912
**What we see:**
- Geometry: Anisotropy 26.34, Rg 31.4A.
- Curvature: High mean curvature (0.181) with hotspots at 199-199 (k=2.69); 164-164 (k=2.50); 235-235 (k=1.98).
- Surface: 159 exposed residues with charge score 0.24.
- Flexibility: Potential hinges at 89-94; 289-292; 312-315; 317-319.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### O00327
**What we see:**
- Geometry: Anisotropy 11.02, Rg 32.1A.
- Curvature: High mean curvature (0.166) with hotspots at 346-346 (k=3.16); 164-164 (k=1.97); 408-409 (k=1.91).
- Surface: 224 exposed residues with charge score 0.36.
- Flexibility: Potential hinges at 55-57; 146-148; 219-224; 328-332.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### P11532
**What we see:**
- Geometry: Anisotropy 1.73, Rg 22.8A.
- Curvature: High mean curvature (0.174) with hotspots at 261-261 (k=2.08); 246-246 (k=1.76); 158-158 (k=0.72).
- Surface: 239 exposed residues with charge score 0.35.
- Flexibility: Potential hinges at 6-10; 293-300; 313-317; 350-355; 372-378; 495-500.
**Why it matters:**
- Mixed geometry suggests a multifunctional role.
**Confidence:** HIGH. (Reliable backbone geometry).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### Q15746
**What we see:**
- Geometry: Anisotropy 2.14, Rg 41.5A.
- Curvature: High mean curvature (0.184) with hotspots at 491-491 (k=3.14); 1530-1530 (k=3.07); 1484-1484 (k=2.87).
- Surface: 819 exposed residues with charge score 0.31.
- Flexibility: Potential hinges at 57-60; 74-76; 83-86; 110-112; 185-188; 196-199; 201-204; 211-214; 235-239; 425-428; 453-455; 465-467; 538-541; 561-563; 587-589; 633-637; 665-667; 683-687; 699-701; 744-747; 757-765; 772-774; 798-800; 914-916; 1139-1142; 1273-1275; 1372-1374; 1470-1474; 1496-1501; 1595-1597; 1621-1623; 1664-1667; 1834-1836; 1859-1862; 1886-1888.
**Why it matters:**
- Mixed geometry suggests a multifunctional role.
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.


## Best Next Move
Prioritize high-anisotropy candidates (Anisotropy > 3.0) for mechanical simulation of 'counter-curvature' generation.
