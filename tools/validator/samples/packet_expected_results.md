# Packet Validator Expected Results

status: first-slice candidate

```text
repository example: pass
baseline sample: pass
unknown schema: fail
executable status: fail
missing required field: fail
unknown BASE/TASK/SG/FLOW: fail
BASE/NORMALIZE mismatch: fail
minimum gate missing: fail
FLOW order violation: fail
missing authority rail: fail
normalized state: fail
PKT:v1: fail
broad push/release authority: warn
out-of-scope document: pass/info
wrapper packet valid/invalid: expected exit preserved
wrapper all valid Packet: pass
```
