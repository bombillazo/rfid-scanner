# rfid-scanner
A very simple interface program written in Python. The purpose of this application is to read RFID devices via an RFID reader connected to a Raspberry Pi and send the data to an HTTP endpoint. The Raspberry Pi and HTTP endpoint must have network access to each other. 

## How to use
Copy this script into your Raspberry Pi. Run the Python script via the command line, passing the `HTTP endpoint` as a parameter to the script. While the script runs, it will wait until an RFID scan triggers the read sequence. If the data can be decoded succesfully, it will send the data via an HTTP request to the HTTP endpoint specified by the initial parameter.

### Parameter

Parameter | Format | Description
--- | --- | ---
`HTTP endpoint` | `http://<IP\|URL>:<PORT><API_ENDPOINT_PATH>` | HTTP Endpoint where the read RFID data will be sent. Data will be sent in JSON format in the following schema: `{'cardId': '<READ_DATA>'}`

## Project Specs
- **Raspberry Pi:** 3 Model B+ 
- **RFID Reader:** Schlage LNL-MT11
- **Comms Protocol:** Wiegand Protocol

## Circuit Diagram

![alt text](imgs/circuit.jpg "circuit")

Made with :heart: by [@bombillazo](https://twitter.com/bombillazo)
