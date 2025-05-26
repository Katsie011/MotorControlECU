import can
import struct

# Configure CAN interface
bus = can.interface.Bus(channel='can0', bustype='socketcan', bitrate=500000)

# Source Address of iso175 device (per manual)
ISO175_SA = 0xF4

# PGN base to CAN ID: 0x18FF00 | (PGN & 0xFF) << 8 | SA
def pgn_to_can_id(pgn, sa=ISO175_SA):
    return 0x18FF0000 | ((pgn & 0xFF) << 8) | sa

# Decode PGN 65281 – General Info
def decode_pgn_65281(data):
    r_iso_corr = struct.unpack_from('<H', data, 0)[0]
    r_iso_status = data[2]
    meas_count = data[3]
    alarms = data[4]
    device_state = data[5]

    print("\n[PGN 65281 - General Info]")
    print(f"  R_iso_corrected: {r_iso_corr} kΩ" if r_iso_corr != 0xFFFF else "  R_iso_corrected: SNV")
    print(f"  R_iso_status: 0x{r_iso_status:02X}")
    print(f"  Measurement Counter: {meas_count}")
    print(f"  Alarms Bitfield: 0x{alarms:02X}")
    print(f"  Device State: {device_state} ({['Init', 'Normal', 'SelfTest'][device_state] if device_state < 3 else 'Unknown'})")

# Decode PGN 65283 – Voltage Info
def decode_pgn_65283(data):
    hv_sys = struct.unpack_from('<H', data, 0)[0] * 0.05
    hv_neg = (struct.unpack_from('<H', data, 2)[0] - 32128) * 0.05
    hv_pos = (struct.unpack_from('<H', data, 4)[0] - 32128) * 0.05

    print("\n[PGN 65283 - Voltage Info]")
    print(f"  HV System Voltage: {hv_sys:.2f} V")
    print(f"  HV- to Earth: {hv_neg:.2f} V")
    print(f"  HV+ to Earth: {hv_pos:.2f} V")

print("Listening to CAN bus... Press Ctrl+C to stop.\n")

try:
    while True:
        msg = bus.recv()

        if msg is None or msg.is_extended_id is False:
            continue

        can_id = msg.arbitration_id
        data = msg.data
        pgn = (can_id >> 8) & 0xFFFF
        sa = can_id & 0xFF

        if sa != ISO175_SA:
            continue

        if pgn == 65281:
            decode_pgn_65281(data)
        elif pgn == 65283:
            decode_pgn_65283(data)

except KeyboardInterrupt:
    print("\nStopped.")

