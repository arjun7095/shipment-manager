import email.utils
import json
import urllib.request
from base64 import b64decode
from datetime import datetime
from http import HTTPStatus as statuses
from http.client import HTTPResponse
from os import path, linesep
from urllib.request import Request

from oauthlib.oauth2 import WebApplicationServer

from test.fake_responder.fake_socket import FakeSocket
from test.fake_responder.fake_validator import FakeValidator

ENC = "utf-8"


class FakeResponder:
    api_ver = "v1"
    item_name = "package"
    http_version = "HTTP/1.1"
    fixed_headers = {
        "Server": "nginx/1.14.1",
        "Content-Type": "text/html; charset=UTF-8",
        "Connection": "close",
        "Expires": "Thu, 19 Nov 1981 08:52:00 GMT",
        "Cache-Control": "no-store, no-cache, must-revalidate, post-check=0, pre-check=0",
        "Pragma": "no-cache",
        "Access-Control-Allow-Origin": "*",
        "Access-Control-Expose-Headers": "Content-Type, X-Requested-With, X-authentication, X-client",
        "Referrer-Policy": "",
    }

    def __init__(self, initial_auth_data):
        validator = FakeValidator(initial_auth_data)
        self._auth_endpoint = WebApplicationServer(validator)

        current_dir = path.dirname(path.realpath(__file__))
        content_path = path.join(current_dir, "package", "packages.json")
        with open(content_path) as f:
            self.data = json.load(f)

        id_and_secret_entries = [
            ("cfbf408c2556fbc45b38d82d969f11fe", "5ebe2294ecd0e0f08eab7690d2a6ee69")
        ]
        self.auth_strings = [
            bytes(":".join(auth_entry), ENC) for auth_entry in id_and_secret_entries
        ]

    def _generate_response(self, content="null", method="GET", status=statuses.OK):
        """Create a HTTPResponse object with response code"""
        prepared_content = self._prepare_content(content, status)
        response = HTTPResponse(FakeSocket(prepared_content), method=method)
        response.begin()
        return response

    def _prepare_content(self, content, status):
        headers = self._get_headers(content)
        content = linesep.join(
            (
                " ".join((self.http_version, str(status.value), status.name)),
                linesep.join(f"{k}: {str(v)}" for k, v in headers.items()),
                "",
                content,
            )
        )
        return content

    def _get_headers(self, content):
        return {
            **self.fixed_headers,
            **{
                "Date": email.utils.format_datetime(datetime.now()),
                "Content-Length": len(content),
            },
        }

    def handle_request(self, request):
        """
        :type request: urllib.request.Request
        """
        if request.get_header("Content-type") not in [
            "application/json",
            "application/x-www-form-urlencoded;charset=UTF-8",
        ]:
            return self._generate_response(
                "false", request.get_method(), statuses.BAD_REQUEST
            )

        if self._url_path_last_part(request) in ["token", "refresh"]:
            auth_headers, authorization_result, status = self.token(request)
            return self._generate_response(
                authorization_result, request.get_method(), statuses(status)
            )

        if not self._authorize(request):
            return self._generate_response(
                "false", request.method, statuses.UNAUTHORIZED
            )

        if request.data and isinstance(request.data, str):
            # test if request data is in JSON format
            try:
                request_data = json.loads(request.data.decode("utf-8"))
            except:
                return self._generate_response(
                    "false", request.method, statuses.INTERNAL_SERVER_ERROR
                )
        method_handlers = {
            "GET": self.return_data,
            "POST": self.create_entity,
            "PUT": self.update_entity,
            "DELETE": self.delete_entity,
        }
        if any(
            part not in request.get_full_url().split(path.sep)
            for part in (self.api_ver, self.item_name)
        ):
            return self._generate_response(
                "false", request.get_method(), statuses.BAD_REQUEST
            )
        try:
            processed_data = method_handlers[request.get_method()](request)
            response_content = json.dumps(processed_data)
            response = self._generate_response(
                response_content,
                request.get_method(),
                statuses.OK if processed_data is not None else statuses.NOT_FOUND,
            )
            return response
        except Exception as e:
            return self._generate_response(
                "false", request.get_method(), statuses.INTERNAL_SERVER_ERROR
            )

    def return_data(self, request):
        """
        :type request: urllib.request.Request
        """
        url_last_part = self._url_path_last_part(request)
        if url_last_part == self.item_name:
            return self.data
        elif url_last_part in self.data.keys():
            return self.data[url_last_part]
        else:
            return None

    @staticmethod
    def _url_path_last_part(request):
        _, url_last_part = path.split(request.get_full_url())
        return url_last_part

    @staticmethod
    def _get_request_data(request):
        data = (
            request.data
            if isinstance(request.data, dict)
            else json.loads(request.data.decode("utf-8"))
        )
        return data

    def create_entity(self, request):
        """
        :type request: urllib.request.Request
        """
        data = self._get_request_data(request)
        data["id"] = self._generate_id()
        self.data[data["id"]] = data
        return data

    def _generate_id(self):
        return "T" + str(
            int(max("".join(filter(str.isdigit, el)) for el in self.data)) + 1
        )

    def update_entity(self, request):
        """
        :type request: urllib.request.Request
        """
        data = self._get_request_data(request)
        package = self.return_data(request)
        if not package:
            return None
        # TODO: remove later
        self.data[package["id"]].update(data)
        return self.data[package["id"]]

    def delete_entity(self, request):
        """
        :type request: urllib.request.Request
        """
        package = self.return_data(request)
        if not package:
            return None

        copy = package.copy()
        del self.data[package["id"]]
        return copy

    def _authorize(self, request):
        auth_header = request.get_header("Authorization")
        if not (auth_header and isinstance(auth_header, str)):
            return False
        authorization_name = f"_{auth_header.split()[0].lower()}_authorization"
        return hasattr(self, authorization_name) and getattr(self, authorization_name)(
            request
        )

    def _basic_authorization(self, request):
        auth_header = request.get_header("Authorization")
        return b64decode(bytes(auth_header.split()[1], ENC)) in self.auth_strings

    def _bearer_authorization(self, request):
        """implement Bearer authorization handling"""
        _, r = self._auth_endpoint.verify_request(
            request.get_full_url(),
            request.get_method(),
            request.data,
            request.headers,
            (request.data or {}).get("scopes"),
        )
        return True

    def token(self, request):
        """

        :type request: Request
        """
        return self._auth_endpoint.create_token_response(
            request.get_full_url(), request.get_method(), request.data, request.headers
        )
