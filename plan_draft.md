Based on the memories and the user's request:
The objective is to expand the current framework to include concrete computational modeling for the multi-segment Cosserat rod model that predicts Lenke curves 1-6. This is detailed in the prompt, emphasizing that the global Hopf bifurcation is the trigger, but multi-segment eigenvalue problem defines the shape. The user states "build further on this- especially lenke's curves" and "concrete computational modeling and programmatic coding".
We have `scripts/experiments/experiment_lenke_classes.py` and `scripts/experiments/toy_model_lenke_classes.py` existing but as scripts. The memory says:
> The multi-segment Cosserat rod extension for predicting Lenke curve types (1-6) is implemented as a generalized 1D buckling eigenvalue problem `(B y'')'' = \lambda Q y` via `solve_multi_segment_cosserat_buckling` in `src/spinalmodes/countercurvature/multi_segment.py` and simulated in `scripts/experiments/experiment_polygenic_lenke_cosserat.py`, outputting to `outputs/experiments/polygenic_lenke_cosserat_results.csv` and `outputs/experiments/polygenic_lenke_cosserat_plot.png`.

Looking at `src/spinalmodes/countercurvature/multi_segment.py` - it doesn't exist yet! We need to create it.
We also need to create `scripts/experiments/experiment_polygenic_lenke_cosserat.py`.

Memory:
> In the multi-segment Cosserat rod model (multi_segment.py), the normalized spine length (z from 0 to 1) is regionalized into lumbar (0.0-0.3), thoracolumbar junction (0.3-0.4), thoracic (0.4-0.8), and proximal thoracic (0.8-1.0) sections to modulate stiffness (B) and instability drive (Q) for Lenke curve prediction.

So, I need to:
1. Create `src/spinalmodes/countercurvature/multi_segment.py` containing `solve_multi_segment_cosserat_buckling`.
2. Update `src/spinalmodes/countercurvature/__init__.py` to expose this.
3. Create `scripts/experiments/experiment_polygenic_lenke_cosserat.py` which uses this to generate the required outputs.
4. Run `experiment_polygenic_lenke_cosserat.py` and ensure it creates the specified csv and png in `outputs/experiments/`.
5. Check if we need to do anything about the `2-4%` Polygenic Threshold Model mentioned in the prompt. Wait, the user already mentioned it in the text. Let's make sure the script covers it or if another script like `experiment_polygenic_stacking.py` already exists (it does). Maybe I should ensure `experiment_polygenic_stacking.py` also runs or is complete. But the memory explicitly names `experiment_polygenic_lenke_cosserat.py` simulating this. So the focus is on creating `experiment_polygenic_lenke_cosserat.py` that ties both polygenic stacking and Lenke Cosserat rod together.
6. Verify test suite (`make test` or `pytest`) runs.
7. Run `pre_commit_instructions` and complete pre-commit steps.
