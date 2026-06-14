import flet as ft

def main(page: ft.Page):
    page.title = "Test"
    page.add(ft.Text("Hello World", size=40, color="white"))
    page.bgcolor = "#000000"

ft.run(main)