# KDSL Runtime-Control Canonicalization v0.1 Draft

status: v2-draft adopted
canonical: v2-draft
canonicalization_id: kdsl-runtime-control-c14n@0.1-draft
applies_to:
  - kdsl-k1@0.1-draft
  - kdsl-pf1@0.1-draft

## 1. Purpose

Define deterministic semantic projection and content identity for K1/PF1 definitions.

```text
source document
→ parse one canonical K1 or PF1 envelope
→ construct schema-ordered semantic projection
→ serialize canonical JSON
→ UTF-8 encode
→ SHA-256
```

```text
source digest != semantic equivalence
matching digest != executable|authority|approval
```

## 2. Canonical projection

Only schema-defined semantic fields participate in the projection.

```text
Markdown headings/comments/explanatory prose outside the canonical envelope:=excluded
unknown field:=blocked
duplicate field:=blocked
implicit default:=prohibited
```

Projection rules:

```text
object key order:=schema-declared order
array order:=preserved exactly
string normalization:=none beyond JSON escaping
Unicode normalization:=none
line-ending meaning inside strings:=preserved as `\n`
number form:=base-10 JSON number / no NaN / no Infinity
boolean:=true|false
null:=JSON null only where schema permits
```

Paths, commands, URLs, repository names, branch names, tag names, package names, API names, class/method/property names, file names, extensions, and Windows paths must remain exact strings.

## 3. Canonical JSON serialization

The projection is serialized as compact JSON:

```text
UTF-8
no BOM
no insignificant whitespace
object keys in schema-declared order
array order preserved
JSON escaping only
final newline excluded from digest input
```

Digest form:

```text
sha256:<64 lowercase hexadecimal characters>
```

The digest is computed over the canonical JSON bytes, not over the Markdown/YAML source bytes.

### 3.1 Self-digest substitution

`IDENTITY.digest` is required in the stored instance but its stored value must not be hashed as-is.

Digest computation uses this deterministic substitution:

```text
1. construct the complete schema-ordered semantic projection
2. replace only IDENTITY.digest with the fixed string `sha256:SELF`
3. serialize canonical JSON
4. UTF-8 encode
5. compute SHA-256
6. store `sha256:<computed lowercase hex>` in IDENTITY.digest
```

Validation repeats the same substitution and compares the computed digest with the stored digest.

```text
stored digest included as-is in digest input→prohibited
stored digest=`sha256:SELF`→blocked
other fields excluded to avoid recursion→prohibited
```

The substitution removes self-reference without removing the `IDENTITY.digest` key from the canonical field structure.

## 4. Identity record

Every canonical K1/PF1 instance declares:

```yaml
IDENTITY:
  id: "<exact id>"
  revision: "<exact revision>"
  canonicalization: kdsl-runtime-control-c14n@0.1-draft
  digest: "sha256:<hex>"
  source_ref: "<exact immutable or reviewable source reference>"
```

```text
id only != content identity
revision only != content identity
source_ref only != immutable identity
digest only != semantic equivalence
```

Digest mismatch, unsupported canonicalization ID, invalid self-digest substitution, unknown field, or duplicate field results in `blocked`.

## 5. Nested referenced definitions

Presets, aliases, routes, approval references, and capability references are projected as explicit records. Their external content is not silently included.

```text
external ref used→exact id/revision/digest or immutable_ref required
unresolved external ref→blocked
```

Expanded preset/alias values must be present in later binding evidence with provenance. Expansion does not alter the source K1/PF1 digest.

## 6. Compatibility

Project-local K1/PF1 files without this canonical projection are compatibility evidence only.

```text
legacy file hash != canonical digest
legacy runtime_control_rev != schema ID
canonical promotion→explicit migration + lint + review required
```

## 7. Non-goals

```text
cryptographic signer authentication
semantic equivalence proof
approval authenticity proof
runtime capability proof
execution authorization
runtime binding implementation
```
