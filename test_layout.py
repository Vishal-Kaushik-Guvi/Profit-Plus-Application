import flet as ft
def main(page: ft.Page):
    sidebar = ft.Container(width=200, bgcolor='red', content=ft.Column(controls=[ft.Text('Top'), ft.Container(expand=True, bgcolor='green'), ft.Text('Bottom')]))
    main_content = ft.Container(expand=True, bgcolor='blue', content=ft.Text('Main'))
    page.add(ft.Row(expand=True, controls=[sidebar, main_content]))
ft.app(target=main)
