
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

def read32Float(client,address):
    result = client.read_holding_registers(address, 2,  unit=1)
    decoder = BinaryPayloadDecoder.fromRegisters(result.registers)
    decoded = decoder.decode_32bit_float()
    return decoded


ip_address = 'localhost'

client = ModbusTcpClient(ip_address, port=5020)
if client.connect():    # connection is OK

    print("-" * 60)
    print("Test Functions")
    print("-" * 60)
    print()

    UNIT=1
    rq = client.write_register(1, 10, unit=UNIT)
    rr = client.read_holding_registers(1, 1, unit=UNIT)
    print(rr.registers[0])
 
    write32Float(client, 0, 0.05)
    write32Float(client, 1, 1.15)
    write32Float(client, 6, 99.2)
    write32Float(client, 97, 65.78)
    print (read32Float(client, 0))
    print (read32Float(client, 1))
    print (read32Float(client, 2))
    print (read32Float(client, 3))
    print (read32Float(client, 97))

    rq = client.write_register(98, 10, unit=UNIT)
    rr = client.read_holding_registers(98, 1, unit=UNIT)

    print(rr.registers[0])
    
    rr = client.read_holding_registers(95, 1, unit=UNIT)

    print(rr.registers[0])


    client.close()

