# KDSL Semantic Parser Foundation v2

status: design-candidate
phase: 6A
tracking_issue: 55
repository: tk999jp/kdsl-spec
base_reviewed: main@9434628aefb966d0b66e9d865a956d961b551ef2
review_date: 2026-07-13
authority: non-normative implementation design

## 1. Purpose

Define an additive parser/AST v2 contract that can become the shared structural input surface for KDSL validators while preserving all canonical specification, safety, authority, runtime, and release boundaries.

```text
canonical specification > parser design > validator implementation > examples
parser output != specification authority
parser pass != semantic equivalence proof
parser pass != complete safety proof
parser pass != U approval
parser pass != RT:v
parser pass != execution authority
```

This document is a design input. It does not modify Core/Profile/R1/Packet semantics and does not make Packet executable.

## 2. Confirmed Phase 1 baseline

Current implementation:

```text
tools/validator/kdsl_parser.py
tools/validator/kdsl_parser_adapter.py
tools/validator/kdsl_parse.py
tools/validator/run_parser_samples.py
```

Current node/diagnostic surface:

```text
DocumentNode
EnvelopeNode
FieldNode
SourceSpan
ParseIssue
DiagnosticBag
```

Current capabilities:

```text
UTF-8 text loading
CRLF/CR normalization to LF
source line/column spans
first matching envelope lookup
ordered field extraction
raw field text retention
duplicate field diagnostics
tab indentation diagnostics
multiline JSON-compatible value capture
block scalar extraction
mapping/sequence/record/nested-list helpers
legacy checker adapters
```

Current adapter consumers:

```text
kdsl_r1c.py
kdsl_packet.py
kdsl_packet_normalization.py
kdsl_safety_gate.py
```

Current parser corpus:

```text
run_parser_samples.py: 11 cases
```

## 3. Confirmed limitations

### 3.1 First-match envelope model

`DocumentNode.find_envelope(marker)` returns the first matching envelope. Multiple envelopes with the same marker are not represented as first-class document children.

Risk:

```text
duplicate envelope ambiguity
mixed-document ordering unavailable
later envelope silently outside checker input
```

### 3.2 Field-only AST

Nested values are not represented by typed AST nodes. Helper functions return Python values such as:

```text
dict[str, str]
list[str]
list[dict[str, str]]
dict[str, list[str]]
```

Risk:

```text
nested source span loss
nested raw text loss
nested duplicate/order diagnostics incomplete
checker-specific reparsing remains
```

### 3.3 Legacy namespace adapter

`kdsl_parser_adapter.py` installs parser-backed functions by mutating checker module namespaces.

Risk:

```text
parser dependency is implicit
checker unit isolation is difficult
legacy extraction contracts remain authoritative in practice
adapter removal cannot be proven incrementally without explicit parity tests
```

### 3.4 Header/profile structure is not first-class

Full KDSL and CompactPrompt header axes are not represented through a general header node contract:

```text
format
profile
mode
safety
lexicon
envelope
```

CompactPrompt structural aliases and free-text safety rules therefore remain primarily checker-specific.

### 3.5 Parser preflight is shallow

`kdsl_validate.py` parser preflight currently checks document issues and selected envelope issues, then launches separate checker processes.

It does not pass a shared AST object to the checkers.

### 3.6 Semantic scanning remains distributed

Several checkers retain regex/string scanning for protected wording, triggers, authority expressions, RT basis, and section boundaries.

This is expected for Phase 1 but prevents a single typed structural source from supporting later semantic work.

## 4. AST v2 design goals

```text
G1: preserve exact source text and source spans
G2: represent all structural values as typed nodes
G3: retain document/envelope/field/value ordering
G4: distinguish raw value from normalized value
G5: diagnose duplicate/unknown/ambiguous structure without inference
G6: support multiple envelopes and mixed document content
G7: provide explicit compatibility views for existing checkers
G8: keep semantic policy outside parser core
G9: prohibit implicit defaults and unknown schema/alias inference
G10: permit phased migration with parity evidence
```

## 5. Proposed AST v2 model

```text
DocumentNodeV2
  source_text
  normalized_text
  line_index
  children: DocumentChildNode[]
  issues: Diagnostic[]

DocumentChildNode
  HeaderNode | EnvelopeNodeV2 | MarkdownNode | TextNode | FenceNode

HeaderNode
  key
  raw_value
  normalized_scalar
  span
  raw_span

EnvelopeNodeV2
  marker
  fields: FieldNodeV2[]
  span
  raw_span
  issues

FieldNodeV2
  name
  value: ValueNode
  span
  name_span
  value_span
  raw_span

ValueNode
  ScalarNode
  BlockScalarNode
  MappingNode
  SequenceNode
  RecordSequenceNode
  JsonNode
  EmptyNode
  InvalidNode

MappingEntryNode
  key
  value
  span
  key_span
  value_span

SequenceItemNode
  value
  span
```

The final class names may change during implementation, but the following properties are mandatory:

```text
ordered children
source spans
raw source slice
normalized interpretation
diagnostics attached to exact nodes
no authority/safety inference in parser core
```

## 6. Raw and normalized value contract

Every parsed value must support both channels:

```text
raw_text:=exact source slice after newline normalization policy
normalized_value:=structural interpretation for checker consumption
```

Rules:

```text
raw_text must preserve protected wording and exact strings
normalization must not invent omitted values
quotes must not be discarded without raw preservation
block scalar folding must retain original style marker
mapping/sequence order must be retained
JSON parse success must retain original JSON text
JSON parse failure must produce InvalidNode + diagnostic, not guessed value
```

## 7. Document and envelope policy

### 7.1 Multiple envelopes

Parser v2 must expose every detected envelope in source order.

Checker policy remains separate:

```text
parser: report all envelopes
checker: decide zero/one/many validity for its target
```

### 7.2 Markdown and code fences

The parser must identify fence boundaries and markdown headings without treating arbitrary fenced examples as active envelopes unless the caller selects an explicit parsing context.

Required parse contexts:

```text
active-document
fenced-example
raw-envelope
```

Default validator context:

```text
active-document
```

No automatic execution or authority meaning follows from any context.

### 7.3 Header axes

The parser must structurally expose declared axes but must not correct unknown values.

```text
known value validation:=profile/core checker responsibility
unknown value inference:=prohibited
missing value default insertion:=prohibited
```

## 8. Diagnostics contract

Proposed diagnostic fields:

```text
severity: error|warning|info
code
message
primary_span
related_spans[]
node_path
origin: parser|schema|checker
```

Initial parser diagnostic classes:

```text
PARSER_TAB_INDENT
PARSER_DUPLICATE_ENVELOPE
PARSER_DUPLICATE_FIELD
PARSER_DUPLICATE_MAPPING_KEY
PARSER_INVALID_JSON
PARSER_INVALID_INDENT
PARSER_UNCLOSED_FENCE
PARSER_AMBIGUOUS_VALUE_SHAPE
PARSER_UNEXPECTED_CONTENT
```

Compatibility rule:

```text
existing Phase 1 diagnostic codes must remain available until migration closeout
new diagnostics must not silently downgrade existing errors
```

## 9. Compatibility strategy

### Stage A — additive v2 surface

```text
retain DocumentNode/EnvelopeNode/FieldNode
add v2 parse entrypoint and typed nodes
no checker migration
```

### Stage B — explicit compatibility views

Replace namespace mutation with explicit objects/functions:

```text
R1CCompatibilityView
PacketCompatibilityView
NormalizationCompatibilityView
SafetyGateCompatibilityView
```

Compatibility views must be derived from AST v2 and tested against current adapter outputs.

### Stage C — checker-by-checker migration

Migration order:

```text
1. R1C structural extraction
2. Full R1 structural extraction
3. CompactPrompt/header extraction
4. Safety Gate records
5. Packet
6. Packet Normalization
7. strict Packet semantic/property helpers
```

Reasoning:

```text
R1C has strict field/order/JSON shape and is suitable for parity testing
Full R1/CompactPrompt establish general envelope/header surfaces
Safety Gate/Packet have broader protected-language and authority coupling
strict property helpers migrate last to avoid weakening validated properties
```

### Stage D — legacy adapter retirement

`kdsl_parser_adapter.py` may be removed only when:

```text
all adapter consumers use explicit AST v2 views
legacy-vs-v2 parity corpus passes
unified expectations pass
no protected wording/authority/RT/Packet boundary regression is observed
```

## 10. Semantic ownership boundary

Parser core may determine:

```text
structure
order
source location
raw source slices
syntactic value shape
JSON syntax validity
indentation/fence/envelope boundaries
```

Parser core must not determine:

```text
Safety Gate satisfied/blocked meaning
protected wording equivalence
approval validity
execution authority
RT:v validity
NEXT execution permission
COMMIT permission
Packet executable status transition
P1/P1L normalization completion
stable/public-ready readiness
```

These remain specification/checker decisions.

## 11. Test strategy

### 11.1 Golden corpus

```text
Full KDSL headers
CompactPrompt standard
KDSL-CP漢 structural aliases
KDSL_RESULT / Full R1
R1C inline JSON
R1C multiline JSON
SAFETY_GATES nested records
PACKET_DRAFT
NORMALIZATION_DRAFT
multiple envelopes
markdown plus fenced examples
Windows CRLF
UTF-8 Japanese protected wording
block scalar | and >
empty/missing/duplicate fields
unknown schema/profile values
```

### 11.2 Mutation properties

```text
field order mutation detected
field duplication detected
mapping-key duplication detected
indentation mutation detected
fence mutation detected
exact-string mutation visible in raw channel
normalized-value mutation visible in structural channel
envelope duplication visible to checker
unknown values retained without inference
```

### 11.3 Compatibility parity

For each current adapter consumer:

```text
legacy extraction result == v2 compatibility view result
legacy expected exit == v2 expected exit
legacy protected wording input == v2 raw source input
```

### 11.4 Required regression gates

```text
existing unified expectations: 257 / failed 0
existing parser suite: 11 / failed 0
KDSL Validation: success
Packet Semantic Property: success
```

New counts are recorded after implementation; they must not be claimed before execution.

## 12. Stop conditions

Stop implementation and report `blocked` or `needs_user` when:

```text
canonical syntax ownership is ambiguous
parser normalization would change protected wording
legacy and v2 views disagree on authority/runtime/public/data/KDSL-DP boundaries
unknown schema/profile would require inference
multiple-envelope policy requires semantic reinterpretation
checker migration changes expected exits without approved specification change
Packet appears executable or normalized through parser output
```

## 13. Phase boundaries

### Phase 6A

```text
design/inventory/status only
implementation change:none
semantic policy change:none
```

### Phase 6B

```text
additive AST v2 core
compatibility retained
checker migration:none or one bounded pilot only
```

### Phase 6C

```text
checker migration with per-checker parity evidence
legacy adapter retained until final parity
```

### Phase 6D

```text
property/corpus verification
legacy adapter retirement decision
Phase 6 closeout
```

## 14. Fixed non-goals

```text
complete YAML parser claim
complete natural-language parser claim
semantic equivalence proof
complete safety proof
arbitrary cross-document Safety Gate proof
Packet normalization completion
canonical P1/P1L schema definition
Packet executable promotion
stable/public-ready/tag/release/Release Assets operation
```
