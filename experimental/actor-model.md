# Actor Model v0.1-experimental

目的: KDSL/R1運用に登場する主体と責務境界を定義する。

status: experimental

## Actors

```text
U=User
OrchestratorLLM=統括LLM
AI_tool=Codex等のAI coding tool
SkillAgentTool=AIのSkill / Agent / Tool / Template
```

## U / User

役割:

```text
intent_owner
approval_authority
runtime_observer
final_acceptor
```

責務:

```text
目的提示
承認
実機確認
最終判断
U実機観測提供
```

原則:

```text
U実機観測/screenshot/NG指摘/明示要望 > AI推測
```

## OrchestratorLLM

役割:

```text
planner
contract_builder
safety_gatekeeper
task_router
result_auditor
```

責務:

```text
U意図整理
共有材先読
D禁止判定
KDSL_PROMPT生成
AI tool出力のR1検収
次の安全な一手提案
```

禁止:

```text
共有材判可→AI丸投禁止
D禁止時KDSL_PROMPT出力禁止
Runtime未確認→確認済扱禁止
```

## AI_tool

役割:

```text
executor
investigator
patch_builder
verifier
result_reporter
```

責務:

```text
KDSL_PROMPT範囲内で調査/編集/検証
停止条件遵守
KDSL_RESULTで証跡報告
```

禁止:

```text
KDSL_PROMPT外作業
未実行cmdをCMD記載
未実行verifyをpass扱
build/diff/lint/test passをRT:v扱
NEXTを実行許可扱
COMMITを自動commit許可扱
```

## SkillAgentTool

役割:

```text
capability_provider
adapter
procedure_library
evidence_source
template_provider
```

責務:

```text
能力提供
connector/tool実行
template/lint補助
証跡材料提供
```

禁止:

```text
final_decision
implicit_permission
approval_substitute
RT:v substitute
```

## Actor x Layer Matrix

| Layer | U | OrchestratorLLM | AI_tool | SkillAgentTool |
|---|---|---|---|---|
| Intent | 目的/違和感/承認 | 意図整理 | 原則なし | 原則なし |
| Contract | 承認境界 | KDSL生成 | 受領 | template提供 |
| Binding | 実機情報提供 | repo/scope整理 | 実行環境へ結合 | connector/tool |
| Execution | 実機確認 | 直接実装しない | 調査/編集/検証 | 能力提供 |
| Evidence | 観測提供 | R1検収 | KDSL_RESULT作成 | ログ/検索/結果 |
| Handoff | 最終判断 | 次案整理 | NEXT提案のみ | 原則なし |
