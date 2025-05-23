# AsyncUA OPC Server with Variable Change Callbacks

This project demonstrates how to use the AsyncUA library to implement an OPC UA server with variable monitoring and callback functionality.

## Features

- OPC UA server with multiple variables of different data types
- Variable subscription mechanism for monitoring changes
- Callback function implementation triggered by variable changes
- Server methods that can be called by clients
- Simple client examples to demonstrate variable manipulation
- Proper error handling and graceful shutdown
- Comprehensive logging for debugging
- Configurable server parameters

## Requirements

- Python 3.7 or higher
- AsyncUA library

## Installation

1. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

### Starting the OPC UA Server

1. Run the server:
   ```bash
   python server.py
   ```

2. The server will start at `opc.tcp://0.0.0.0:4840/asyncua/server/`

### Running the Client Examples

1. Basic client example (reads and writes variables, calls methods):
   ```bash
   python client.py
   ```

2. Client with subscription and callback example:
   ```bash
   python example_callback.py
   ```

## Project Structure

- `server.py`: Main OPC UA server implementation
- `variables.py`: OPC UA variable setup and configuration
- `callbacks.py`: Callback handler for variable changes
- `config.py`: Server configuration settings
- `client.py`: Basic client example
- `example_callback.py`: Client example with variable subscription and callback

## Customizing the Server

You can customize the server by modifying the `config.py` file. The following settings can be changed:

- Server name and endpoint
- Namespace URI
- Server metadata
- Subscription period
- Monitored variable name

## Implementing Custom Callbacks

To implement a custom callback function:

1. Define your callback function that accepts two parameters: `variable_name` and `new_value`
2. Register the callback with the handler using `handler.register_callback(your_callback_function)`
3. Set the monitored variable name using `handler.set_monitored_variable("variable_name")`

Example:

```python
def my_callback(variable_name, new_value):
    print(f"Variable {variable_name} changed to {new_value}")
    # Implement your business logic here

# Register the callback
handler.register_callback(my_callback)
```

## License

MIT