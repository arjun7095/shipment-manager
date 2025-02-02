import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from unittest.mock import Mock
from app.shipment_manager import ShipmentManager


class TestShipmentManager(unittest.TestCase):
    def setUp(self):
        self.mock_client = Mock()
        self.manager = ShipmentManager(self.mock_client)

    def test_get_shipment(self):
        self.mock_client.get.return_value = {"shipment_id": 1, "status": "Delivered"}
        response = self.manager.get_shipment(1)
        self.assertEqual(response["shipment_id"], 1)
        self.assertEqual(response["status"], "Delivered")

    def test_register_shipment(self):
        self.mock_client.post.return_value = {"message": "Shipment Registered"}
        response = self.manager.register_shipment({"status": "In Transit"})
        self.assertEqual(response["message"], "Shipment Registered")

    def test_update_shipment(self):
        self.mock_client.put.return_value = {"message": "Shipment Updated"}
        response = self.manager.update_shipment(1, {"status": "Delivered"})
        self.assertEqual(response["message"], "Shipment Updated")

    def test_delete_shipment(self):
        self.mock_client.delete.return_value = {"message": "Shipment Deleted"}
        response = self.manager.delete_shipment(1)
        self.assertEqual(response["message"], "Shipment Deleted")


if __name__ == "__main__":
    unittest.main()
