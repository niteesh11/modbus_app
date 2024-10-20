from flask import Flask, render_template, request
from pymodbus.client import AsyncModbusTcpClient
import asyncio
import logging

app = Flask(__name__)

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Modbus server parameters
MODBUS_SERVER_IP = '127.0.0.1'
MODBUS_SERVER_PORT = 5020

# Asynchronous function to read holding registers
async def read_holding_registers(address, count):
    async with AsyncModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT) as client:
        log.info(f"Connecting to Modbus server at {MODBUS_SERVER_IP}:{MODBUS_SERVER_PORT}")
        
        result = await client.read_holding_registers(address, count)
        
        if result.isError():
            log.error(f"Modbus Error: {result}")
            return None
        
        return result.registers

# Synchronous wrapper to call the async function
def sync_read_holding_registers(address, count):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    return loop.run_until_complete(read_holding_registers(address, count))

@app.route('/', methods=['GET', 'POST'])
def index():
    values = None
    address = None
    count = None
    if request.method == 'POST':
        try:
            address = int(request.form['address'])
            count = int(request.form['count'])

            # Call the synchronous wrapper
            values = sync_read_holding_registers(address, count)

        except Exception as e:
            log.error(f"Error in index route: {e}")
            values = str(e)

    return render_template('index.html', values=values, address=address, count=count)

if __name__ == '__main__':
    app.run(debug=True)
