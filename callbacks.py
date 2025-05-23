import logging
from asyncua.common.subscription import DataChangeNotif
from asyncua.ua.uaerrors import UaError

logger = logging.getLogger(__name__)

class ChangeCallbackHandler:
    """
    Handler for data change notifications from OPC UA subscriptions.
    """
    def __init__(self):
        self.monitored_variable = None
        self._callback_functions = []
    
    def set_monitored_variable(self, variable_name):
        """
        Set the name of the variable to monitor.
        
        Args:
            variable_name: Name of the variable to monitor
        """
        self.monitored_variable = variable_name
        logger.info(f"Set monitored variable: {variable_name}")
    
    def register_callback(self, callback_function):
        """
        Register a callback function to be called when the monitored variable changes.
        
        Args:
            callback_function: Function to be called when the monitored variable changes.
                               The function should accept two parameters: variable_name and new_value.
        """
        self._callback_functions.append(callback_function)
        logger.info(f"Registered callback function: {callback_function.__name__}")
    
    async def datachange_notification(self, node, val, data):
        """
        Called when a monitored variable changes.
        
        Args:
            node: Node that changed
            val: New value
            data: Additional data about the change
        """
        try:
            # Get the variable name from the node browse name
            if isinstance(data, DataChangeNotif):
                var_name = data.monitored_item.nodeid.Identifier
                logger.info(f"Variable changed: {var_name} = {val}")
                
                # If this is our monitored variable, call all registered callbacks
                if var_name == self.monitored_variable:
                    await self._handle_monitored_variable_change(var_name, val)
                
        except UaError as e:
            logger.error(f"OPC UA error in callback: {e}")
        except Exception as e:
            logger.error(f"General error in callback: {e}", exc_info=True)
    
    async def _handle_monitored_variable_change(self, variable_name, new_value):
        """
        Handle a change to the monitored variable by calling all registered callbacks.
        
        Args:
            variable_name: Name of the variable that changed
            new_value: New value of the variable
        """
        logger.info(f"Monitored variable {variable_name} changed to {new_value}")
        
        # Call all registered callbacks
        for callback in self._callback_functions:
            try:
                callback(variable_name, new_value)
                logger.info(f"Called callback: {callback.__name__}")
            except Exception as e:
                logger.error(f"Error in callback {callback.__name__}: {e}", exc_info=True)
                
    def event_notification(self, event):
        """
        Called when an event is received.
        
        Args:
            event: Event data
        """
        logger.info(f"Event received: {event}")