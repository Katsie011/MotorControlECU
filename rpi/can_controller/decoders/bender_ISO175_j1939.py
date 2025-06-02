import can
import struct


class ISO175Decoder:
    """Decoder class for ISO175 device messages following J1939 protocol.

    📊 J1939 Signal Table - iso175 Insulation Monitoring Device

    | **PGN** | **CAN ID (SrcAddr=244)** | **Name**                   | **Byte(s)** | **Signal**                                 | **Unit / Description**                |
    | ------- | ------------------------ | -------------------------- | ----------- | ------------------------------------------ | ------------------------------------- |
    | 65281   | `0x18FF01F4`             | PGN_Info_General           | 0-1         | `R_iso_corrected` (neg. tolerance shifted) | kΩ (0-35000); 65535 = SNV             |
    |         |                          |                            | 2           | `R_iso_status`                             | 0xFC-0xFE = startup state; 0xFF = SNV |
    |         |                          |                            | 3           | `Isolation Measurement Counter`            | Incremented per new reading           |
    |         |                          |                            | 4           | `Status: Warnings and Alarms`              | Bit field - see below                 |
    |         |                          |                            | 5           | `Status: Device Activity`                  | 0 = Init, 1 = Normal, 2 = Self-test   |
    | 65282   | `0x18FF02F4`             | PGN_Info_IsolationDetail   | 0-1         | `R_iso_neg`                                | kΩ (0-50000)                          |
    |         |                          |                            | 2-3         | `R_iso_pos`                                | kΩ (0-50000)                          |
    |         |                          |                            | 4-5         | `R_iso_original`                           | kΩ (0-50000)                          |
    |         |                          |                            | 6           | `Isolation Measurement Counter`            | Same as above                         |
    |         |                          |                            | 7           | `Isolation Quality`                        | % (0-100), 255 = SNV                  |
    | 65283   | `0x18FF03F4`             | PGN_Info_Voltage           | 0-1         | `HV System Voltage`                        | V = value × 0.05                      |
    |         |                          |                            | 2-3         | `HV_neg to Earth`                          | V = (value - 32128) × 0.05            |
    |         |                          |                            | 4-5         | `HV_pos to Earth`                          | V = (value - 32128) × 0.05            |
    |         |                          |                            | 6           | `Voltage Measurement Counter`              | -                                     |
    | 65284   | `0x18FF04F4`             | PGN_Info_IT-System         | 0-1         | `Capacity Measured Value`                  | μF = value × 0.1                      |
    |         |                          |                            | 2           | `Capacity Measurement Counter`             | -                                     |
    |         |                          |                            | 3-4         | `Unbalance Measured Value`                 | % (0-100), 255 = SNV                  |
    |         |                          |                            | 5           | `Unbalance Measurement Counter`            | -                                     |
    |         |                          |                            | 6-7         | `Voltage Frequency`                        | Hz = value × 0.1                      |

    ⚠️ Bitfield: Status: Warnings and Alarms (Byte 4 of PGN 65281)

    Each bit represents a status flag:
    Bit	Meaning
    | **Bit** | **Meaning**                          |
    | ------- | ------------------------------------ |
    | 0       | Device error active                  |
    | 1       | HV_pos connection failure            |
    | 2       | HV_neg connection failure            |
    | 3       | Earth connection failure             |
    | 4       | Iso Alarm (value < error threshold)  |
    | 5       | Iso Warning (value < warning thresh) |
    | 6       | Iso Outdated (value too old)         |
    | 7       | Unbalance Alarm                      |
    | 8       | Undervoltage Alarm                   |
    | 9       | Unsafe to Start                      |
    | 10      | Earthlift open                       |

    (*Byte 4 is technically 8 bits, but the document implies an extended field; you may see an additional byte or alternate PGN to deliver bits 8-10.)

    🧩 Notes for Decoding

    All PGNs are 8 bytes long.
    Byte order is Intel (little-endian).
    Values like voltage and resistance may use offsets and scaling factors, such as:
    Voltage to earth uses offset 32128, scaled by 0.05.
    Capacity scaled by 0.1 µF.
    65535 (0xFFFF) or 255 (0xFF) generally means Signal Not Valid (SNV).

    """

    def __init__(self):
        # Source Address of iso175 device (per manual)
        # This is a fixed address for the Bender ISO175 device
        self.source_address = 0xF4
        self.decoders = {
            65281: self.decode_pgn_65281,
            65282: self.decode_pgn_65282,
            65283: self.decode_pgn_65283,
            65284: self.decode_pgn_65284,
        }

    def decode(self, pgn: int, data: bytes) -> bool:
        """Decode a message based on its PGN.

        Args:
            pgn: Parameter Group Number as string
            data: Raw message data

        Returns:
            bool: True if message was decoded successfully, False otherwise
        """
        decoder = self.decoders.get(pgn)
        if decoder is not None:
            return decoder(data)
        print(f"PGN: {pgn} not found!")
        return False

    def decode_pgn_65281(self, data: bytes) -> bool:
        """Decode PGN 65281 - General Info containing device status and measurements."""
        try:
            # Unpack 16-bit values using little-endian format (<H)
            r_iso_corr = struct.unpack_from("<H", data[:2])[
                0
            ]  # Corrected isolation resistance
            r_iso_status = data[2]  # Status byte for isolation measurement
            meas_count = data[3]  # Counter for measurements
            alarms = struct.unpack_from("<H", data[4:6])[
                0
            ]  # Bitfield containing alarm states
            device_state = data[6]  # Current state of the device

            r_iso_status_meaning = {
                0xFC: "estimated isolation value during startup",
                0xFD: "first measured isolation value during startup",
                0xFE: "isolation value in normal operation",
                0xFF: "SNV",
            }.get(r_iso_status, "unknown status")

            # Store decoded values as instance variables
            self.general_info = {
                "r_iso_corrected": r_iso_corr if r_iso_corr != 0xFFFF else "SNV",
                "r_iso_status": r_iso_status,
                "r_iso_status_meaning": r_iso_status_meaning,
                "measurement_counter": meas_count,
                "alarms": alarms,
                "device_state": device_state,
                "device_state_meaning": (
                    ["Init", "Normal", "SelfTest"][device_state]
                    if device_state < 3
                    else "Unknown"
                ),
            }
            return True
        except Exception as e:
            print(f"Error decoding PGN 65281: {e}")
            return False

    def decode_pgn_65282(self, data: bytes) -> bool:
        """Decode PGN 65282 - Isolation Detail containing detailed isolation measurements."""
        try:
            # Extract isolation resistance values (in kΩ)
            r_kΩ_negative = struct.unpack_from("<H", data[:2])[0]
            r_kΩ_positive = struct.unpack_from("<H", data[2:4])[0]
            r_kΩ_original = struct.unpack_from("<H", data[4:6])[0]
            iso_measurement_count = data[6]
            iso_measurement_quality = data[7]

            # Store decoded values
            self.isolation_detail = {
                "isolation_negative": r_kΩ_negative,
                "isolation_positive": r_kΩ_positive,
                "isolation_original": r_kΩ_original,
                "measurement_count": iso_measurement_count,
                "measurement_quality": iso_measurement_quality,
            }
            return True
        except Exception as e:
            print(f"Error decoding PGN 65282: {e}")
            return False

    def decode_pgn_65283(self, data: bytes) -> bool:
        """Decode PGN 65283 - Voltage Info containing high voltage system measurements."""
        try:
            # Convert raw values to voltage (V)
            hv_sys = struct.unpack_from("<H", data, 0)[0] * 0.05
            hv_neg = (struct.unpack_from("<H", data, 2)[0] - 32128) * 0.05
            hv_pos = (struct.unpack_from("<H", data, 4)[0] - 32128) * 0.05

            # Store decoded values
            self.voltage_info = {
                "hv_system_voltage": hv_sys,
                "hv_negative_to_earth": hv_neg,
                "hv_positive_to_earth": hv_pos,
            }
            return True
        except Exception as e:
            print(f"Error decoding PGN 65283: {e}")
            return False

    def decode_pgn_65284(self, data: bytes) -> bool:
        """Decode PGN 65284 - IT-System Info containing system capacitance measurements."""
        try:
            # Extract measurements
            capacity_measured = struct.unpack_from("<H", data[:2])[0]  # in μF
            if capacity_measured == 65535:
                capacity_measured = "SNV"

            capacity_measure_count = data[2]
            unbalance_measure_value = data[3]
            unbalance_measurement = data[4]
            voltage_frequency = struct.unpack_from("<H", data[5:7])[0]  # in Hz

            # Store decoded values
            self.it_system_info = {
                "capacity_measured": capacity_measured,
                "capacity_measure_count": capacity_measure_count,
                "unbalance_measure_value": unbalance_measure_value,
                "unbalance_measurement": unbalance_measurement,
                "voltage_frequency": voltage_frequency,
            }
            return True
        except Exception as e:
            print(f"Error decoding PGN 65284: {e}")
            return False


if __name__ == "__main__":
    # Configure CAN interface with 500 kbps bitrate
    bus = can.interface.Bus(channel="can0", bustype="socketcan", bitrate=500000)
    iso175 = ISO175Decoder()
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
            if iso175.source_address != sa:
                continue

            # Route message to appropriate decoder based on PGN
            iso175.decode(pgn=pgn, data=data)

    except KeyboardInterrupt:
        print("\nStopped.")
