from fastmcp import FastMCP
import random
import json

mcp = FastMCP("Simple Calculator Server")

# Tool: Add two numbers
@mcp.tool
def add(a: int, b: int) -> int:
    return a + b


# Tool: Generate a random number between a and b
@mcp.tool
def random_number(a: int, b: int) -> int:
    return random.randint(a, b)



 # Resource: Server Information   
@mcp.resource("info://server")
def server_info() -> str:
    info = {
        "name": "Simple Calculator Server",
        "version": "1.0.0",
        "description": "A simple calculator server",
        "tools": ["add", "random_number"],
        "author": "Pravakar Adhikari"
    }
    return json.dumps(info, indent = 2)




# Start the server
if __name__ == "__main__":
    mcp.run(transport = "http", host = "0.0.0.0", port = 8000)
    

