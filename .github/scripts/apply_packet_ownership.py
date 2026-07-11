from pathlib import Path


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected exactly one match, got {count}: {old!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


# Packet schema adopted-state labels.
replace_once("spec/packet/kdsl-packet-schema.md", "# KDSL Packet Schema v0.1 Draft Candidate", "# KDSL Packet Schema v0.1 Draft")
replace_once("spec/packet/kdsl-packet-schema.md", "This candidate defines a compact authoring envelope", "This v2-draft schema defines a compact authoring envelope")
replace_once("spec/packet/kdsl-packet-schema.md", "KDSL-Packet:=authoring/transport candidate", "KDSL-Packet:=v2-draft authoring/transport schema")
replace_once(
    "spec/packet/kdsl-packet-schema.md",
    "schema: kdsl-packet@0.1-draft\nstatus: design-candidate\nexecutable: no",
    "schema: kdsl-packet@0.1-draft\nstatus: v2-draft adopted\nexecutable: no",
)
replace_once("spec/packet/kdsl-packet-schema.md", "This candidate may be reviewed, linted, summarized, or normalized.", "This schema may be reviewed, linted, summarized, or normalized.")
replace_once(
    "spec/packet/kdsl-packet-schema.md",
    "> adopted Safety Gate/R1C mappings\n> Packet candidate\n> Packet lint candidate",
    "> adopted Safety Gate/R1C mappings\n> Packet v2-draft schema/registries\n> Packet lint",
)
replace_once("spec/packet/kdsl-packet-schema.md", "## 5. Candidate record shape", "## 5. Record shape")
replace_once(
    "spec/packet/kdsl-packet-schema.md",
    "The example shape is illustrative. Registry adoption and Packet lint implementation are separate phases.",
    "This shape defines the adopted v2-draft authoring structure. Packet validator implementation remains a separate phase.",
)
replace_once("spec/packet/kdsl-packet-schema.md", "## 7. Candidate invariants", "## 7. Adopted invariants")

# BASE/TASK/FLOW adopted-state labels.
for path, title, purpose_old, purpose_new, block_old, block_new, entries_old, entries_new in (
    (
        "spec/registry/kdsl-packet-base-registry.md",
        "# KDSL Packet BASE Registry v0.1 Draft Candidate",
        "This candidate defines normalization baselines for a future KDSL-Packet.",
        "This v2-draft registry defines normalization baselines for KDSL-Packet authoring.",
        "registry: kdsl-packet-base@0.1-draft\nstatus: design-candidate\nadopted: no",
        "registry: kdsl-packet-base@0.1-draft\nstatus: v2-draft adopted\nadopted: yes",
        "## 4. Candidate entries",
        "## 4. Adopted entries",
    ),
    (
        "spec/registry/kdsl-packet-task-registry.md",
        "# KDSL Packet TASK Registry v0.1 Draft Candidate",
        "This candidate classifies the intended work represented by a future KDSL-Packet.",
        "This v2-draft registry classifies intended work represented by KDSL-Packet authoring.",
        "registry: kdsl-packet-task@0.1-draft\nstatus: design-candidate\nadopted: no",
        "registry: kdsl-packet-task@0.1-draft\nstatus: v2-draft adopted\nadopted: yes",
        "## 4. Candidate entries",
        "## 4. Adopted entries",
    ),
    (
        "spec/registry/kdsl-packet-flow-registry.md",
        "# KDSL Packet FLOW Registry v0.1 Draft Candidate",
        "This candidate defines semantic flow opcodes for a future KDSL-Packet.",
        "This v2-draft registry defines semantic flow opcodes for KDSL-Packet authoring.",
        "registry: kdsl-packet-flow@0.1-draft\nstatus: design-candidate\nadopted: no",
        "registry: kdsl-packet-flow@0.1-draft\nstatus: v2-draft adopted\nadopted: yes",
        "## 4. Candidate opcodes",
        "## 4. Adopted opcodes",
    ),
):
    replace_once(path, title, title.replace(" Candidate", ""))
    replace_once(path, purpose_old, purpose_new)
    replace_once(path, block_old, block_new)
    replace_once(path, entries_old, entries_new)

replace_once("spec/registry/kdsl-packet-flow-registry.md", "Candidate step shape:", "Adopted step shape:")

# Packet lint adopted-state label.
replace_once("spec/lint/kdsl-packet-lint.md", "# KDSL Packet Lint v0.1 Draft Candidate", "# KDSL Packet Lint v0.1 Draft")
replace_once("spec/lint/kdsl-packet-lint.md", "This candidate defines semantic and structural checks for Packet design artifacts.", "This v2-draft lint specification defines semantic and structural checks for Packet authoring artifacts.")

# Manifest current Packet boundary: distinguish adoption causality from current state.
replace_once(
    "spec/manifest.md",
    "SG registry v2-draft採用 != Packet schema完成\nSG registry v2-draft採用 != BASE/TASK/FLOW registry完成\nR1C v2-draft採用 != Packet schema/registry完成\nSG registry v2-draft採用 != Packet lint完成\nKDSL-Packet:=draft-non-executable保持\nPKT:v1使用禁止保持",
    "SG/R1C adoption alone != Packet execution readiness\nPacket schema/registry/lint adoption != Packet executable\nPacket validator/normalization proof未充足→実行禁止\nKDSL-Packet:=non-executable / normalization required保持\nPKT:v1使用禁止保持",
)

# Bridge current terminology.
replace_once(
    "spec/bridge/kdsl-cp-packet-bridge.md",
    "scope: CompactPrompt lift / Full KDSL boundary / Safety Gate Registry / R1C / future Packet boundary",
    "scope: CompactPrompt lift / Full KDSL boundary / Safety Gate Registry / R1C / Packet non-executable boundary",
)
replace_once(
    "spec/bridge/kdsl-cp-packet-bridge.md",
    "This bridge defines when KDSL-CP must be lifted to Full KDSL, how the v2-draft Safety Gate Registry may be referenced, and how R1C may serialize results without making a future KDSL-Packet executable.",
    "This bridge defines when KDSL-CP must be lifted to Full KDSL, how the v2-draft Safety Gate Registry and R1C may be referenced, and why adopted KDSL-Packet authoring remains non-executable.",
)
replace_once("spec/bridge/kdsl-cp-packet-bridge.md", "## 4. Mapping: CP to Full KDSL / future Packet", "## 4. Mapping: CP to Full KDSL / Packet authoring")
replace_once(
    "spec/bridge/kdsl-cp-packet-bridge.md",
    "OUT/R1C mappingはfuture Packet設計入力であり実行許可ではない",
    "OUT/R1C mappingはPacket authoring fieldであり実行許可ではない",
)
replace_once(
    "spec/bridge/kdsl-cp-packet-bridge.md",
    "Packet-Summary may summarize a future canonical Packet to KDSL-CP for human-facing or Project file use.",
    "Packet-Summary may summarize an adopted non-executable Packet authoring record to KDSL-CP for human-facing or Project file use.",
)

# Remove this temporary carrier before the apply job commits.
Path(".github/scripts/apply_packet_ownership.py").unlink()
