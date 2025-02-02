class ShipmentManager:
    def __init__(self, client):
        self.client = client

    def get_shipment(self, shipment_id):
        """Get details of a single shipment."""
        return self.client.get(f"/shipments/{shipment_id}")

    def register_shipment(self, shipment_data):
        """Register a new shipment."""
        return self.client.post("/shipments", shipment_data)

    def update_shipment(self, shipment_id, shipment_data):
        """Update an existing shipment."""
        return self.client.put(f"/shipments/{shipment_id}", shipment_data)

    def delete_shipment(self, shipment_id):
        """Delete a shipment."""
        return self.client.delete(f"/shipments/{shipment_id}")
