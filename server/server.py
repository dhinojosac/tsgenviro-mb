#!/usr/bin/env python

# --------------------------------------------------------------------------- #
# import the various server implementations
# --------------------------------------------------------------------------- #
from pymodbus.server.sync import StartTcpServer
from pymodbus.server.sync import StartTlsServer
from pymodbus.server.sync import StartUdpServer
from pymodbus.server.sync import StartSerialServer

from pymodbus.device import ModbusDeviceIdentification
from pymodbus.datastore import ModbusSequentialDataBlock, ModbusSparseDataBlock
from pymodbus.datastore import ModbusSlaveContext, ModbusServerContext

from pymodbus.transaction import ModbusRtuFramer, ModbusBinaryFramer
# --------------------------------------------------------------------------- #
# configure the service logging
# --------------------------------------------------------------------------- #
import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.DEBUG)


def run_server():

    # ----------------------------------------------------------------------- #
    # initialize registers
    # ----------------------------------------------------------------------- #
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [17]*100),      # discrete inputs
        co=ModbusSequentialDataBlock(0, [17]*100),      # coils
        hr=ModbusSequentialDataBlock(0, [17]*100),      # holding register
        ir=ModbusSequentialDataBlock(0, [17]*100))      # input register

    context = ModbusServerContext(slaves=store, single=True)

    # ----------------------------------------------------------------------- #
    # initialize the server information
    # ----------------------------------------------------------------------- #
    import yaml

    with open(r'config.yaml') as file:
        config = yaml.full_load(file)

        for item, doc in config.items():
            print(item, ":", doc)

    identity = ModbusDeviceIdentification()
    identity.VendorName = config["VENDOR_NAME"]
    identity.ProductCode = config["PRODUCT_CODE"]
    identity.VendorUrl = config["VENDOR_URL"]
    identity.ProductName = config["PRODUCT_NAME"]
    identity.ModelName = config["MODEL_NAME"]
    identity.MajorMinorRevision = config["MAJOR_MINOR_REV"]

    # ----------------------------------------------------------------------- #
    # run the server
    # ----------------------------------------------------------------------- #
    # Tcp:
    StartTcpServer(context, identity=identity, address=("", config["SERVER_PORT"]))
    



if __name__ == "__main__":
    print("MODBUS TCP SERVER START\n")
    run_server()
