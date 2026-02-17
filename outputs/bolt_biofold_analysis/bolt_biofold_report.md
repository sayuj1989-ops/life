# Bolt-BioFold Analysis Report

**Date:** 2026-02-17 03:49:52
**Source:** Local AlphaFold Predictions (Default Seed List)
**Code Version:** Bolt-BioFold 2.0 (Surface Metrics Added)

## Results Summary

| Protein | Anisotropy | Rg (A) | Curvature | pLDDT | Domains | Surface (Exposed) | Charge Score |
|---|---|---|---|---|---|---|---|
| PIEZO2 | 19.72 | 43.4 | 0.132 | 79.4 | 7 | 459 | 0.22 |
| PPARGC1A | 4.77 | 31.2 | 0.148 | 52.7 | 4 | 147 | 0.47 |
| IGF1R | 2.04 | 43.2 | 0.180 | 78.0 | 16 | 614 | 0.31 |
| GHR | 26.34 | 31.4 | 0.181 | 58.7 | 3 | 159 | 0.24 |
| ARNTL | 11.02 | 32.1 | 0.166 | 65.5 | 7 | 224 | 0.36 |
| DMD | 1.73 | 22.8 | 0.174 | 76.3 | 2 | 239 | 0.35 |
| MYLK | 2.14 | 41.5 | 0.184 | 65.8 | 28 | 819 | 0.31 |

## Interpretation

### PIEZO2
**What we see:**
- Geometry: Anisotropy 19.72, Rg 43.4A.
- Curvature: High mean curvature (0.132) with hotspots at 403-403 (k=2.78); 498-498 (k=2.62); 551-552 (k=1.73).
- Surface: 459 exposed residues with charge score 0.22.
- Flexibility: Potential hinges at 100-103; 173-183; 378-381; 498-500; 528-532; 578-582; 593-602; 616-618.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
- Ion channel architecture critical for mechanotransduction.
**Confidence:** HIGH. (Reliable backbone geometry).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### PPARGC1A
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

### IGF1R
**What we see:**
- Geometry: Anisotropy 2.04, Rg 43.2A.
- Curvature: High mean curvature (0.180) with hotspots at 1071-1071 (k=3.03); 871-871 (k=2.88); 501-501 (k=2.84).
- Surface: 614 exposed residues with charge score 0.31.
- Flexibility: Potential hinges at 64-68; 184-188; 196-199; 287-290; 314-316; 333-335; 342-344; 364-371; 513-517; 539-542; 586-591; 708-710; 723-725; 871-873; 954-956; 1005-1009; 1037-1041; 1095-1100; 1184-1186.
**Why it matters:**
- Mixed geometry suggests a multifunctional role.
**Confidence:** HIGH. (Reliable backbone geometry).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### GHR
**What we see:**
- Geometry: Anisotropy 26.34, Rg 31.4A.
- Curvature: High mean curvature (0.181) with hotspots at 199-199 (k=2.69); 164-164 (k=2.50); 235-235 (k=1.98).
- Surface: 159 exposed residues with charge score 0.24.
- Flexibility: Potential hinges at 89-94; 289-292; 312-315; 317-319.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### ARNTL
**What we see:**
- Geometry: Anisotropy 11.02, Rg 32.1A.
- Curvature: High mean curvature (0.166) with hotspots at 346-346 (k=3.16); 164-164 (k=1.97); 408-409 (k=1.91).
- Surface: 224 exposed residues with charge score 0.36.
- Flexibility: Potential hinges at 55-57; 146-148; 219-224; 328-332.
**Why it matters:**
- High anisotropy suggests a structural role (fiber/rod) capable of transmitting directional force or resisting gravity.
**Confidence:** LOW. (Caution: IDRs or poor prediction).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### DMD
**What we see:**
- Geometry: Anisotropy 1.73, Rg 22.8A.
- Curvature: High mean curvature (0.174) with hotspots at 261-261 (k=2.08); 246-246 (k=1.76); 158-158 (k=0.72).
- Surface: 239 exposed residues with charge score 0.35.
- Flexibility: Potential hinges at 6-10; 293-300; 313-317; 350-355; 372-378; 495-500.
**Why it matters:**
- Mixed geometry suggests a multifunctional role.
**Confidence:** HIGH. (Reliable backbone geometry).
**Next test:** Simulate dynamics of hinge regions under tensile load.

### MYLK
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
