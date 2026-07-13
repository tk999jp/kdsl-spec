# Phase 6A — Semantic Parser Foundation Contract

status: design-review-candidate
review_date: 2026-07-13
repository: tk999jp/kdsl-spec
base: main@9434628aefb966d0b66e9d865a956d961b551ef2
tracking_issue: 55
implementation_change: none
semantic_policy_change: none

## 1. Goal

Record the current parser/checker coupling and approve an additive AST v2 migration contract before implementation.

```text
meaning preservation > safety gate preservation > branch/authority preservation > parser simplification
```

## 2. Files reviewed

```text
tools/validator/kdsl_parser.py
tools/validator/kdsl_parser_adapter.py
tools/validator/kdsl_parse.py
tools/validator/kdsl_validate.py
tools/validator/run_parser_samples.py
tools/validator/kdsl-parser-implementation-notes.md
tools/validator/README.md
docs/reviews/kdsl-phase1-common-parser.md
docs/project-status.md
```

Checker connection points reviewed:

```text
kdsl_r1c.py
kdsl_packet.py
kdsl_packet_normalization.py
kdsl_safety_gate.py
```

## 3. Inventory result

### Implemented and retained

```text
DocumentNode / EnvelopeNode / FieldNode
SourceSpan / ParseIssue / DiagnosticBag
newline normalization
tab-indentation diagnostics
first-envelope extraction
field order and duplicate detection
raw field text
inline/multiline value capture
JSON syntax diagnostics
block scalar/mapping/sequence/record helper parsing
parser preflight
11-case parser/adapter suite
```

### Coupling that must be retired gradually

```text
kdsl_parser_adapter.py mutates checker namespaces
four checkers consume legacy extraction function shapes
nested parser helpers return untyped dict/list values
checker processes do not receive one shared AST instance
```

### Missing first-class structures

```text
multiple same-marker envelopes
document child ordering
Full KDSL header axes
CompactPrompt header/structural key model
nested value nodes with source spans
fence/context model
related-span diagnostics
explicit compatibility views
```

## 4. Risk classification

### High risk

```text
protected wording raw text loss
authority or RT basis input reinterpretation
Safety Gate record scope/order change
Packet state or execution-boundary weakening
unknown value inference
legacy checker exit-code drift
```

### Medium risk

```text
multiple-envelope handling
markdown/code-fence boundary changes
block scalar folding differences
quote/unquote behavior changes
nested duplicate/order behavior
```

### Low risk

```text
additive typed node classes
new parser-only corpus
explicit node-path diagnostics
read-only compatibility projections
```

## 5. Selected architecture

```text
source text
→ DocumentNodeV2
→ ordered document children
→ HeaderNode / EnvelopeNodeV2 / Markdown/Text/Fence nodes
→ FieldNodeV2
→ typed ValueNode tree
→ explicit compatibility view
→ existing semantic checker
```

The parser owns syntax and source identity. Semantic checkers retain safety, authority, runtime, and specification policy.

## 6. Migration order

```text
6B-1: additive AST v2 core and parser corpus
6B-2: R1C compatibility-view pilot
6C-1: Full R1 and CompactPrompt structure
6C-2: Safety Gate records
6C-3: Packet and Normalization
6C-4: strict Packet semantic/property helpers
6D: mutation/corpus parity and adapter retirement decision
```

## 7. Compatibility requirements

```text
Phase 1 API remains available during 6B/6C
existing diagnostic codes retained until closeout
legacy extraction outputs compared with v2 compatibility views
existing expected exits unchanged unless a separate canonical specification change is approved
raw protected wording must remain available exactly
unknown schema/profile/alias/default inference prohibited
```

## 8. Test matrix

```text
existing unified expectations: 257
existing parser cases: 11
new parser corpus: count to be established by executed implementation
```

Required classes:

```text
CRLF/LF
UTF-8 Japanese
Full KDSL headers
CompactPrompt standard/kanji-v1
Full R1/R1C
Safety Gate nested records
Packet/Normalization
multiple envelopes
fenced examples
block scalar
JSON valid/invalid
duplicate/order/indentation mutation
raw/normalized channel preservation
legacy/v2 parity
```

## 9. Stop conditions

```text
protected wording changes after parsing
legacy/v2 authority, RT, public, data, rollback, KDSL-DP outputs differ
unknown values require guessing
multiple-envelope handling changes canonical meaning
expected exit changes without separate approval
Packet becomes executable/normalized by parser interpretation
```

## 10. Phase 6A decision

```text
AST v2 direction: adopt as implementation design candidate
implementation: deferred to Phase 6B
legacy adapter removal: prohibited in Phase 6A/initial 6B
semantic policy change: none
canonical specification change: none
```

## 11. Authority boundaries

```text
parser pass != semantic equivalence
parser pass != safety proof
parser pass != U approval
parser pass != RT:v
parser pass != execution authority
validator/CI pass != release readiness
NEXT:=proposal only
COMMIT:=no automatic commit authority
```

## 12. Phase 6A acceptance checklist

```text
current dependency inventory: recorded
AST v2 contract: recorded
raw/normalized preservation: recorded
compatibility strategy: recorded
migration order: recorded
test matrix: recorded
stop conditions: recorded
implementation change: none
semantic-policy change: none
```
