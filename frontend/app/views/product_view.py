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


def ProductsView(page: ft.Page, business_id: str):
    from app.component.sidebar_view import BusinessSidebar

    sidebar, business_name_text, business_initials_text = BusinessSidebar(
        page, business_id, f"/businesses/{business_id}/products"
    )

    search_value = ft.Ref[ft.TextField]()
    products_grid = ft.GridView(
        expand=True,
        runs_count=3,
        max_extent=340,
        spacing=20,
        run_spacing=20,
        padding=ft.padding.only(left=4, right=12, top=4, bottom=18),
    )
    all_products = []
    inv_map = {}  # product_id -> inventory_id
    inventory_by_product = {}

    empty_state = ft.Column(
        visible=False,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=14,
        controls=[
            ft.Container(
                width=80,
                height=80,
                border_radius=40,
                bgcolor="#0d1a27",
                border=ft.border.all(1, "#1a2e40"),
                alignment=ft.Alignment(0, 0),
                content=ft.Icon(
                    ft.Icons.INVENTORY_2_OUTLINED, color="#2a4257", size=36
                ),
            ),
            ft.Text(
                "NO PRODUCTS FOUND", color="white", size=18, weight=ft.FontWeight.BOLD
            ),
            ft.Text("Add your first product to get started.", color="#59657a", size=12),
        ],
    )

    # ── Product card ──────────────────────────────────────────────
    def product_card(product):
        pid = product.get("id", "")
        name = product.get("product_name") or "Unnamed Product"
        inventory = inventory_by_product.get(str(pid), {})
        stock = inventory.get("stock_quantity", 0) or 0
        unit = (inventory.get("unit") or "PCS").upper()
        price = inventory.get("selling_price", 0) or 0
        brand = product.get("brand") or "N/A"
        ptype = product.get("business_type") or "N/A"
        category = (product.get("category") or "")[:5].upper() or "GEN"
        low_stock = stock <= (inventory.get("minimum_stock_alert", 5) or 5)
        stock_color = "#fb7185" if low_stock else CYAN

        def on_manage(e):
            inv_id = inv_map.get(str(pid))
            if inv_id:
                page.go(f"/businesses/{business_id}/inventory/{inv_id}/restock")
                return

            try:
                data, status = api_client.create_inventory(business_id, pid)
            except Exception:
                page.go(f"/businesses/{business_id}/inventory")
                return

            if status in (200, 201) and data.get("id"):
                page.go(f"/businesses/{business_id}/inventory/{data['id']}/restock")
            elif status == 401:
                api_client.set_token(None)
                page.go("/login")
            else:
                page.go(f"/businesses/{business_id}/inventory")

        def on_edit(e):
            page.go(f"/businesses/{business_id}/products/{pid}/edit")

        def on_delete(e):
            try:
                data, status = api_client.delete_product(pid)
            except Exception:
                return

            if status == 401:
                api_client.set_token(None)
                page.go("/login")
                return

            if status in (200, 204):
                load_data()

        return ft.Container(
            width=320,
            height=280,
            border_radius=20,
            bgcolor="#070d17",
            border=ft.border.all(1, "#1a2535"),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            content=ft.Column(
                spacing=0,
                controls=[
                    # Top section
                    ft.Container(
                        padding=ft.padding.only(left=20, right=16, top=18, bottom=12),
                        content=ft.Column(
                            spacing=14,
                            controls=[
                                ft.Row(
                                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                                    controls=[
                                        ft.Row(
                                            spacing=12,
                                            controls=[
                                                ft.Container(
                                                    width=52,
                                                    height=52,
                                                    border_radius=14,
                                                    bgcolor="#0d1a27",
                                                    border=ft.border.all(1, "#1a2e40"),
                                                    alignment=ft.Alignment(0, 0),
                                                    content=ft.Icon(
                                                        ft.Icons.INVENTORY_2_OUTLINED,
                                                        color=CYAN,
                                                        size=24,
                                                    ),
                                                ),
                                            ],
                                        ),
                                        ft.Row(
                                            spacing=8,
                                            controls=[
                                                ft.Container(
                                                    padding=ft.padding.symmetric(
                                                        horizontal=10, vertical=5
                                                    ),
                                                    border_radius=20,
                                                    bgcolor="#0d1a27",
                                                    border=ft.border.all(1, "#1a2e40"),
                                                    content=ft.Text(
                                                        category,
                                                        color="white",
                                                        size=9,
                                                        weight=ft.FontWeight.BOLD,
                                                    ),
                                                ),
                                                ft.Container(
                                                    width=32,
                                                    height=32,
                                                    border_radius=8,
                                                    bgcolor="#0d1a27",
                                                    border=ft.border.all(1, "#1a2e40"),
                                                    alignment=ft.Alignment(0, 0),
                                                    on_click=on_edit,
                                                    ink=True,
                                                    content=ft.Icon(
                                                        ft.Icons.EDIT_OUTLINED,
                                                        color="#657188",
                                                        size=14,
                                                    ),
                                                ),
                                                ft.Container(
                                                    width=32,
                                                    height=32,
                                                    border_radius=8,
                                                    bgcolor="#0d1a27",
                                                    border=ft.border.all(1, "#1a2e40"),
                                                    alignment=ft.Alignment(0, 0),
                                                    on_click=on_delete,
                                                    ink=True,
                                                    content=ft.Icon(
                                                        ft.Icons.DELETE_OUTLINE_ROUNDED,
                                                        color="#657188",
                                                        size=14,
                                                    ),
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                ft.Text(
                                    name,
                                    color="white",
                                    size=22,
                                    weight=ft.FontWeight.BOLD,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                ),
                            ],
                        ),
                    ),
                    # Stock & Price row
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=20, vertical=10),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(
                                    spacing=4,
                                    controls=[
                                        ft.Text(
                                            "STOCK",
                                            color="#4a5568",
                                            size=8,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Row(
                                            spacing=5,
                                            controls=[
                                                ft.Text(
                                                    str(stock),
                                                    color=stock_color,
                                                    size=14,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                                ft.Text(
                                                    unit,
                                                    color=stock_color,
                                                    size=14,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                                ft.Column(
                                    spacing=4,
                                    horizontal_alignment=ft.CrossAxisAlignment.END,
                                    controls=[
                                        ft.Text(
                                            "PRICE",
                                            color="#4a5568",
                                            size=8,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Row(
                                            spacing=2,
                                            controls=[
                                                ft.Text(
                                                    f"₹{int(price):,}",
                                                    color="white",
                                                    size=14,
                                                    weight=ft.FontWeight.BOLD,
                                                ),
                                                ft.Text(
                                                    ".00", color="#3d4a5c", size=10
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    # Brand & Type row
                    ft.Container(
                        padding=ft.padding.symmetric(horizontal=20, vertical=6),
                        content=ft.Row(
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            controls=[
                                ft.Column(
                                    spacing=4,
                                    controls=[
                                        ft.Text(
                                            "BRAND",
                                            color="#4a5568",
                                            size=8,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            brand,
                                            color="white",
                                            size=12,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ],
                                ),
                                ft.Column(
                                    spacing=4,
                                    horizontal_alignment=ft.CrossAxisAlignment.END,
                                    controls=[
                                        ft.Text(
                                            "TYPE",
                                            color="#4a5568",
                                            size=8,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                        ft.Text(
                                            ptype,
                                            color=CYAN,
                                            size=12,
                                            weight=ft.FontWeight.BOLD,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ),
                    ft.Container(expand=True),
                    # Manage Stock button
                    ft.Container(
                        margin=ft.margin.only(left=16, right=16, bottom=16),
                        height=44,
                        border_radius=12,
                        bgcolor="#071a14",
                        border=ft.border.all(1, "#0e3326"),
                        alignment=ft.Alignment(0, 0),
                        on_click=on_manage,
                        ink=True,
                        content=ft.Row(
                            tight=True,
                            spacing=8,
                            controls=[
                                ft.Icon(ft.Icons.ADD_ROUNDED, color=GREEN, size=16),
                                ft.Text(
                                    "MANAGE STOCK",
                                    color=GREEN,
                                    size=9,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                        ),
                    ),
                ],
            ),
        )

    # ── Main content ──────────────────────────────────────────────
    content_area = ft.Container(
        expand=True,
        clip_behavior=ft.ClipBehavior.HARD_EDGE,
        content=products_grid,
    )

    empty_state_container = ft.Container(
        expand=True,
        alignment=ft.Alignment(0, 0),
        content=empty_state,
        visible=False,
    )

    def filter_products(e=None):
        query = (search_value.current.value or "").strip().lower()
        products_grid.controls.clear()
        filtered = (
            [
                p
                for p in all_products
                if query in (p.get("product_name") or "").lower()
                or query in (p.get("brand") or "").lower()
            ]
            if query
            else all_products
        )

        if filtered:
            empty_state_container.visible = False
            for p in filtered:
                products_grid.controls.append(product_card(p))
        else:
            empty_state_container.visible = True
        page.update()

    main_content = ft.Container(
        expand=True,
        padding=ft.padding.only(left=36, right=36, top=32, bottom=24),
        content=ft.Column(
            spacing=28,
            controls=[
                ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Column(
                            spacing=5,
                            controls=[
                                ft.Text(
                                    "Products",
                                    color="white",
                                    size=34,
                                    weight=ft.FontWeight.BOLD,
                                ),
                                ft.Text(
                                    "BUSINESS PRODUCT CATALOG",
                                    color="#59657a",
                                    size=9,
                                    weight=ft.FontWeight.BOLD,
                                ),
                            ],
                        ),
                        ft.Row(
                            spacing=14,
                            controls=[
                                ft.Container(
                                    width=260,
                                    height=46,
                                    border_radius=12,
                                    bgcolor="#070d17",
                                    border=ft.border.all(1, "#1a2535"),
                                    padding=ft.padding.symmetric(horizontal=14),
                                    content=ft.Row(
                                        spacing=10,
                                        controls=[
                                            ft.Icon(
                                                ft.Icons.SEARCH_ROUNDED,
                                                color="#3d4a5c",
                                                size=18,
                                            ),
                                            ft.TextField(
                                                ref=search_value,
                                                hint_text="Search products...",
                                                hint_style=ft.TextStyle(
                                                    color="#3d4a5c", size=12
                                                ),
                                                border=ft.InputBorder.NONE,
                                                color="white",
                                                text_size=12,
                                                expand=True,
                                                on_change=filter_products,
                                            ),
                                        ],
                                    ),
                                ),
                                ft.Container(
                                    width=140,
                                    height=46,
                                    border_radius=12,
                                    bgcolor=CYAN,
                                    alignment=ft.Alignment(0, 0),
                                    ink=True,
                                    on_click=lambda e: page.go(
                                        f"/businesses/{business_id}/products/add"
                                    ),
                                    content=ft.Row(
                                        tight=True,
                                        spacing=8,
                                        controls=[
                                            ft.Icon(
                                                ft.Icons.ADD_ROUNDED,
                                                color="#02101a",
                                                size=18,
                                            ),
                                            ft.Text(
                                                "ADD PRODUCT",
                                                color="#02101a",
                                                size=9,
                                                weight=ft.FontWeight.BOLD,
                                            ),
                                        ],
                                    ),
                                ),
                            ],
                        ),
                    ],
                ),
                ft.Stack(
                    expand=True,
                    controls=[
                        content_area,
                        empty_state_container,
                    ],
                ),
            ],
        ),
    )

    # ── Star background ───────────────────────────────────────────
    stars = [
        (25, 38, 1),
        (94, 91, 2),
        (167, 26, 1),
        (246, 70, 2),
        (325, 19, 1),
        (402, 112, 2),
        (487, 44, 1),
        (566, 86, 2),
        (651, 27, 1),
        (735, 103, 2),
        (819, 51, 1),
        (908, 126, 2),
        (998, 34, 1),
        (1075, 78, 2),
        (79, 254, 1),
        (222, 301, 2),
        (371, 238, 1),
        (527, 333, 2),
        (684, 269, 1),
        (841, 350, 2),
        (1012, 282, 1),
        (1128, 377, 2),
        (132, 514, 2),
        (303, 464, 1),
        (486, 551, 2),
        (676, 489, 1),
        (864, 574, 2),
        (1054, 501, 1),
    ]

    star_controls = [
        ft.Container(
            left=float(x),
            top=float(y),
            width=size,
            height=size,
            border_radius=size,
            bgcolor="#a7b1c2",
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
                    star.left = max(0, min(1200, star.left + random.uniform(-50, 50)))
                    star.top = max(0, min(800, star.top + random.uniform(-50, 50)))
                page.update()
            except Exception:
                break
            time.sleep(0.8)

    threading.Thread(target=animate_stars, daemon=True).start()

    # ── Load data ─────────────────────────────────────────────────
    def load_data():
        products_grid.controls.clear()
        inv_map.clear()
        inventory_by_product.clear()

        # Load business name
        try:
            data, status = api_client.get_business(business_id)
            if status == 200:
                name = (data.get("business_name") or "Business").strip()
                business_name_text.value = name
                business_initials_text.value = (
                    "".join(p[0] for p in name.split()[:2]).upper() or "B"
                )
        except Exception:
            pass

        # Build product_id -> inventory_id map
        try:
            data, status = api_client.get_inventory(business_id)
            if status == 200 and isinstance(data, list):
                for inv in data:
                    product_id = str(inv.get("product_id"))
                    inv_map[product_id] = inv.get("id")
                    inventory_by_product[product_id] = inv
        except Exception:
            pass

        # Load products
        try:
            data, status = api_client.get_products(business_id)
            if status == 401:
                api_client.set_token(None)
                page.go("/login")
                return
            if status == 200:
                all_products.clear()
                all_products.extend(data if isinstance(data, list) else [])
                filter_products()
                return
        except Exception as ex:
            print("PRODUCTS ERROR:", ex)
            empty_state_container.visible = True

        page.update()

    load_data()

    return ft.View(
        route=f"/businesses/{business_id}/products",
        padding=0,
        controls=[
            ft.Stack(
                expand=True,
                controls=[
                    background,
                    ft.Row(
                        expand=True,
                        spacing=0,
                        controls=[sidebar, main_content],
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
