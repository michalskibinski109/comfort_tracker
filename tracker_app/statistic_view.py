from flet import Column, Page, UserControl, LinearGradient
from utils import CONFIG, Colors
import flet as ft
from model import Model
from datetime import datetime
from controller import Controller
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import plotly.express as px
from flet.plotly_chart import PlotlyChart
import seaborn as sns

# change plt style
sns.set_style("dark")
sns.set(
    rc={
        "axes.facecolor": Colors.SECONDARY.value,
        "figure.facecolor": Colors.WHITE.value,
        "figure.edgecolor": Colors.SECONDARY.value,
        "axes.grid": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.spines.top": False,
        "axes.spines.bottom": False,
    }
)


class StatisticView(UserControl):
    def __init__(self, model: Model, controller: Controller):
        super().__init__()
        self.model = model
        self.controller = controller

    def close_button(self, opacity=0.5):
        return ft.IconButton(
            icon=ft.icons.CLOSE_OUTLINED,
            icon_size=35,
            opacity=opacity,
            on_click=self._on_close_button_click,
        )

    @property
    def left_col(self):
        return ft.Column(
            [
                ft.IconButton(
                    icon=ft.icons.ARROW_LEFT,
                    on_click=self._on_left_arrow_click,
                    icon_color=Colors.THIRD.value,
                    icon_size=50,
                ),
            ],
            horizontal_alignment="start",
        )

    @property
    def right_col(self):
        return ft.Column(
            [
                self.close_button(opacity=1),
                ft.IconButton(
                    icon=ft.icons.ARROW_RIGHT,
                    on_click=self._on_right_arrow_click,
                    icon_color=Colors.EXTRA.value,
                    icon_size=50,
                ),
                self.close_button(opacity=0),
            ],
            horizontal_alignment="end",
            alignment="spaceBetween",
            height=CONFIG.window_height / 1.1,
        )

    def chart_container(self, chart=None):
        return ft.Container(
            width=CONFIG.window_width / 1.3,
            height=CONFIG.window_height / 1.2,
            bgcolor=Colors.WHITE.value,
            content=chart,
            border_radius=10,
        )

    @property
    def view(self):
        plt.tight_layout()
        fig, ax = plt.subplots()
        # plt.yticks([4, 8, 12])
        # x = self.model._data["date"]
        # # get only day value
        # x = [x.day for day in x]
        ax = sns.pointplot(x="date", y="sleep_time", data=self.model._data)
        ax.set(xlabel="Date", ylabel="Sleep time")
        # ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        # set title
        ax.set_title("Sleep time per day", fontsize=20)
        chart = MatplotlibChart(fig, expand=True)
        return ft.Row(
            [
                self.left_col,
                self.chart_container(chart),
                self.right_col,
            ],
            alignment="center",
        )

    def _on_left_arrow_click(self, e: ft.Event):
        pass

    def _on_right_arrow_click(self, e: ft.Event):
        pass

    def _on_close_button_click(self, e: ft.Event):
        e.page.route = "/"
        e.page.update()

    def build(self):
        return self.view
