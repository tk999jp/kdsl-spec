import re

import kdsl_parser_v2

# Phase 7C bounded registration. The shared parser core is not modified in this
# first slice; P1L is registered only for P1/P1L checker processes.
kdsl_parser_v2.KNOWN_ENVELOPES.add('P1L')

import kdsl_p1_contract as _contract  # noqa: E402

_original_split_p1_segments = _contract.split_p1_segments


def _split_p1_segments_with_legacy_boundary(line):
    stripped = line.strip()
    if stripped.startswith('P1|') and '|SCHEMA=' not in stripped:
        if re.search(r'(?:^|\|)[A-Z][A-Z0-9]*:', stripped[3:]):
            raise ValueError('legacy operational P1 colon syntax is not kdsl-p1@0.1-draft')
    return _original_split_p1_segments(line)


_contract.split_p1_segments = _split_p1_segments_with_legacy_boundary

from kdsl_p1_contract import *  # noqa: F401,F403,E402
