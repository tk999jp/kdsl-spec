# Phase 6B — Typed Semantic Parser Core

status: completed / integrated
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
tracking_issue: 55
design_pull_request: 56
design_squash_commit: bedd63937a9ef746962836833d24ad77ff3f09d0
implementation_pull_request: 57
implementation_source_head: 549c8a7608ade2ea816dfc84d6e3b37cfa0705b0
implementation_squash_commit: 54c214587cedfc4af634edba9d3df7cdea30d524
workflow_run_id: 29222907053
workflow_run_number: 257
workflow_conclusion: success

## 1. Goal

Implement the Phase 6A parser design as an additive typed AST v2 surface without replacing the Phase 1 parser, compatibility adapter, or existing semantic checkers.

```text
additive parser core > premature checker migration
compatibility evidence > adapter removal
meaning/safety/authority retention > parser simplification
```

## 2. Integrated implementation

Added:

```text
tools/validator/kdsl_parser_v2.py
tools/validator/kdsl_parse_v2.py
tools/validator/run_parser_v2_samples.py
tools/validator/samples/parser-v2/*
```

Updated:

```text
tools/validator/run_all_samples.py
```

Unchanged:

```text
tools/validator/kdsl_parser.py
tools/validator/kdsl_parser_adapter.py
existing semantic checker policy
canonical specification files
```

## 3. AST v2 surface

```text
DocumentNodeV2
HeaderNode
EnvelopeNodeV2
FieldNodeV2
SourceSpanV2
DiagnosticV2

ScalarNode
BlockScalarNode
JsonNode
EmptyNode
InvalidNode
MappingNode / MappingEntryNode
SequenceNode / SequenceItemNode
RecordSequenceNode
FenceNode
MarkdownNode
TextNode
```

## 4. Implemented structural properties

```text
ordered document children
formal header-axis representation
multiple envelope exposure
raw source + normalized value channels
nested typed mapping/sequence/record values
source spans for nested values
related-span duplicate diagnostics
duplicate envelope detection
duplicate field detection
duplicate mapping-key detection
invalid multiline JSON detection
unclosed markdown fence detection
active-document fence isolation
CRLF to LF normalization
UTF-8/Japanese protected wording preservation
unknown header values retained without inference
```

## 5. Verification evidence

Pull-request workflow:

```text
workflow: KDSL Validation
run_id: 29222907053
run_number: 257
conclusion: success
jobs:
  KDSL Validation: success
  Packet Semantic Property: success
```

Corpus:

```text
Phase 1 parser/adapter suite: 11 / failed 0
Phase 6B parser-v2 suite: 12 / failed 0
previous unified total: 257 / failed 0
current unified total: 269 / failed 0
```

The current unified total is the deterministic aggregate of the previously integrated 257 expectations and the successful 12-case parser-v2 runner. The unified workflow fails when a child runner fails or omits its summary.

## 6. New parser-v2 corpus classes

```text
formal Full KDSL headers
nested mapping/sequence/record nodes
literal/folded block scalars
duplicate envelope
duplicate field
duplicate mapping key
invalid multiline JSON
unclosed fence
fenced inactive example isolation
unknown header values without inference
exact Japanese protected wording
CRLF normalization
```

## 7. Compatibility boundary retained

```text
Phase 1 parser remains active for existing checkers
legacy namespace adapter remains
checker migration: none
legacy adapter retirement: prohibited
```

Existing adapter consumers remain:

```text
R1C
Packet
Packet Normalization
Safety Gate
```

AST v2 is not yet the semantic input authority for these checkers.

## 8. Semantic and authority boundaries

```text
parser pass != semantic equivalence
parser pass != complete safety proof
parser pass != U approval
parser pass != RT:v
parser pass != execution authority
parser pass != release readiness
```

Retained:

```text
KDSL-DP直接実行禁止
KDSL-DP→P1/P1L正規化必須
NEXT:=提案, 実行許可扱禁止
COMMIT自動commit許可扱禁止
Packet executable:no
Packet state:not_normalized
PKT:v1使用禁止
stable/public-ready/tag/release/Release Assets操作なし
```

## 9. Known limitations after Phase 6B

```text
AST v2 compatibility views are not implemented
existing checkers do not consume AST v2
legacy-vs-v2 parity corpus is not complete
legacy adapter retirement proof is absent
active-document/raw-envelope are first-slice contexts only
not a complete YAML parser
not a complete natural-language semantic parser
full semantic equivalence not proven
complete safety proof not proven
```

## 10. Phase 6C entry condition

The next safe migration is a bounded R1C compatibility-view pilot because R1C has strict envelope, field order, and JSON-compatible value contracts.

```text
Phase 6C-1:
  add explicit R1CCompatibilityView
  compare legacy and AST v2 extraction
  retain existing R1C checker exits
  do not remove legacy adapter
```

Stop when:

```text
legacy and v2 field order/value/raw text differ
RT/NEXT/COMMIT inputs change
unknown schema/default inference would be required
existing expected exits change without specification approval
```

## 11. Closeout decision

```text
Phase 6A design: integrated
Phase 6B typed AST v2 core: integrated
Phase 6C checker migration: pending
Issue #55: remain open
semantic equivalence: not_proven
complete safety proof: not_proven
Packet executable: no
public_ready: no
stable_release: no
```
