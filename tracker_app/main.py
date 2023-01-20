from flet import Page
from utils import CONFIG, Colors
import flet as ft
from model import Model
from controller import Controller
from main_view import MainView
from statistic_view import StatisticView
from miskibin import get_logger
from datetime import datetime
from pathlib import Path
import yaml


def init_page(page: Page):
    page.title = "Comfort Tracker"
    page.window_min_width = CONFIG.window_width
    page.window_min_height = CONFIG.window_height
    page.window_height = CONFIG.window_height
    page.window_width = CONFIG.window_width
    page.bgcolor = Colors.SECONDARY.value
    page.padding = 10
    return page


def main(page: Page):
    file_name = datetime.now().strftime("%Y-%m-%d_%H")
    log_path = Path(__file__).parent / "logs" / f"{file_name}.log"
    logger = get_logger(
        lvl=10,
        file_name=log_path,
        format="%(levelname)-8s:: %(asctime)-9s:: %(message)s (%(filename)s:%(lineno)d)",
    )
    model = Model(_logger=logger)
    controller = Controller(model, logger)
    main_view = MainView(model, controller, logger)
    statisitcs_view = StatisticView(model, controller, logger)
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
