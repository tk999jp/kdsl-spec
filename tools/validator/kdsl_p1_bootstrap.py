import kdsl_parser_v2

# Phase 7C bounded registration. The shared parser core is not modified in this
# first slice; P1L is registered only for P1/P1L checker processes.
kdsl_parser_v2.KNOWN_ENVELOPES.add('P1L')

from kdsl_p1_contract import *  # noqa: F401,F403,E402
