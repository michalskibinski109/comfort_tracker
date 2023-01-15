import datetime
import pytest

from pathlib import Path

from tracker_app.model import Model


class TestModel:
    @pytest.fixture(autouse=True)
    def setup(self):
        self.data_path = Path("test_comfort_data.csv")
        yield
        self.data_path.unlink(missing_ok=True)

    def test_init(self):
        model = Model(_data_path=self.data_path)
        assert isinstance(model, Model)
        assert isinstance(model.date, datetime.date)
        assert isinstance(model._data_path, Path)
        assert model._data.empty

    def test_save(self):
        model = Model(_data_path=self.data_path)
        model.save()
        assert model._data.shape[0] == 1
        model = Model(_data_path=self.data_path)
        model.save()
        assert model._data.shape[0] == 1  # date is the same, so no new row

    def test_update(self):
        model = Model(_data_path=self.data_path)
        model.save()
        assert model._data.shape[0] == 1

        model.mc_donalds = 10
        model.update()
        assert model._data.shape[0] == 1
        assert model._data.iloc[-1]["mc_donalds"] == 10

    def test_load_data(self):
        model = Model(_data_path=self.data_path, mc_donalds=10)
        model.save()
        model2 = Model(_data_path=self.data_path)
        assert model2.mc_donalds == 10

    def test_change_data(self):
        model = Model(
            _data_path=self.data_path, mc_donalds=10, date=datetime.date(2020, 1, 2)
        )
        model.save()
        model2 = Model(_data_path=self.data_path)
        model2.change_date(datetime.date(2020, 1, 2))
        assert model2.mc_donalds == 10
