from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one match, got {count}: {old!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


# Adopt candidate headers without making Packet executable/stable.
replace_once(
    "spec/packet/kdsl-packet-schema.md",
    "status: design-candidate\ncanonical: no\nschema_id: kdsl-packet@0.1-draft\nexecutable: no",
    "status: v2-draft adopted\ncanonical: v2-draft\nschema_id: kdsl-packet@0.1-draft\nexecutable: no",
)
for path, registry in (
    ("spec/registry/kdsl-packet-base-registry.md", "kdsl-packet-base"),
    ("spec/registry/kdsl-packet-task-registry.md", "kdsl-packet-task"),
    ("spec/registry/kdsl-packet-flow-registry.md", "kdsl-packet-flow"),
):
    replace_once(
        path,
        f"status: design-candidate\ncanonical: no\nregistry: {registry}",
        f"status: v2-draft adopted\ncanonical: v2-draft\nregistry: {registry}",
    )
replace_once(
    "spec/lint/kdsl-packet-lint.md",
    "status: design-candidate\ncanonical: no\nvalidator: not implemented",
    "status: v2-draft adopted\ncanonical: v2-draft\nvalidator: not implemented",
)

# Registry index.
replace_once(
    "spec/registry/README.md",
    "## Current design-candidate registries",
    "## Current v2-draft adopted Packet registries",
)
replace_once(
    "spec/registry/README.md",
    "Candidate status:\n\n```text\nadopted: no\ncanonical: no\nstable/public-ready: no\nPacket executable effect: none\nvalidator: not implemented\n```",
    "Packet registry status:\n\n```text\nadopted: v2-draft\ncanonical: v2-draft only\nstable/public-ready: no\nPacket executable effect: none\nvalidator: not implemented\n```",
)
replace_once(
    "spec/registry/README.md",
    "Packet BASE/TASK/FLOW registries:=design-candidate only",
    "Packet BASE/TASK/FLOW registries:=v2-draft adopted / non-executable",
)
replace_once(
    "spec/registry/README.md",
    "Adoption in `spec/manifest.md` authorizes v2-draft reference use only. Design-candidate registry presence does not authorize adoption, stable promotion, execution authority, Packet execution, tag/release operations, or Release Assets changes.",
    "Adoption in `spec/manifest.md` authorizes v2-draft reference use only. Registry adoption does not authorize stable promotion, normalization completion, execution authority, Packet execution, tag/release operations, or Release Assets changes.",
)

# Manifest file map.
replace_once(
    "spec/manifest.md",
    "| `spec/registry/kdsl-safety-gate-composition.md` | Registry draft | additive multi-gate composition | v2 draft adopted |\n| `spec/r1/r1-result-spec.md` | R1 | KDSL_RESULT / RT / Evidence / Authority | Yes |",
    "| `spec/registry/kdsl-safety-gate-composition.md` | Registry draft | additive multi-gate composition | v2 draft adopted |\n| `spec/registry/kdsl-packet-base-registry.md` | Registry draft | Packet normalization baseline IDs | v2 draft adopted / non-executable |\n| `spec/registry/kdsl-packet-task-registry.md` | Registry draft | Packet task-class IDs / minimum gate sets | v2 draft adopted / non-executable |\n| `spec/registry/kdsl-packet-flow-registry.md` | Registry draft | Packet semantic flow opcodes | v2 draft adopted / non-executable |\n| `spec/packet/kdsl-packet-schema.md` | Packet authoring schema draft | PACKET_DRAFT fields / normalization / authority boundary | v2 draft adopted / non-executable |\n| `spec/r1/r1-result-spec.md` | R1 | KDSL_RESULT / RT / Evidence / Authority | Yes |",
)
replace_once(
    "spec/manifest.md",
    "| `spec/lint/kdsl-r1c-lint.md` | Lint draft | R1C field/order/RT/NEXT/COMMIT/round-trip boundary lint | v2 draft adopted |\n| `spec/bridge/kdsl-adps-bridge.md` | Bridge | KDSL/KDSL-DP/ADPS/P1/P1L/R1境界 | Yes |",
    "| `spec/lint/kdsl-r1c-lint.md` | Lint draft | R1C field/order/RT/NEXT/COMMIT/round-trip boundary lint | v2 draft adopted |\n| `spec/lint/kdsl-packet-lint.md` | Lint draft | Packet envelope/registry/gate/authority/normalization lint | v2 draft adopted / validator not implemented |\n| `spec/bridge/kdsl-adps-bridge.md` | Bridge | KDSL/KDSL-DP/ADPS/P1/P1L/R1境界 | Yes |",
)
replace_once(
    "spec/manifest.md",
    "### KDSL-CP\n",
    "### KDSL-Packet authoring schema\n\n```text\nv2-draft adopted schema:\n  spec/packet/kdsl-packet-schema.md\n\nregistries:\n  kdsl-packet-base@0.1-draft\n  kdsl-packet-task@0.1-draft\n  kdsl-packet-flow@0.1-draft\n\nlint:\n  spec/lint/kdsl-packet-lint.md\n```\n\nOwnership rules:\n\n```text\nCore/Profile/R1/Bridge meaning > Packet schema/registry > Packet lint > Example/Tool\nKDSL-Packet:=non-executable authoring/transport schema\nPacket != Full KDSL/P1/P1L/KDSL_RESULT\nBASE/TASK/FLOW ID != authority\nSTATUS:non-executable固定\nNORMALIZE.required:true固定\nNORMALIZE.state:not_normalized固定\nnormalization artifact未生成/未検証→実行禁止\nunknown schema/registry/ID/opcode推測禁止\nPKT:v1使用禁止\n```\n\n### KDSL-CP\n",
)
replace_once(
    "spec/manifest.md",
    "future Packet:\n  draft-non-executable\n  PKT:v1使用禁止\n  BASE/TASK/FLOW/Packet schema/lint未定義→実行禁止",
    "current Packet:\n  schema/BASE/TASK/FLOW/lint:=v2-draft adopted\n  executable:=no\n  PKT:v1使用禁止\n  validator/normalization round-trip/stable dependency未充足→実行禁止",
)
replace_once(
    "spec/manifest.md",
    "R1C required field削除/alias置換/default追加→breaking候補\nexample追加→patch候補",
    "R1C required field削除/alias置換/default追加→breaking候補\nPacket schema/registry追加→compatible v2-draft候補\nPacket adopted ID/opcode意味変更→breaking候補または新ID必須\nPacket authority/normalization非実行境界弱化→breaking/prohibited\nexample追加→patch候補",
)
replace_once(
    "spec/manifest.md",
    "canonical R1 replacement:=none\nKDSL-Packet:=draft-non-executable",
    "canonical R1 replacement:=none\nkdsl-packet@0.1-draft:=v2-draft authoring schema adopted\nPacket BASE/TASK/FLOW registries:=v2-draft adopted\nPacket lint:=v2-draft adopted / validator not implemented\nKDSL-Packet:=draft-non-executable / normalization required",
)

# Bridge ownership and current dependency state.
replace_once(
    "spec/bridge/kdsl-cp-packet-bridge.md",
    "# KDSL-CP / KDSL-Packet Bridge v0.4-draft",
    "# KDSL-CP / KDSL-Packet Bridge v0.5-draft",
)
replace_once(
    "spec/bridge/kdsl-cp-packet-bridge.md",
    "KDSL-Packet:=将来のpacket envelope候補",
    "KDSL-Packet:=v2-draft adopted authoring envelope / non-executable",
)
replace_once(
    "spec/bridge/kdsl-cp-packet-bridge.md",
    "将来: canonical Packet schema/registry完成後のみKDSL-Packet使用可",
    "将来: Packet validator/normalization/execution promotion条件全充足後のみ実行可能性を再審査",
)
replace_once(
    "spec/bridge/kdsl-cp-packet-bridge.md",
    "## 7. KDSL-Packet draft boundary\n\nKDSL-Packet is not executable in this repository state because the following canonical specifications do not yet exist.\n\n```text\nPacket schema\nBASE registry\nTASK registry\nFLOW opcode registry\ncanonical/stable SG registry\nPacket lint\n```\n\nCurrent dependency status:\n\n```text\nkdsl-sg@0.1-draft:=v2-draft registry adopted\nSafety Gate validator:=first heuristic slice integrated\nkdsl-r1c@0.1-draft:=v2-draft serialization profile adopted\nR1C validator:=first heuristic slice integrated\nstable/canonical Packet dependency:=not satisfied\n```\n\nTherefore:\n\n```text\nKDSL-Packet未正規化→実行指示扱禁止\nPacket draft valid-looking != executable\nPKT:v1使用禁止\nunknown BASE/TASK/FLOW/SG/R1C推測禁止\nPacket registry未定義→停止\n```\n\nAllowed design notation:\n\n```text\nPACKET_DRAFT:\nstatus: non-executable\nschema: undefined\n```\n\nThis notation is for design discussion only and must not be passed to an AI coding tool as an implementation contract.",
    "## 7. KDSL-Packet adopted non-executable boundary\n\nCurrent v2-draft components:\n\n```text\nschema: kdsl-packet@0.1-draft\nsource: spec/packet/kdsl-packet-schema.md\nBASE registry: kdsl-packet-base@0.1-draft\nTASK registry: kdsl-packet-task@0.1-draft\nFLOW registry: kdsl-packet-flow@0.1-draft\nlint: spec/lint/kdsl-packet-lint.md\nvalidator: not implemented\n```\n\nAdoption boundary:\n\n```text\nPacket schema/registry/lint:=v2-draft adopted\nKDSL-Packet:=non-executable authoring/transport envelope\nSTATUS:non-executable固定\nNORMALIZE.required:true固定\nNORMALIZE.state:not_normalized固定\nBASE/TASK/FLOW ID/opcode != authority\nnormalization artifact未生成/未検証→実行禁止\n```\n\nUnresolved execution dependencies:\n\n```text\nPacket validator/sample matrix\nnormalization transformer and round-trip proof\nSafety Gate completeness/inheritance proof\nstable/canonical execution dependency\nexplicit executable promotion review/U承認\n```\n\nTherefore:\n\n```text\nKDSL-Packet未正規化→実行指示扱禁止\nPacket valid-looking/lint-looking != executable\nPKT:v1使用禁止\nunknown BASE/TASK/FLOW/SG/R1C推測禁止\nvalidator未実装→Packet lint pass扱禁止\n```\n\nRequired design notation:\n\n```text\nPACKET_DRAFT:\nSCHEMA: kdsl-packet@0.1-draft\nSTATUS: non-executable\n...\nNORMALIZE:\n  required: true\n  state: not_normalized\n```\n\nThis notation remains design/authoring input only and must not be passed directly to an AI coding tool as an implementation contract.",
)
replace_once(
    "spec/bridge/kdsl-cp-packet-bridge.md",
    "PACKET_DRAFT:\nstatus: non-executable\nschema: undefined\nfields: BASE/TASK/SRC/READ/TGT/OBS/GOAL/NON/STOP/FLOW/VERIFY/OUT",
    "PACKET_DRAFT:\nSCHEMA: kdsl-packet@0.1-draft\nSTATUS: non-executable\nfields: BASE/TASK/SRC/READ/TGT/OBS/GOAL/NON/SG/STOP/FLOW/VERIFY/OUT/AUTHORITY/NORMALIZE",
)

# Glossary Packet section.
replace_once(
    "spec/glossary-v2-draft.md",
    "## Packet terms\n\n### KDSL-Packet\n\n```text\nKDSL-Packet:=AI coding work-contract用packet envelope候補\n```\n\nCurrent status:\n\n```text\ndraft-non-executable\n```\n\nReason:\n\n```text\nPacket schema未定義\nBASE/TASK/FLOW registry未定義\nSG registryはv2-draftのみでstable/canonical Packet dependency未充足\nR1Cはv2-draft adoptedだがPacket全体の実行条件未充足\nPacket lint未定義\n```\n\n### PACKET_DRAFT\n\n```text\nPACKET_DRAFT:=未定義Packetを設計検討するための非実行表記\n```\n\nRequired marker:\n\n```text\nstatus: non-executable\nschema: undefined\n```\n\nConstraints:\n\n```text\nAI coding tool直接投入禁止\nvalid-looking != executable\nPKT:v1使用禁止\nunknown registry推測禁止\n```\n",
    "## Packet terms\n\n### KDSL-Packet\n\n```text\nKDSL-Packet:=v2-draft adoptedのnon-executable authoring/transport envelope\nschema: kdsl-packet@0.1-draft\n```\n\nCurrent status:\n\n```text\nv2-draft adopted\ncanonical/stable/executable: no\nvalidator: not implemented\nnormalization required: yes\n```\n\n### PACKET_DRAFT\n\n```text\nPACKET_DRAFT:=KDSL-Packet authoring recordの非実行top-level marker\n```\n\nRequired marker:\n\n```text\nSCHEMA: kdsl-packet@0.1-draft\nSTATUS: non-executable\nNORMALIZE.required: true\nNORMALIZE.state: not_normalized\n```\n\nConstraints:\n\n```text\nAI coding tool直接投入禁止\nvalid-looking/lint-looking != executable\nPKT:v1使用禁止\nunknown schema/registry/ID/opcode推測禁止\n```\n\n### Packet BASE\n\n```text\nBASE:=normalization/source-contract classification\nregistry: kdsl-packet-base@0.1-draft\n```\n\n```text\nBASE-DESIGN-ONLY\nBASE-KDSL-DEV\nBASE-ADPS-P1\nBASE ID != permission/normalization completion\n```\n\n### Packet TASK\n\n```text\nTASK:=work-risk/task-class classification\nregistry: kdsl-packet-task@0.1-draft\n```\n\nTASK ID selects minimum gate expectations but does not satisfy gates or grant authority.\n\n### Packet FLOW\n\n```text\nFLOW:=ordered semantic work-state transition labels\nregistry: kdsl-packet-flow@0.1-draft\n```\n\n```text\nFLOW opcode != command\nFLOW opcode != authority\none-character opcode未定義\n```\n\n### Packet NORMALIZE\n\n```text\nNORMALIZE:=PacketからFull KDSLまたはP1/P1Lへの別artifact変換要求\n```\n\n```text\nrequired:true固定\nPacket内state:not_normalized固定\nKDSL-DP→P1/P1L正規化必須\nnormalization未検証→実行禁止\n```\n",
)

# README current status/navigation/Packet positioning.
replace_once(
    "README.md",
    "R1C independent canonical/stable status: no\nvalidator sample suite: 49 expectations",
    "R1C independent canonical/stable status: no\nPacket schema: kdsl-packet@0.1-draft / v2-draft adopted / non-executable\nPacket BASE/TASK/FLOW registries: v2-draft adopted\nPacket validator: not implemented\nvalidator sample suite: 49 expectations",
)
replace_once(
    "README.md",
    "Registries:\n  spec/registry/README.md\n  spec/registry/kdsl-safety-gate-registry.md\n  spec/registry/kdsl-safety-gate-composition.md",
    "Registries:\n  spec/registry/README.md\n  spec/registry/kdsl-safety-gate-registry.md\n  spec/registry/kdsl-safety-gate-composition.md\n  spec/registry/kdsl-packet-base-registry.md\n  spec/registry/kdsl-packet-task-registry.md\n  spec/registry/kdsl-packet-flow-registry.md\n\nPacket:\n  spec/packet/kdsl-packet-schema.md",
)
replace_once(
    "README.md",
    "  spec/lint/kdsl-r1c-lint.md",
    "  spec/lint/kdsl-r1c-lint.md\n  spec/lint/kdsl-packet-lint.md",
)
replace_once(
    "README.md",
    "  examples/r1c/*\n  examples/midfd/*",
    "  examples/r1c/*\n  examples/packet/*\n  examples/midfd/*",
)
replace_once(
    "README.md",
    "KDSL-Packet:=future packet envelope candidate / draft-non-executable",
    "KDSL-Packet:=kdsl-packet@0.1-draft authoring envelope / v2-draft adopted / non-executable",
)
replace_once(
    "README.md",
    "Current unresolved Packet dependencies:\n\n```text\nPacket schema\nBASE registry\nTASK registry\nFLOW opcode registry\ncanonical/stable SG dependency\nPacket lint\n```\n\n```text\nSafety Gate Registry/validator実装 != Packet executable\nR1C adoption/validator実装 != Packet executable\n```",
    "Current adopted Packet components:\n\n```text\nschema: kdsl-packet@0.1-draft\nBASE: kdsl-packet-base@0.1-draft\nTASK: kdsl-packet-task@0.1-draft\nFLOW: kdsl-packet-flow@0.1-draft\nlint: spec/lint/kdsl-packet-lint.md\nstatus: non-executable\n```\n\nCurrent unresolved execution dependencies:\n\n```text\nPacket validator/sample matrix\nnormalization transformer/round-trip proof\nSafety Gate completeness/inheritance proof\nstable/canonical execution dependency\nexplicit executable promotion review/U承認\n```\n\n```text\nRegistry/lint adoption != Packet executable\nSafety Gate Registry/validator実装 != Packet executable\nR1C adoption/validator実装 != Packet executable\n```",
)
replace_once(
    "README.md",
    "Packet schema/BASE/TASK/FLOW registry未定義\nPacket lint未定義\nKDSL-Packet:=draft-non-executable",
    "Packet validator/sample matrix未実装\nPacket normalization transformer/round-trip proofなし\nPacket Safety Gate completeness/inheritance proofなし\nKDSL-Packet:=v2-draft adopted / non-executable",
)
replace_once(
    "README.md",
    "P1:\n  Packet BASE/TASK/FLOW registry\n  Packet schema/lint\n\nP2:\n  Safety Gate protected wording/inheritance validator拡張",
    "P1:\n  Packet validator first slice\n  Packet positive/negative sample matrix\n\nP2:\n  Packet normalization round-trip tooling/tests\n\nP3:\n  Safety Gate protected wording/inheritance validator拡張",
)
replace_once(
    "README.md",
    "P3:\n  R1C round-trip/property-based validator検討\n\nP4:",
    "P4:\n  R1C round-trip/property-based validator検討\n\nP5:",
)

# CHANGELOG.
replace_once(
    "CHANGELOG.md",
    "### Added\n\n#### R1C v2-draft ownership alignment",
    "### Added\n\n#### Packet v2-draft ownership alignment\n\n- Adopted `kdsl-packet@0.1-draft` as a v2-draft non-executable authoring schema.\n- Adopted BASE / TASK / FLOW registries as v2-draft classification registries.\n- Adopted Packet lint requirements while keeping the validator unimplemented.\n- Required `STATUS:non-executable`, `NORMALIZE.required:true`, and `NORMALIZE.state:not_normalized`.\n- Kept registry IDs/opcodes separate from authority, Safety Gate satisfaction, commands, and normalization completion.\n- Kept `PKT:v1` prohibited and direct AI coding tool execution forbidden.\n\n#### Packet registry and schema design candidate\n\n- Added `kdsl-packet@0.1-draft`.\n- Added `kdsl-packet-base@0.1-draft`, `kdsl-packet-task@0.1-draft`, and `kdsl-packet-flow@0.1-draft`.\n- Added Packet lint candidate, design-only example, and design review record.\n- PR #10 regression CI: run #78 / existing 49 expectations / failed 0.\n- Design integration did not make Packet adopted, canonical, stable, or executable until the separate ownership review.\n\n#### R1C v2-draft ownership alignment",
)
replace_once(
    "CHANGELOG.md",
    "KDSL-Packet:=draft-non-executable\nPacket schema/BASE/TASK/FLOW registry/Packet lint:=undefined\nPKT:v1:=prohibited",
    "KDSL-Packet:=kdsl-packet@0.1-draft / v2-draft adopted / non-executable\nPacket BASE/TASK/FLOW registries:=v2-draft adopted\nPacket lint:=v2-draft adopted / validator not implemented\nnormalization transformer/round-trip proof:=not implemented\nPKT:v1:=prohibited",
)

# Project status: PR records and current state.
replace_once(
    "docs/project-status.md",
    "final_head_ci_note: workflow-history approval state; not a sample failure\nstable_effect: none\n```\n\n## 3. Current architecture direction",
    "final_head_ci_note: workflow-history approval state; not a sample failure\nstable_effect: none\n```\n\n### PR #10 — Packet registry and schema design candidate\n\n```yaml\npull_request: 10\nmerge_status: merged\nmerge_method: squash\nsource_branch: agent/kdsl-packet-design\nsource_head: 5c8d16ed8f49e7263f870e95f928772b689f4137\nsquash_commit: 49cfdc665b4bf74e5324df019073aefbf786c383\nschema_id: kdsl-packet@0.1-draft\nbase_registry: kdsl-packet-base@0.1-draft\ntask_registry: kdsl-packet-task@0.1-draft\nflow_registry: kdsl-packet-flow@0.1-draft\nstatus: design_candidate_integrated\nexecutable: no\nworkflow_run_id: 29147274104\nworkflow_run_number: 78\nworkflow_conclusion: success\nsample_total: 49\nsample_failed: 0\nstable_effect: none\n```\n\n### PR #11 — Packet v2-draft ownership alignment\n\n```yaml\npull_request: 11\nmerge_status: pending\nsource_branch: agent/kdsl-packet-ownership\ntarget_status: v2_draft_adopted_non_executable\ncanonical_effect: none\nexecution_effect: none\nstable_effect: none\n```\n\n## 3. Current architecture direction",
)
replace_once(
    "docs/project-status.md",
    "R1C canonical R1 replacement:=なし\nKDSL-Packet:=draft-non-executable",
    "R1C canonical R1 replacement:=なし\nPacket design candidate:=main統合済み\nPacket ownership:=v2-draft adopted authoring schema/registries/lint\nKDSL-Packet:=non-executable / normalization required",
)
replace_once(
    "docs/project-status.md",
    "## 5. Validator maturity",
    "## 5. Packet current status\n\n```yaml\npacket:\n  schema_id: kdsl-packet@0.1-draft\n  status: v2_draft_adopted\n  canonical: v2_draft_only\n  stable: no\n  executable: no\n  base_registry: kdsl-packet-base@0.1-draft\n  task_registry: kdsl-packet-task@0.1-draft\n  flow_registry: kdsl-packet-flow@0.1-draft\n  lint: adopted\n  validator: not_implemented\n  normalize_required: true\n  packet_state: not_normalized\n  pkt_v1: prohibited\n```\n\n```text\nRegistry/opcode != authority\nvalid-looking/lint-looking != executable\nnormalization artifact未生成/未検証→実行禁止\nKDSL-DP→P1/P1L正規化必須\n```\n\n## 6. Validator maturity",
)
# Renumber later headings for readability.
for old, new in (("## 6. Safety and authority boundaries", "## 7. Safety and authority boundaries"), ("## 7. Validation evidence", "## 8. Validation evidence"), ("## 8. Known gaps before stable", "## 9. Known gaps before stable"), ("## 9. Recommended positioning", "## 10. Recommended positioning"), ("## 10. Next safe steps", "## 11. Next safe steps")):
    replace_once("docs/project-status.md", old, new)
replace_once(
    "docs/project-status.md",
    "Packet OUT/R1C integration lint\n```",
    "Packet validator/sample matrix\nPacket normalization transformer/round-trip proof\nPacket Safety Gate completeness/inheritance proof\nPacket OUT/R1C integration lint\n```",
)
replace_once(
    "docs/project-status.md",
    "### R1C validator\n",
    "### Packet design candidate regression\n\n```yaml\npull_request: 10\nsource_head: 5c8d16ed8f49e7263f870e95f928772b689f4137\nworkflow_run_id: 29147274104\nrun_number: 78\nconclusion: success\nsample_total: 49\nfailed: 0\nmeaning: existing validator regression evidence; not Packet lint pass\n```\n\n### R1C validator\n",
)
replace_once(
    "docs/project-status.md",
    "Packet schema未定義\nBASE/TASK/FLOW registry未定義\nPacket lint未定義\nKDSL-Packetはdraft-non-executable",
    "Packet validator/sample matrix未実装\nPacket normalization transformer/round-trip proofなし\nPacket Safety Gate completeness/inheritance proofなし\nKDSL-Packetはv2-draft adopted / non-executable",
)
replace_once(
    "docs/project-status.md",
    "  R1C v2-draft adopted compact serialization profile\n  experimental heuristic validator helpers",
    "  R1C v2-draft adopted compact serialization profile\n  Packet v2-draft adopted non-executable authoring schema\n  experimental heuristic validator helpers",
)
replace_once(
    "docs/project-status.md",
    "P0: local mainをorigin/mainへ同期 / 49 sample runner再確認\nP1: Packet BASE/TASK/FLOW registry/schema/lint設計\nP2: Safety Gate protected wording/inheritance validator拡張\nP3: R1C round-trip/property-based validator検討\nP4: public-facing v2 overview / CI required check検討",
    "P0: PR #11 CI確認 / squash merge / ownership closeout\nP1: Packet validator first slice / sample matrix\nP2: Packet normalization round-trip tooling/tests\nP3: Safety Gate protected wording/inheritance validator拡張\nP4: R1C round-trip/property-based validator検討\nP5: public-facing v2 overview / CI required check検討",
)

# Ownership review record.
Path("docs/reviews/kdsl-packet-ownership-integration.md").write_text(
    """# KDSL Packet Ownership Integration\n\nstatus: merge-pending\nreview_date: 2026-07-11\nbranch: agent/kdsl-packet-ownership\ntarget: main\npull_request: 11\n\n## Adopted ownership\n\n```text\nCore/Profile/R1/Bridge canonical meaning\n> Packet schema/registries/lint v2-draft mapping\n> examples/tools\n```\n\n```text\nkdsl-packet@0.1-draft:=v2-draft adopted authoring schema\nBASE/TASK/FLOW registries:=v2-draft adopted\nPacket lint:=v2-draft adopted / validator not implemented\ncanonical/stable/executable:=no\n```\n\n## Required non-execution boundary\n\n```text\nSTATUS:non-executable\nNORMALIZE.required:true\nNORMALIZE.state:not_normalized\nRegistry/opcode != authority\nnormalization artifact未生成/未検証→実行禁止\nPKT:v1使用禁止\n```\n\n## Remaining promotion dependencies\n\n```text\nPacket validator/sample matrix\nnormalization transformer and round-trip proof\nSafety Gate completeness/inheritance proof\nstable/canonical execution dependency\nexplicit executable promotion review/U承認\n```\n\n## Verification boundary\n\n```text\nPR #10 run #78 success / existing 49 expectations / failed 0\nPacket validator not implemented\nCI pass != Packet lint pass\nCI pass != semantic equivalence/safety proof/RT:v/authority/release readiness\n```\n\n## Non-actions\n\n```text\nPacket direct executionなし\nPKT:v1有効化なし\ncanonical Core/R1/KDSL-DP境界変更なし\ntag/release/Release Assets操作なし\nstable/public-ready化なし\nsource branch削除なし\n```\n""",
    encoding="utf-8",
)

# Remove temporary script; workflow is restored by the job before commit.
Path(".github/scripts/apply_packet_ownership.py").unlink()
