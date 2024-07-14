"""
Main file for API.
"""
# Standard Library Imports

# Third Party Imports
from fastapi import FastAPI

# Local Imports
from routes import *

# Create FastAPI instance
app: FastAPI = FastAPI()

# Register routes
app.include_router(api_router)

