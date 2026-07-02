import flet as ft

from app.api_client import api_client
from app.views.home_view import HomeView
from app.views.login_view import LoginView
from app.views.forgot_password_view import ForgotPasswordView
from app.views.createbusiness_view import CreateBusinessView
from app.views.business_dashboard_view import BusinessDashboardView
from app.views.mybusiness_view import MyBusinessView
from app.views.signup_view import SignupView
from app.views.product_view import ProductsView
from app.views.addproduct_view import AddProductView
from app.views.inventory_view import InventoryView
from app.views.restock_view import RestockView


def main(page: ft.Page):
    page.title = "Profit Plus"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window.width = 1200
    page.window.height = 800

    def route_change(e):
        page.views.clear()

        # Global auth guard
        public_routes = ["/", "/login", "/signup", "/forgot-password"]
        if page.route not in public_routes and not api_client.token:
            page.go("/login")
            return

        if page.route == "/":
            page.views.append(HomeView(page))

        elif page.route == "/login":
            page.views.append(LoginView(page))

        elif page.route == "/signup":
            page.views.append(SignupView(page))

        elif page.route == "/forgot-password":
            page.views.append(ForgotPasswordView(page))

        elif page.route == "/businesses":
            page.views.append(MyBusinessView(page))

        elif page.route == "/businesses/create":
            page.views.append(CreateBusinessView(page))

        elif page.route.startswith("/businesses/") and page.route.endswith(
            "/dashboard"
        ):
            business_id = page.route.split("/")[2]
            page.views.append(BusinessDashboardView(page, business_id))

        elif page.route.startswith("/businesses/") and "/products" in page.route:
            parts = page.route.split("/")
            business_id = parts[2]

            if page.route.endswith("/products"):
                page.views.append(ProductsView(page, business_id))

            elif page.route.endswith("/products/add"):
                page.views.append(AddProductView(page, business_id))

            elif len(parts) >= 6 and parts[5] == "edit":
                product_id = parts[4]
                page.views.append(AddProductView(page, business_id, product_id))

            else:
                page.go(f"/businesses/{business_id}/products")
                return

        elif page.route.startswith("/businesses/") and "/inventory" in page.route:
            parts = page.route.split("/")
            business_id = parts[2]

            if page.route.endswith("/inventory"):
                page.views.append(InventoryView(page, business_id))

            elif len(parts) >= 6 and parts[5] == "restock":
                inv_id = parts[4]
                page.views.append(RestockView(page, business_id, inv_id))

            else:
                page.go(f"/businesses/{business_id}/inventory")
                return

        elif page.route.startswith("/businesses/") and "/billing" in page.route:
            business_id = page.route.split("/")[2]
            page.views.append(
                ft.View(
                    page.route,
                    [ft.Text("Billing — Coming Soon", color="white", size=24)],
                )
            )

        elif page.route.startswith("/businesses/") and "/emi" in page.route:
            business_id = page.route.split("/")[2]
            page.views.append(
                ft.View(
                    page.route,
                    [ft.Text("EMI Management — Coming Soon", color="white", size=24)],
                )
            )

        elif page.route.startswith("/businesses/") and "/sales" in page.route:
            business_id = page.route.split("/")[2]
            page.views.append(
                ft.View(
                    page.route,
                    [ft.Text("Sales History — Coming Soon", color="white", size=24)],
                )
            )

        elif page.route.startswith("/businesses/") and "/analytics" in page.route:
            business_id = page.route.split("/")[2]
            page.views.append(
                ft.View(
                    page.route,
                    [ft.Text("Analytics — Coming Soon", color="white", size=24)],
                )
            )

        elif page.route.startswith("/businesses/") and "/customers" in page.route:
            business_id = page.route.split("/")[2]
            page.views.append(
                ft.View(
                    page.route,
                    [ft.Text("Customers — Coming Soon", color="white", size=24)],
                )
            )

        elif page.route.startswith("/businesses/") and "/subscription" in page.route:
            business_id = page.route.split("/")[2]
            page.views.append(
                ft.View(
                    page.route,
                    [ft.Text("Subscription — Coming Soon", color="white", size=24)],
                )
            )

        else:
            page.go("/")
            return

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)


    page.on_route_change = route_change
    page.on_view_pop = view_pop

    # ✅ First render the page, then check auth
    route_change(None)  # renders current route first

    # ✅ Then check token and redirect if needed
    if api_client.token:
        data, status = api_client.get_me()
        if status == 200:
            page.go("/businesses")
        else:
            api_client.set_token(None)
            page.go("/")
    else:
        page.go("/")

    page.update()

if __name__ == "__main__":
    ft.app(target=main)
