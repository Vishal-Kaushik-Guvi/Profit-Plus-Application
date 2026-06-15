import flet as ft
from app.views.home_view import HomeView
from app.views.signup_view import SignupView  # 👈 add this

def main(page: ft.Page):
    page.title = "Profit Plus"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 1200
    page.window_height = 800
    page.window_center()

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(HomeView(page))
        elif page.route == "/login":
            page.views.append(
                ft.View("/login", [ft.Text("Login - Coming Next", size=30, color="white")])
            )
        elif page.route == "/signup":
            page.views.append(SignupView(page))  # 👈 replace placeholder
        elif page.route == "/businesses":
            page.views.append(
                ft.View("/businesses", [ft.Text("My Businesses - Coming Next", size=30, color="white")])
            )

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