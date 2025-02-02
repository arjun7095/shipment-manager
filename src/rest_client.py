import base64
import requests


class RestClient:
    def __init__(self, base_url, client_id, client_secret):
        self.base_url = base_url
        self.client_id = client_id
        self.client_secret = client_secret
        self.token = None

    def get_auth_header(self):
        """Generate Basic Auth header."""
        credentials = f"{self.client_id}:{self.client_secret}"
        encoded_credentials = base64.b64encode(credentials.encode()).decode()
        return {"Authorization": f"Basic {encoded_credentials}"}

    def fetch_token(self):
        """Fetch a new OAuth token."""
        url = f"{self.base_url}/auth/token"
        response = requests.post(url, headers=self.get_auth_header())
        if response.status_code == 200:
            self.token = response.json().get("access_token")
        else:
            raise Exception("Failed to fetch token")

    def request(self, method, endpoint, data=None):
        """Make an authenticated API request."""
        headers = {"Authorization": f"Bearer {self.token}"}
        url = f"{self.base_url}{endpoint}"
        response = requests.request(method, url, json=data, headers=headers)

        if response.status_code not in [200, 201, 204]:
            raise Exception(f"Error: {response.status_code}, {response.text}")

        return response.json() if response.content else None

    def get(self, endpoint):
        return self.request("GET", endpoint)

    def post(self, endpoint, data):
        return self.request("POST", endpoint, data)

    def put(self, endpoint, data):
        return self.request("PUT", endpoint, data)

    def delete(self, endpoint):
        return self.request("DELETE", endpoint)
