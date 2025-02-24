#!/usr/bin/env python3

from pymodbus.client import ModbusTcpClient
import logging

def run_modbus_client():
    # Configure logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
    
    # Server IP and Port
    server_ip = '127.0.0.1'
    server_port = 5020
    
    # Create Modbus client
    client = ModbusTcpClient(server_ip, port=server_port)
    connection = client.connect()
    if connection:
        logging.info(f'Connected to Modbus server at {server_ip}:{server_port}')
    else:
        logging.error(f'Failed to connect to Modbus server at {server_ip}:{server_port}')
        return

    try:
        # Write the integer 1 to holding register at address 0
        write_value = [1]
        write_address = 0
        write_response = client.write_registers(write_address, write_value)
        if write_response.isError():
            logging.error(f'Write error: {write_response}')
        else:
            logging.info(f'Wrote value {write_value[0]} to holding register at address {write_address}')
    finally:
        client.close()
        logging.info('Modbus client connection closed.')

if __name__ == '__main__':
    run_modbus_client()

