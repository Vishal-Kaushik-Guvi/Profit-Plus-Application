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


def InventoryView(page: ft.Page, business_id: str):
    from app.component.sidebar_view import BusinessSidebar

    sidebar, business_name_text, business_initials_text = BusinessSidebar(
        page, business_id, f"/businesses/{business_id}/inventory"
    )

    search_ref = ft.Ref[ft.TextField]()
    all_rows = []

    # ── Table header ──────────────────────────────────────────────
    def col_header(label, flex):
        return ft.Container(
            expand=flex,
            content=ft.Text(label, color="#59657a", size=9,
                            weight=ft.FontWeight.BOLD),
        )

    table_header = ft.Container(
        padding=ft.padding.symmetric(horizontal=24, vertical=14),
        border=ft.border.only(bottom=ft.BorderSide(1, "#131b2a")),
        content=ft.Row(
            controls=[
                col_header("PRODUCT NAME", 4),
                col_header("QUANTITY", 2),
                col_header("UNIT PRICE", 2),
                col_header("STATUS", 2),
                col_header("ACTIONS", 3),
            ],
        ),
    )

    # ── Table body ────────────────────────────────────────────────
    table_body = ft.Column(spacing=0)

    empty_state = ft.Container(
        visible=False,
        padding=ft.padding.symmetric(vertical=60),
        alignment=ft.Alignment(0, 0),
        content=ft.Column(
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=14,
            controls=[
                ft.Container(
                    width=72, height=72, border_radius=36,
                    bgcolor="#0d1a27",
                    border=ft.border.all(1, "#1a2e40"),
                    alignment=ft.Alignment(0, 0),
                    content=ft.Icon(ft.Icons.WAREHOUSE_OUTLINED,
                                    color="#2a4257", size=32),
                ),
                ft.Text("NO INVENTORY FOUND", color="white", size=16,
                        weight=ft.FontWeight.BOLD),
                ft.Text("Add products first to manage inventory.",
                        color="#59657a", size=12),
            ],
        ),
    )

    def make_row(item, index):
        product = item.get("product") or {}
        name = product.get("product_name") or item.get(
            "product_name") or "Unknown"
        brand = product.get("brand") or item.get("brand") or ""
        stock = item.get("stock_quantity", 0) or 0
        unit = (item.get("unit") or "PCS").upper()
        price = item.get("selling_price", 0) or 0
        inv_id = item.get("id", "")
        product_id = item.get("product_id", "")
        in_stock = stock > 0

        row_bg = "#070d17" if index % 2 == 0 else "#050b14"

        def on_adjust(e):
            page.go(
                f"/businesses/{business_id}/inventory/{inv_id}/restock"
            )

        def on_delete(e):
            pass  # TODO: confirm dialog

        return ft.Container(
            bgcolor=row_bg,
            padding=ft.padding.symmetric(horizontal=24, vertical=18),
            border=ft.border.only(bottom=ft.BorderSide(1, "#0e1622")),
            content=ft.Row(
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    # Product Name + Brand
                    ft.Container(
                        expand=4,
                        content=ft.Row(
                            spacing=10,
                            controls=[
                                ft.Container(
                                    width=36, height=36,
                                    border_radius=10,
                                    bgcolor="#0d1a27",
                                    border=ft.border.all(1, "#1a2e40"),
                                    alignment=ft.Alignment(0, 0),
                                    content=ft.Icon(
                                        ft.Icons.INVENTORY_2_OUTLINED,
                                        color=CYAN, size=16,
                                    ),
                                ),
                                ft.Row(
                                    spacing=6,
                                    controls=[
                                        ft.Text(name, color="white",
                                                size=13,
                                                weight=ft.FontWeight.BOLD),
                                        ft.Text(
                                            f"({brand})" if brand else "",
                                            color="#59657a", size=11,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),

                    # Quantity
                    ft.Container(
                        expand=2,
                        content=ft.Row(
                            spacing=5,
                            controls=[
                                ft.Text(f"{int(stock)}", color="white",
                                        size=13, weight=ft.FontWeight.BOLD),
                                ft.Text(unit, color="#59657a", size=11),
                            ],
                        ),
                    ),

                    # Unit Price
                    ft.Container(
                        expand=2,
                        content=ft.Row(
                            spacing=2,
                            controls=[
                                ft.Text(f"₹{int(price):,}", color="white",
                                        size=13, weight=ft.FontWeight.BOLD),
                                ft.Text(
                                    f".{int((price % 1) * 100):02d}",
                                    color="#3d4a5c", size=10,
                                ),
                            ],
                        ),
                    ),

                    # Status badge
                    ft.Container(
                        expand=2,
                        content=ft.Container(
                            padding=ft.padding.symmetric(
                                horizontal=12, vertical=6),
                            border_radius=20,
                            bgcolor="#071a14" if in_stock else "#1a0710",
                            border=ft.border.all(
                                1, "#0e3326" if in_stock else "#3a0e20"),
                            content=ft.Text(
                                "IN STOCK" if in_stock else "OUT OF STOCK",
                                color=GREEN if in_stock else "#fb7185",
                                size=9, weight=ft.FontWeight.BOLD,
                            ),
                        ),
                    ),

                    # Actions
                    ft.Container(
                        expand=3,
                        content=ft.Row(
                            spacing=10,
                            controls=[
                                # Stock Adj button
                                ft.Container(
                                    height=36,
                                    padding=ft.padding.symmetric(
                                        horizontal=14),
                                    border_radius=8,
                                    bgcolor="#071a14",
                                    border=ft.border.all(1, "#0e3326"),
                                    alignment=ft.Alignment(0, 0),
                                    ink=True,
                                    on_click=on_adjust,
                                    content=ft.Row(
                                        tight=True, spacing=6,
                                        controls=[
                                            ft.Icon(ft.Icons.ADD_ROUNDED,
                                                    color=GREEN, size=13),
                                            ft.Text("STOCK ADJ.",
                                                    color=GREEN, size=9,
                                                    weight=ft.FontWeight.BOLD),
                                        ],
                                    ),
                                ),
                                # Delete button
                                ft.Container(
                                    width=36, height=36,
                                    border_radius=8,
                                    bgcolor="#0d1a27",
                                    border=ft.border.all(1, "#1a2e40"),
                                    alignment=ft.Alignment(0, 0),
                                    ink=True,
                                    on_click=on_delete,
                                    content=ft.Icon(
                                        ft.Icons.DELETE_OUTLINE_ROUNDED,
                                        color="#657188", size=16,
                                    ),
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    def render_rows(data):
        table_body.controls.clear()
        if not data:
            empty_state.visible = True
        else:
            empty_state.visible = False
            for i, item in enumerate(data):
                table_body.controls.append(make_row(item, i))
        page.update()

    def filter_items(e=None):
        query = (search_ref.current.value or "").strip().lower()
        if not query:
            render_rows(all_rows)
            return
        filtered = [
            r for r in all_rows
            if query in (
                (r.get("product") or {}).get("product_name") or
                r.get("product_name") or ""
            ).lower()
        ]
        render_rows(filtered)

    # ── Main content ──────────────────────────────────────────────
    main_content = ft.Container(
        expand=True,
        padding=ft.padding.only(left=36, right=36, top=32, bottom=24),
        content=ft.Column(
            spacing=24,
            controls=[
                # Header row
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text("Inventory", color="white",
                                        size=34, weight=ft.FontWeight.BOLD),
                                ft.Text("MANAGE ITEMS & STOCK",
                                        color="#59657a", size=9,
                                        weight=ft.FontWeight.BOLD),
                            ],
                        ),
                        ft.Row(
                            spacing=14,
                            controls=[
                                # Search
                                ft.Container(
                                    width=240, height=44,
                                    border_radius=12,
                                    bgcolor="#070d17",
                                    border=ft.border.all(1, "#1a2535"),
                                    padding=ft.padding.symmetric(
                                        horizontal=14),
                                    content=ft.Row(
                                        spacing=10,
                                        controls=[
                                            ft.Icon(ft.Icons.SEARCH_ROUNDED,
                                                    color="#3d4a5c",
                                                    size=16),
                                            ft.TextField(
                                                ref=search_ref,
                                                hint_text="Search items...",
                                                hint_style=ft.TextStyle(
                                                    color="#3d4a5c",
                                                    size=12),
                                                border=ft.InputBorder.NONE,
                                                color="white",
                                                text_size=12,
                                                expand=True,
                                                on_change=filter_items,
                                            ),
                                        ],
                                    ),
                                ),
                                # Quick Add button
                                ft.Container(
                                    height=44,
                                    padding=ft.padding.symmetric(
                                        horizontal=20),
                                    border_radius=12,
                                    bgcolor=CYAN,
                                    alignment=ft.Alignment(0, 0),
                                    ink=True,
                                    on_click=lambda e: page.go(
                                        f"/businesses/{business_id}/products/add"
                                    ),
                                    content=ft.Row(
                                        tight=True, spacing=8,
                                        controls=[
                                            ft.Icon(ft.Icons.BOLT_ROUNDED,
                                                    color="#02101a",
                                                    size=16),
                                            ft.Text("QUICK ADD",
                                                    color="#02101a",
                                                    size=9,
                                                    weight=ft.FontWeight.BOLD),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),

                # Table card
                ft.Container(
                    expand=True,
                    border_radius=16,
                    bgcolor="#070d17",
                    border=ft.border.all(1, "#131b2a"),
                    clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
                    content=ft.Column(
                        spacing=0,
                        controls=[
                            table_header,
                            ft.Container(
                                expand=True,
                                content=ft.Column(
                                    scroll=ft.ScrollMode.AUTO,
                                    spacing=0,
                                    controls=[
                                        table_body,
                                        empty_state,
                                    ],
                                ),
                            ),
                        ],
                    ),
                ),
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

    def animate_stars():
        time.sleep(0.5)
        while True:
            try:
                for star in star_controls:
                    star.left = max(
                        0, min(1200, star.left + random.uniform(-50, 50)))
                    star.top = max(
                        0, min(800, star.top + random.uniform(-50, 50)))
                page.update()
            except Exception:
                break
            time.sleep(0.8)

    threading.Thread(target=animate_stars, daemon=True).start()

    # ── Load data ─────────────────────────────────────────────────
    def load_data():
        try:
            data, status = api_client.get_business(business_id)
            if status == 200:
                name = (data.get("business_name") or "Business").strip()
                business_name_text.value = name
                business_initials_text.value = "".join(
                    p[0] for p in name.split()[:2]
                ).upper() or "B"
        except Exception:
            pass

        try:
            data, status = api_client.get_inventory(business_id)
            if status == 401:
                api_client.set_token(None)
                page.go("/login")
                return
            if status == 200:
                all_rows.clear()
                all_rows.extend(data if isinstance(data, list) else [])
                render_rows(all_rows)
                return
        except Exception:
            pass

        render_rows([])

    load_data()

    return ft.View(
        route=f"/businesses/{business_id}/inventory",
        padding=0,
        controls=[
            ft.Stack(
                expand=True,
                controls=[
                    background,
                    ft.Row(
                        expand=True, spacing=0,
                        controls=[sidebar, main_content],
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
