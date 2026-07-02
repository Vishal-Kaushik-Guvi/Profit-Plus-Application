import base64
import os
from pathlib import Path

import requests

BASE_URL = "http://127.0.0.1:8000"
TOKEN_FILE = Path(__file__).resolve().parents[1] / ".auth_token"


class ApiClient:

    def __init__(self):
        self.token = self._load_token()
        print("=== API CLIENT INIT ===")
        print("TOKEN FILE EXISTS:", TOKEN_FILE.exists())
        print("TOKEN FILE PATH:", TOKEN_FILE)
        print("LOADED TOKEN:", self.token[:20] if self.token else None)

    def _load_token(self):
        try:
            token = TOKEN_FILE.read_text(encoding="utf-8").strip()
            return token or None
        except OSError:
            return None

    def set_token(self, token: str):
        self.token = token
        if token:
            TOKEN_FILE.write_text(token, encoding="utf-8")
            return
        try:
            TOKEN_FILE.unlink()
        except FileNotFoundError:
            pass

    def _headers(self):
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"
        return headers

    @staticmethod
    def absolute_url(path: str):
        if not path:
            return path
        if path.startswith("http://") or path.startswith("https://"):
            return path
        if path.startswith("/"):
            return f"{BASE_URL}{path}"
        return path

    @staticmethod
    def _result(response):
        try:
            return response.json(), response.status_code
        except requests.exceptions.JSONDecodeError:
            message = response.text.strip() or "Server returned an invalid response"
            return {"detail": message}, response.status_code

    # ── Auth ──────────────────────────────────────────────────────

    def send_otp(self, email: str, purpose: str = "signup", phone: str = ""):
        payload = {"purpose": purpose, "email": email}
        if phone:
            payload["phone"] = phone
        response = requests.post(
            f"{BASE_URL}/auth/send-otp", json=payload, headers=self._headers()
        )
        return self._result(response)

    def signup(self, name: str, phone: str, email: str, password: str, otp: str):
        response = requests.post(
            f"{BASE_URL}/auth/signup",
            json={
                "name": name,
                "phone": phone,
                "email": email,
                "password": password,
                "otp": otp,
            },
            headers=self._headers(),
        )
        return self._result(response)

    def login(self, email: str, password: str):
        response = requests.post(
            f"{BASE_URL}/auth/login",
            json={"email": email, "password": password},
            headers=self._headers(),
        )
        return self._result(response)

    def get_me(self):
        response = requests.get(f"{BASE_URL}/auth/me", headers=self._headers())
        return self._result(response)

    def reset_password(self, email: str, otp: str, new_password: str):
        response = requests.post(
            f"{BASE_URL}/auth/reset-password",
            json={"email": email, "otp": otp, "new_password": new_password},
            headers=self._headers(),
        )
        return self._result(response)

    # ── Business ──────────────────────────────────────────────────

    def get_my_businesses(self):
        response = requests.get(
            f"{BASE_URL}/business/my-businesses", headers=self._headers()
        )
        return self._result(response)

    def get_business(self, business_id: str):
        response = requests.get(
            f"{BASE_URL}/business/{business_id}", headers=self._headers()
        )
        return self._result(response)

    def create_business(
        self,
        business_name: str,
        phone: str = "",
        email: str = "",
        address: str = "",
        city: str = "",
        pincode: str = "",
        state: str = "",
        country: str = "",
        gst: str = "",
        referred_by_code: str = "",
        logo_path: str = "",
    ):
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
        if logo_path:
            with open(logo_path, "rb") as logo_file:
                payload["logo_filename"] = os.path.basename(logo_path)
                payload["logo_data"] = base64.b64encode(logo_file.read()).decode(
                    "ascii"
                )
        response = requests.post(
            f"{BASE_URL}/business/register", json=payload, headers=self._headers()
        )
        return self._result(response)

    def get_dashboard_stats(self, business_id: str):
        response = requests.get(
            f"{BASE_URL}/analytics/dashboard/{business_id}", headers=self._headers()
        )
        return self._result(response)

    # ── Products ──────────────────────────────────────────────────

    def create_product(
        self,
        business_id,
        product_name,
        category="",
        brand="",
        description="",
        hsn_code="",
        tax_percentage=0.0,
        color="",
        size="",
        business_type="",
    ):
        response = requests.post(
            f"{BASE_URL}/products/",
            json={
                "business_id": business_id,
                "product_name": product_name,
                "category": category,
                "brand": brand,
                "description": description,
                "hsn_code": hsn_code,
                "tax_percentage": tax_percentage,
                "color": color,
                "size": size,
                "business_type": business_type,
            },
            headers=self._headers(),
        )
        return self._result(response)

    def get_products(self, business_id: str):
        response = requests.get(
            f"{BASE_URL}/products/business/{business_id}", headers=self._headers()
        )
        return self._result(response)

    def get_product(self, product_id: str):
        response = requests.get(
            f"{BASE_URL}/products/{product_id}", headers=self._headers()
        )
        return self._result(response)

    def update_product(self, product_id: str, payload: dict):
        response = requests.put(
            f"{BASE_URL}/products/{product_id}", json=payload, headers=self._headers()
        )
        return self._result(response)

    def delete_product(self, product_id: str):
        response = requests.delete(
            f"{BASE_URL}/products/{product_id}", headers=self._headers()
        )
        return self._result(response)

    # ── Inventory ─────────────────────────────────────────────────

    def get_inventory(self, business_id: str):
        response = requests.get(
            f"{BASE_URL}/inventory/business/{business_id}", headers=self._headers()
        )
        return self._result(response)

    def update_inventory(self, inventory_id: str, payload: dict):
        response = requests.put(
            f"{BASE_URL}/inventory/{inventory_id}",
            json=payload,
            headers=self._headers(),
        )
        return self._result(response)

    def create_inventory(self, business_id: str, product_id: str):
        response = requests.post(
            f"{BASE_URL}/inventory/",
            json={"business_id": business_id, "product_id": product_id},
            headers=self._headers(),
        )
        return self._result(response)


api_client = ApiClient()
