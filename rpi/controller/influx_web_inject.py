"""
This script handles curl requests to inject messages into an InfluxDB instance running in a container.
The messages are stand-ins for CAN-bus messages that will later be used to store readings from an engine's ECU on a vehicle.
The script uses the InfluxDB client library to connect to the database and write the messages.
"""

import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from flask import Flask, request, jsonify

app = Flask(__name__)

# InfluxDB configuration
bucket = "REX"
# org = "your_org"
# token = "your_token"
url = "http://localhost:8086"

client = influxdb_client.InfluxDBClient(url=url)  # , token=token, org=org)
write_api = client.write_api(write_options=SYNCHRONOUS)


@app.route("/inject", methods=["POST"])
def inject_message():
    try:
        data = request.json
        point = (
            influxdb_client.Point("can_bus")
            .tag("device", "ECU")
            .field("message", data["message"])
        )
        # write_api.write(bucket=bucket, org=org, record=point)
        write_api.write(bucket=bucket, record=point)
        return (
            jsonify({"status": "success", "message": "Data injected successfully"}),
            200,
        )
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
