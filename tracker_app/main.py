from flet import Column, Page, UserControl, LinearGradient
from utils import CONFIG, Colors
import flet as ft
from model import Model
from datetime import datetime


class ComfortTracker(UserControl):
    def __init__(self, model: Model):
        super().__init__()
        self.model = model

    def input_fields_container(self, content=None):
        return ft.Container(
            col={"xs": 10, "sm": 8, "md": 4, "lg": 4, "xl": 4},
            width=CONFIG.window_width // 3.3,
            height=CONFIG.window_height // 2.4,
            alignment=ft.alignment.center,
            content=content,
            # bgcolor=Colors.DEBUG.value,
        )

    def radio_group(self, label: str, value: str):

        return ft.Column(
            controls=[
                ft.Text(label, color=Colors.EXTRA2.value, text_align="center"),
                ft.RadioGroup(
                    value=value,
                    content=ft.Row(
                        [
                            ft.Radio(
                                value="0",
                                label="0",
                                fill_color=Colors.EXTRA2.value,
                            ),
                            ft.Radio(
                                value="1",
                                label="1",
                                fill_color=Colors.EXTRA2.value,
                            ),
                            ft.Radio(
                                value="2",
                                label="2",
                                fill_color=Colors.EXTRA2.value,
                            ),
                        ],
                        alignment="center",
                    ),
                ),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            alignment="center",
        )

    def text_field(self, label: str, value: str):
        return ft.TextField(
            label=label,
            value=value if value != 0 else None,
            color=Colors.EXTRA2.value,
            border_color=Colors.EXTRA2.value,
            cursor_color=Colors.EXTRA2.value,
            width=CONFIG.window_width // 4,
        )

    def tile(self, label: str, icon: ft.Icon):
        return ft.Container(
            aspect_ratio=1,
            expand=False,
            animate_offset=True,
            on_hover=self._on_tile_hover,
            border_radius=12,
            bgcolor=Colors.EXTRA.value,
            alignment=ft.alignment.center,
            col={"xs": 5, "sm": 5, "md": 5, "lg": 5, "xl": 5},
            content=ft.Column(
                controls=[
                    ft.Text(label, size=15, color=Colors.SECONDARY.value),
                    ft.Icon(
                        icon,
                        size=40,
                        color=Colors.SECONDARY.value,
                    ),
                ],
            ),
        )

    @property
    def input_row(self):
        return ft.Row(
            controls=[
                self.input_fields_container(
                    ft.Column(
                        [
                            self.text_field("work hours", self.model.work_time),
                            self.text_field("study hours", self.model.study_time),
                            self.text_field("sleep hours", self.model.sleep_time),
                        ],
                        alignment="spaceAround",
                    )
                ),
                self.input_fields_container(
                    ft.Column(
                        [
                            self.radio_group("mc_donalds", value=self.model.mc_donalds),
                            self.radio_group("txt", value=self.model.bad_habits),
                            self.radio_group(
                                "red bulls", value=self.model.energy_drinks
                            ),
                        ],
                        alignment="center",
                    ),
                ),
                self.input_fields_container(
                    ft.ResponsiveRow(
                        [
                            self.tile("Gym", ft.icons.FITNESS_CENTER),
                            self.tile("Gym", ft.icons.FITNESS_CENTER),
                            self.tile("Gym", ft.icons.FITNESS_CENTER),
                            self.tile("Gym", ft.icons.FITNESS_CENTER),
                        ],
                    )
                ),
            ],
            alignment="spaceAround",
        )

    def _go_day_back(self, e):
        self.model.go_to_previous_day()
        self.update_all(e)

    def _go_day_forward(self, e):
        self.model.go_to_next_day()
        self.update_all(e)

    @property
    def header(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.IconButton(
                        icon=ft.icons.ARROW_BACK_OUTLINED,
                        icon_color=Colors.EXTRA2.value,
                        on_click=self._go_day_back,
                        icon_size=40,
                    ),
                    ft.Text(
                        f"{self.model.date} {'(today)' if self.model.date == datetime.now().date() else ''}",
                        style=ft.TextThemeStyle.TITLE_LARGE,
                        color=Colors.EXTRA2.value,
                    ),
                    ft.IconButton(
                        icon=ft.icons.ARROW_FORWARD_OUTLINED,
                        icon_color=Colors.EXTRA2.value,
                        on_click=self._go_day_forward,
                        icon_size=40,
                    ),
                ],
                alignment="spaceBetween",
            ),
            margin=5,
            padding=10,
            # bgcolor=Colors.PRIMARY.value,
            width=CONFIG.window_width / 1.2,
        )

    @property
    def footer(self):
        return ft.Container(
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Reset",
                        color=Colors.SECONDARY.value,
                        bgcolor=Colors.THIRD.value,
                        icon=ft.icons.REPLAY,
                    ),
                    ft.ElevatedButton(
                        "Save",
                        color=Colors.SECONDARY.value,
                        bgcolor=Colors.EXTRA.value,
                        icon=ft.icons.SAVE,
                        on_click=self.update_all,
                    ),
                ],
                alignment="spaceBetween",
            ),
            padding=10,
            # bgcolor=Colors.DEBUG.value,
        )

    @property
    def slider_container(self):
        return ft.Container(
            alignment=ft.alignment.center,
            content=ft.Slider(
                thumb_color=Colors.EXTRA.value,
                active_color=Colors.EXTRA.value,
                inactive_color=Colors.EXTRA2.value,
                min=0,
                max=5,
                divisions=5,
                value=float(self.model.overall_score),
                label="overall score: {value}",
            ),
            margin=5,
            padding=10,
            width=CONFIG.window_width / 1.2,
            # bgcolor=Colors.DEBUG.value,
        )

    def build(self):
        return Column(
            alignment="spaceBetween",
            controls=[
                ft.Row([self.header], alignment="center"),
                self.input_row,
                ft.Row([self.slider_container], alignment="center"),
                self.footer,
            ],
        )

    def _on_tile_hover(self, event: ft.Event):
        if event.data == "true":
            print("hover")
            event.control.border_radius = 20
            event.control.update()
        else:
            print("not hover")
            event.control.border_radius = 12
            event.control.update()

    def update_all(self, event: ft.Event):
        page = event.page
        page.controls.pop()
        page.controls.append(ComfortTracker(self.model))
        page.update()
        print(f"page updated: {page}")


def main(page: Page):
    model = Model()
    page.title = "Comfort Tracker"
    page.window_min_width = CONFIG.window_width
    page.window_min_height = CONFIG.window_height
    page.window_height = CONFIG.window_height
    page.window_width = CONFIG.window_width
    page.bgcolor = Colors.SECONDARY.value
    page.padding = 20
    app = ComfortTracker(model)
    page.add(app)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
