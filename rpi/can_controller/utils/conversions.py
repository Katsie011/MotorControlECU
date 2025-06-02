# PGN (Parameter Group Number) to CAN ID conversion
# Format: 0x18FF0000 | ((PGN & 0xFF) << 8) | SA
# This follows the J1939 protocol format for extended CAN IDs
def pgn_to_can_id(pgn, sa="ISO175_SA"):
    return 0x18FF0000 | ((pgn & 0xFF) << 8) | sa
