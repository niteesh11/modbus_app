import asyncio
import logging
from pymodbus.client import AsyncModbusTcpClient

# Configure logging
logging.basicConfig(level=logging.INFO)
log = logging.getLogger(__name__)

# Modbus server parameters
MODBUS_SERVER_IP = '127.0.0.1'  # Server IP
MODBUS_SERVER_PORT = 5020        # Server Port

async def read_holding_registers(address, count):
    async with AsyncModbusTcpClient(MODBUS_SERVER_IP, port=MODBUS_SERVER_PORT) as client:
        log.info(f"Connecting to Modbus server at {MODBUS_SERVER_IP}:{MODBUS_SERVER_PORT}")
        
        result = await client.read_holding_registers(address, count)
        
        if result.isError():
            log.error(f"Modbus Error: {result}")
            return None
        
        return result.registers

async def main():
    address = -1  # Starting address for the read operation
    count = 9    # Number of registers to read (adjust based on server initialization)

    log.info(f"Reading {count} holding registers starting from address {address}")
    registers = await read_holding_registers(address, count)

    if registers is not None:
        log.info(f"Read registers: {registers}")
    else:
        log.error("Failed to read registers.")

if __name__ == "__main__":
    asyncio.run(main())
