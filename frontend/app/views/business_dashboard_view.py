import flet as ft

from app.api_client import api_client


BG = "#020710"
SIDEBAR_BG = "#070816"
BORDER = "#172231"
CYAN = "#16cdf2"
GREEN = "#14d59b"
PURPLE = "#6d22d9"


def BusinessDashboardView(page: ft.Page, business_id: str):
    business_name = ft.Text(
        "Loading business...",
        color="white",
        size=11,
        weight=ft.FontWeight.BOLD,
        max_lines=1,
        overflow=ft.TextOverflow.ELLIPSIS,
    )
    business_initials = ft.Text(
        "--", color="white", size=10, weight=ft.FontWeight.BOLD
    )
    error_text = ft.Text("", color="#fb7185", size=12)

    def back_to_hub(e=None):
        page.go("/businesses")

    def menu_item(icon, label, active=False):
        return ft.Container(
            height=38,
            padding=ft.padding.symmetric(horizontal=16),
            border_radius=8,
            bgcolor="#1c073c" if active else None,
            border=ft.border.all(1, "#32105f") if active else None,
            content=ft.Row(
                spacing=14,
                controls=[
                    ft.Icon(
                        icon,
                        color=PURPLE if active else "#657188",
                        size=16,
                    ),
                    ft.Text(
                        label,
                        color=PURPLE if active else "#7a869b",
                        size=10,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
            ),
        )

    sidebar = ft.Container(
        width=220,
        bgcolor=SIDEBAR_BG,
        border=ft.border.only(right=ft.BorderSide(1, "#171b29")),
        padding=ft.padding.only(left=16, right=16, top=24, bottom=14),
        content=ft.Column(
            controls=[
                ft.Container(
                    padding=ft.padding.only(left=6),
                    content=ft.Column(
                        spacing=9,
                        controls=[
                            ft.Text(
                                "PROFIT",
                                color="white",
                                size=17,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "B U S I N E S S   D A S H B O A R D",
                                color="#5d687d",
                                size=7,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                ),
                ft.Container(height=26),
                ft.Text(
                    "  MENU",
                    color="#5d687d",
                    size=7,
                    weight=ft.FontWeight.BOLD,
                ),
                ft.Container(height=10),
                menu_item(ft.Icons.HOME_OUTLINED, "Dashboard", True),
                menu_item(ft.Icons.RECEIPT_LONG_OUTLINED, "Billing"),
                menu_item(ft.Icons.INVENTORY_2_OUTLINED, "Products"),
                menu_item(ft.Icons.WAREHOUSE_OUTLINED, "Inventory"),
                menu_item(ft.Icons.SCHEDULE_OUTLINED, "EMI Management"),
                menu_item(ft.Icons.RECEIPT_OUTLINED, "Sales History"),
                menu_item(ft.Icons.BAR_CHART_ROUNDED, "Analytics"),
                menu_item(ft.Icons.CALCULATE_OUTLINED, "Taxation"),
                menu_item(ft.Icons.GROUP_OUTLINED, "Customers"),
                menu_item(ft.Icons.CREDIT_CARD_OUTLINED, "Subscription"),
                ft.Container(expand=True),
                ft.Divider(color="#171b29", height=1),
                ft.Container(height=12),
                ft.Container(
                    height=68,
                    padding=12,
                    border_radius=11,
                    border=ft.border.all(1, "#1a2130"),
                    content=ft.Row(
                        spacing=11,
                        controls=[
                            ft.Container(
                                width=37,
                                height=37,
                                border_radius=19,
                                border=ft.border.all(1, "#496078"),
                                bgcolor="#111b29",
                                alignment=ft.Alignment(0, 0),
                                content=business_initials,
                            ),
                            ft.Container(
                                width=125,
                                content=ft.Column(
                                    alignment=ft.MainAxisAlignment.CENTER,
                                    spacing=3,
                                    controls=[
                                        business_name,
                                        ft.Text(
                                            "BUSINESS PROFILE",
                                            color="#59657a",
                                            size=7,
                                        ),
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
                ft.Container(height=10),
                ft.Container(
                    height=38,
                    border_radius=8,
                    on_click=back_to_hub,
                    ink=True,
                    content=ft.Row(
                        spacing=12,
                        controls=[
                            ft.Icon(
                                ft.Icons.ARROW_BACK_ROUNDED,
                                color="#657188",
                                size=16,
                            ),
                            ft.Text(
                                "BACK TO HUB",
                                color="#657188",
                                size=8,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                ),
            ],
        ),
    )

    def badge(text, color, bgcolor):
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=14,
            bgcolor=bgcolor,
            border=ft.border.all(1, color),
            content=ft.Text(
                text, color=color, size=8, weight=ft.FontWeight.BOLD
            ),
        )

    def metric_card(title, value, badge_text, accent, badge_bg, expand=1):
        return ft.Container(
            expand=expand,
            height=145,
            padding=26,
            border_radius=32,
            bgcolor="#060b14",
            border=ft.border.all(1, BORDER),
            gradient=(
                ft.RadialGradient(
                    center=ft.Alignment(0.85, 0),
                    radius=1.1,
                    colors=["#08251f", "#060b14"],
                )
                if accent == GREEN
                else None
            ),
            content=ft.Column(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                controls=[
                    ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                            ft.Text(title, color="#657188", size=9),
                            ft.Icon(
                                ft.Icons.INFO_OUTLINE_ROUNDED,
                                color="#3f4b5e",
                                size=14,
                            ),
                        ],
                    ),
                    ft.Text(
                        value,
                        color="white",
                        size=24,
                        weight=ft.FontWeight.BOLD,
                    ),
                    ft.Row(controls=[badge(badge_text, accent, badge_bg)]),
                ],
            ),
        )

    def gst_value(label, value, highlighted=False):
        return ft.Container(
            expand=True,
            height=64,
            padding=14,
            border_radius=10,
            bgcolor="#073342" if highlighted else "#141b27",
            border=ft.border.all(1, "#1e2a39"),
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Text(label, color="#68758a", size=7),
                    ft.Text(
                        value,
                        color="white",
                        size=12,
                        weight=ft.FontWeight.BOLD,
                    ),
                ],
            ),
        )

    gst_summary = ft.Container(
        height=118,
        padding=26,
        border_radius=30,
        bgcolor="#080d16",
        border=ft.border.all(1, BORDER),
        content=ft.Row(
            spacing=24,
            controls=[
                ft.Container(
                    width=145,
                    content=ft.Row(
                        spacing=12,
                        controls=[
                            ft.Icon(
                                ft.Icons.RECEIPT_LONG_OUTLINED,
                                color=CYAN,
                                size=18,
                            ),
                            ft.Text(
                                "GST SUMMARY",
                                color="white",
                                size=15,
                                weight=ft.FontWeight.BOLD,
                            ),
                        ],
                    ),
                ),
                gst_value("Output GST (Collected)", "₹0.00"),
                gst_value("Input GST (ITC Paid)", "₹0.00"),
                gst_value("Net GST Payable", "₹0.00", True),
            ],
        ),
    )

    dashboard = ft.Container(
        expand=True,
        padding=ft.padding.only(left=32, right=32, top=25, bottom=20),
        content=ft.Column(
            spacing=25,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text(
                                    "SHOP MANAGER",
                                    color="white",
                                    size=26,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    "Store activity for today",
                                    color="#68758a",
                                    size=10,
                                ),
                            ],
                        ),
                        ft.Container(
                            width=145,
                            height=49,
                            border_radius=11,
                            bgcolor=GREEN,
                            alignment=ft.Alignment(0, 0),
                            ink=True,
                            content=ft.Row(
                                tight=True,
                                spacing=10,
                                controls=[
                                    ft.Icon(
                                        ft.Icons.ADD_ROUNDED,
                                        color="#03110d",
                                        size=19,
                                    ),
                                    ft.Text(
                                        "NEW BILL",
                                        color="#03110d",
                                        size=9,
                                        weight=ft.FontWeight.BOLD,
                                    ),
                                ],
                            ),
                        ),
                    ],
                ),
                ft.Row(
                    spacing=18,
                    controls=[
                        metric_card(
                            "Gross Sales Today",
                            "₹0.00",
                            "TOTAL BUSINESS DONE",
                            "#5a9cf0",
                            "#101e32",
                        ),
                        metric_card(
                            "Cash Collected Today",
                            "₹0.00",
                            "LIQUID CASH IN HAND",
                            GREEN,
                            "#07372d",
                        ),
                        metric_card(
                            "Today's Profit Margin",
                            "₹0.00",
                            "0% ACCRUED MARGIN",
                            CYAN,
                            "#082936",
                        ),
                    ],
                ),
                ft.Row(
                    spacing=18,
                    controls=[
                        metric_card(
                            "EMI Received Today",
                            "₹0.00",
                            "HOVER FOR MONTH",
                            "#f59e0b",
                            "#32200d",
                        ),
                        metric_card(
                            "EMI Due Today",
                            "₹0.00",
                            "ALL CLEAR",
                            "#7d899e",
                            "#181f2b",
                        ),
                    ],
                ),
                gst_summary,
                error_text,
            ],
        ),
    )

    stars = [
        (25, 38, 1), (94, 91, 2), (167, 26, 1), (246, 70, 2),
        (325, 19, 1), (402, 112, 2), (487, 44, 1), (566, 86, 2),
        (651, 27, 1), (735, 103, 2), (819, 51, 1), (908, 126, 2),
        (998, 34, 1), (1075, 78, 2), (79, 254, 1), (222, 301, 2),
        (371, 238, 1), (527, 333, 2), (684, 269, 1), (841, 350, 2),
        (1012, 282, 1), (1128, 377, 2), (132, 514, 2), (303, 464, 1),
        (486, 551, 2), (676, 489, 1), (864, 574, 2), (1054, 501, 1),
    ]
    background = ft.Stack(
        expand=True,
        controls=[
            ft.Container(
                expand=True,
                gradient=ft.RadialGradient(
                    center=ft.Alignment(0.75, 0.35),
                    radius=1.2,
                    colors=["#06151f", BG],
                ),
            ),
            *[
                ft.Container(
                    left=x,
                    top=y,
                    width=size,
                    height=size,
                    border_radius=size,
                    bgcolor="#a7b1c2",
                )
                for x, y, size in stars
            ],
        ],
    )

    def load_business():
        try:
            data, status_code = api_client.get_business(business_id)
        except Exception:
            error_text.value = "Unable to connect to the server"
            page.update()
            return

        if status_code == 401:
            api_client.set_token(None)
            page.go("/login")
            return
        if status_code == 404:
            page.go("/businesses")
            return
        if status_code != 200:
            error_text.value = data.get(
                "detail", "Unable to load this business"
            )
            page.update()
            return

        name = (data.get("business_name") or "Business").strip()
        business_name.value = name
        business_initials.value = "".join(
            part[0] for part in name.split()[:2]
        ).upper() or "B"
        page.update()

    load_business()

    return ft.View(
        route=f"/businesses/{business_id}/dashboard",
        padding=0,
        controls=[
            ft.Stack(
                expand=True,
                controls=[
                    background,
                    ft.Row(
                        expand=True,
                        spacing=0,
                        controls=[sidebar, dashboard],
                    ),
                    ft.Container(
                        right=14,
                        bottom=12,
                        width=48,
                        height=48,
                        border_radius=24,
                        bgcolor=CYAN,
                        alignment=ft.Alignment(0, 0),
                        content=ft.Icon(
                            ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED,
                            color="#02101a",
                            size=20,
                        ),
                    ),
                ],
            )
        ],
    )
