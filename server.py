import asyncio
import logging
import sys
from asyncua import Server, ua
from asyncua.common.subscription import Subscription
from config import ServerConfig
from variables import setup_variables
from callbacks import ChangeCallbackHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OPCUAServer:
    def __init__(self, config):
        self.config = config
        self.server = Server()
        self.running = False
        self.subscription = None
        self.monitored_items = {}
        self.nodes = {}

    async def init(self):
        """Initialize the OPC UA server with the configuration settings."""
        # Server setup
        await self.server.init()
        self.server.set_endpoint(self.config.endpoint)
        self.server.set_server_name(self.config.name)

        # Set server capabilities
        await self.server.set_build_info(
            product_uri=self.config.product_uri,
            manufacturer_name=self.config.manufacturer,
            product_name=self.config.product_name,
            software_version=self.config.software_version,
            build_number=self.config.build_number,
            build_date=self.config.build_date
        )

        # Register namespace
        idx = await self.server.register_namespace(self.config.uri)
        logger.info(f"Registered namespace: {self.config.uri} with index {idx}")

        # Create objects and variables
        objects = self.server.nodes.objects
        
        # Create a folder to organize our nodes
        self.nodes['device'] = await objects.add_folder(idx, "Device")
        logger.info(f"Created Device folder")
        
        # Setup variables
        self.nodes.update(await setup_variables(self.server, self.nodes['device'], idx))
        
        # Setup callback handler
        self.callback_handler = ChangeCallbackHandler()
        
        # Create a subscription for variables
        self.subscription = await self.server.create_subscription(
            period=self.config.subscription_period,
            handler=self.callback_handler
        )
        
        # Monitor the specific variable for changes
        target_node = self.nodes[self.config.monitored_variable]
        handle = await self.subscription.subscribe_data_change(target_node)
        self.monitored_items[handle] = self.config.monitored_variable
        logger.info(f"Monitoring variable: {self.config.monitored_variable}")
        
        # Link the specific variable name to the callback handler
        self.callback_handler.set_monitored_variable(self.config.monitored_variable)
        
        return idx

    async def start(self):
        """Start the OPC UA server."""
        self.running = True
        await self.server.start()
        logger.info(f"Server started at {self.config.endpoint}")
        logger.info(f"Server namespace: {self.config.uri}")
        logger.info(f"Press Ctrl+C to exit")

    async def stop(self):
        """Stop the OPC UA server."""
        if self.running:
            if self.subscription:
                await self.subscription.delete()
            await self.server.stop()
            self.running = False
            logger.info("Server stopped")

async def main():
    # Create server instance with configuration
    config = ServerConfig()
    server = OPCUAServer(config)
    
    try:
        # Initialize and start the server
        await server.init()
        await server.start()
        
        # Keep the server running
        while server.running:
            await asyncio.sleep(1)
            
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, stopping server...")
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
    finally:
        # Ensure proper cleanup
        await server.stop()

if __name__ == "__main__":
    # Run the server
    asyncio.run(main())