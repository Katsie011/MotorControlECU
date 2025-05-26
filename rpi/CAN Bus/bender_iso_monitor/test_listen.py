import can
import struct

# Source Address of iso175 device (per manual)
# This is a fixed address for the Bender ISO175 device
ISO175_SA = 0xF4


# PGN (Parameter Group Number) to CAN ID conversion
# Format: 0x18FF0000 | ((PGN & 0xFF) << 8) | SA
# This follows the J1939 protocol format for extended CAN IDs
def pgn_to_can_id(pgn, sa=ISO175_SA):
    return 0x18FF0000 | ((pgn & 0xFF) << 8) | sa


# Decode PGN 65281 – General Info
# This PGN contains general device status and measurements
def decode_pgn_65281(data):
    # TODO: Add input validation for data length
    # TODO: Add typing
    print("Received a message for PGN 65281 - PGN_Info_General")

    # Unpack 16-bit values using little-endian format (<H)
    r_iso_corr = struct.unpack_from("<H", data, 0)[0]  # Corrected isolation resistance
    r_iso_status = data[2]  # Status byte for isolation measurement
    meas_count = data[3]  # Counter for measurements
    alarms = data[4]  # Bitfield containing alarm states
    device_state = data[5]  # Current state of the device

    print("\n[PGN 65281 - General Info]")
    """
r_iso_status:
    0xFC: estimated iso-lation value during startup
    0xFD: first measured isolation value during startup
    0xFE: isolation value in normal operation
    0xFF: SNV
"""
    print(
        f"  R_iso_corrected: {r_iso_corr} kΩ"
        if r_iso_corr != 0xFFFF
        else "  R_iso_corrected: SNV"
    )
    print(f"  R_iso_status: 0x{r_iso_status:02X}")
    print(f"  Measurement Counter: {meas_count}")
    print(f"  Alarms Bitfield: 0x{alarms:02X}")

    # Device states: 0=Init, 1=Normal, 2=SelfTest
    print(
        f"  Device State: {device_state} ({['Init', 'Normal', 'SelfTest'][device_state] if device_state < 3 else 'Unknown'})"
    )


# Decode PGN 65282 – Isolation Detail
# Contains detailed isolation resistance measurements
def decode_pgn_65282(data):
    # TODO: Add input validation for data length
    print("Received a message for PGN 65282 - PGN_Info_IsolationDetail")

    # Extract isolation resistance values (in kΩ)
    r_kΩ_negative = struct.unpack_from("<H", data[:2])[0]
    r_kΩ_positive = struct.unpack_from("<H", data[2:4])[0]
    r_kΩ_original = struct.unpack_from("<H", data[4:6])[0]
    iso_measurement_count = data[6]
    iso_measurement_quality = data[7]

    print("\n[PGN 65282 - Isolation Detail]")
    print(f"    Isolation negative: {r_kΩ_negative} kΩ")
    print(f"    Isolation positive: {r_kΩ_positive} kΩ")
    print(f"    Isolation original: {r_kΩ_original} kΩ")
    print(f"    Isolation measurement count: {iso_measurement_count}")
    print(f"    Isolation measurement quality: {iso_measurement_quality}")


# Decode PGN 65283 – Voltage Info
# Contains high voltage system measurements
def decode_pgn_65283(data):
    # TODO: Add input validation for data length
    print("Received a message for PGN 65283 - PGN_Info_Voltage")

    # Convert raw values to voltage (V)
    # Scale factor: 0.05 V per count
    # Offset: 32128 for negative and positive measurements
    hv_sys = struct.unpack_from("<H", data, 0)[0] * 0.05
    hv_neg = (struct.unpack_from("<H", data, 2)[0] - 32128) * 0.05
    hv_pos = (struct.unpack_from("<H", data, 4)[0] - 32128) * 0.05

    print("\n[PGN 65283 - Voltage Info]")
    print(f"    HV System Voltage: {hv_sys:.2f} V")
    print(f"    HV- to Earth: {hv_neg:.2f} V")
    print(f"    HV+ to Earth: {hv_pos:.2f} V")


# Decode PGN 65284 – IT-System Info
# Contains system capacitance and unbalance measurements
def decode_pgn_65284(data):
    # TODO: Add input validation for data length
    print("Received a message for PGN 65284 - PGN_Info_IT-System")

    # Extract measurements
    capacity_measured = struct.unpack_from("<H", data[:2])[0]  # in μF
    if capacity_measured == 65535:
        capacity_measured = "SNV"

    capacity_measure_count = data[2]
    unbalance_measure_value = data[3]
    unbalance_measurement = data[4]
    voltage_frequency = struct.unpack_from("<H", data[5:7])[0]  # in Hz

    print("\n[PGN 65284 - IT-System Info]")
    """
    capacity_measured
        1…200: capacity value [0.1μF]
        65535: SNV 
    """
    print(f"    Capacity measured: {capacity_measured} μF")
    print(f"    Capacity measurement count: {capacity_measure_count}")
    print(f"    Unbalance measure value: {unbalance_measure_value}")
    print(f"    Unbalance measurement: {unbalance_measurement}")
    print(f"    Voltage frequency: {voltage_frequency} Hz")


if __name__ == "__main__":
    # Configure CAN interface with 500 kbps bitrate
    bus = can.interface.Bus(channel="can0", bustype="socketcan", bitrate=500000)

    print("Listening to CAN bus... Press Ctrl+C to stop.\n")

    try:
        while True:
            msg = bus.recv()

            # Skip non-extended ID messages
            if msg is None or msg.is_extended_id is False:
                continue

            # Extract message components
            can_id = msg.arbitration_id
            data = msg.data
            pgn = (can_id >> 8) & 0xFFFF  # Extract PGN from CAN ID
            sa = can_id & 0xFF  # Extract Source Address

            # Only process messages from our device
            if sa != ISO175_SA:
                continue

            # Route message to appropriate decoder based on PGN
            if pgn == 65281:
                decode_pgn_65281(data)
            elif pgn == 65282:
                decode_pgn_65282(data)
            elif pgn == 65283:
                decode_pgn_65283(data)
            elif pgn == 65284:
                decode_pgn_65284(data)

    except KeyboardInterrupt:
        print("\nStopped.")
