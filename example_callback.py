import asyncio
import logging
from asyncua import Client, ua
from callbacks import ChangeCallbackHandler

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define a callback function
def temperature_changed(variable_name, new_value):
    """
    Callback function that will be called when the temperature variable changes.
    
    Args:
        variable_name: Name of the variable that changed
        new_value: New value of the variable
    """
    logger.info(f"CALLBACK: Temperature changed to {new_value}°C")
    
    # Implement your business logic here
    if new_value > 30.0:
        logger.warning(f"ALERT: Temperature exceeds threshold! Current value: {new_value}°C")
    elif new_value < 10.0:
        logger.warning(f"ALERT: Temperature below minimum threshold! Current value: {new_value}°C")
    else:
        logger.info(f"Temperature within normal range: {new_value}°C")

async def run_client_with_subscription():
    """
    Example client that subscribes to a variable and registers a callback.
    """
    # URL of the OPC UA server
    server_url = "opc.tcp://localhost:4840/asyncua/server/"
    
    # Create client
    client = Client(url=server_url)
    
    try:
        # Connect to server
        await client.connect()
        logger.info(f"Connected to server at {server_url}")
        
        # Get namespace index
        uri = "http://examples.asyncua.server"
        nsidx = await client.get_namespace_index(uri)
        
        # Create subscription
        handler = ChangeCallbackHandler()
        subscription = await client.create_subscription(500, handler)
        
        # Set the monitored variable
        handler.set_monitored_variable("temperature")
        
        # Register our callback function
        handler.register_callback(temperature_changed)
        
        # Subscribe to data change for temperature variable
        var = client.get_node(ua.NodeId("temperature", nsidx))
        handle = await subscription.subscribe_data_change(var)
        
        # Loop to demonstrate subscription
        for i in range(10):
            # Simulate temperature changes
            new_temp = 15.0 + i * 2  # Increasing temperature
            await var.write_value(new_temp)
            logger.info(f"Changed temperature to {new_temp}")
            
            # Wait a bit
            await asyncio.sleep(2)
            
        # Extra test for alert conditions
        logger.info("Testing alert conditions...")
        await var.write_value(35.0)  # High temperature alert
        await asyncio.sleep(2)
        await var.write_value(5.0)   # Low temperature alert
        await asyncio.sleep(2)
        await var.write_value(22.5)  # Back to normal
        await asyncio.sleep(2)
        
        # Cleanup subscription
        await subscription.unsubscribe(handle)
        await subscription.delete()
        
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
    finally:
        # Disconnect from server
        await client.disconnect()
        logger.info("Disconnected from server")

if __name__ == "__main__":
    # Run the example
    asyncio.run(run_client_with_subscription())