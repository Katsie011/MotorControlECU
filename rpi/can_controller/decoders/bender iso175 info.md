📊 J1939 Signal Table – iso175 Insulation Monitoring Device

| **PGN** | **CAN ID (SrcAddr=244)** | **Name**                   | **Byte(s)** | **Signal**                                 | **Unit / Description**                |
| ------- | ------------------------ | -------------------------- | ----------- | ------------------------------------------ | ------------------------------------- |
| 65281   | `0x18FF01F4`             | PGN\_Info\_General         | 0–1         | `R_iso_corrected` (neg. tolerance shifted) | kΩ (0–35000); 65535 = SNV             |
|         |                          |                            | 2           | `R_iso_status`                             | 0xFC–0xFE = startup state; 0xFF = SNV |
|         |                          |                            | 3           | `Isolation Measurement Counter`            | Incremented per new reading           |
|         |                          |                            | 4           | `Status: Warnings and Alarms`              | Bit field – see below                 |
|         |                          |                            | 5           | `Status: Device Activity`                  | 0 = Init, 1 = Normal, 2 = Self-test   |
| 65282   | `0x18FF02F4`             | PGN\_Info\_IsolationDetail | 0–1         | `R_iso_neg`                                | kΩ (0–50000)                          |
|         |                          |                            | 2–3         | `R_iso_pos`                                | kΩ (0–50000)                          |
|         |                          |                            | 4–5         | `R_iso_original`                           | kΩ (0–50000)                          |
|         |                          |                            | 6           | `Isolation Measurement Counter`            | Same as above                         |
|         |                          |                            | 7           | `Isolation Quality`                        | % (0–100), 255 = SNV                  |
| 65283   | `0x18FF03F4`             | PGN\_Info\_Voltage         | 0–1         | `HV System Voltage`                        | V = value × 0.05                      |
|         |                          |                            | 2–3         | `HV_neg to Earth`                          | V = (value − 32128) × 0.05            |
|         |                          |                            | 4–5         | `HV_pos to Earth`                          | V = (value − 32128) × 0.05            |
|         |                          |                            | 6           | `Voltage Measurement Counter`              | –                                     |
| 65284   | `0x18FF04F4`             | PGN\_Info\_IT-System       | 0–1         | `Capacity Measured Value`                  | μF = value × 0.1                      |
|         |                          |                            | 2           | `Capacity Measurement Counter`             | –                                     |
|         |                          |                            | 3–4         | `Unbalance Measured Value`                 | % (0–100), 255 = SNV                  |
|         |                          |                            | 5           | `Unbalance Measurement Counter`            | –                                     |
|         |                          |                            | 6–7         | `Voltage Frequency`                        | Hz = value × 0.1                      |
⚠️ Bitfield: Status: Warnings and Alarms (Byte 4 of PGN 65281)

Each bit represents a status flag:

Bit	Meaning
| **Bit** | **Meaning**                          |
| ------- | ------------------------------------ |
| 0       | Device error active                  |
| 1       | HV\_pos connection failure           |
| 2       | HV\_neg connection failure           |
| 3       | Earth connection failure             |
| 4       | Iso Alarm (value < error threshold)  |
| 5       | Iso Warning (value < warning thresh) |
| 6       | Iso Outdated (value too old)         |
| 7       | Unbalance Alarm                      |
| 8       | Undervoltage Alarm                   |
| 9       | Unsafe to Start                      |
| 10      | Earthlift open                       |

(*Byte 4 is technically 8 bits, but the document implies an extended field; you may see an additional byte or alternate PGN to deliver bits 8–10.)

🧩 Notes for Decoding

All PGNs are 8 bytes long.
Byte order is Intel (little-endian).
Values like voltage and resistance may use offsets and scaling factors, such as:
Voltage to earth uses offset 32128, scaled by 0.05.
Capacity scaled by 0.1 µF.
65535 (0xFFFF) or 255 (0xFF) generally means Signal Not Valid (SNV).