import datetime
import pandas as pd
from pathlib import Path
from dataclasses import dataclass
from logging import Logger

"""
TODO 
1. Add validation rules for each field.
2. Add github actions for testing.
"""

FIELDS = {
    "date": ("datetime64", datetime.datetime.now().date()),
    "work_time": ("float", 0.0),
    "study_time": ("float", 0.0),
    "sleep_time": ("float", 0.0),
    "chess_tasks": ("bool", False),
    "code_tasks": ("bool", False),
    "party": ("bool", False),
    "mc_donalds": ("int", -1),
    "gym": ("bool", False),
    "energy_drinks": ("int", -1),
    "bad_habits": ("int", -1),
    "overall_score": ("int", 0),
}


@dataclass
class Model:
    """
    Model for the comfort tracker app. Here all fields are defined and the data is loaded and saved.
    If todey's data is already in the data file, the initial values are set to the last row.
    Model has set of validation rules for each field. If the validation fails,
    the field will be set to the default value.
    (For now works only for the fields that are set in the init method.)

    Args:
        `_data_path` (private attribute): Path to the data file. If it does not exist, it will be created.
        `_logger` (private attribute): Logger for this class.
        `_data` (private attribute): Data loaded from the data file. It is a private attribute.

    methods:
        `save`: Saves the data to the data file.
        `update`: Updates the data with the current values.
        `change_date`: Changes the date of the entry.
        `__str__`: Returns representation of the model.
    """

    _logger: Logger = None
    _data_path: Path = Path("comfort_data.csv")
    _data: pd.DataFrame = None

    def __post_init__(self):
        global FIELDS
        # set fields as class attributes
        self.set_default_values(True)

        self._data = self.__load_data(self._data_path)
        self.__set_initial_values()

    def set_default_values(self, with_date=False) -> None:
        global FIELDS
        for field, (field_type, default_value) in FIELDS.items():
            if field != "date" or with_date:
                self.__setattr__(field, default_value)

    def save(self) -> None:
        self.update()
        self._logger.info(f"Saving data to {self._data_path}")
        self._data.to_csv(self._data_path, index=False)

    def update(self) -> None:
        self._data = self._data[self._data["date"] != self.date]
        # sort by date
        self._data = pd.concat(
            [
                self._data,
                pd.DataFrame(self.fields, index=[0]),
            ],
            ignore_index=True,
        )
        # set types for each column
        self.__validate_fields()
        self._data["date"] = pd.to_datetime(self._data["date"]).dt.date
        self._data = self._data.sort_values(by="date")

    @property
    def fields(self) -> dict:
        fields = {k: v for k, v in self.__dict__.items() if not k.startswith("_")}
        return fields

    def __validate_fields(self) -> bool:
        global FIELDS
        for field, (field_type, default_value) in FIELDS.items():
            try:
                self._data[field] = self._data[field].astype(field_type)
            except ValueError as exc:
                self._logger.error(
                    f"Invalid value for {field}. Should be {field_type}. "
                )
                raise exc

    def __set_initial_values(self) -> None:
        try:
            row = (
                self._data[self._data["date"] == self.date]
                .reset_index(drop=True)
                .iloc[-1]
            )
        except IndexError:
            self._logger.info(f"No data from {self.date}. Setting initial values.")
            self.set_default_values()
            # reset values to 0
            return
        self._logger.info(
            f"Found row with data from {self.date} . Setting initial values."
        )
        for k in self.fields.keys():
            if k != "date":
                setattr(self, k, row[k])

    def __load_data(self, data_path: Path) -> pd.DataFrame:
        if not data_path.exists():
            self._logger.warning(f"File {data_path} does not exist. Creating it.")
            df = pd.DataFrame(columns=self.fields.keys())
            df.to_csv(data_path, index=False)
            self._logger.info(f"Created file with header {df.head(0).columns}")
        else:
            self._logger.debug(f"File {data_path} exists. Loading it.")
            df = pd.read_csv(data_path)
            # set dtype of date to date
            df["date"] = pd.to_datetime(df["date"]).dt.date
            if tuple(map(str, self.fields.keys())) != tuple(df.columns):
                msg = f"File {data_path} has different columns than expected. Expected: \n{list(self.fields.keys())}\nGOT: \n{list(df.columns)}"
                self._logger.error(msg)
                raise ValueError(msg)
        return df

    def __change_date(self, date: datetime.date) -> None:
        """Changes the date and sets the initial values to the  row from this date if exists.
        Args:
            `date` (datetime.date): Date to change to.
        """
        self._logger.debug(
            f"Changing date to {date} ({type(date)}). Setting initial values."
        )
        self.date = datetime.datetime.strptime(str(date), "%Y-%m-%d").date()
        self.__set_initial_values()
        # make sure that the date is a datetime.date

    def go_to_next_day(self) -> datetime.date:
        """Changes the date to the next day and sets the initial values to the  row from this date if exists."""
        self.__change_date(self.date + datetime.timedelta(days=1))
        return self.date

    def go_to_previous_day(self) -> datetime.date:
        self.__change_date(self.date - datetime.timedelta(days=1))
        return self.date

    def __str__(self) -> str:
        return "\n".join(f"{k:<15}: {v}" for k, v in self.fields.items())
