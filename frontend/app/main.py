import flet as ft
from app.views.home_view import HomeView
# from app.views.auth_view import AuthView  # 👈 commented out for now

def main(page: ft.Page):
    page.title = "Profit Plus"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 0
    page.window_width = 1200
    page.window_height = 600
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
            page.views.append(
                ft.View("/signup", [ft.Text("Signup - Coming Next", size=30, color="white")])
            )

        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    page.go(page.route or "/")

if __name__ == "__main__":
    ft.app(target=main)