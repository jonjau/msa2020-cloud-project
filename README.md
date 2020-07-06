# Telemetry simulation using Azure IoT Hub and Power BI

**This project is a submission for the 2020**
**Microsoft Student Accelerator Program, Azure Cloud Fundamentals bootcamp**
**(technical stream).**

## Description

The python script [`simulated_device.py`](simulated_device.py) simulates a
point-of-sale machine in a small ice cream shop. It generates data
continuously every second, each message sent is to represent data from a
single trading period (day).

The data sent contains daily revenue, temperature and humidity information,
as well as the number of purchases for each ice cream flavour.

Simulation details:

* Higher temperature increases the number of customers (purchases).
* Higher humidity increases the number of customers (purchases).
* There are 5 flavours, each priced differently, and customers are more likely
  to choose more expensive flavours.

The above details are reflected in the visualisation done in Power BI.
