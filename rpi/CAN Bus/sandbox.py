# pip install can-j1939
import logging
import time
from typing import Literal
import can
import j1939


logging.getLogger("j1939").setLevel(logging.DEBUG)
logging.getLogger("can").setLevel(logging.DEBUG)

# compose the name descriptor for the new ca
name = j1939.Name(
    arbitrary_address_capable=0,
    industry_group=j1939.Name.IndustryGroup.Industrial,
    vehicle_system_instance=1,
    vehicle_system=1,
    function=1,
    function_instance=1,
    ecu_instance=1,
    manufacturer_code=666,
    identity_number=1234567,
)

# create the ControllerApplications
ca = j1939.ControllerApplication(name, 128)


def to_little_endian(data: int):
    """Convert an integer to a little endian byte array.
    Args:
        data (int): The integer to convert
    Returns:
        bytearray: Little endian representation of the integer
    """
    # Convert to bytes in little endian format
    return bytearray(data.to_bytes((data.bit_length() + 7) // 8, byteorder="little"))


def hex_to_decimal(
    hex_byte: int, byteorder: Literal["little", "big"] = "little", signed: bool = False
) -> int:
    """Convert a hex byte to decimal using Intel byte ordering (little endian).

    Args:
        hex_byte (int): The hex byte to convert

    Returns:
        int: The decimal value
    """
    # Convert to bytes in little endian format and unpack as unsigned char
    return int.from_bytes(bytes([hex_byte]), byteorder=byteorder, signed=signed)
    # return eval("0b" + '{0:08b}'.format(hex_byte)[::-1][:-2])


def ca_receive(priority, pgn, source, timestamp, data):
    """Feed incoming message to this CA.
    (OVERLOADED function)
    :param int priority:
        Priority of the message
    :param int pgn:
        Parameter Group Number of the message
    :param intsa:
        Source Address of the message
    :param int timestamp:
        Timestamp of the message
    :param bytearray data:
        Data of the PDU
    """
    # TODO: This needs to log to file
    print("PGN {} length {}".format(pgn, len(data)))


def ca_timer_callback1(cookie):
    """Callback for sending messages

    This callback is registered at the ECU timer event mechanism to be
    executed every 500ms.

    :param cookie:
        A cookie registered at 'add_timer'. May be None.
    """
    # wait until we have our device_address
    if ca.state != j1939.ControllerApplication.State.NORMAL:
        # returning true keeps the timer event active
        return True

    # create data with 8 bytes
    data = [j1939.ControllerApplication.FieldValue.NOT_AVAILABLE_8] * 8

    # sending normal broadcast message
    ca.send_pgn(0, 0xFD, 0xED, 6, data)

    # sending normal peer-to-peer message, destintion address is 0x04
    ca.send_pgn(0, 0xE0, 0x04, 6, data)

    # returning true keeps the timer event active
    return True


# def ca_timer_callback2(cookie):
#     """Callback for sending messages

#     This callback is registered at the ECU timer event mechanism to be
#     executed every 500ms.

#     :param cookie:
#         A cookie registered at 'add_timer'. May be None.
#     """
#     # wait until we have our device_address
#     if ca.state != j1939.ControllerApplication.State.NORMAL:
#         # returning true keeps the timer event active
#         return True

#     # create data with 100 bytes
#     data = [j1939.ControllerApplication.FieldValue.NOT_AVAILABLE_8] * 100

#     # sending multipacket message with TP-BAM
#     ca.send_pgn(0, 0xFE, 0xF6, 6, data)

#     # sending multipacket message with TP-CMDT, destination address is 0x05
#     ca.send_pgn(0, 0xD0, 0x05, 6, data)

#     # returning true keeps the timer event active
#     return True


def ca_timer_callback2(cookie):
    """Callback for sending messages

    This callback is registered at the ECU timer event mechanism to be
    executed every 2s.

    :param cookie:
        A cookie registered at 'add_timer'. May be None.
    """
    # wait until we have our device_address
    if ca.state != j1939.ControllerApplication.State.NORMAL:
        # returning true keeps the timer event active
        return True

    pgn_iso175_request = 0xEFF4
    data = bytearray(0) + to_little_endian(0x0A)
    print(
        f"Sending periodic message with data: \n\tpriority=0\n\tparameter_group_number={pgn_iso175_request}\n\tdata={data}"
    )
    ca.send_message(priority=0, parameter_group_number=pgn_iso175_request, data=data)

    # returning true keeps the timer event active
    return True


def main():
    print("Initializing")

    # create the ElectronicControlUnit (one ECU can hold multiple ControllerApplications)
    ecu = j1939.ElectronicControlUnit()

    # Connect to the CAN bus
    # Arguments are passed to python-can's can.interface.Bus() constructor
    # (see https://python-can.readthedocs.io/en/stable/bus.html).
    ecu.connect(bustype="socketcan", channel="can0")
    # ecu.connect(bustype='kvaser', channel=0, bitrate=250000)
    # ecu.connect(bustype='pcan', channel='PCAN_USBBUS1', bitrate=250000)
    # ecu.connect(bustype='ixxat', channel=0, bitrate=250000)
    # ecu.connect(bustype='vector', app_name='CANalyzer', channel=0, bitrate=250000)
    # ecu.connect(bustype='nican', channel='CAN0', bitrate=250000)
    # ecu.connect('testchannel_1', bustype='virtual')

    # add CA to the ECU
    ecu.add_ca(controller_application=ca)
    ca.subscribe(ca_receive)
    # callback every 2s
    ca.add_timer(2, ca_timer_callback1)
    # callback every 5s
    ca.add_timer(5, ca_timer_callback2)
    # by starting the CA it starts the address claiming procedure on the bus
    ca.start()

    time.sleep(120)

    print("Deinitializing")
    ca.stop()
    ecu.disconnect()


if __name__ == "__main__":
    main()
