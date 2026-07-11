# R1C Validator Verification

status: candidate verification / final CI pending
branch: agent/kdsl-r1c-validator
schema: kdsl-r1c@0.1-draft
validator: tools/validator/kdsl_r1c.py

## 1. Repository CI evidence

Initial pull-request run:

```text
pull_request: 7
source_head: 5a48aa3a81789a4406c75820f9389be50b291118
workflow: Validator CI
workflow_run_id: 29144103000
run_number: 44
status: completed
conclusion: success
```

Expected runner summary:

```text
SUMMARY:
  total: 49
  failed: 0
```

The workflow step `Run validator samples` completed successfully. The runner returns non-zero when any expected exit differs.

## 2. Covered valid cases

```text
R1C success repository example
R1C blocked repository example
R1C needs_user repository example
Full R1 fallback/out-of-scope
wrapper --target r1c valid
```

## 3. Covered invalid cases

```text
unknown schema
required field missing
short alias
invalid JSON-compatible value
RT:v with CI-only basis
NEXT authority not proposal_only
COMMIT automatic authority
VERIFY class contradiction
required field order mismatch
wrapper --target r1c invalid
```

## 4. Final branch gate

After documentation/alignment commits:

```text
python tools/validator/run_samples.py
```

Required:

```text
total: 49
failed: 0
Validator CI: completed/success
```

Final immutable head/run evidence is recorded in PR #7 after the branch head is fixed.

## 5. Verification boundary

```text
CI success != semantic equivalence
CI success != safety proof
CI success != RT:v
CI success != U承認
CI success != execution authority
CI success != R1C canonical/stable promotion
CI success != Packet readiness
```
