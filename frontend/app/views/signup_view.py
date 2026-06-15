import flet as ft
from app.theme import Colors
from app.api_client import api_client


def SignupView(page: ft.Page):

    # ── State ────────────────────────────────────────────────────
    state = {"otp_method": "phone", "otp_sent": False}

    # ── Tab Buttons (Phone OTP / Email OTP) ─────────────────────────
    def select_phone_tab(e):
        state["otp_method"] = "phone"
        phone_field.visible = True
        email_field.visible = False
        phone_tab.bgcolor = Colors.SECONDARY
        phone_tab_text.color = "black"
        email_tab.bgcolor = "#13131f"
        email_tab_text.color = Colors.TEXT_SECONDARY
        page.update()

    def select_email_tab(e):
        state["otp_method"] = "email"
        phone_field.visible = False
        email_field.visible = True
        email_tab.bgcolor = Colors.SECONDARY
        email_tab_text.color = "black"
        phone_tab.bgcolor = "#13131f"
        phone_tab_text.color = Colors.TEXT_SECONDARY
        page.update()

    phone_tab_text = ft.Text("PHONE OTP", size=12, weight=ft.FontWeight.BOLD, color="black")
    email_tab_text = ft.Text("EMAIL OTP", size=12, weight=ft.FontWeight.BOLD, color=Colors.TEXT_SECONDARY)

    phone_tab = ft.Container(
        content=phone_tab_text,
        bgcolor=Colors.SECONDARY,
        padding=ft.padding.symmetric(vertical=12),
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        expand=True,
        on_click=select_phone_tab,
        ink=True,
    )

    email_tab = ft.Container(
        content=email_tab_text,
        bgcolor="#13131f",
        padding=ft.padding.symmetric(vertical=12),
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        expand=True,
        on_click=select_email_tab,
        ink=True,
    )

    tab_row = ft.Container(
        content=ft.Row(
            controls=[phone_tab, email_tab],
            spacing=4,
        ),
        bgcolor="#0d0d18",
        border_radius=10,
        padding=4,
        border=ft.border.all(1, Colors.BORDER),
    )

    # ── Form Fields ──────────────────────────────────────────────────
    name_field = ft.TextField(
        label="FULL NAME",
        hint_text="Enter your name",
        color="white",
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY, size=11, weight=ft.FontWeight.BOLD),
        border_color=Colors.BORDER,
        focused_border_color=Colors.SECONDARY,
        bgcolor="#0d0d18",
        border_radius=10,
        width=350,
    )

    phone_field = ft.TextField(
        label="PHONE NUMBER",
        hint_text="123 456 7890",
        color="white",
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY, size=11, weight=ft.FontWeight.BOLD),
        border_color=Colors.BORDER,
        focused_border_color=Colors.SECONDARY,
        bgcolor="#0d0d18",
        border_radius=10,
        width=350,
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=10,
        visible=True,
    )

    email_field = ft.TextField(
        label="EMAIL ADDRESS",
        hint_text="you@example.com",
        color="white",
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY, size=11, weight=ft.FontWeight.BOLD),
        border_color=Colors.BORDER,
        focused_border_color=Colors.SECONDARY,
        bgcolor="#0d0d18",
        border_radius=10,
        width=350,
        visible=False,
    )

    password_field = ft.TextField(
        label="PASSWORD",
        hint_text="Create a password",
        password=True,
        can_reveal_password=True,
        color="white",
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY, size=11, weight=ft.FontWeight.BOLD),
        border_color=Colors.BORDER,
        focused_border_color=Colors.SECONDARY,
        bgcolor="#0d0d18",
        border_radius=10,
        width=350,
    )

    otp_field = ft.TextField(
        label="ENTER OTP",
        hint_text="6-digit code",
        color="white",
        label_style=ft.TextStyle(color=Colors.TEXT_SECONDARY, size=11, weight=ft.FontWeight.BOLD),
        border_color=Colors.BORDER,
        focused_border_color=Colors.SECONDARY,
        bgcolor="#0d0d18",
        border_radius=10,
        width=350,
        keyboard_type=ft.KeyboardType.NUMBER,
        max_length=6,
        visible=False,
    )

    error_text = ft.Text("", color=Colors.DANGER, size=12)
    status_text = ft.Text("", color=Colors.SUCCESS, size=12)

    # ── Button Logic ─────────────────────────────────────────────────

    def get_otp_clicked(e):
        error_text.value = ""

        if not name_field.value:
            error_text.value = "Please enter your name"
            page.update()
            return

        if not password_field.value or len(password_field.value) < 6:
            error_text.value = "Password must be at least 6 characters"
            page.update()
            return

        if state["otp_method"] == "phone":
            if not phone_field.value or len(phone_field.value) != 10:
                error_text.value = "Enter a valid 10-digit phone number"
                page.update()
                return

            data, status_code = api_client.send_otp(
                phone=phone_field.value, purpose="signup"
            )
        else:
            if not email_field.value or "@" not in email_field.value:
                error_text.value = "Enter a valid email address"
                page.update()
                return

            data, status_code = api_client.send_otp(
                email=email_field.value, purpose="signup"
            )

        if status_code == 200:
            state["otp_sent"] = True
            otp_field.visible = True
            status_text.value = f"OTP sent! (Demo: {data.get('otp')})"
            main_button.content = ft.Text("CREATE ACCOUNT", color="white",
                                            weight=ft.FontWeight.BOLD, size=14)
        else:
            error_text.value = data.get("detail", "Failed to send OTP")

        page.update()

    def create_account_clicked(e):
        error_text.value = ""

        if not otp_field.value or len(otp_field.value) != 6:
            error_text.value = "Enter a valid 6-digit OTP"
            page.update()
            return

        if state["otp_method"] == "phone":
            data, status_code = api_client.signup(
                name=name_field.value,
                password=password_field.value,
                otp=otp_field.value,
                otp_method="phone",
                phone=phone_field.value
            )
        else:
            data, status_code = api_client.signup(
                name=name_field.value,
                password=password_field.value,
                otp=otp_field.value,
                otp_method="email",
                email=email_field.value
            )

        if status_code == 200:
            api_client.set_token(data["access_token"])
            page.go("/businesses")  # we'll build this next
        else:
            error_text.value = data.get("detail", "Signup failed")

        page.update()

    def main_button_clicked(e):
        if not state["otp_sent"]:
            get_otp_clicked(e)
        else:
            create_account_clicked(e)

    main_button = ft.Container(
        content=ft.Text("GET OTP", color="white", weight=ft.FontWeight.BOLD, size=14),
        bgcolor=Colors.PRIMARY,
        padding=ft.padding.symmetric(vertical=16),
        border_radius=10,
        alignment=ft.Alignment(0, 0),
        width=350,
        on_click=main_button_clicked,
        ink=True,
    )

    def go_to_login(e):
        page.go("/login")

    # ── Card Layout ──────────────────────────────────────────────────
    signup_card = ft.Container(
        width=420,
        padding=40,
        bgcolor="#0a0a14",
        border_radius=20,
        border=ft.border.all(1, Colors.BORDER),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=18,
            controls=[
                ft.Text("Join the Void", size=28, weight=ft.FontWeight.BOLD, color="white"),
                ft.Text("Start your journey as a shop owner.", size=13, color=Colors.TEXT_SECONDARY),

                ft.Container(height=10),
                tab_row,

                name_field,
                phone_field,
                email_field,
                password_field,
                otp_field,

                ft.Container(height=4),
                main_button,

                status_text,
                error_text,

                ft.Container(height=10),
                ft.Row(
                    alignment=ft.MainAxisAlignment.CENTER,
                    controls=[
                        ft.Text("Already have an account? ", size=13, color=Colors.TEXT_SECONDARY),
                        ft.TextButton(
                            "Log in",
                            on_click=go_to_login,
                            style=ft.ButtonStyle(color=Colors.SECONDARY),
                        )
                    ]
                )
            ]
        )
    )

    # ── Page Layout ──────────────────────────────────────────────────
    return ft.View(
        route="/signup",
        padding=0,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(
                expand=True,
                bgcolor="#06060c",
                alignment=ft.Alignment(0, 0),
                padding=40,
                content=signup_card
            )
        ]
    )