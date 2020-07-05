import random
import time
# TODO: timezone needed?
#from datetime import datetime, timedelta
import datetime
import json


# Using the Python Device SDK for IoT Hub:
#   https://github.com/Azure/azure-iot-sdk-python
from azure.iot.device import IoTHubDeviceClient, Message

# The device connection string to authenticate the device with your IoT hub.
# Using the Azure CLI:
# az iot hub device-identity show-connection-string --hub-name {YourIoTHubName} --device-id MyNodeDevice --output table
CONNECTION_STRING = "HostName=iot-hub-jonjau.azure-devices.net;DeviceId=TempHumidSensor;SharedAccessKey=4+gg7Gk7yGY+g55m+KmZw7ellMrye9tkcxz1XDFRQgE="

# Define the JSON message to send to IoT Hub.
TEMPERATURE = 20.0
HUMIDITY = 60
#MSG_TXT = '{{"temperature": {temperature}, "humidity": {humidity}, "revenue": {revenue}}}'

MENU = {'Vanilla': 7.0,
        'Chocolate': 8.0,
        'Mint': 9.0,
        'Strawberry':7.0,
        'Oreo':10.0}

START_TIME =  datetime.datetime.combine(datetime.datetime.now(),datetime.time())

def simulate_telemetry(client):
    curr_time = START_TIME
    while True:
        msg_json = {}

        # Build the message with simulated telemetry values.
        temperature = TEMPERATURE + (random.random() * 20)
        humidity = HUMIDITY + (random.random() * 20)
        n_customers = 160

        daily_revenue = 0

        for customer in range(n_customers):
            flavour, price = random.choice(list(MENU.items()))
            daily_revenue += price

        curr_time += datetime.timedelta(hours=8)
        print(curr_time)

        msg_json['time'] = curr_time.strftime("%d %h %H:%M")
        msg_json['temperature'] = temperature
        msg_json['humidity'] = humidity
        msg_json['revenue'] = daily_revenue

        msg_json_text = json.dumps(msg_json)
        #msg_json_text = MSG_TXT.format(temperature=temperature, humidity=humidity, revenue=daily_revenue)
        message = Message(msg_json_text)

        # Send the message.
        print( "Sending message: {}".format(message) )
        client.send_message(message)
        print ( "Message successfully sent" )
        time.sleep(1)

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