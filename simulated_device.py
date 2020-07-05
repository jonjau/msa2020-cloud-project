import random
import time
# TODO: timezone needed?
#from datetime import datetime, timedelta
import datetime
import json
import collections

# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
from azure.iot.device import IoTHubDeviceClient, Message

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string \
#   --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = (
    "HostName=iot-hub-jonjau.azure-devices.net;"
    "DeviceId=TempHumidSensor;"
    "SharedAccessKey=4+gg7Gk7yGY+g55m+KmZw7ellMrye9tkcxz1XDFRQgE="
)

# Define the JSON message to send to IoT Hub.
AVG_TEMP = 25.0
TEMP_RANGE = 10.0

AVG_HUMID = 60.0
HUMID_RANGE = 20.0

TEMP_COEFF = 10
BASE_N_CUSTOMERS = 100

#MSG_TXT = '{{"temperature": {temperature}, "humidity": {humidity}, "revenue": {revenue}}}'

MENU = {'vanilla': 7.0,
        'chocolate': 8.0,
        'mint': 9.0,
        'strawberry':7.0,
        'oreo':10.0}
PRICES = MENU.values()
FLAVOURS = MENU.keys()

START_TIME = datetime.datetime.combine(datetime.datetime.now(),datetime.time())


def simulate_telemetry(client):
    curr_time = START_TIME
    while True:
        msg_json = {}

        # Build the message with simulated telemetry values.
        # n_customers = simulate_n_customers()
        temperature_diff = (random.random() * TEMP_RANGE) - TEMP_RANGE/2
        temperature = AVG_TEMP + temperature_diff

        humidity_diff = (random.random() * HUMID_RANGE) - HUMID_RANGE/2
        humidity = AVG_HUMID + humidity_diff

        humidity_factor = humidity / AVG_HUMID

        n_customers = BASE_N_CUSTOMERS + TEMP_COEFF * temperature_diff
        n_customers = int(n_customers * humidity_factor)

        daily_revenue = 0
        flavour_counts = collections.Counter(FLAVOURS)

        for customer in range(n_customers):
            choice = random.choices(
                population=list(MENU.items()),
                weights=[(max(PRICES) - price) for price in PRICES])
            flavour, price = choice[0]
            flavour_counts[flavour] += 1
            daily_revenue += price

        curr_time += datetime.timedelta(days=1)
        print(curr_time)

        msg_json['time'] = curr_time.strftime("%Y-%m-%d")
        msg_json['temperature'] = temperature
        msg_json['humidity'] = humidity
        msg_json['revenue'] = daily_revenue
        for flavour_name in MENU.keys():
            msg_json[flavour_name] = flavour_counts[flavour_name]

        msg_json_text = json.dumps(msg_json)
        #msg_json_text = MSG_TXT.format(temperature=temperature, humidity=humidity, revenue=daily_revenue)
        message = Message(msg_json_text)

        # Send the message.
        print("Sending message: {}".format(message))
        client.send_message(message)
        print ("Message successfully sent")
        time.sleep(5)

def iothub_client_init():
    # Create an IoT Hub client
    client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
    return client

def iothub_client_telemetry_sample_run():
    try:
        client = iothub_client_init()
        print("IoT Hub device sending periodic messages, press Ctrl-C to exit")

        simulate_telemetry(client)

    except KeyboardInterrupt:
        print("IoTHubClient sample stopped")

if __name__ == '__main__':
    print("Press Ctrl-C to exit")

    iothub_client_telemetry_sample_run()