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


def main(page: ft.Page):
    page.title = "Profit Plus"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window.width = 1200
    page.window.height = 600
    page.window.center()

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(HomeView(page))

        elif page.route == "/login":
            page.views.append(LoginView(page))

        elif page.route == "/signup":
            page.views.append(SignupView(page))

        elif page.route == "/forgot-password":
            page.views.append(ForgotPasswordView(page))

        elif page.route == "/businesses":
            if not api_client.token:
                page.go("/login")
                return
            page.views.append(MyBusinessView(page))

        elif page.route == "/businesses/create":
            if not api_client.token:
                page.go("/login")
                return
            page.views.append(CreateBusinessView(page))

        elif page.route.startswith("/businesses/") and page.route.endswith("/dashboard"):
            if not api_client.token:
                page.go("/login")
                return
            business_id = page.route.split("/")[2]
            page.views.append(BusinessDashboardView(page, business_id))

        elif page.route.startswith("/businesses/") and "/products" in page.route:
            if not api_client.token:
                page.go("/login")
                return
            parts = page.route.split("/")
            business_id = parts[2]

            if page.route.endswith("/products"):
                # /businesses/{id}/products
                page.views.append(ProductsView(page, business_id))

            elif page.route.endswith("/products/add"):
                # /businesses/{id}/products/add
                page.views.append(AddProductView(page, business_id))

            elif len(parts) >= 6 and parts[5] == "inventory":
                # /businesses/{id}/products/{product_id}/inventory
                product_id = parts[4]
                page.views.append(ft.View(
                    page.route,
                    [ft.Text("Restock Inventory — Coming Soon",
                             color="white", size=24)]
                ))

            elif len(parts) >= 6 and parts[5] == "edit":
                # /businesses/{id}/products/{product_id}/edit
                product_id = parts[4]
                page.views.append(ft.View(
                    page.route,
                    [ft.Text("Edit Product — Coming Soon",
                             color="white", size=24)]
                ))

            else:
                page.go(f"/businesses/{business_id}/products")
                return

        elif page.route.startswith("/businesses/") and "/billing" in page.route:
            if not api_client.token:
                page.go("/login")
                return
            business_id = page.route.split("/")[2]
            page.views.append(ft.View(
                page.route,
                [ft.Text("Billing — Coming Soon", color="white", size=24)]
            ))

        elif page.route.startswith("/businesses/") and "/emi" in page.route:
            if not api_client.token:
                page.go("/login")
                return
            business_id = page.route.split("/")[2]
            page.views.append(ft.View(
                page.route,
                [ft.Text("EMI Management — Coming Soon",
                         color="white", size=24)]
            ))

        elif page.route.startswith("/businesses/") and "/sales" in page.route:
            if not api_client.token:
                page.go("/login")
                return
            business_id = page.route.split("/")[2]
            page.views.append(ft.View(
                page.route,
                [ft.Text("Sales History — Coming Soon",
                         color="white", size=24)]
            ))

        elif page.route.startswith("/businesses/") and "/analytics" in page.route:
            if not api_client.token:
                page.go("/login")
                return
            business_id = page.route.split("/")[2]
            page.views.append(ft.View(
                page.route,
                [ft.Text("Analytics — Coming Soon", color="white", size=24)]
            ))

        elif page.route.startswith("/businesses/") and "/customers" in page.route:
            if not api_client.token:
                page.go("/login")
                return
            business_id = page.route.split("/")[2]
            page.views.append(ft.View(
                page.route,
                [ft.Text("Customers — Coming Soon", color="white", size=24)]
            ))

        elif page.route.startswith("/businesses/") and "/subscription" in page.route:
            if not api_client.token:
                page.go("/login")
                return
            business_id = page.route.split("/")[2]
            page.views.append(ft.View(
                page.route,
                [ft.Text("Subscription — Coming Soon",
                         color="white", size=24)]
            ))

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

    route_change(None)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
