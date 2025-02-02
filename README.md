# REST client for shipping company - pytools

## Introduction

A simple and customizable shipment manager with a client for a REST API of a shipping company uses a simple Basic Auth and uses its own custom, serializable data structures.
This task will test practical Python 3 skills as well as basic REST API interaction knowledge.

This application uses `Python 3` and `OAuthLib 3.*`.

## Task details

1. Please do NOT modify any tests unless specifically told to do so.
2. Make tests pass by implementing the missing features in the production code.
3. There are multiple tests placed in the project that will help you verify your solution. Please use them as a guide when developing the project. Keep in mind that only a subset of the tests is visible to you and that your solution will be tested against many edge cases.

### Problem Statement:

#### Task 1
- Add a basic auth header implementation to the `RestClient` based on `client_id` and `client_secret` (with proper encoding).
- Implement the OAuth token exchanging mechanism:
    - Fetching a new token,
    - Refreshing the token based on the _refresh_token_.
- Arm the `RestClient` with an authentication header using a Bearer token.
    
#### Task 2
- Implement the HTTP requests methods (GET, POST, PUT, DELETE) for the REST Client in the `RestClient` class:
- Handle the HTTP errors returned from the API with suitable _Exceptions_.

### Task 3
Implement shipment management operations in the `ShipmentManager` using the rest client from task 1 and 2.
- Getting a single package details,
- Registering a new package,
- Replacing a known package with new details (Hint: use the `PUT` request method),
- Removing a package.

## Hints

Follow the methods docstrings with their parameters and return types.

For the HTTP requests, please use `urllib.request.urlopen`.

To exchange the authorization tokens, use the `WebApplicationClient` from the `OAuthLib`.

## Environment setup

To execute the unit tests, use:

```
pip install -q -e . && python3 setup.py pytest
```
