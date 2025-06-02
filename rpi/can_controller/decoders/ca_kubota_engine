import struct
from typing import Dict
import j1939

# import logging


# logging.getLogger("j1939").setLevel(logging.DEBUG)
# logging.getLogger("can").setLevel(logging.DEBUG)

# Type alias for cyclic message functions
# Each tuple contains (callback_function, interval_ms)
# Type for the cyclic messages returned by the class.
## For python 3.12:
type CYCLIC_MESSAGE_TYPE = tuple[function, int]


class Kubota_D902k_CA(j1939.ControllerApplication):
    """
    Controller Application for reading and writing to the Kubota D902k engine

    """

    def __init__(self, name, device_address_preferred=None) -> None:
        self.decoders = {
            61444: self.decode_61444,
            61443: self.decode_61443,
            65247: self.decode_65247,
            65262: self.decode_65262,
            65266: self.decode_65266,
            65271: self.decode_65271,
            65269: self.decode_65269,
            65257: self.decode_65257,
            65252: self.decode_65252,
        }
        self.vehicle_speed = j1939.ControllerApplication.FieldValue.NOT_AVAILABLE_8

        self.cyclic_message_functions: Dict[int, CYCLIC_MESSAGE_TYPE] = {
            65265: (self.timer_callback_65265, 100)
        }

        super().__init__(name, device_address_preferred)

    def decode(self, pgn, data):
        """Dispatch decoder based on PGN."""
        decoder = self.decoders.get(pgn)
        return decoder(data) if decoder else {"error": f"No decoder for PGN {pgn}"}

    def decode_61444(self, data):
        """EEC1 - Engine Speed, Torque, Starter Mode, etc."""
        engine_speed = struct.unpack_from("<H", data, 3)[0] * 0.125
        demand_torque = data[1] - 125
        actual_torque = data[2] - 125
        starter_mode = (
            data[6] & 0xF0
        ) >> 4  # TODO: Not convinced this is right. Needs to be checked
        tsc1_src_address = data[5]
        return {
            "PGN": 61444,
            "Engine Speed (RPM)": engine_speed,
            "Driver's Demand Torque (%)": demand_torque,
            "Actual Engine Torque (%)": actual_torque,
            "Starter Mode": starter_mode,
            "TSC1 Source Address": tsc1_src_address,
        }

    def decode_61443(self, data):
        """EEC2 - Pedal Position, Engine Load"""
        engine_load = data[2] * 1.0
        accel_pos = data[1] * 0.4
        return {
            "PGN": 61443,
            "Engine Load (%)": engine_load,
            "Accelerator Pedal Position (%)": accel_pos,
        }

    def decode_65247(self, data):
        """EEC3 - Desired Engine Speed"""
        desired_speed = struct.unpack_from("<H", data, 1)[0] * 0.125
        return {
            "PGN": 65247,
            "Desired Engine Speed (RPM)": desired_speed,
        }

    def decode_65262(self, data):
        """ET1 - Engine Coolant Temperature"""
        temp_c = data[0] - 40
        return {
            "PGN": 65262,
            "Engine Coolant Temp (°C)": temp_c,
        }

    def set_vehicle_speed_65265(self, km_hr: float):
        """Transmit vehicle speed"""
        self.vehicle_speed = int(km_hr / 250.996)
        priority = 6
        rate_ms = 100
        raise NotImplementedError
        # CCVS	18FEF1VA*	65265	2-3	2 bytes	84	Vehicle Speed		X	6	100	0 to 250.996 km/h, 1/256 km/h per bit, 0 offset

    def timer_callback_65265(self, cookie):
        """Callback for sending the vehicle speed message for the kubota to read

        This callback is registered at the ECU timer event mechanism to be
        executed every 100ms.

        :param cookie:
            A cookie registered at 'add_timer'. May be None.
        """
        # wait until we have our device_address
        if self.state != j1939.ControllerApplication.State.NORMAL:
            # returning true keeps the timer event active
            return True

        pgn = 65265  # pgn  for the vehicle speed.

        # Alternatively, this works:
        # pgn = j1939.ParameterGroupNumber(
        #     0, # data_page
        #  0xFE, # pdu_format
        # 65265, # pdu_specific
        # )

        self.send_message(6, pgn, self.vehicle_speed)

        # returning true keeps the timer event active
        return True

    def decode_65266(self, data):
        """LFE - Fuel Rate, Throttle Position"""

        # 2 bytes, position 1-2,  0 to 3212.75 L/h, 0.05 L/h per bit, 0 offset
        fuel_rate = (
            struct.unpack_from("<H", data, 0)[0] * 0.05
        )  # Check that this decodes 2 bytes

        # Starts position 7, 1 byte,  0 to 100%, 0.4 %/bit, 0 offset
        throttle = data[6] * 0.4
        return {
            "PGN": 65266,
            "Fuel Rate (L/h)": fuel_rate,
            "Throttle Position (%)": throttle,
        }

    def decode_65271(self, data):
        """VEP1 - Battery Potential"""
        # position 5-6, 2 bytes,  0 to 3212.75 V, 0.05 V/bit, 0 offset, rate 1000ms
        voltage = struct.unpack_from("<H", data, 4)[0] * 0.05
        return {
            "PGN": 65271,
            "Battery Voltage (V)": voltage,
        }

    def decode_65269(self, data):
        """AMB - Barometric Pressure"""
        #  0 to 125 kPa, 0.5 kPa/bit, 0 offset
        pressure = data[0] * 0.5
        return {
            "PGN": 65269,
            "Barometric Pressure (kPa)": pressure,
        }

    def decode_65257(self, data):
        """LFC - Total Fuel Used"""
        #  0 to 2105540607.5 L, 0.5 L/bit, 0 offset
        fuel_total = struct.unpack_from("<I", data, 4)[0] * 0.5
        return {
            "PGN": 65257,
            "Total Fuel Used (L)": fuel_total,
        }

    def decode_65252(self, data):
        """SHUTDN - Wait to Start Lamp, Shutdown Status"""
        wait_to_start = data[3] & 0x03
        shutdown = data[4] & 0x03
        return {
            "PGN": 65252,
            "Wait to Start Lamp": wait_to_start,
            "Shutdown Active": shutdown,
        }


# struct.unpack assumes little endian and uses <H for unsigned short, <I for unsigned int
