import asyncio
import logging
import sys
from asyncua import Client
from asyncua import ua

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OPCUAClient:
    def __init__(self, url):
        self.url = url
        self.client = Client(url=url)
        self.running = False
        
    async def connect(self):
        """Connect to the OPC UA server."""
        try:
            await self.client.connect()
            self.running = True
            logger.info(f"Connected to server at {self.url}")
            
            # Get namespace index
            uri = "http://examples.asyncua.server"
            nsidx = await self.client.get_namespace_index(uri)
            logger.info(f"Namespace index for {uri} is {nsidx}")
            
            return nsidx
        except Exception as e:
            logger.error(f"Failed to connect: {e}")
            raise
            
    async def disconnect(self):
        """Disconnect from the OPC UA server."""
        if self.running:
            await self.client.disconnect()
            self.running = False
            logger.info("Disconnected from server")
            
    async def read_variable(self, node_id, nsidx):
        """
        Read a variable from the server.
        
        Args:
            node_id: Node ID of the variable
            nsidx: Namespace index
            
        Returns:
            Value of the variable
        """
        try:
            node = self.client.get_node(ua.NodeId(node_id, nsidx))
            value = await node.read_value()
            logger.info(f"Read variable {node_id}: {value}")
            return value
        except Exception as e:
            logger.error(f"Failed to read variable {node_id}: {e}")
            raise
            
    async def write_variable(self, node_id, nsidx, value):
        """
        Write a value to a variable on the server.
        
        Args:
            node_id: Node ID of the variable
            nsidx: Namespace index
            value: Value to write
        """
        try:
            node = self.client.get_node(ua.NodeId(node_id, nsidx))
            await node.write_value(value)
            logger.info(f"Wrote variable {node_id}: {value}")
        except Exception as e:
            logger.error(f"Failed to write variable {node_id}: {e}")
            raise
            
    async def call_method(self, node_id, parent_id, nsidx, *args):
        """
        Call a method on the server.
        
        Args:
            node_id: Node ID of the method
            parent_id: Node ID of the parent object
            nsidx: Namespace index
            *args: Method arguments
            
        Returns:
            Method result
        """
        try:
            method_node = self.client.get_node(ua.NodeId(node_id, nsidx))
            parent_node = self.client.get_node(ua.NodeId(parent_id, nsidx))
            result = await parent_node.call_method(method_node, *args)
            logger.info(f"Called method {node_id}({args}): {result}")
            return result
        except Exception as e:
            logger.error(f"Failed to call method {node_id}: {e}")
            raise

async def main():
    # URL of the OPC UA server
    server_url = "opc.tcp://localhost:4840/asyncua/server/"
    
    # Create client instance
    client = OPCUAClient(server_url)
    
    try:
        # Connect to the server
        nsidx = await client.connect()
        
        # Read variables
        temperature = await client.read_variable("temperature", nsidx)
        status = await client.read_variable("status", nsidx)
        counter = await client.read_variable("counter", nsidx)
        message = await client.read_variable("message", nsidx)
        
        # Write variables
        await client.write_variable("temperature", nsidx, 25.5)
        await client.write_variable("status", nsidx, True)
        await client.write_variable("counter", nsidx, 42)
        await client.write_variable("message", nsidx, "Hello from client")
        
        # Read variables again to confirm changes
        temperature = await client.read_variable("temperature", nsidx)
        status = await client.read_variable("status", nsidx)
        counter = await client.read_variable("counter", nsidx)
        message = await client.read_variable("message", nsidx)
        
        # Call method
        result = await client.call_method("increment_value", "Device", nsidx, 10)
        logger.info(f"Method result: {result}")
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
    finally:
        # Ensure proper cleanup
        await client.disconnect()

if __name__ == "__main__":
    # Run the client
    asyncio.run(main())