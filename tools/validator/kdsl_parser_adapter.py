from kdsl_parser import (
    blocks_from_entries_legacy,
    emit_legacy,
    extract_gate_block_legacy,
    extract_multiline_legacy,
    extract_scope_lines,
    load_text,
    parse_list_field_legacy,
    parse_list_records_legacy,
    parse_nested_lists_legacy,
    parse_nested_scalars_legacy,
    parse_registry_legacy,
    parse_sequence_items_legacy,
    parse_top_level_legacy,
    unquote,
)


def install_r1c(namespace):
    namespace['load_text'] = load_text
    namespace['emit'] = emit_legacy
    namespace['extract_result_scope'] = lambda text: extract_scope_lines(text, 'KDSL_RESULT')
    namespace['parse_top_level'] = lambda scope: parse_top_level_legacy(
        scope,
        'KDSL_RESULT',
        combine_multiline_json=True,
    )


def install_packet(namespace):
    namespace['load_text'] = load_text
    namespace['emit'] = emit_legacy
    namespace['extract_packet_scope'] = lambda text: extract_scope_lines(text, 'PACKET_DRAFT')
    namespace['parse_top_level'] = lambda scope: parse_top_level_legacy(scope, 'PACKET_DRAFT')
    namespace['blocks_from_entries'] = blocks_from_entries_legacy
    namespace['unquote'] = unquote
    namespace['parse_nested_scalars'] = parse_nested_scalars_legacy
    namespace['parse_list_field'] = parse_list_field_legacy
    namespace['parse_sequence_items'] = parse_sequence_items_legacy


def install_normalization(namespace):
    namespace['load_text'] = load_text
    namespace['emit'] = emit_legacy
    namespace['extract_scope'] = lambda text: extract_scope_lines(text, 'NORMALIZATION_DRAFT')
    namespace['parse_top_level'] = lambda scope: parse_top_level_legacy(scope, 'NORMALIZATION_DRAFT')
    namespace['blocks_from_entries'] = blocks_from_entries_legacy
    namespace['unquote'] = unquote
    namespace['parse_nested_scalars'] = parse_nested_scalars_legacy
    namespace['parse_list_records'] = parse_list_records_legacy
    namespace['parse_nested_lists'] = parse_nested_lists_legacy
    namespace['extract_multiline'] = extract_multiline_legacy


def install_safety_gate(namespace):
    namespace['load_text'] = load_text
    namespace['emit'] = emit_legacy
    namespace['extract_gate_block'] = extract_gate_block_legacy
    namespace['parse_registry'] = parse_registry_legacy
