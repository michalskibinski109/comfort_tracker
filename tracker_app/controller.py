from miskibin import get_logger
from logging import Logger
from model import Model


class Controller:
    def __init__(self, model: Model, logger: Logger = get_logger()) -> None:
        self.logger = logger
        self.model = model

    def reset_values(self) -> None:
        self.logger.info("Resetting values")
        self.model.reset_values()

    def save_data(self):
        self.model.save()
