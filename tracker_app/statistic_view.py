from flet import UserControl
from utils import CONFIG, Colors
import flet as ft
from model import Model
from controller import Controller
import matplotlib.pyplot as plt
from flet.matplotlib_chart import MatplotlibChart
import seaborn as sns
import pandas as pd
from logging import Logger

# change plt style
sns.set_style("dark")
plt.tight_layout()
sns.set(
    rc={
        # "axes.facecolor": Colors.SECONDARY.value,
        "figure.facecolor": Colors.WHITE.value,
        # "figure.edgecolor": Colors.SECONDARY.value,
        # "axes.grid": False,
        "axes.spines.right": False,
        "axes.spines.left": False,
        "axes.spines.top": False,
        "axes.spines.bottom": False,
    }
)


class StatisticView(UserControl):
    def __init__(self, model: Model, controller: Controller, logger: Logger):
        super().__init__()
        self.charts_iter = self.charts_iterator()
        self.logger = logger
        self.model = model
        self.controller = controller

    def charts_iterator(self):
        while True:
            for attr in self.__class__.__dict__:
                if attr.endswith("_chart"):
                    self.logger.debug(f"Found chart: {attr}")
                    yield getattr(self, attr)

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
                    disabled=True,
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

    @property
    def chart_container(self):
        return ft.Container(
            width=CONFIG.window_width / 1.3,
            height=CONFIG.window_height / 1.2,
            bgcolor=Colors.WHITE.value,
            content=next(self.charts_iter),
            border_radius=10,
        )

    @property
    def view(self):
        # plt.tight_layout()
        # fig, ax = plt.subplots()
        # plt.yticks([4, 8, 12])
        # x = self.model._data["date"]
        # # get only day value
        # x = [x.day for day in x]
        # ax = sns.pointplot(x="date", y="sleep_time", data=self.model._data)
        # ax.set(xlabel="Date", ylabel="Sleep time")
        # # ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
        # # set title
        # ax.set_title("Sleep time per day", fontsize=20)
        # chart = MatplotlibChart(fig, expand=True)
        return ft.Row(
            [
                self.left_col,
                self.chart_container,
                self.right_col,
            ],
            alignment="center",
        )

    @property
    def sleep_time_per_weekday_chart(self):
        fig, ax = plt.subplots()
        df = self.model._data.copy()
        df["weekday"] = df["date"].apply(lambda x: pd.to_datetime(x).day_name())
        avg_sleep_time = df.groupby("weekday")["sleep_time"].mean()
        ax = sns.barplot(x=avg_sleep_time.index, y=avg_sleep_time.values)
        ax.set(xlabel="Weekday", ylabel="Sleep time")
        ax.set_title("Sleep time per weekday", fontsize=20)
        plt.tight_layout()
        # set size of chart

        return MatplotlibChart(fig, expand=True)

    @property
    def score_vs_sleep_time_chart(self):
        fig, ax = plt.subplots()
        ax = sns.barplot(x="overall_score", y="sleep_time", data=self.model._data)
        ax.set_title("Sleep time vs overarall score", fontsize=20)
        plt.tight_layout()
        return MatplotlibChart(fig, expand=True)

    def _on_right_arrow_click(self, e: ft.Event):
        view = self.build()
        e.page.controls.pop(0)
        e.page.controls.insert(0, view)
        e.page.update()

    def _on_close_button_click(self, e: ft.Event):
        e.page.route = "/"
        e.page.update()

    def build(self):
        return self.view
