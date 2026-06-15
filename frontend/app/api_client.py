import requests

BASE_URL = "http://127.0.0.1:8000"

class ApiClient:

    def __init__(self):
        self.token = None

    def set_token(self, token: str):
        self.token = token

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    # ── Auth Endpoints ──────────────────────────────────────────────

    def send_otp(self, phone: str = None, email: str = None, purpose: str = "signup"):
        """POST /auth/send-otp - phone OR email"""
        payload = {"purpose": purpose}
        if phone:
            payload["phone"] = phone
        if email:
            payload["email"] = email

        response = requests.post(
            f"{BASE_URL}/auth/send-otp",
            json=payload,
            headers=self._headers()
        )
        return response.json(), response.status_code

    def signup(self, name: str, password: str, otp: str, otp_method: str,
               phone: str = None, email: str = None):
        """POST /auth/signup"""
        payload = {
            "name": name,
            "password": password,
            "otp": otp,
            "otp_method": otp_method
        }
        if phone:
            payload["phone"] = phone
        if email:
            payload["email"] = email

        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json=payload,
            headers=self._headers()
        )
        return response.json(), response.status_code

    def login(self, identifier: str, password: str):
        """POST /auth/login - identifier = phone or email"""
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"identifier": identifier, "password": password},
            headers=self._headers()
        )
        return response.json(), response.status_code

    def get_me(self):
        """GET /auth/me"""
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers=self._headers()
        )
        return response.json(), response.status_code


api_client = ApiClient()