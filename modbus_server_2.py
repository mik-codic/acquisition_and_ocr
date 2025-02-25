#!/usr/bin/env python3

from pymodbus.server import StartTcpServer
from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusServerContext, ModbusSlaveContext
from pymodbus.datastore import ModbusSequentialDataBlock
import logging
import queue

# Create a thread-safe queue to store received values
received_values_queue = queue.Queue()

def run_modbus_server():
    # Configure logging
    logging.basicConfig(format='%(asctime)s %(levelname)s: %(message)s', level=logging.INFO)
    
    # Create a custom data block that stores received values
    class PrintingDataBlock(ModbusSequentialDataBlock):
        def setValues(self, address, values):
            super().setValues(address, values)
            # Store the values in the queue
            received_values_queue.put((address, values))
            # Print the values for logging purposes
            print(f"Server received values at address {address}: {values}")
    
    # Initialize data store with 100 holding registers using the custom data block
    store = ModbusSlaveContext(
        hr=PrintingDataBlock(0, [0]*100)
    )
    context = ModbusServerContext(slaves=store, single=True)
    
    # Set up device identity (optional)
    identity = ModbusDeviceIdentification()
    identity.VendorName = 'Jetson AGX Orin Modbus Server'
    identity.ProductCode = 'JAOMBS'
    identity.VendorUrl = 'http://yourcompany.com'
    identity.ProductName = 'Modbus Server'
    identity.ModelName = 'Modbus Server Model'
    identity.MajorMinorRevision = '1.0'
    
    # Start Modbus TCP server
    PORT = 5020  # Use a non-privileged port if not running as root
    logging.info(f'Starting Modbus TCP Server on 192.168.0.11:{PORT}')
    StartTcpServer(context=context, identity=identity, address=("192.168.0.11", PORT))
#run_modbus_server()
if __name__ == '__main__':
    run_modbus_server()
