
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

ip_address = 'localhost'

client = ModbusTcpClient(ip_address, port=5020)
if client.connect():    # connection is OK

    # Create builder
    builder = BinaryPayloadBuilder()
     
    DataFloat = -22.34

    #builder.add_16bit_float(DataFloat)
    #builder.add_16bit_float(DataFloat)
    #builder.add_32bit_float(DataFloat)
    builder.add_32bit_float(DataFloat)

    payload = builder.to_registers()

    print("-" * 60)
    print("Writing Registers")
    print("-" * 60)
    print(payload)
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

    client.close()