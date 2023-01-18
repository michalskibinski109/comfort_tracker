from flet import Page
from utils import CONFIG, Colors
import flet as ft
from model import Model
from controller import Controller
from main_view import MainView
from statistic_view import StatisticView


def init_page(page: Page):
    page.title = "Comfort Tracker"
    page.window_min_width = CONFIG.window_width
    page.window_min_height = CONFIG.window_height
    page.window_height = CONFIG.window_height
    page.window_width = CONFIG.window_width
    page.bgcolor = Colors.SECONDARY.value
    page.padding = 20
    return page


def main(page: Page):
    model = Model()
    controller = Controller(model)
    main_view = MainView(model, controller)
    statisitcs_view = StatisticView(model, controller)
    page = init_page(page)
    page.add(main_view)
    page.update()

    def on_route_change(e: ft.Event):
        nonlocal page
        e.page.controls.pop()
        print(page.route)
        if page.route == "/":
            page.controls.append(main_view)
        elif page.route == "/statistics":
            page.controls.append(statisitcs_view)
        page.update()

    page.on_route_change = on_route_change


if __name__ == "__main__":
    ft.app(target=main)
