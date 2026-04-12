# RCU Decision v0.1 Minimal Experiment Log

```bash
python3 mini_psc_rcu_decision_v01_minimal.py
```
```text
=== STEP 0 ===
[INIT] select B

=== STEP 1 ===
[CHECK] selected=B best=B improve=0.000 stab=0.665 persist=0
[KEEP]

=== STEP 2 ===
[CHECK] selected=B best=A improve=0.031 stab=0.560 persist=0
[KEEP]

=== STEP 3 ===
[CHECK] selected=B best=A improve=0.164 stab=0.245 persist=1
[KEEP]

=== STEP 4 ===
[CHECK] selected=B best=A improve=0.243 stab=0.140 persist=2
[KEEP]

=== STEP 5 ===
[CHECK] selected=B best=A improve=0.332 stab=0.035 persist=3
[KEEP]

=== STEP 6 ===
[CHECK] selected=B best=A improve=0.364 stab=0.000 persist=4
[SWITCH] B -> A

=== STEP 7 ===
[CHECK] selected=A best=A improve=0.000 stab=0.900 persist=0
[KEEP]

=== STEP 8 ===
[CHECK] selected=A best=A improve=0.000 stab=0.900 persist=0
[KEEP]

=== STEP 9 ===
[CHECK] selected=A best=A improve=0.000 stab=0.900 persist=0
[KEEP]
```

## Summary

- Initial selection favored Path B due to higher performance.
- Path B gradually degraded over time (increasing instability).
- Switching did not occur immediately despite degradation.
- Switching was triggered only after:
  - stability dropped below threshold
  - degradation persisted beyond the configured limit
  - improvement over alternative path was sufficient
- This confirms that hysteresis and persistence-based switching are functioning correctly.

---
