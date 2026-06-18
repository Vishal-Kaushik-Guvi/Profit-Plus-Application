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

    @staticmethod
    def _result(response):
        try:
            return response.json(), response.status_code
        except requests.exceptions.JSONDecodeError:
            message = response.text.strip() or "Server returned an invalid response"
            return {"detail": message}, response.status_code

    # ── Auth Endpoints ──────────────────────────────────────────────

    def send_otp(self, email: str, purpose: str = "signup"):
        """POST /auth/send-otp"""
        payload = {"purpose": purpose}
        payload["email"] = email

        response = requests.post(
            f"{BASE_URL}/auth/send-otp",
            json=payload,
            headers=self._headers()
        )
        return self._result(response)

    def signup(self, name: str, phone: str, email: str, password: str, otp: str):
        """POST /auth/signup"""
        payload = {
            "name": name,
            "phone": phone,
            "email": email,
            "password": password,
            "otp": otp
        }

        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json=payload,
            headers=self._headers()
        )
        return self._result(response)

    def get_me(self):
        """GET /auth/me"""
        response = requests.get(
            f"{BASE_URL}/auth/me",
            headers=self._headers()
        )
        return self._result(response)

    def login(self, email: str, password: str):
        """POST /auth/login"""
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password},
            headers=self._headers()
        )
        return self._result(response)

    def get_my_businesses(self):
        """GET /business/my-businesses"""
        response = requests.get(
            f"{BASE_URL}/business/my-businesses",
            headers=self._headers()
        )
        return self._result(response)

    def get_business(self, business_id: str):
        """GET /business/{business_id}"""
        response = requests.get(
            f"{BASE_URL}/business/{business_id}",
            headers=self._headers()
        )
        return self._result(response)

    def create_business(self, business_name: str, phone: str = "", email: str = "",
                        address: str = "", city: str = "", pincode: str = "",
                        state: str = "", country: str = "", gst: str = "",
                        referred_by_code: str = ""):
        """POST /business/register"""
        payload = {
            "business_name": business_name,
            "phone": phone or None,
            "email": email or None,
            "address": address or None,
            "city": city or None,
            "pincode": pincode or None,
            "state": state or None,
            "country": country or None,
            "gst": gst or None,
            "referred_by_code": referred_by_code or None,
        }
        response = requests.post(
            f"{BASE_URL}/business/register",
            json=payload,
            headers=self._headers()
        )
        return self._result(response)


api_client = ApiClient()
