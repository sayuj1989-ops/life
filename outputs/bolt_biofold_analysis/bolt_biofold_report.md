# Bolt-BioFold Analysis Report

**Date:** 2026-02-18 19:12:50
**Source:** AlphaFold DB (Default Seed List)
**Code Version:** Bolt-BioFold 2.1 (PAE Integration)

## Results Summary

| Gene | Anisotropy | Rg (A) | Curvature | pLDDT | Domains | PAE Blockiness | Surface | Charge |
|---|---|---|---|---|---|---|---|---|
| PIEZO1 | 15.18 | 58.9 | 0.135 | 72.0 | 24 | 14.6 | 1094 | 0.22 |
| YAP1 | 3.96 | 23.6 | 0.219 | 57.4 | 3 | 22.1 | 124 | 0.27 |
| COL1A1 | 7.82 | 23.5 | 0.226 | 52.7 | 2 | 24.5 | 181 | 0.30 |
| FLNA | 6.26 | 56.9 | 0.173 | 76.5 | 27 | 24.0 | 1283 | 0.32 |
| IGF1R | 2.04 | 43.2 | 0.180 | 78.0 | 13 | 18.3 | 614 | 0.31 |
| DMD | 1.73 | 22.8 | 0.174 | 76.3 | 2 | 22.8 | 239 | 0.35 |
| PPARGC1A | 4.77 | 31.2 | 0.148 | 52.7 | 1 | 0.0 | 147 | 0.47 |
| GHR | 26.34 | 31.4 | 0.181 | 58.7 | 3 | 13.9 | 159 | 0.24 |

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

### COL1A1 (P02452)
**What we see:**
- Geometry: Anisotropy 7.82, Rg 23.5A.
- Curvature: High mean curvature (0.226) with hotspots at 64-64 (k=2.94); 1280-1280 (k=2.51); 1293-1293 (k=2.48).
- Surface: 181 exposed residues with charge score 0.30.
- PAE: Mean 27.4, Blockiness 24.5.
- Flexibility: Potential hinges at 77-88; 1218-1220; 1222-1224; 1317-1319.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### FLNA (P21333)
**What we see:**
- Geometry: Anisotropy 6.26, Rg 56.9A.
- Curvature: High mean curvature (0.173) with hotspots at 1990-1990 (k=2.24); 336-336 (k=2.17); 928-928 (k=2.09).
- Surface: 1283 exposed residues with charge score 0.32.
- PAE: Mean 26.8, Blockiness 24.0.
- Flexibility: Potential hinges at 117-119; 154-157; 162-166; 270-273; 296-299; 308-311; 335-338; 392-399; 408-412; 436-439; 447-451; 460-462; 507-511; 533-535; 556-558; 573-575; 602-605; 615-617; 626-628; 665-667; 683-687; 713-715; 779-787; 796-800; 811-815; 828-831; 839-843; 851-855; 881-890; 898-902; 912-917; 928-930; 938-943; 951-954; 981-986; 996-999; 1010-1013; 1022-1026; 1034-1038; 1046-1050; 1078-1083; 1091-1096; 1104-1108; 1116-1119; 1127-1131; 1139-1143; 1171-1176; 1185-1188; 1199-1201; 1211-1214; 1222-1226; 1235-1238; 1265-1273; 1283-1289; 1299-1302; 1322-1326; 1335-1338; 1367-1371; 1379-1384; 1393-1396; 1404-1407; 1416-1419; 1428-1430; 1458-1464; 1475-1478; 1488-1492; 1501-1504; 1525-1527; 1555-1564; 1572-1576; 1586-1589; 1598-1601; 1622-1624; 1663-1667; 1675-1679; 1689-1693; 1702-1705; 1713-1718; 1725-1729; 1736-1739; 1796-1801; 1810-1813; 1822-1825; 1833-1838; 1847-1849; 1877-1880; 1889-1894; 1902-1906; 1914-1917; 1925-1929; 1937-1941; 1963-1965; 1976-1980; 1988-1992; 2001-2004; 2012-2016; 2024-2028; 2059-2063; 2073-2076; 2084-2088; 2096-2099; 2107-2111; 2119-2123; 2153-2157; 2164-2170; 2179-2182; 2192-2195; 2204-2207; 2214-2219; 2227-2237; 2249-2254; 2263-2267; 2275-2279; 2287-2290; 2300-2302; 2311-2314; 2328-2330; 2343-2348; 2357-2360; 2382-2385; 2393-2397; 2406-2409; 2453-2458; 2466-2468; 2477-2481; 2499-2504; 2517-2521; 2584-2586; 2595-2599.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** HIGH. (Reliable backbone geometry).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### IGF1R (P08069)
**What we see:**
- Geometry: Anisotropy 2.04, Rg 43.2A.
- Curvature: High mean curvature (0.180) with hotspots at 1071-1071 (k=3.03); 871-871 (k=2.88); 501-501 (k=2.84).
- Surface: 614 exposed residues with charge score 0.31.
- PAE: Mean 23.6, Blockiness 18.3.
- Flexibility: Potential hinges at 64-68; 184-188; 196-199; 287-290; 314-316; 333-335; 342-344; 364-371; 513-517; 539-542; 586-591; 708-710; 723-725; 871-873; 954-956; 1005-1009; 1037-1041; 1095-1100; 1184-1186.
**Why it matters:**
- Mixed geometry suggests a multifunctional role.
**Confidence:** HIGH. (Reliable backbone geometry).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### DMD (P11532)
**What we see:**
- Geometry: Anisotropy 1.73, Rg 22.8A.
- Curvature: High mean curvature (0.174) with hotspots at 261-261 (k=2.08); 246-246 (k=1.76); 158-158 (k=0.72).
- Surface: 239 exposed residues with charge score 0.35.
- PAE: Mean 19.0, Blockiness 22.8.
- Flexibility: Potential hinges at 6-10; 293-300; 313-317; 350-355; 372-378; 495-500.
**Why it matters:**
- Mixed geometry suggests a multifunctional role.
**Confidence:** HIGH. (Reliable backbone geometry).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### PPARGC1A (Q9UBK2)
**What we see:**
- Geometry: Anisotropy 4.77, Rg 31.2A.
- Curvature: High mean curvature (0.148) with hotspots at 711-711 (k=1.92); 103-103 (k=0.44); 697-698 (k=0.43).
- Surface: 147 exposed residues with charge score 0.47.
- PAE: Mean 28.1, Blockiness 0.0.
- Flexibility: Potential hinges at 44-47; 100-105; 142-144; 381-385; 711-713; 736-742; 750-752.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### GHR (P10912)
**What we see:**
- Geometry: Anisotropy 26.34, Rg 31.4A.
- Curvature: High mean curvature (0.181) with hotspots at 199-199 (k=2.69); 164-164 (k=2.50); 235-235 (k=1.98).
- Surface: 159 exposed residues with charge score 0.24.
- PAE: Mean 25.8, Blockiness 13.9.
- Flexibility: Potential hinges at 89-94; 289-292; 312-315; 317-319.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.


## Best Next Move
Prioritize high-anisotropy candidates (Anisotropy > 3.0) for mechanical simulation of 'counter-curvature' generation.
