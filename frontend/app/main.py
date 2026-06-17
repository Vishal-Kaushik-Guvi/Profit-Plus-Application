import flet as ft

from app.api_client import api_client
from app.views.home_view import HomeView
from app.views.login_view import LoginView
from app.views.mybusiness_view import MyBusinessView
from app.views.signup_view import SignupView


def main(page: ft.Page):
    page.title = "Profit Plus"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window.width = 1200
    page.window.height = 700
    page.window.center()

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(HomeView(page))
        elif page.route == "/login":
            page.views.append(LoginView(page))
        elif page.route == "/signup":
            page.views.append(SignupView(page))
        elif page.route == "/businesses":
            if not api_client.token:
                page.go("/login")
                return
            page.views.append(MyBusinessView(page))
        elif page.route == "/forgot-password":
            page.views.append(
                ft.View(
                    "/forgot-password",
                    [ft.Text("Forgot Password - Coming Soon", size=30, color="white")],
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

    route_change(None)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
