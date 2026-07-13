from kdsl_packet import SCHEMA_ID, parse_top_level


def describe(scope):
    return SCHEMA_ID, parse_top_level(scope)
