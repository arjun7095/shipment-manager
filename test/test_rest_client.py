import unittest
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from unittest.mock import patch, Mock
from app.rest_client import RestClient


class TestRestClient(unittest.TestCase):
    def setUp(self):
        self.client = RestClient("https://mock-api.com", "mock_client_id", "mock_client_secret")

    @patch("app.rest_client.requests.post")
    def test_fetch_token(self, mock_post):
        mock_post.return_value = Mock(status_code=200, json=lambda: {"access_token": "mocked_token"})
        self.client.fetch_token()
        self.assertEqual(self.client.token, "mocked_token")

    @patch("app.rest_client.requests.request")
    def test_get(self, mock_request):
        mock_request.return_value = Mock(status_code=200, json=lambda: {"shipment_id": 1})
        response = self.client.get("/shipments/1")
        self.assertEqual(response["shipment_id"], 1)

    @patch("app.rest_client.requests.request")
    def test_post(self, mock_request):
        mock_request.return_value = Mock(status_code=201, json=lambda: {"message": "Created"})
        response = self.client.post("/shipments", {"status": "In Transit"})
        self.assertEqual(response["message"], "Created")


if __name__ == "__main__":
    unittest.main()
