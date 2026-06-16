# Protocol Stack / Work Stack v0.1-experimental

目的: KDSL/R1を Human-AI Work Protocol Stack として整理する。

status: experimental

## 基本モデル

```text
Human Intent
  ↓
KDSL Surface
  ↓
Contract / Safety
  ↓
Runtime Binding
  ↓
Execution
  ↓
Evidence / R1
  ↓
Human Handoff
```

## Layers

### L0 Intent

```text
U目的
U観測
承認境界
実機確認対象
```

### L1 Surface

```text
KDSL syntax
format/profile/mode/safety
operator/abbrev
KDSL_PROMPT
```

### L2 Contract

```text
pre
allow
deny
invariant
stop
post
```

### L3 Binding

```text
repo
branch
HEAD
target_slice
commands
tool
runtime
```

### L4 Evidence

```text
CMD
VERIFY
RT
OBSERVED
INFERRED
NOT_OBSERVED
UNVERIFIED
```

### L5 Handoff

```text
STATUS
RISK
NEXT
COMMIT
USER_CHECK
```

## Planes

```text
Data Plane: Phase/目的/対象Slice/変更内容/cmd/diff
Control Plane: 禁止/停止条件/承認待/D禁止/RT状態
Management Plane: state/docs/decision_log/phase_backlog/lint/template version
Evidence Plane: CMD/VERIFY/RT/observed/not_observed/unverified
```

## 原則

```text
層を増やしすぎない
KDSL直投入性を壊さない
template未読時は停止
層間自動継承禁止
KDSL-DP valid != executable
executed != verified
verified != runtime verified
build pass != RT:v
```
