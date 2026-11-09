# Initial geometry-check attempt

The initial CPU run failed its analytic-accuracy assertion. The symmetry,
zero-gravity, gravity-scaling and translation controls were below 1e-10 N m.
The synthetic helix's base-torque errors at 32, 64, 128 and 256 segments were
0.0138262300, 0.00346122727, 0.000865598884 and 0.000216417978 N m.
The last error exceeded the specified 1e-4 N m accuracy criterion.

The next attempt retains that criterion and adds 512 and 1024 segments.
This is mesh refinement of a synthetic quadrature identity, not a biological
experiment or a change to the frozen Newton campaign.
