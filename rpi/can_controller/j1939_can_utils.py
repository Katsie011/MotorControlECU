import can
# See https://gist.github.com/agmangas/4f8ef5febcb7564274f77c49ccbc0ffb

def can_id_to_pgn(can_id):
    """Takes a 29-bit CAN ID and returns the PGN.

    We only support the SAE J1939 Page 0 data page (EDP == 0 and DP == 0).
    The other data pages (NMEA2000, SAE J1939 Reserved and ISO 15765-3) will raise a ValueError.

    :type can_id: int | can.message.Message
    :rtype: int
    :raises ValueError: If the EDP or DP bits are not 0
    """

    can_id = can_id.arbitration_id if isinstance(can_id, can.Message) else can_id

    reserved = can_id >> 25 & 0x1
    data_page = can_id >> 24 & 0x1

    if reserved != 0:
        raise ValueError("Reserved (Extended Data Page) bit for CAN ID {} is != 0".format(hex(can_id)))

    if data_page != 0:
        raise ValueError("Data Page bit for CAN ID {} is != 0".format(hex(can_id)))

    pdu_format = can_id >> 16 & 0xFF
    pdu_specific = can_id >> 8 & 0xFF

    if is_specific_pgn_can_id(can_id):
        return pdu_format << 8
    else:
        return (pdu_format << 8) | pdu_specific


def is_specific_pgn_can_id(can_id):
    """Returns True if the PGN extracted from the given CAN ID is a Specific PGN.

    :type can_id: int
    :rtype: bool
    """

    pdu_format = can_id >> 16 & 0xFF
    return pdu_format < 0xF0
