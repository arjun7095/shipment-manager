from oauthlib.oauth2 import RequestValidator, Client


class FakeValidator(RequestValidator):
    def __init__(self, initial_authorization_data):
        self.permitted_grant_types = ["authorization_code", "refresh_token"]
        self.permitted_client_ids = ["cfbf408c2556fbc45b38d82d969f11fe"]
        self.auth_data = initial_authorization_data

    def validate_refresh_token(self, refresh_token, client, request, *args, **kwargs):
        user, scopes = next(
            (
                (k, v["scopes"])
                for k, v in self.auth_data.items()
                if refresh_token == v["token"]["refresh_token"]
            ),
            (None, None),
        )
        if user and scopes:
            request.user, request.scopes = user, scopes
            return True
        return False

    def validate_redirect_uri(self, client_id, redirect_uri, request, *args, **kwargs):
        pass

    def get_default_redirect_uri(self, client_id, request, *args, **kwargs):
        return "https://api.example.com/"

    def validate_scopes(self, client_id, scopes, client, request, *args, **kwargs):
        pass

    def get_default_scopes(self, client_id, request, *args, **kwargs):
        pass

    def validate_response_type(
        self, client_id, response_type, client, request, *args, **kwargs
    ):
        pass

    def save_authorization_code(self, client_id, code, request, *args, **kwargs):
        pass

    def client_authentication_required(self, request, *args, **kwargs):
        return False

    def authenticate_client(self, request, *args, **kwargs):
        pass

    def authenticate_client_id(self, client_id, request, *args, **kwargs):
        if not request.client:
            request.client = Client(client_id)
        else:
            request.client.client_id = client_id
        return client_id in self.permitted_client_ids

    def validate_code(self, client_id, code, client, request, *args, **kwargs):
        user, scopes = next(
            (
                (k, v["scopes"])
                for k, v in self.auth_data.items()
                if code == v["token"]["access_token"]
            ),
            (None, None),
        )
        if user and scopes:
            request.user, request.scopes = user, scopes
            return True
        return False

    def confirm_redirect_uri(
        self, client_id, code, redirect_uri, client, request, *args, **kwargs
    ):
        return True

    def validate_grant_type(
        self, client_id, grant_type, client, request, *args, **kwargs
    ):
        return grant_type in self.permitted_grant_types

    def save_bearer_token(self, token, request, *args, **kwargs):
        self.auth_data[request.user]["token"].update(token)
        pass

    def invalidate_authorization_code(self, client_id, code, request, *args, **kwargs):
        pass

    def validate_bearer_token(self, token, scopes, request):
        return next(
            (
                v["token"]
                for v in self.auth_data.values()
                if token in [v["token"]["access_token"], v["token"]["refresh_token"]]
            ),
            None,
        )

    def get_original_scopes(self, refresh_token, request, *args, **kwargs):
        return ["shipping"]

    def introspect_token(self, token, token_type_hint, request, *args, **kwargs):
        pass

    def revoke_token(self, token, token_type_hint, request, *args, **kwargs):
        pass

    def validate_client_id(self, client_id, request, *args, **kwargs):
        pass

    def validate_user(self, username, password, client, request, *args, **kwargs):
        pass

    def get_code_challenge_method(self, code, request):
        pass
