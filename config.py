import datetime

class ServerConfig:
    """Configuration settings for the OPC UA server."""
    
    def __init__(self):
        # Server identification
        self.name = "AsyncUA Example Server"
        self.endpoint = "opc.tcp://0.0.0.0:4840/asyncua/server/"
        self.uri = "http://examples.asyncua.server"
        
        # Server metadata
        self.product_uri = "urn:asyncua:example:server"
        self.manufacturer = "AsyncUA Examples"
        self.product_name = "AsyncUA Example Server"
        self.software_version = "1.0.0"
        self.build_number = "1"
        self.build_date = datetime.datetime.now()
        
        # Subscription settings
        self.subscription_period = 500  # milliseconds
        
        # Monitored variable
        self.monitored_variable = "temperature"  # This is the variable we'll monitor for changes