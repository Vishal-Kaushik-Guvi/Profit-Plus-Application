import flet as ft
import threading
import time
import random
from app.api_client import api_client

BG = "#020710"
SIDEBAR_BG = "#070816"
BORDER = "#172231"
CYAN = "#16cdf2"
GREEN = "#14d59b"
PURPLE = "#6d22d9"


def BusinessDashboardView(page: ft.Page, business_id: str):
    from app.component.sidebar_view import BusinessSidebar
    sidebar, business_name, business_initials = BusinessSidebar(
        page, business_id, f"/businesses/{business_id}/dashboard"
    )
    error_text = ft.Text("", color="#fb7185", size=12)

    # ── Metric value refs ─────────────────────────────────────────
    gross_sales_val = ft.Text("₹0.00", color="white", size=24,
                              weight=ft.FontWeight.BOLD)
    cash_val = ft.Text("₹0.00", color="white", size=24,
                       weight=ft.FontWeight.BOLD)
    profit_val = ft.Text("₹0.00", color="white", size=24,
                         weight=ft.FontWeight.BOLD)
    margin_badge_val = ft.Text("0% ACCRUED MARGIN", color=CYAN,
                               size=8, weight=ft.FontWeight.BOLD)
    emi_received_val = ft.Text("₹0.00", color="white", size=24,
                               weight=ft.FontWeight.BOLD)
    emi_due_val = ft.Text("₹0.00", color="white", size=24,
                          weight=ft.FontWeight.BOLD)
    emi_due_badge_val = ft.Text("ALL CLEAR", color="#7d899e",
                                size=8, weight=ft.FontWeight.BOLD)

    # GST values
    output_gst_val = ft.Text("₹0.00", color="white", size=12,
                             weight=ft.FontWeight.BOLD)
    input_gst_val = ft.Text("₹0.00", color="white", size=12,
                            weight=ft.FontWeight.BOLD)
    net_gst_val = ft.Text("₹0.00", color="white", size=12,
                          weight=ft.FontWeight.BOLD)



    # ── Badge ─────────────────────────────────────────────────────
    def badge(text_ctrl, color, bgcolor):
        return ft.Container(
            padding=ft.padding.symmetric(horizontal=12, vertical=6),
            border_radius=14,
            bgcolor=bgcolor,
            border=ft.border.all(1, color),
            content=text_ctrl,
        )

    # ── GST value cell ────────────────────────────────────────────
    def gst_cell(label, value_ctrl, highlighted=False):
        return ft.Container(
            expand=True, height=64, padding=14,
            border_radius=10,
            bgcolor="#073342" if highlighted else "#141b27",
            border=ft.border.all(1, "#1e2a39"),
            content=ft.Column(
                spacing=6,
                controls=[
                    ft.Text(label, color="#68758a", size=7),
                    value_ctrl,
                ],
            ),
        )

    # ── Dashboard layout ──────────────────────────────────────────
    dashboard = ft.Container(
        expand=True,
        padding=ft.padding.only(left=32, right=32, top=25, bottom=20),
        content=ft.Column(
            scroll=ft.ScrollMode.AUTO,
            spacing=25,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                        ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text("SHOP MANAGER", color="white",
                                        size=26, weight=ft.FontWeight.BOLD),
                                ft.Text("Store activity for today",
                                        color="#68758a", size=10),
                            ],
                        ),
                        ft.Container(
                            width=145, height=49, border_radius=11,
                            bgcolor=GREEN, alignment=ft.Alignment(0, 0),
                            ink=True,
                            on_click=lambda e: page.go(
                                f"/businesses/{business_id}/billing"),
                            content=ft.Row(
                                tight=True, spacing=10,
                                controls=[
                                    ft.Icon(ft.Icons.ADD_ROUNDED,
                                            color="#03110d", size=19),
                                    ft.Text("NEW BILL", color="#03110d",
                                            size=9,
                                            weight=ft.FontWeight.BOLD),
                                ],
                            ),
                        ),
                    ],
                ),

                # Row 1 — Sales metrics
                ft.Row(
                    spacing=18,
                    controls=[
                        ft.Container(
                            expand=True, height=145, padding=26,
                            border_radius=32, bgcolor="#060b14",
                            border=ft.border.all(1, BORDER),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Gross Sales Today",
                                                    color="#657188", size=9),
                                            ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED,
                                                    color="#3f4b5e", size=14),
                                        ]
                                    ),
                                    gross_sales_val,
                                    ft.Row(controls=[
                                        badge(ft.Text("TOTAL BUSINESS DONE",
                                                      color="#5a9cf0", size=8,
                                                      weight=ft.FontWeight.BOLD),
                                              "#5a9cf0", "#101e32")
                                    ]),
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=True, height=145, padding=26,
                            border_radius=32, bgcolor="#060b14",
                            border=ft.border.all(1, BORDER),
                            gradient=ft.RadialGradient(
                                center=ft.Alignment(0.85, 0),
                                radius=1.1,
                                colors=["#08251f", "#060b14"],
                            ),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Cash Collected Today",
                                                    color="#657188", size=9),
                                            ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED,
                                                    color="#3f4b5e", size=14),
                                        ]
                                    ),
                                    cash_val,
                                    ft.Row(controls=[
                                        badge(ft.Text("LIQUID CASH IN HAND",
                                                      color=GREEN, size=8,
                                                      weight=ft.FontWeight.BOLD),
                                              GREEN, "#07372d")
                                    ]),
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=True, height=145, padding=26,
                            border_radius=32, bgcolor="#060b14",
                            border=ft.border.all(1, BORDER),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("Today's Profit Margin",
                                                    color="#657188", size=9),
                                            ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED,
                                                    color="#3f4b5e", size=14),
                                        ]
                                    ),
                                    profit_val,
                                    ft.Row(controls=[
                                        badge(margin_badge_val,
                                              CYAN, "#082936")
                                    ]),
                                ],
                            ),
                        ),
                    ],
                ),

                # Row 2 — EMI metrics
                ft.Row(
                    spacing=18,
                    controls=[
                        ft.Container(
                            expand=True, height=145, padding=26,
                            border_radius=32, bgcolor="#060b14",
                            border=ft.border.all(1, BORDER),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("EMI Received Today",
                                                    color="#657188", size=9),
                                            ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED,
                                                    color="#3f4b5e", size=14),
                                        ]
                                    ),
                                    emi_received_val,
                                    ft.Row(controls=[
                                        badge(ft.Text("HOVER FOR MONTH",
                                                      color="#f59e0b", size=8,
                                                      weight=ft.FontWeight.BOLD),
                                              "#f59e0b", "#32200d")
                                    ]),
                                ],
                            ),
                        ),
                        ft.Container(
                            expand=True, height=145, padding=26,
                            border_radius=32, bgcolor="#060b14",
                            border=ft.border.all(1, BORDER),
                            content=ft.Column(
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                controls=[
                                    ft.Row(
                                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                        controls=[
                                            ft.Text("EMI Due Today",
                                                    color="#657188", size=9),
                                            ft.Icon(ft.Icons.INFO_OUTLINE_ROUNDED,
                                                    color="#3f4b5e", size=14),
                                        ]
                                    ),
                                    emi_due_val,
                                    ft.Row(controls=[
                                        badge(emi_due_badge_val,
                                              "#7d899e", "#181f2b")
                                    ]),
                                ],
                            ),
                        ),
                    ],
                ),

                # GST Summary
                ft.Container(
                    height=118, padding=26, border_radius=30,
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
                                        ft.Icon(ft.Icons.RECEIPT_LONG_OUTLINED,
                                                color=CYAN, size=18),
                                        ft.Text("GST SUMMARY", color="white",
                                                size=15,
                                                weight=ft.FontWeight.BOLD),
                                    ],
                                ),
                            ),
                            gst_cell("Output GST (Collected)", output_gst_val),
                            gst_cell("Input GST (ITC Paid)", input_gst_val),
                            gst_cell("Net GST Payable", net_gst_val, True),
                        ],
                    ),
                ),

                error_text,
            ],
        ),
    )

    # ── Star background ───────────────────────────────────────────
    stars = [
        (25, 38, 1), (94, 91, 2), (167, 26, 1), (246, 70, 2),
        (325, 19, 1), (402, 112, 2), (487, 44, 1), (566, 86, 2),
        (651, 27, 1), (735, 103, 2), (819, 51, 1), (908, 126, 2),
        (998, 34, 1), (1075, 78, 2), (79, 254, 1), (222, 301, 2),
        (371, 238, 1), (527, 333, 2), (684, 269, 1), (841, 350, 2),
        (1012, 282, 1), (1128, 377, 2), (132, 514, 2), (303, 464, 1),
        (486, 551, 2), (676, 489, 1), (864, 574, 2), (1054, 501, 1),
    ]

    star_controls = [
        ft.Container(
            left=float(x), top=float(y),
            width=size, height=size,
            border_radius=size, bgcolor="#a7b1c2",
            animate_position=800,
        )
        for x, y, size in stars
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
            *star_controls,
        ],
    )

    # ── Animated star thread ──────────────────────────────────────
    _stop_flag = threading.Event()

    def animate_stars():
        time.sleep(0.5)  # small initial delay so the view renders first
        while not _stop_flag.is_set():
            try:
                if page.route != f"/businesses/{business_id}/dashboard":
                    break
                for star in star_controls:
                    star.left = max(
                        0, min(1200, star.left + random.uniform(-50, 50)))
                    star.top = max(
                        0, min(800,  star.top + random.uniform(-50, 50)))
                page.update()
            except Exception:
                break
            time.sleep(0.8)

    t = threading.Thread(target=animate_stars, daemon=True)
    t.start()

    # ── Load data ─────────────────────────────────────────────────
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
            error_text.value = data.get("detail", "Unable to load business")
            page.update()
            return

        name = (data.get("business_name") or "Business").strip()
        business_name.value = name
        business_initials.value = "".join(
            part[0] for part in name.split()[:2]
        ).upper() or "B"
        page.update()

    def load_stats():
        try:
            data, status_code = api_client.get_dashboard_stats(business_id)
        except Exception:
            return

        if status_code != 200:
            return

        gross = data.get("gross_sales_today", 0)
        cash = data.get("cash_collected_today", 0)
        profit = data.get("profit_today", 0)
        margin = data.get("margin_pct", 0)
        emi_recv = data.get("emi_received_today", 0)
        emi_due = data.get("emi_due_today", 0)
        out_gst = data.get("output_gst", 0)
        in_gst = data.get("input_gst", 0)
        net_gst = data.get("net_gst", 0)

        gross_sales_val.value = f"₹{gross:,.2f}"
        cash_val.value = f"₹{cash:,.2f}"
        profit_val.value = f"₹{profit:,.2f}"
        margin_badge_val.value = f"{margin}% ACCRUED MARGIN"
        emi_received_val.value = f"₹{emi_recv:,.2f}"
        emi_due_val.value = f"₹{emi_due:,.2f}"
        emi_due_badge_val.value = (
            f"₹{emi_due:,.2f} DUE" if emi_due > 0 else "ALL CLEAR"
        )
        output_gst_val.value = f"₹{out_gst:,.2f}"
        input_gst_val.value = f"₹{in_gst:,.2f}"
        net_gst_val.value = f"₹{net_gst:,.2f}"
        page.update()

    load_business()
    load_stats()

    return ft.View(
        route=f"/businesses/{business_id}/dashboard",
        padding=0,
        controls=[
            ft.Stack(
                expand=True,
                controls=[
                    background,
                    ft.Row(
                        expand=True, spacing=0,
                        controls=[sidebar, dashboard],
                    ),
                    ft.Container(
                        right=14, bottom=12,
                        width=48, height=48, border_radius=24,
                        bgcolor=CYAN, alignment=ft.Alignment(0, 0),
                        content=ft.Icon(
                            ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED,
                            color="#02101a", size=20,
                        ),
                    ),
                ],
            )
        ],
    )
