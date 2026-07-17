# Phase 8 — Shared AST v2 P1L First-Class Integration Review

status: integrated / closeout merged / final status pending
review_date: 2026-07-18
repository: tk999jp/kdsl-spec
tracking_issue: 128
implementation_pull_request: 129
closeout_pull_request: 130
implementation_source_head: 3285995a4c31c749537e190956f53c38bf35c627
implementation_squash_commit: a9e27531b7dc2d9bca68de5284a76616956a7242
closeout_alignment_head: 9613cc1d4943da9be446104dd740f705d3dd5b97
closeout_squash_commit: cdb907d139bf562bc6cca9c4fdb436d12d802ea6
workflow_run_id: 29613070208
workflow_run_number: 449
workflow_conclusion: success
closeout_targeted_run_id: 29613547376
closeout_targeted_conclusion: success
closeout_workflow_run_id: 29613621345
closeout_workflow_run_number: 455
closeout_workflow_conclusion: success

## 1. Goal

Promote canonical `P1L:` recognition from checker-local bootstrap registration into the shared typed AST v2 parser without changing contract meaning or making P1L/P1 executable.

## 2. Integrated change

```text
shared KNOWN_ENVELOPES += P1L
legacy colon-P1 rejection ownership → kdsl_p1_contract.py
known P1/P1L consumers → kdsl_p1_contract imports
kdsl_p1_bootstrap.py → removed
run_p1_shared_ast_samples.py → added
run_all_samples.py → shared P1L runner integrated
```

P1 compact serialization remains a dedicated delimiter-aware scanner and was not promoted to an AST envelope.

## 3. Compatibility corpus

```text
P1L shared marker registration
canonical P1L field-order projection
active-document fence isolation
duplicate P1L envelope detection
legacy colon-P1 rejection ownership
P1 compact non-envelope boundary
bootstrap file/import inventory
known consumer migration
```

Result:

```text
shared P1L compatibility corpus: 10 / failed 0
P1L/P1 contract corpus: 14 / failed 0
Packet→P1L/P1 normalization corpus: 17 / failed 0
```

## 4. Verification evidence

Implementation review head:

```text
workflow run: 29613070208 / #449
KDSL Validation: success
Packet Semantic Property: success
Packet P1 Normalization Property: success
```

Closeout targeted verification:

```text
workflow run: 29613547376
shared P1L compatibility corpus: success
P1L/P1 contract corpus: success
Packet→P1L/P1 normalization corpus: success
```

Closeout review head:

```text
workflow run: 29613621345 / #455
KDSL Validation: success
Packet Semantic Property: success
Packet P1 Normalization Property: success
```

Final project-status review must still pass repository-required checks before Phase 8 is marked complete.

## 5. Corrective history

```text
initial branch patch trigger did not run on connector-created push
PR-trigger patch applied but shared runner inventory self-matched
first correction exposed generated newline escaping defect
second correction exposed generated indentation defect
clean raw-string/dedent generation passed all targeted checks
final review removed an unnecessary leading line-continuation character
run #449 succeeded after the clean-up commit
```

These failures occurred before merge and were not treated as implementation success.

## 6. Preserved boundaries

```text
P1L AST recognition != executable contract
P1L/P1 valid|lint|round-trip pass != authority
BINDING.executable:false
P1 compact remains non-envelope serialization
Packet remains non-executable/not_normalized
P1L_PREVIEW != P1L:
P1_PREVIEW != P1|
semantic_equivalence:not_proven
execution_authority:none
RT:v/NEXT/COMMIT meanings unchanged
```

## 7. Not implemented / not proven

```text
runtime binding
K1/PF1 canonical runtime-control schema
executable transformer
Packet normalized-state promotion
AI coding tool direct execution from P1L/P1/preview
complete semantic equivalence
complete safety proof
stable/public-ready promotion
```

No tag, release, or Release Assets operation was performed.
