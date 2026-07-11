# Packet Normalization Expected Results

status: first-slice candidate
expected_total_suite: 93

```text
repository Full KDSL preview: pass
repository P1 blocked: pass
repository critical-loss blocked: pass
baseline normalization: pass
schema/status/source/target/authority violations: fail
P1 resolved: fail
executable target marker: fail
critical loss + resolved target: fail
blocked target + preview: fail
out-of-scope: pass/info
wrapper normalization valid/invalid: expected exits
wrapper all valid normalization: pass
mapper Full KDSL: non-executable preview / exit 0
mapper P1: blocked / no preview / exit 1
mapper invalid Packet: no normalization output / exit 2
```
