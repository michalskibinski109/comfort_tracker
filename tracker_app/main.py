from flet import Column, Page, UserControl, LinearGradient
from utils import CONFIG, Colors
import flet as ft
from model import Model
from datetime import datetime
from controller import Controller

SAVED = False


class ComfortTracker(UserControl):
    def __init__(self, model: Model, controller: Controller):
        super().__init__()
        self.model = model
        self.controller = controller

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
                ft.Text(
                    label,
                    color=Colors.EXTRA2.value,
                    text_align="center",
                    style=ft.TextThemeStyle.TITLE_MEDIUM,
                ),
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

    def _on_tile_click(self, e):
        e.control.data = not e.control.data
        if e.control.bgcolor == Colors.THIRD.value:
            e.control.bgcolor = Colors.EXTRA.value
        else:
            e.control.bgcolor = Colors.THIRD.value
        e.control.update()

    def tile(self, label: str, icon: ft.Icon, value: int = 0):
        return ft.Container(
            aspect_ratio=1,
            expand=False,
            animate_offset=True,
            on_hover=self._on_tile_hover,
            on_click=self._on_tile_click,
            border_radius=12,
            data=bool(value),
            # disabled=True,
            bgcolor=Colors.THIRD.value if value == 0 else Colors.EXTRA.value,
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
                alignment="center",
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
        )

    @property
    def input_row(self):
        self.work_time_field = self.text_field("work hours", self.model.work_time)
        self.study_time_field = self.text_field("study hours", self.model.study_time)
        self.sleep_time_field = self.text_field("sleep hours", self.model.sleep_time)
        self.mc_donalds_radio = self.radio_group(
            "mc_donalds", value=self.model.mc_donalds
        )
        self.bad_habbits_radio = self.radio_group("txt", value=self.model.bad_habits)
        self.energy_drinks_radio = self.radio_group(
            "red bulls", value=self.model.energy_drinks
        )
        self.gym_tile = self.tile("Gym", ft.icons.FITNESS_CENTER, self.model.gym)
        self.chess_tile = self.tile("Chess", ft.icons.CHURCH, self.model.chess_tasks)
        self.code_tile = self.tile("Code task", ft.icons.CODE, self.model.code_tasks)

        return ft.Row(
            controls=[
                self.input_fields_container(
                    ft.Column(
                        [
                            self.work_time_field,
                            self.study_time_field,
                            self.sleep_time_field,
                        ],
                        alignment="spaceAround",
                    )
                ),
                self.input_fields_container(
                    ft.Column(
                        [
                            self.mc_donalds_radio,
                            self.bad_habbits_radio,
                            self.energy_drinks_radio,
                        ],
                        alignment="center",
                    ),
                ),
                self.input_fields_container(
                    ft.ResponsiveRow(
                        [
                            self.gym_tile,
                            self.chess_tile,
                            self.code_tile,
                            self.tile("", None),
                        ],
                    )
                ),
            ],
            alignment="spaceAround",
        )

    def _go_day_back(self, e):
        global SAVED
        SAVED = False
        self.model.go_to_previous_day()
        self.update_all(e)

    def _go_day_forward(self, e):
        global SAVED
        SAVED = False
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
        global SAVED
        return ft.Container(
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Reset",
                        color=Colors.SECONDARY.value,
                        bgcolor=Colors.THIRD.value,
                        on_click=self._on_reset_button_click,
                        icon=ft.icons.REPLAY,
                    ),
                    ft.IconButton(
                        icon=ft.icons.DONE_ALL,
                        icon_color=Colors.EXTRA.value,
                        icon_size=40,
                        opacity=float(SAVED),
                        # disabled=True,
                    ),
                    ft.ElevatedButton(
                        "submit",
                        color=Colors.SECONDARY.value,
                        bgcolor=Colors.EXTRA.value,
                        icon=ft.icons.SAVE,
                        on_click=self._on_save_click,
                    ),
                ],
                alignment="spaceBetween",
            ),
            padding=10,
            # bgcolor=Colors.DEBUG.value,
        )

    def _on_save_click(self, e):
        global SAVED
        self.model.bad_habits = self.bad_habbits_radio.controls[1].value
        self.model.energy_drinks = self.energy_drinks_radio.controls[1].value
        self.model.mc_donalds = self.mc_donalds_radio.controls[1].value
        self.model.chess_tasks = self.chess_tile.data
        self.model.code_tasks = self.code_tile.data
        self.model.gym = self.gym_tile.data
        self.model.work_time = (
            self.work_time_field.value if self.work_time_field.value else 0
        )
        self.model.study_time = (
            self.study_time_field.value if self.work_time_field.value else 0
        )
        self.model.sleep_time = (
            self.sleep_time_field.value if self.work_time_field.value else 0
        )
        self.controller.save_data()
        SAVED = True
        self.update_all(e)

    def _on_reset_button_click(self, e):
        global SAVED
        self.controller.reset_values()
        SAVED = False
        self.update_all(e)

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
                on_change=self._on_slider_change,
                label="overall score: {value}",
            ),
            margin=5,
            padding=10,
            width=CONFIG.window_width / 1.2,
            # bgcolor=Colors.DEBUG.value,
        )

    def _on_slider_change(self, e):
        self.model.overall_score = int(e.control.value)

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
            event.control.border_radius = 20
            event.control.update()
        else:
            event.control.border_radius = 12
            event.control.update()

    def update_all(self, event: ft.Event):
        page = event.page
        page.controls.pop()
        page.controls.append(ComfortTracker(self.model, self.controller))
        page.update()


def main(page: Page):
    model = Model()
    controller = Controller(model)
    page.title = "Comfort Tracker"
    page.window_min_width = CONFIG.window_width
    page.window_min_height = CONFIG.window_height
    page.window_height = CONFIG.window_height
    page.window_width = CONFIG.window_width
    page.bgcolor = Colors.SECONDARY.value
    page.padding = 20
    app = ComfortTracker(model, controller)
    page.add(app)
    page.update()


if __name__ == "__main__":
    ft.app(target=main)
