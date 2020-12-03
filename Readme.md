# tsgenviro modbus tcp
## Información Adicional
### Servidor TCP MODBUS
Para información más acabada ver la documentación de la librería [pymodbus](https://pymodbus.readthedocs.io/en/latest/readme.html) o la página de sus mantenedor [riptideio](http://riptideio.github.io/pymodbus/).

El servidor puede funcionar como servidor MODBUS completamente funcional, en este caso es del tipo TCP.

Se inicializan los registros del servidor MODBUS en cuatro bancos de datos, bobinas (coils), entradas discratas (discrete inputs), registros de retención (holding registers) y registros de entrada (input registers). Los bloques asignados para este servidor son direcciones de memoria secuenciales.
En la función [`ModbusSequentialDataBlock`](https://pymodbus.readthedocs.io/en/latest/source/library/pymodbus.datastore.html#pymodbus.datastore.ModbusSequentialDataBlock), el primer parámetro indica la dirección inicial, el segundo parámetro inicializa todos los valores en cero, en este caso un bloque secuencial de 100 ceros.
```
    store = ModbusSlaveContext(
        di=ModbusSequentialDataBlock(0, [0]*100),      # discrete inputs
        co=ModbusSequentialDataBlock(0, [0]*100),      # coils
        hr=ModbusSequentialDataBlock(0, [0]*100),      # holding register
        ir=ModbusSequentialDataBlock(0, [0]*100))      # input register

    context = ModbusServerContext(slaves=store, single=True)
```
La configuración de identidad y puerto del servidor está en el archivo `config.yaml`.
```
SERVER_PORT: 5020
```

## Instalación
Se deben tener instalado python3 y pip3, y luego las dependencias con el siguiente comando:
```sh
$ pip3 install -r requeriments.txt
```

## Run
Para arrancar el servidor:
```sh
$ cd server
$ python3 server.py
```

## Crear servicio de arranque
Crear archivo en `/etc/systemd/system/modbus-server-tcp.service`.
```
[Unit]
Description= MODBUS SERVER TCP
After=network.target
StartLimitIntervalSec=0

[Service]
Type=simple
Restart=always
RestartSec=1
User=root
WorkingDirectory=/home/user/<folder>
ExecStart=/home/user/<folder>/server/server.py

[Install]
WantedBy=multi-user.target
```
Luego de esto, correr el servicio con el comando:
```
systemctl start modbus-server-tcp.service
```


#### Autor
Diego Hinojosa Córdova
02-Dic-2020