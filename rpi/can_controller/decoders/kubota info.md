| Acronym | ID | PGN (Decimal) | Start Position | Length | SPN | Message | Transmit | Receive | Priority | Rate [msec] | Notes |
|---------|----|---------------|----------------|--------|-----|---------|----------|---------|----------|-------------|-------|
| EEC1 | 0CF00400 | 61444 | 4-5 | 2 bytes | 190 | Engine Speed | X | | 3 | 20 | 0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset |
| | | | 2 | 1 byte | 512 | Driver's Demand Engine Percent - Torque | X | | 3 | 20 | -125% to 125%, 1 %/bit, -125% offset |
| | | | 3 | 1 byte | 513 | Actual Engine - Percent Torque | X | | 3 | 20 | -125% to 125%, 1 %/bit, -125% offset |
| | | | 7.1 | 4 bits | 1675 | Engine Starter Mode | X | | 3 | 20 | 0000: start not requested<br>0010: starter active (gear engaged)<br>0100: starter inhibited due to engine already running<br>1100: starter inhibited<br>Other status are not supported |
| | | | 6 | 1 byte | 1483 | Source Address of TSC1 | X | | 3 | 20 | 1 source address/bit, 0 offset |
| EEC2 | 0CF00300 | 61443 | 3 | 1 byte | 92 | Engine Percent Load At Current Speed | X | | 3 | 50 | 0 to 250%, 1 %/bit, 0 offset |
| | | | 2 | 1 byte | 91 | Accelerator Position (%) | X | | 3 | 50 | 0 to 100%, 0.4 %/bit, 0 offset |
| EEC3 | 18FEDF00 | 65247 | 2-3 | 2 bytes | 515 | Desired Engine Speed | X | | 6 | 250 | 0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset |
| EEC4 | 18FEBE00 | 65214 | 3-4 | 2 bytes | 189 | Engine Rated Speed | X | | 6 | On Request | 0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset |
| EC1 | 18FEE300 | 65251 | 20-21 | 2 bytes | 544 | Reference Engine Torque | X | | 6 | On Request | 0 to 64255 Nm, 1 Nm/bit, 0 offset |
| | | | 1-2 | 2 bytes | 188 | Engine Speed (Low Idle Point) | X | | 6 | On Request | 0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset |
| | | | 16-17 | 2 bytes | 532 | Engine Speed (High Idle Point) | X | | 6 | On Request | 0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset |
| | | | 25 | 1 byte | 535 | Requested Speed Lower Limit | X | | 6 | On Request | 0 to 2500 rpm, 10 rpm/bit, 0 offset |
| | | | 26 | 1 byte | 536 | Requested Speed Upper Limit | X | | 6 | On Request | 0 to 2500 rpm, 10 rpm/bit, 0 offset |
| | | | 27 | 1 byte | 537 | Requested Torque Lower Limit | X | | 6 | On Request | -125% to 125%, 1 %/bit, -125% offset |
| | | | 28 | 1 byte | 538 | Requested Torque Upper Limit | X | | 6 | On Request | -125% to 125%, 1 %/bit, -125% offset |
| ET1 | 18FEEE00 | 65262 | 1 | 1 byte | 110 | Engine Coolant Temperature | X | | 6 | 1000 | -40 to 210 deg. C, 1 deg. C/bit, -40 deg. C offset |
| CCVS | 18FEF1VA* | 65265 | 2-3 | 2 bytes | 84 | Vehicle Speed | | X | 6 | 100 | 0 to 250.996 km/h, 1/256 km/h per bit, 0 offset |
| LFE | 18FEF200 | 65266 | 1-2 | 2 bytes | 183 | Fuel Rate | X | | 6 | 100 | 0 to 3212.75 L/h, 0.05 L/h per bit, 0 offset |
| | | | 7 | 1 byte | 51 | Throttle Position | X | | 6 | 100 | 0 to 100%, 0.4 %/bit, 0 offset |
| VEP1 | 18FEF700 | 65271 | 5-6 | 2 bytes | 168 | Battery Potential | X | | 6 | 1000 | 0 to 3212.75 V, 0.05 V/bit, 0 offset |
| AMB | 18FEF500 | 65269 | 1 | 1 byte | 108 | Barometric Pressure | X | | 6 | 1000 | 0 to 125 kPa, 0.5 kPa/bit, 0 offset |
| LFC | 18FEE900 | 65257 | 5-8 | 4 bytes | 250 | Total Fuel Used | X | | 6 | 1000 | 0 to 2105540607.5 L, 0.5 L/bit, 0 offset |
| HOURS | 18FEE500 | 65253 | 1-4 | 4 bytes | 247 | Total Engine Hours | X | | 6 | On Request | 0 to 210554060.75 h, 0.05 h/bit, 0 offset |
| S2 | 1CFE8E00 | 65166 | 2-3 | 2 bytes | 1350 | Time at Last Service | X | | 7 | On Request | 0 to 64255 h, 1 h/bit, 0 h offset |
| ETC5 | 1CFEC3VA* | 65219 | 2.3 | 2 bits | 604 | Transmission Neutral Switch | | X | 7 | 100 | 00: Off, 01: On, 10: Error, 11: Not available |
| ETC5 | 1CFEC300 | 65219 | 2.3 | 2 bits | 604 | Transmission Neutral Switch | X | | 7 | 100 | only used by Hard switch input<br>00: Off, 01: On, 10: Error, 11: Not available |
| EFL/P1 | 18FEEF00 | 65263 | 4 | 1 byte | 100 | Engine Oil Pressure | X | | 6 | 500 | 0 to 1000 kPa, 4 kPa/bit, 0 offset<br>Oil switch input is converted to fixed value: Off -> 200 kPa, On -> 0 kPa |
| CI | 18FEEB00 | 65259 | 2-21 | 20 bytes | 587 | Model | X | | 6 | On Request | ex) V3800DICR |
| | | | 23-39 | 17 bytes | 588 | Serial Number | X | | 6 | On Request | ex) 5A1234 |
| SOFT | 18FEDA00 | 65242 | 1 | 1 byte | 965 | Number of Software Identification Field | X | | 6 | On Request | 1 step/bit, 0 offset, 0 to 250 steps |
| | | | 2-26 | 25 bytes | 234 | Software Identification | X | | 6 | On Request | Kubota Software ID ex) 1H00012345 (25 char) |
| SHUTDN | 18FEE400 | 65252 | 4.1 | 2 bits | 1081 | Wait to Start Lamp | X | | 6 | 1000 | 00: Off, 01: On, 10: Error, 11: Not available |
| | | | 5.1 | 2 bits | 1110 | Engine Protection System has Shutdown Engine | X | | 6 | 1000 | 00: No, 01: Yes, 10: Error, 11: Not available |
Acronym	ID	PGN (Decimal)	Start Position	Length	SPN	Message	Transmit	Receive	Priority	 Rate [msec]	Notes
EEC1	0CF00400	61444	4-5	2 bytes	190	 Engine Speed	X		3	20	 0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset
			2	1 byte	512	 Driver's Demand Engine Percent - Torque	X		3	20	 -125% to 125%, 1 %/bit, -125% offset
			3	1 byte	513	 Actual Engine - Percent Torque	X		3	20	 -125% to 125%, 1 %/bit, -125% offset
			7.1	4 bits	1675	 Engine Starter Mode	X		3	20	" 0000: start not requested
 0010: starter active (gear engaged)
 0100: starter inhibited due to engine already running
 1100: starter inhibited
 Other status are not supported"
			6	1 byte	1483	 Source Address of TSC1	X		3	20	 1 source address/bit, 0 offset
EEC2	0CF00300	61443	3	1 byte	92	 Engine Percent Load At Current Speed	X		3	50	 0 to 250%, 1 %/bit, 0 offset
			2	1 byte	91	 Accelerator Position (%)	X		3	50	 0 to 100%, 0.4 %/bit, 0 offset
EEC3	18FEDF00	65247	2-3	2 bytes	515	 Desired Engine Speed	X		6	250	 0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset
EEC4	18FEBE00	65214	3-4	2 bytes	189	 Engine Rated Speed	X		6	On Request	 0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset
EC1	18FEE300	65251	20-21	2 bytes	544	 Reference Engine Torque	X		6	On Request	 0 to 64255 Nm, 1 Nm/bit, 0 offset
			1-2	2 bytes	188	 Engine Speed (Low Idle Point)	X		6	On Request	 0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset
			16-17	2 bytes	532	 Engine Speed (High Idle Point)	X		6	On Request	 0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset
			25	1 byte	535	 Requested Speed Lower Limit	X		6	On Request	 0 to 2500 rpm, 10 rpm/bit, 0 offset
			26	1 byte	536	 Requested Speed Upper Limit	X		6	On Request	 0 to 2500 rpm, 10 rpm/bit, 0 offset
			27	1 byte	537	 Requested Torque Lower Limit	X		6	On Request	 -125% to 125%, 1 %/bit, -125% offset
			28	1 byte	538	 Requested Torque Upper Limit	X		6	On Request	 -125% to 125%, 1 %/bit, -125% offset
ET1	18FEEE00	65262	1	1 byte	110	 Engine Coolant Temperature	X		6	1000	 -40 to 210 deg. C, 1 deg. C/bit, -40 deg. C offset
CCVS	18FEF1VA*	65265	2-3	2 bytes	84	 Vehicle Speed		X	6	100	 0 to 250.996 km/h, 1/256 km/h per bit, 0 offset
LFE	18FEF200	65266	1-2	2 bytes	183	 Fuel Rate	X		6	100	 0 to 3212.75 L/h, 0.05 L/h per bit, 0 offset
			7	1 byte	51	 Throttle Position	X		6	100	 0 to 100%, 0.4 %/bit, 0 offset
VEP1	18FEF700	65271	5-6	2 bytes	168	 Battery Potential	X		6	1000	 0 to 3212.75 V, 0.05 V/bit, 0 offset
AMB	18FEF500	65269	1	1 byte	108	 Barometric Pressure	X		6	1000	 0 to 125 kPa, 0.5 kPa/bit, 0 offset
LFC	18FEE900	65257	5-8	4 bytes	250	 Total Fuel Used	X		6	1000	 0 to 2105540607.5 L, 0.5 L/bit, 0 offset
HOURS	18FEE500	65253	1-4	4 bytes	247	 Total Engine Hours	X		6	On Request	 0 to 210554060.75 h, 0.05 h/bit, 0 offset
S2	1CFE8E00	65166	2-3	2 bytes	1350	 Time at Last Service	X		7	On Request	 0 to 64255 h, 1 h/bit, 0 h offset
ETC5	1CFEC3VA*	65219	2.3	2 bits	604	 Transmission Neutral Switch		X	7	100	 00: Off, 01: On, 10: Error, 11: Not available
ETC5	1CFEC300	65219	2.3	2 bits	604	 Transmission Neutral Switch	X		7	100	" only used by Hard switch input
 00: Off, 01: On, 10: Error, 11: Not available"
EFL/P1	18FEEF00	65263	4	1 byte	100	 Engine Oil Pressure	X		6	500	" 0 to 1000 kPa, 4 kPa/bit, 0 offset
 Oil switch input is converted to fixed value: Off -> 200 kPa, On -> 0 kPa"
CI	18FEEB00	65259	2-21	20 bytes	587	 Model	X		6	On Request	 ex) V3800DICR
			23-39	17 bytes	588	 Serial Number	X		6	On Request	 ex) 5A1234
SOFT	18FEDA00	65242	1	1 byte	965	 Number of Software Identification Field	X		6	On Request	 1 step/bit, 0 offset, 0 to 250 steps
			2-26	25 bytes	234	 Software Identification	X		6	On Request	 Kubota Software ID ex) 1H00012345 (25 char)
SHUTDN	18FEE400	65252	4.1	2 bits	1081	 Wait to Start Lamp	X		6	1000	 00: Off, 01: On, 10: Error, 11: Not available
			5.1	2 bits	1110	 Engine Protection System has Shutdown Engine	X		6	1000	 00: No, 01: Yes, 10: Error, 11: Not available
TSC1	0C0000VA*	0	1.1	2 bits	695	 Override Control Mode		X	3	10	" 00: Override disabled, 01: Speed control, 10: Torque control, 11: Speed/Torque limit
 control"
			1.5	2 bits	897	 Override Control Mode Priority		X	3	10	 00: Highest priority, 01: High priority, 10: Medium priority, 11: Low priority
			2-3	2 bytes	898	 Engine Requested/Limit Speed control		X	3	10	 0 to 8031.875 rpm, 0.125 rpm/bit, 0 offset
			4	1 byte	518	 Engine Requested/Limit Torque control		X	3	10	 -125% to 125%, 1 %/bit, -125% offset
proprietary	18FF5000	65360	See other sheets			 Kubota Proprietary Engine Information	X		6	10	
proprietary	18FF5100	65361	See other sheets			 Kubota Proprietary Engine Information	X		6	1000	
proprietary	18FF53VA*	65363	See other sheets			 Kubota Proprietary Messages to Engine		X	6	10	
EOI	0CFD9200	64914	6.5	2 bits	3607	 Engine Emergency (Immediate) Shutdown Indication	X		3	250	 00: Off (No Shutdown Requested), 01: On (Shutdown Requested), 4 states/2 bit, 0 offset
DM1	18FECA00	65226				 Active Diagnostics	X		6	1000	
DM2	18FECB00	65227				 Logged Diagnostics	X		6	On Request	" Logged Diagnostics is disappeared
 when same Diagnostics is appeared in Active Diagnostics"
DM3	18FECCVA*	65228				 Clear Logged Diagnostics		X	6	On Request	
DM4	18FECD00	65229				 Freeze Frame Parameters	X		6		
DM5	18FECE00	65230	1	1 byte	1218	 Active Trouble Codes	X		6	On Request	
			2	1 byte	1219	 Previously Active Diagnostic Trouble Codes					
DM11	18FED3VA*	65235				 Diagnostic Data Clear/Reset For Active DTCs		X	6		
DM13	"18DF00VA*
18DFFFVA*"	57088				 Stop Start Broadcast		X	6		
TP_DT	1CEBFF00	60160			n/a	 Transport Protocol (DT)	X		7		 Multi Packet
TP_CM	1CECFF00	60416			n/a	 Transport Protocol (BAM & RTS)	X		7		
ACKM	18E8FF00	59392			n/a	 Acknowledge	X		6		
RQST	"18EA00VA*
18EAFFVA*"	59904			n/a	 PGN Request		X	6		
AC	18EEVA*00	60928		11 bits		 Manufacture Code in NAME Fields	X		6	On Request	 See SAE J1939-81 4.1.1
WFI	18FEFF00	65279	1.1	2 bits	97	 Water in Fuel Indicator	X		6	10000	 00: No, 01: Yes, 10: Error, 11: Not available