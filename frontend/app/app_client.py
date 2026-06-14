import requests

# Your FastAPI backend URL
BASE_URL = "http://127.0.0.1:8000"

class ApiClient:
    """
    Centralized API client.
    In Java → like a Retrofit interface or RestTemplate wrapper.
    """

    def __init__(self):
        self.token = None  # JWT token stored after login

    def set_token(self, token: str):
        """Save token after successful login"""
        self.token = token

    def _headers(self):
        """
        Build request headers.
        If logged in, attach Authorization header.
        In Java → HttpHeaders with Bearer token
        """
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    # ── Auth Endpoints ──────────────────────────────────────────────

    def send_otp(self, phone: str):
        """POST /auth/send-otp"""
        response = requests.post(
            f"{BASE_URL}/auth/send-otp",
            json={"phone": phone},
            headers=self._headers()
        )
        return response.json(), response.status_code

    def verify_otp(self, phone: str, otp: str, name: str = None):
        """POST /auth/verify-otp"""
        payload = {"phone": phone, "otp": otp}
        if name:
            payload["name"] = name

        response = requests.post(
            f"{BASE_URL}/auth/verify-otp",
            json=payload,
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


# Single shared instance — used across all views
# In Java → like a @Singleton @Bean
api_client = ApiClient()