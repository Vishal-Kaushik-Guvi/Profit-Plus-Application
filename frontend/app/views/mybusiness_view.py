import flet as ft

from app.api_client import api_client
from app.theme import Colors


def MyBusinessView(page: ft.Page):
    businesses_column = ft.Column(spacing=12)
    error_text = ft.Text("", color=Colors.DANGER, size=12)
    status_text = ft.Text("", color=Colors.SUCCESS, size=12)

    def logout(e):
        api_client.set_token(None)
        page.go("/login")

    def field_style():
        return ft.TextStyle(
            color=Colors.TEXT_SECONDARY,
            size=11,
            weight=ft.FontWeight.BOLD,
        )

    def input_field(label, hint="", width=260, keyboard_type=None):
        return ft.TextField(
            label=label,
            hint_text=hint,
            width=width,
            color="white",
            label_style=field_style(),
            border_color=Colors.BORDER,
            focused_border_color=Colors.SECONDARY,
            bgcolor="#0d0d18",
            border_radius=8,
            keyboard_type=keyboard_type,
        )

    business_name_field = input_field("BUSINESS NAME", "Your shop name", 330)
    phone_field = input_field("PHONE", "1234567890", keyboard_type=ft.KeyboardType.NUMBER)
    email_field = input_field("EMAIL", "shop@example.com")
    gst_field = input_field("GST", "Optional")
    address_field = input_field("ADDRESS", "Street / area", 330)
    city_field = input_field("CITY")
    pincode_field = input_field("PINCODE", keyboard_type=ft.KeyboardType.NUMBER)
    state_field = input_field("STATE")
    country_field = input_field("COUNTRY", "India")

    create_button = ft.Container(
        content=ft.Text("ADD BUSINESS", color="white", weight=ft.FontWeight.BOLD, size=13),
        bgcolor=Colors.PRIMARY,
        padding=ft.padding.symmetric(horizontal=22, vertical=14),
        border_radius=8,
        alignment=ft.Alignment(0, 0),
        ink=True,
    )

    def set_create_button(text):
        create_button.content = ft.Text(
            text,
            color="white",
            weight=ft.FontWeight.BOLD,
            size=13,
        )

    def set_create_loading():
        create_button.content = ft.Row(
            tight=True,
            alignment=ft.MainAxisAlignment.CENTER,
            controls=[
                ft.ProgressRing(width=16, height=16, stroke_width=2, color="white")
            ],
        )

    def business_card(business):
        location = ", ".join(
            part for part in [
                business.get("city"),
                business.get("state"),
            ]
            if part
        )
        subtitle = location or business.get("email") or "No location added"

        return ft.Container(
            padding=18,
            border_radius=8,
            bgcolor="#0d0d18",
            border=ft.border.all(1, Colors.BORDER),
            content=ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Row(
                        spacing=14,
                        controls=[
                            ft.Container(
                                width=42,
                                height=42,
                                border_radius=8,
                                bgcolor="#15162a",
                                alignment=ft.Alignment(0, 0),
                                content=ft.Icon(
                                    ft.Icons.STORE_MALL_DIRECTORY_ROUNDED,
                                    color=Colors.SECONDARY,
                                    size=22,
                                ),
                            ),
                            ft.Column(
                                spacing=4,
                                controls=[
                                    ft.Text(
                                        business.get("business_name", "Untitled business"),
                                        color="white",
                                        size=16,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                    ft.Text(subtitle, color=Colors.TEXT_SECONDARY, size=12),
                                ],
                            ),
                        ],
                    ),
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=10, vertical=6),
                        border_radius=6,
                        bgcolor="#12251a",
                        content=ft.Text(
                            business.get("subscription_type", "FREE"),
                            color=Colors.SUCCESS,
                            size=11,
                            weight=ft.FontWeight.BOLD,
                        ),
                    ),
                ],
            ),
        )

    def render_businesses(businesses):
        businesses_column.controls.clear()

        if not businesses:
            businesses_column.controls.append(
                ft.Container(
                    padding=24,
                    border_radius=8,
                    bgcolor="#0d0d18",
                    border=ft.border.all(1, Colors.BORDER),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Column(
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=8,
                        controls=[
                            ft.Icon(ft.Icons.STORE_OUTLINED, color=Colors.TEXT_MUTED, size=34),
                            ft.Text("No businesses yet", color="white", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text("Add your first shop below.", color=Colors.TEXT_SECONDARY, size=12),
                        ],
                    ),
                )
            )
            return

        for business in businesses:
            businesses_column.controls.append(business_card(business))

    def load_businesses():
        error_text.value = ""
        try:
            data, status_code = api_client.get_my_businesses()
        except Exception:
            error_text.value = "Unable to connect to the server"
            render_businesses([])
            page.update()
            return

        if status_code == 200:
            render_businesses(data)
        elif status_code == 401:
            api_client.set_token(None)
            page.go("/login")
            return
        else:
            error_text.value = data.get("detail", "Failed to load businesses")
            render_businesses([])

        page.update()

    def create_business_clicked(e):
        error_text.value = ""
        status_text.value = ""
        business_name = (business_name_field.value or "").strip()

        if not business_name:
            error_text.value = "Enter your business name"
            page.update()
            return

        set_create_loading()
        page.update()

        try:
            data, status_code = api_client.create_business(
                business_name=business_name,
                phone=(phone_field.value or "").strip(),
                email=(email_field.value or "").strip(),
                address=(address_field.value or "").strip(),
                city=(city_field.value or "").strip(),
                pincode=(pincode_field.value or "").strip(),
                state=(state_field.value or "").strip(),
                country=(country_field.value or "").strip(),
                gst=(gst_field.value or "").strip(),
            )
        except Exception:
            error_text.value = "Unable to connect to the server"
            set_create_button("ADD BUSINESS")
            page.update()
            return

        set_create_button("ADD BUSINESS")

        if status_code == 200:
            for field in [
                business_name_field,
                phone_field,
                email_field,
                gst_field,
                address_field,
                city_field,
                pincode_field,
                state_field,
                country_field,
            ]:
                field.value = ""
            status_text.value = "Business added successfully"
            load_businesses()
            return

        if status_code == 401:
            api_client.set_token(None)
            page.go("/login")
            return

        error_text.value = data.get("detail", "Failed to add business")
        page.update()

    create_button.on_click = create_business_clicked

    header = ft.Container(
        padding=ft.padding.symmetric(horizontal=34, vertical=22),
        border=ft.border.only(bottom=ft.BorderSide(1, Colors.BORDER)),
        content=ft.Row(
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            controls=[
                ft.Row(
                    spacing=12,
                    controls=[
                        ft.Container(
                            width=36,
                            height=36,
                            border_radius=8,
                            bgcolor=Colors.PRIMARY,
                            alignment=ft.Alignment(0, 0),
                            content=ft.Icon(ft.Icons.BOLT_ROUNDED, color="white", size=19),
                        ),
                        ft.Text("Profit Plus", size=18, weight=ft.FontWeight.BOLD, color="white"),
                    ],
                ),
                ft.TextButton(
                    "Log out",
                    on_click=logout,
                    style=ft.ButtonStyle(color=Colors.TEXT_SECONDARY),
                ),
            ],
        ),
    )

    form_panel = ft.Container(
        padding=24,
        border_radius=8,
        bgcolor="#0a0a14",
        border=ft.border.all(1, Colors.BORDER),
        content=ft.Column(
            spacing=16,
            controls=[
                ft.Text("Add Business", color="white", size=18, weight=ft.FontWeight.BOLD),
                ft.Row(wrap=True, spacing=14, run_spacing=14, controls=[
                    business_name_field,
                    phone_field,
                    email_field,
                    gst_field,
                    address_field,
                    city_field,
                    pincode_field,
                    state_field,
                    country_field,
                ]),
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(spacing=4, controls=[status_text, error_text]),
                        create_button,
                    ],
                ),
            ],
        ),
    )

    content = ft.Container(
        expand=True,
        padding=34,
        content=ft.Column(
            spacing=22,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=6,
                            controls=[
                                ft.Text("My Businesses", color="white", size=30, weight=ft.FontWeight.BOLD),
                                ft.Text("Choose or register a shop to continue.", color=Colors.TEXT_SECONDARY, size=13),
                            ],
                        ),
                    ],
                ),
                businesses_column,
                form_panel,
            ],
        ),
    )

    load_businesses()

    return ft.View(
        route="/businesses",
        padding=0,
        scroll=ft.ScrollMode.AUTO,
        controls=[
            ft.Container(
                expand=True,
                bgcolor="#06060c",
                content=ft.Column(
                    spacing=0,
                    controls=[header, content],
                ),
            )
        ],
    )
