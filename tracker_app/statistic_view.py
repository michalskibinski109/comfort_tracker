from flet import Column, Page, UserControl, LinearGradient
from utils import CONFIG, Colors
import flet as ft
from model import Model
from datetime import datetime
from controller import Controller
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart

# change plt style

plt.style.use("ggplot")


class StatisticView(UserControl):
    def __init__(self, model: Model, controller: Controller):
        super().__init__()
        self.model = model
        self.controller = controller

    @property
    def close_button(self):
        return ft.OutlinedButton("Close", on_click=self._on_close_button_click)

    def _on_close_button_click(self, e: ft.Event):
        e.page.route = "/"
        e.page.update()

    def build(self):
        fig, ax = plt.subplots(2, 2, figsize=(9, 5))
        # use tight layout to avoid overlapping
        fig.tight_layout()

        x = self.model._data["date"]
        # get only day number from date
        x = [date.day for date in x]
        y1 = self.model._data["sleep_time"]
        y2 = self.model._data["work_time"]
        y3 = self.model._data["study_time"]
        y4 = self.model._data["energy_drinks"]

        ax[0, 0].plot(x, y1, label="Sleep time")
        ax[0, 0].set_title("Sleep time")
        ax[0, 0].set_xlabel("Day")
        ax[0, 0].set_ylabel("Hours")

        ax[0, 1].plot(x, y2, label="Work time")
        ax[0, 0].set_title("Work time")
        ax[0, 1].set_xlabel("Day")
        ax[0, 1].set_ylabel("Hours")
        ax[1, 0].plot(x, y3, label="Study time")
        ax[1, 1].bar(x, y4, label="Energy drinks")
        self.chart = MatplotlibChart(fig)
        return ft.Container(
            width=CONFIG.window_width,
            height=CONFIG.window_height,
            content=ft.Column(
                [
                    ft.IconButton(
                        icon=ft.icons.CLOSE,
                        on_click=self._on_close_button_click,
                        icon_color=Colors.THIRD.value,
                    ),
                    self.chart,
                ],
                horizontal_alignment="end",
            ),
        )
