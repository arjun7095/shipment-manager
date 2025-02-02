## Shipment Manager
A simple and customizable shipment management system with a REST API client for a sharing company.

## Features
    OAuth authentication using client_id and client_secret
    Supports GET, POST, PUT, DELETE requests
    Handles API errors with proper exceptions
# Shipment management:
        Retrieve package details
        Register a new package
        Update package details
        Remove a package

##  Running Unit Tests
        python -m unittest discover tests

# run a specific test:
        python -m unittest tests.test_rest_client
        python -m unittest tests.test_shipment_manager

