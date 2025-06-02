import can
import csv
import struct
import os
import logging
from datetime import datetime
from collections import defaultdict
from tkinter import Tk, filedialog

# Constants
PGN_INFO_BASE = 0x18FF0000
CSV_PATH = "iso175_pgn_map.csv"
DEFAULT_CAN_CHANNEL = "can0"
DEFAULT_CAN_BUSTYPE = "socketcan"

# Generate a unique log file with timestamp
log_filename = f"can_decoder_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(
    filename=log_filename,
    filemode='a',
    format='%(asctime)s [%(levelname)s] %(message)s',
    level=logging.INFO
)

# Prompt for CSV file if not found
def prompt_for_csv():
    root = Tk()
    root.withdraw()
    root.update()
    file_path = filedialog.askopenfilename(
        title="Select the PGN decoder CSV file",
        filetypes=[("CSV files", "*.csv")]
    )
    root.destroy()
    return file_path

# Load PGN decoder from CSV
def load_decoder(csv_path):
    if not os.path.exists(csv_path):
        print(f"Decoder CSV not found at default location: {csv_path}")
        logging.warning(f"Decoder CSV not found at default location: {csv_path}")
        csv_path = prompt_for_csv()
        if not csv_path:
            raise FileNotFoundError("No decoder CSV file selected.")

    decoder = defaultdict(list)
    with open(csv_path, newline='') as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                pgn = int(row['PGN'].strip())
                signal = {
                    'name': row['Signal Name'],
                    'start': int(row['Byte Start']),
                    'length': int(row['Length']),
                    'endian': row['Endian'],
                    'scale': float(row['Scale']),
                    'offset': float(row['Offset']),
                    'unit': row['Unit'],
                    'enum': row['Enum'],
                    'description': row['Description'],
                    'pgn_description': row['PGN Description']
                }
                decoder[pgn].append(signal)
            except (ValueError, KeyError) as e:
                logging.warning(f"Skipping invalid row in CSV: {row} ({e})")
    return decoder

# Decode signal value from raw CAN data
def decode_signal(data, signal):
    start = signal['start']
    end = start + signal['length']
    if end > len(data):
        return "Out of range"

    segment = data[start:end]
    try:
        if signal['length'] == 1:
            raw = segment[0]
        elif signal['length'] == 2:
            raw = struct.unpack('<H' if signal['endian'] == 'little' else '>H', segment)[0]
        elif signal['length'] == 3:
            raw = int.from_bytes(segment, byteorder=signal['endian'], signed=False)
        elif signal['length'] == 4:
            raw = struct.unpack('<I' if signal['endian'] == 'little' else '>I', segment)[0]
        else:
            return "Unsupported length"

        if raw in (0xFF, 0xFFFF, 0xFFFFFF):
            return "SNV"

        value = raw * signal['scale'] + signal['offset']
        return f"{value:.2f} {signal['unit']}" if signal['unit'] else f"{value:.2f}"
    except Exception as e:
        return f"Decode error: {e}"

# Extract PGN from 29-bit CAN ID
def get_pgn(can_id):
    pf = (can_id >> 16) & 0xFF
    ps = (can_id >> 8) & 0xFF
    if pf < 240:
        return pf << 8
    return (pf << 8) | ps

# Main CAN listener and decoder
def main():
    try:
        decoder_map = load_decoder(CSV_PATH)
    except FileNotFoundError as e:
        logging.error(e)
        print(e)
        return

    try:
        bus = can.interface.Bus(channel=DEFAULT_CAN_CHANNEL, bustype=DEFAULT_CAN_BUSTYPE)
    except Exception as e:
        logging.error(f"Failed to initialize CAN interface: {e}")
        print(f"Failed to initialize CAN interface: {e}")
        return

    print("Listening for PGN_Info messages... Press Ctrl+C to stop.")
    logging.info("Started CAN decoder listener")

    try:
        while True:
            msg = bus.recv(timeout=1)
            if not msg or not msg.is_extended_id:
                continue

            pgn = get_pgn(msg.arbitration_id)
            if pgn not in decoder_map:
                continue

            pgn_desc = decoder_map[pgn][0]['pgn_description']
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            header = f"[{timestamp}] PGN {pgn} ({pgn_desc})"
            print(f"\n{header}")
            logging.info(header)

            for signal in decoder_map[pgn]:
                decoded = decode_signal(msg.data, signal)
                output = f"  {signal['name']}: {decoded}  -- {signal['description']}"
                print(output)
                logging.info(output)

    except KeyboardInterrupt:
        print("\nStopped.")
        logging.info("Decoder stopped by user")
    except Exception as e:
        logging.exception(f"Runtime error: {e}")
        print(f"Runtime error: {e}")

if __name__ == "__main__":
    main()
