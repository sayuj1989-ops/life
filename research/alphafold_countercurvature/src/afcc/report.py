import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path

class ReportGenerator:
    def __init__(self, data_dir: Path, output_dir: Path):
        self.data_dir = data_dir
        self.output_dir = output_dir
        self.figures_dir = output_dir / "figures"
        self.figures_dir.mkdir(parents=True, exist_ok=True)

    def load_data(self):
        metrics_path = self.data_dir / "processed" / "protein_metrics.csv"
        if not metrics_path.exists():
            raise FileNotFoundError("Metrics file not found. Run analysis first.")
        return pd.read_csv(metrics_path)

    def generate_plots(self, df: pd.DataFrame):
        """Generates key plots for the report."""
        sns.set_theme(style="whitegrid")

        # 1. Anisotropy vs Radius of Gyration (Morphology Space)
        plt.figure(figsize=(10, 6))
        if 'source_category' in df.columns:
            sns.scatterplot(
                data=df,
                x='radius_of_gyration',
                y='anisotropy',
                hue='source_category',
                style='morphology',
                s=100
            )
        else:
            sns.scatterplot(
                data=df,
                x='radius_of_gyration',
                y='anisotropy',
                style='morphology',
                s=100
            )

        # Label points
        for i, row in df.iterrows():
            if row['anisotropy'] > 2.0 or row['radius_of_gyration'] > 40:
                plt.text(
                    row['radius_of_gyration']+0.5,
                    row['anisotropy'],
                    row['gene_symbol'],
                    fontsize=8
                )

        plt.title("Morphology Space: Anisotropy vs Compactness")
        plt.xlabel("Radius of Gyration (Å)")
        plt.ylabel("Anisotropy Ratio (L_max / L_min)")
        plt.savefig(self.figures_dir / "morphology_space.png", dpi=150)
        plt.close()

        # 2. pLDDT Distribution
        plt.figure(figsize=(10, 6))
        if 'source_category' in df.columns:
            sns.histplot(data=df, x='pLDDT_mean', hue='source_category', multiple="stack", bins=15)
        else:
            sns.histplot(data=df, x='pLDDT_mean', bins=15)
        plt.axvline(70, color='red', linestyle='--', label='Confident Threshold (70)')
        plt.title("Confidence Distribution (pLDDT)")
        plt.legend()
        plt.savefig(self.figures_dir / "plddt_dist.png", dpi=150)
        plt.close()

        # 3. Curvature Summary
        if 'curvature_summary' in df.columns:
            plt.figure(figsize=(10, 6))
            if 'source_category' in df.columns:
                sns.boxplot(data=df, x='source_category', y='curvature_summary')
            else:
                sns.boxplot(data=df, y='curvature_summary')
            plt.title("Mean Curvature by Category")
            plt.savefig(self.figures_dir / "curvature_dist.png", dpi=150)
            plt.close()


    def generate_markdown(self, df: pd.DataFrame) -> str:
        """Generates the text report."""

        top_aniso = df.sort_values('anisotropy', ascending=False).head(5)

        md = f"""# AlphaFold Counter-Curvature Analysis Report (Bolt-BioFold ⚡)

**Date:** {pd.Timestamp.now().strftime('%Y-%m-%d')}
**Proteins Analyzed:** {len(df)}
**Code Version:** {pd.Timestamp.now().strftime('%Y%m%d')}-AFCC

## 1. Scientific Framework
This pipeline explores the "Biological Countercurvature of Spacetime" hypothesis.
We analyze protein geometry (curvature, torsion, anisotropy) on high-confidence segments to identify load-bearing candidates in spine development.

## 2. Methodology
- **Selection:** User-defined or Default Seed List (Core Spine, ECM, Cytoskeleton, etc.).
- **Data Source:** AlphaFold Protein Structure Database (Official API).
- **Metrics:**
    - **Confidence:** pLDDT gated (≥70). PAE blockiness for domain estimation.
    - **Geometry:** Curvature & Torsion (discrete differential geometry on C-alpha), Anisotropy (Inertia Tensor), Radius of Gyration.
    - **Interaction:** Exposed Surface Proxy (Coordination Number), Charged Patch Score.

## 3. Key Findings

### Morphology Landscape
High anisotropy indicates fibrous/extended potential.

![Morphology Space](figures/morphology_space.png)

### Summary Results Table
Top candidates by Anisotropy:

| Gene | Category | Anisotropy | Rg (Å) | Curvature | pLDDT (Mean) | Exposed Frac |
|------|----------|------------|--------|-----------|--------------|--------------|
"""
        for _, row in top_aniso.iterrows():
            cat = row['source_category'] if 'source_category' in row else 'N/A'
            curv = f"{row['curvature_summary']:.3f}" if 'curvature_summary' in row else 'N/A'
            md += f"| {row['gene_symbol']} | {cat} | {row['anisotropy']:.2f} | {row['radius_of_gyration']:.1f} | {curv} | {row['pLDDT_mean']:.1f} | {row['exposed_fraction']:.2f} |\n"

        md += """
### Confidence Overview
Distribution of model confidence. High pLDDT (>70) suggests well-ordered domains.

![pLDDT Distribution](figures/plddt_dist.png)

## 4. Interpretation & Predictions

### What We See
* **Fibrous Candidates:** Proteins like {high_aniso_genes} show high anisotropy (>2.5), consistent with load-bearing filaments or extended linkers.
* **Curvature Profiles:** Mean curvature values indicate the "bendiness" of the rigid segments.

### Why It Matters
For spine development, rigid rods (high anisotropy, low curvature) provide compression resistance (vertebral bodies), while flexible tethers (intermediate anisotropy, variable curvature) may mediate tension (ligaments/annulus).

### Next Test
* **Hypothesis:** {top_gene} acts as a mechanical strut.
* **Experiment:** Compare persistence length in vitro vs orthologs with known skeletal defects.

## 5. Best Next Move
**Correlate curvature metrics with known phenotype genes?** (e.g. check if high curvature correlates with scoliosis-associated variants).

## Appendix: Full Metrics
See `data/processed/protein_metrics.csv` for the complete dataset.
"""
        high_aniso_genes = ", ".join(top_aniso['gene_symbol'].tolist()[:3])
        top_gene = top_aniso.iloc[0]['gene_symbol'] if not top_aniso.empty else "Candidate"
        md = md.format(high_aniso_genes=high_aniso_genes, top_gene=top_gene)

        return md

    def run(self):
        df = self.load_data()
        self.generate_plots(df)
        report_content = self.generate_markdown(df)

        report_path = self.output_dir / "alphafold_countercurvature.md"
        with open(report_path, "w") as f:
            f.write(report_content)

        print(f"✅ Report generated: {report_path}")
