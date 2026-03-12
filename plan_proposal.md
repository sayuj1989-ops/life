1. **Create Simulation Script**
   - Use `write_file` to create `scripts/experiment_energy_deficit_window.py`.
   - The script will import `solve_beam_static` from `src.spinalmodes.iec`.
   - The script will compute `P_counter(L)` and `S_proprio(L)` for varying `L` from 0.25 to 0.55.
   - For each `L`, construct the spatial domain `s` using `np.linspace(0, L, 100)` and the bimodal Gaussian coherence field from `s_norm`.
   - Compute `kappa_target = chi_kappa * grad_I * L`.
   - Run `solve_beam_static(s, kappa_target, E_field, M_active)` for the IEC model, passing `E_field=E0` and `M_active=0`. For the passive model, run it with `kappa_target=0`.
   - `P_counter` is computed as `eta_a * rho * A * g * L^2 * mean((kappa_IEC - kappa_passive)**2)`.
   - Compute `S_proprio` for `alpha=0.5` and `alpha=1.0`. Find `L_crit` based on intersection.
   - Save the CSV to `outputs/thermodynamic_cost/energy_deficit_window.csv`.
   - Create a plot and save to `outputs/figures/energy_deficit_window.png`. The file will have `matplotlib.use('Agg')` at the top.

2. **Verify Script Execution**
   - Use `run_in_bash_session` to execute `python3 scripts/experiment_energy_deficit_window.py`.
   - Verify the outputs are generated correctly without errors using `ls -la outputs/thermodynamic_cost/energy_deficit_window.csv` and `ls -la outputs/figures/energy_deficit_window.png`.

3. **Update Manuscript Results**
   - Use `replace_with_git_merge_diff` to add the required text about the energy deficit window at the end of section 4.6 (just before `\subsection{Testable Predictions}`) in `manuscript/sections/results.tex`.

4. **Update Manuscript Figures**
   - Use `replace_with_git_merge_diff` to modify `manuscript/sections/figures.tex`. Update the `% Figure 7: Energy Deficit Window` label to `% Figure 6: Energy Deficit Window` if there are two figures labeled Figure 6, or re-order if appropriate. The user specifically asked to "Add a Figure 6 entry for the energy deficit window plot." Based on the current text, it is marked as Figure 7 in comments. I will rewrite the figure comment to Figure 6 and adjust adjacent figure comments if needed using `replace_with_git_merge_diff`.

5. **Run tests**
   - Use `run_in_bash_session` to run `pytest tests/` to ensure no functionality is broken.

6. **Complete pre-commit steps**
   - Complete pre commit steps to make sure proper testing, verifications, reviews and reflections are done.

7. **Commit and Submit**
   - Use `run_in_bash_session` to run `git add .` and `git commit -m "feat: simulate P_counter(L) energy deficit window with figure"`.
   - Call the `submit` tool without parameters.
