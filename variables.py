import logging
from asyncua import ua
from datetime import datetime

logger = logging.getLogger(__name__)

async def setup_variables(server, parent_node, idx):
    """
    Set up all OPC UA variables on the server.
    
    Args:
        server: The OPC UA server instance
        parent_node: The parent node to add variables to
        idx: Namespace index
        
    Returns:
        Dictionary of created nodes
    """
    nodes = {}
    
    # Create variables with different data types
    
    # Boolean variable
    nodes['status'] = await parent_node.add_variable(
        ua.NodeId("status", idx), 
        "Status", 
        ua.Variant(False, ua.VariantType.Boolean)
    )
    await nodes['status'].set_writable()
    logger.info("Added variable: status (Boolean)")
    
    # Integer variable
    nodes['counter'] = await parent_node.add_variable(
        ua.NodeId("counter", idx), 
        "Counter", 
        ua.Variant(0, ua.VariantType.Int32)
    )
    await nodes['counter'].set_writable()
    logger.info("Added variable: counter (Int32)")
    
    # Float variable
    nodes['temperature'] = await parent_node.add_variable(
        ua.NodeId("temperature", idx), 
        "Temperature", 
        ua.Variant(22.5, ua.VariantType.Float)
    )
    await nodes['temperature'].set_writable()
    logger.info("Added variable: temperature (Float)")
    
    # String variable
    nodes['message'] = await parent_node.add_variable(
        ua.NodeId("message", idx), 
        "Message", 
        ua.Variant("Hello OPC UA", ua.VariantType.String)
    )
    await nodes['message'].set_writable()
    logger.info("Added variable: message (String)")
    
    # DateTime variable
    nodes['timestamp'] = await parent_node.add_variable(
        ua.NodeId("timestamp", idx), 
        "Timestamp", 
        ua.Variant(datetime.now(), ua.VariantType.DateTime)
    )
    await nodes['timestamp'].set_writable()
    logger.info("Added variable: timestamp (DateTime)")
    
    # Add a method to the server
    await add_server_method(server, parent_node, idx)
    
    return nodes

async def add_server_method(server, parent_node, idx):
    """
    Add a method to the OPC UA server.
    
    Args:
        server: The OPC UA server instance
        parent_node: The parent node to add the method to
        idx: Namespace index
    """
    # Define the method arguments
    input_args = [
        ua.Argument(
            name="value",
            data_type=ua.NodeId(ua.ObjectIds.Int32),
            value_rank=-1,
            array_dimensions=[],
            description=ua.LocalizedText("Value to increment")
        )
    ]
    
    # Define the method output arguments
    output_args = [
        ua.Argument(
            name="result",
            data_type=ua.NodeId(ua.ObjectIds.Int32),
            value_rank=-1,
            array_dimensions=[],
            description=ua.LocalizedText("Incremented value")
        )
    ]
    
    # Create a method node
    method_node = await parent_node.add_method(
        ua.NodeId("increment_value", idx),
        "IncrementValue",
        increment_value,
        input_args,
        output_args
    )
    
    logger.info("Added method: IncrementValue")

async def increment_value(parent, inputs):
    """
    Method implementation for incrementing a value.
    
    Args:
        parent: The parent node
        inputs: Method input arguments
        
    Returns:
        List of output values
    """
    value = inputs[0]
    result = value + 1
    logger.info(f"Method called: IncrementValue({value}) -> {result}")
    return [result]