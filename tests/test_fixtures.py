import dataclasses
import json
import pathlib
import unittest
from typing import Any

from coinspay import models
from coinspay._operations import OPERATIONS

FIXTURES = pathlib.Path(__file__).resolve().parent / "data" / "fixtures"


def strict(model: Any, data: Any, where: str) -> None:
    """Every key of data is a field of the model, recursively through nested models."""
    names = {field.name for field in dataclasses.fields(model)} - {"raw"}
    unknown = set(data) - names
    if unknown:
        raise AssertionError(f"{where}: {sorted(unknown)} not in {type(model).__name__}")
    for name in names:
        value = getattr(model, name)
        if isinstance(value, models.Model):
            strict(value, data[name], f"{where}.{name}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                if isinstance(item, models.Model):
                    strict(item, data[name][index], f"{where}.{name}[{index}]")


@unittest.skipUnless((FIXTURES / "getShop.json").exists(), "no fixtures")
class Fixtures(unittest.TestCase):
    def test_answers_decode_strictly(self) -> None:
        for operation, spec in OPERATIONS.items():
            with self.subTest(operation):
                data = json.loads((FIXTURES / f"{operation}.json").read_text(encoding="utf-8"))
                cls = getattr(models, spec["returns"])
                if spec["page"]:
                    items = data[spec["page"]]
                elif spec["many"]:
                    items = data[spec["unwrap"]]
                elif spec["unwrap"]:
                    items = [data[spec["unwrap"]]]
                else:
                    items = [data]
                for item in items:
                    strict(cls.from_dict(item), item, operation)

    def test_events_decode_strictly(self) -> None:
        for event in json.loads((FIXTURES / "events.json").read_text(encoding="utf-8")):
            with self.subTest(event["type"]):
                cls = models.EVENT_CLASSES[event["type"]]
                strict(cls.from_dict(event), event, event["type"])


if __name__ == "__main__":
    unittest.main()
