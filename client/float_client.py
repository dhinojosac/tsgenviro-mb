
#!/usr/bin/env python

from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.client.sync import ModbusTcpClient

import logging
FORMAT = ('%(asctime)-15s %(threadName)-15s'
          ' %(levelname)-8s %(module)-15s:%(lineno)-8s %(message)s')
logging.basicConfig(format=FORMAT)
log = logging.getLogger()
log.setLevel(logging.INFO)

def write32Float(client,address, value):
    builder = BinaryPayloadBuilder()
    builder.add_32bit_float(value)
    payload = builder.to_registers()
    payload = builder.build()
    client.write_registers(address, payload, skip_encode=True, unit=1) # write registers

def read32Float(client,addres):
    result = client.read_holding_registers(address, 2,  unit=1)
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers)
    decoded = decoder.decode_32bit_float()
    return decoded


ip_address = 'localhost'

client = ModbusTcpClient(ip_address, port=5020)
if client.connect():    # connection is OK

    # Create builder
    builder = BinaryPayloadBuilder()
     
    DataFloat = -512.34

    #builder.add_16bit_float(DataFloat)
    #builder.add_16bit_float(DataFloat)
    #builder.add_32bit_float(DataFloat)
    builder.add_32bit_float(DataFloat)

    payload = builder.to_registers()

    print("-" * 60)
    print("Writing Registers")
    print("-" * 60)
    print(payload)
    print(len(payload))
    print("\n")

    payload = builder.build()

    address = 0
    client.write_registers(address, payload, skip_encode=True, unit=1) # write registers

    # read registers
    count = len(payload)
    result = client.read_holding_registers(address, count,  unit=1)
    print("-" * 60)
    print("Registers")
    print("-" * 60)
    print(result.registers)
    print("\n")

    # decode registers to float32
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers)
    decoded = decoder.decode_32bit_float()
    print("-" * 60)
    print("Decoded Data")
    print("-" * 60)
    print("%s\t", hex(decoded) if isinstance(decoded, int) else decoded)

    print("-" * 60)
    print("Test Functions")
    print("-" * 60)

    write32Float(client, 0, -34.1)
    print (read32Float(client, 0))

    client.close()

