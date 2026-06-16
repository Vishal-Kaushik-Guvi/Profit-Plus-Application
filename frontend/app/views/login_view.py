import flet as ft
from app.theme import Colors
from app.api_client import api_client


def LoginView(page: ft.Page):

    def go_to_signup(e):
        page.go("/signup")

    def go_to_home(e):
        page.go("/")

    # ── Form Fields ──────────────────────────────────────────────────
    email_field = ft.TextField(
        label="EMAIL ADDRESS",
        hint_text="you@example.com",
        color="white",
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY, size=11, weight=ft.FontWeight.BOLD),
        border_color=Colors.BORDER,
        focused_border_color=Colors.PRIMARY,
        bgcolor="#0d0d18",
        border_radius=10,
        width=350,
    )

    password_field = ft.TextField(
        label="PASSWORD",
        hint_text="Enter your password",
        password=True,
        can_reveal_password=True,
        color="white",
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY, size=11, weight=ft.FontWeight.BOLD),
        border_color=Colors.BORDER,
        focused_border_color=Colors.PRIMARY,
        bgcolor="#0d0d18",
        border_radius=10,
        width=350,
    )

    error_text = ft.Text("", color=Colors.DANGER, size=12)

    forgot_password_button = ft.TextButton(
        "FORGOT PASSWORD?",
        style=ft.ButtonStyle(
            color=Colors.SECONDARY,
            text_style=ft.TextStyle(size=11, weight=ft.FontWeight.BOLD)
        )
    )

    login_button = ft.Container(
        content=ft.Text("LOG IN", color="white", weight=ft.FontWeight.BOLD, size=14),
        bgcolor=Colors.PRIMARY,
        padding=ft.padding.symmetric(vertical=16),
        border_radius=10,
        alignment=ft.Alignment(0, 0),
        width=350,
        ink=True,
    )

    # ── Login Logic ──────────────────────────────────────────────────

    def login_clicked(e):
        error_text.value = ""

        if not email_field.value or "@" not in email_field.value:
            error_text.value = "Enter a valid email address"
            page.update()
            return

        if not password_field.value:
            error_text.value = "Enter your password"
            page.update()
            return

        login_button.content = ft.Row(
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[ft.ProgressRing(width=18, height=18, stroke_width=2, color="white")]
        )
        page.update()

        data, status_code = api_client.login(
            email=email_field.value,
            password=password_field.value
        )

        if status_code == 200:
            api_client.set_token(data["access_token"])
            page.go("/businesses")
        else:
            error_text.value = data.get("detail", "Invalid email or password")
            login_button.content = ft.Text("LOG IN", color="white",
                                            weight=ft.FontWeight.BOLD, size=14)
            page.update()

    def guest_clicked(e):
        page.go("/businesses")

    def forgot_password_clicked(e):
        page.go("/forgot-password")

    login_button.on_click = login_clicked
    forgot_password_button.on_click = forgot_password_clicked


    # ── Card Layout — WITH TEST MARKERS ────────────────────────────
    login_card = ft.Container(
        width=420,
        padding=40,
        bgcolor="#0a0a14",
        border_radius=20,
        border=ft.border.all(1, Colors.BORDER),
        #forgot pass
content=ft.Column(
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    spacing=18,
    controls=[
        ft.Text("Welcome Back", size=28, weight=ft.FontWeight.BOLD, color="white"),
        ft.Text("Log in to manage your shop.", size=13, color=Colors.TEXT_SECONDARY),
        ft.Container(height=10),
        email_field,
        ft.Container(
            width=350,
            alignment=ft.Alignment(1, 0),
            content=forgot_password_button
        ),
        ft.Text("TEST MARKER 1", color="red"),
        password_field,
        ft.Text("TEST MARKER 2", color="red"),
        login_button,
        ft.Text("TEST MARKER 3", color="red"),
    ]
)
    )



    # ── Page Layout ──────────────────────────────────────────────────
    return ft.View(
        route="/login",
        padding=0,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(
                expand=True,
                bgcolor="#06060c",
                alignment=ft.Alignment(0, 0),
                padding=40,
                content=login_card
            )
        ]
    )