from src.rest_client import RestClient
from src.shipment_manager import ShipmentManager

if __name__ == "__main__":
    client = RestClient("https://mock-api.com", "mock_client_id", "mock_client_secret")
    client.fetch_token()

    manager = ShipmentManager(client)

    # Test API calls
    print("Fetching shipment:", manager.get_shipment(1))
    print("Registering shipment:", manager.register_shipment({"status": "In Transit", "destination": "NYC"}))
    print("Updating shipment:", manager.update_shipment(1, {"status": "Delivered"}))
    print("Deleting shipment:", manager.delete_shipment(1))
