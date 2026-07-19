import asyncio
from bleak import BleakScanner
from utils.logger import get_logger

logger = get_logger("Discovery")

class BluetoothDiscovery:
    @staticmethod
    async def scan_devices():
        logger.info("Scanning for Bluetooth devices...")
        try:
            devices = await BleakScanner.discover(timeout=5.0)
            return [{"name": d.name or "Unknown Device", "address": d.address} for d in devices]
        except Exception as e:
            logger.error(f"Scan failed: {e}")
            return []
