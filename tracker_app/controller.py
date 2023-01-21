from logging import Logger
from model import Model


class Controller:
    def __init__(self, model: Model, logger: Logger) -> None:
        self.logger = logger
        self.model = model

    def reset_values(self) -> None:
        self.logger.info("Resetting values")
        self.model.set_default_values()

    def save_data(self, data: dict) -> None:
        self.model.set_values(data)
        self.model.save()
