from miskibin import get_logger
import datetime
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from logging import Logger


@dataclass
class Model:
    """
    Model for the comfort tracker app. Here all fields are defined and the data is loaded and saved.
    If todey's data is already in the data file, the initial values are set to the last row.
    Model has set of validation rules for each field. If the validation fails,
    the field will be set to the default value.
    (For now works only for the fields that are set in the init method.)

    Args:
        `date` (str): Date of the entry. DO NOT SET IT MANUALLY. It will be set automatically.
        `work_time` (int): Time spent working in hours.
        `study_time` (int): Time spent studying in hours.
        `sleep_time` (float): Time spent sleeping in hours.
        `mc_donalds` (int): Number of mc donalds eaten.
        `gym` (bool): Whether the gym was visited.
        `energy_drinks` (int): Number of energy drinks consumed.
        `bad_habits` (int): Everyone can define their own bad habits. It could be smoking, drinking, watching porn, etc.
        `overall_score` (int): How was the day overall? 1 is bad, 5 is good.
        `_data_path` (private attribute): Path to the data file. If it does not exist, it will be created.
        `_logger` (private attribute): Logger for this class.
        `_data` (private attribute): Data loaded from the data file. It is a private attribute.

    methods:
        `save`: Saves the data to the data file.
        `update`: Updates the data with the current values.
        `change_date`: Changes the date of the entry.
        `__str__`: Returns representation of the model.
    """

    _logger: Logger = get_logger("Model", lvl=10)
    _data_path: Path = Path("comfort_data.csv")
    _data: pd.DataFrame = None
    date: datetime.date = datetime.datetime.now().date()
    work_time: int = 0
    study_time: int = 0
    sleep_time: float = 8.0
    mc_donalds: int = 0
    gym: bool = False
    energy_drinks: int = 0
    bad_habits: int = 0
    overall_score: int = 3

    def __post_init__(self):
        self._data = self.__load_data(self._data_path)
        self.__set_initial_values()

    def save(self) -> None:
        self.update()
        self._logger.info(f"Saving data to {self._data_path}")
        self._data.to_csv(self._data_path, index=False)

    def update(self) -> None:
        self._data = self._data[self._data["date"] != self.date]
        self._data = pd.concat(
            [
                self._data,
                pd.DataFrame(self.fields, index=[0]),
            ],
            ignore_index=True,
        )

    @property
    def fields(self) -> dict:
        fields = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}

        return fields

    def __set_initial_values(self) -> None:
        try:
            row = (
                self._data[self._data["date"] == str(self.date)]
                .reset_index(drop=True)
                .iloc[-1]
            )
        except IndexError:
            self._logger.warning("No rows from today. Setting initial values.")
            return
        self._logger.warning("Last row is from today. Setting initial values.")
        for k in self.fields.keys():
            setattr(self, k, row[k])
        self._data = self._data[self._data["date"] != self.date]

    def __load_data(self, data_path: Path) -> pd.DataFrame:
        if not data_path.exists():
            self._logger.warning(f"File {data_path} does not exist. Creating it.")
            df = pd.DataFrame(columns=self.fields.keys())
            df.to_csv(data_path, index=False)
            self._logger.info(f"Created file with header {df.head(0).columns}")
        else:
            self._logger.debug(f"File {data_path} exists. Loading it.")
            df = pd.read_csv(data_path)
            if tuple(map(str, self.fields.keys())) != tuple(df.columns):
                msg = f"File {data_path} has different columns than expected. Expected: \n{list(self.fields.keys())}\nGOT: \n{list(df.columns)}"
                self._logger.error(msg)
                raise ValueError(msg)
        return df

    def change_date(self, date: datetime.date) -> None:
        """Changes the date and sets the initial values to the  row from this date if exists.
        Args:
            `date` (datetime.date): Date to change to.
        """
        self.date = date
        self._logger.info(
            f"Changing date to {date}. All fields will be set to the last row from this date or default"
        )
        self.__set_initial_values()

    def __str__(self) -> str:
        return "\n".join(f"{k:<15}: {v}" for k, v in self.fields.items())
