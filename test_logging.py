# test_logging.py
import os
from weather_api import get_weather, close_logger


def test_logging_error():
    log_file = "error.log"

    if os.path.exists(log_file):
        os.remove(log_file)

    result = get_weather("FakeCityThatDoesNotExist", "6596f316a56103539735bd87c6246997")
    assert "error" in result

    close_logger()

    assert os.path.exists(log_file)

    with open(log_file, "r", encoding="utf-8") as f:
        content = f.read()
        print("\n\n[DEBUG LOG CONTENT]\n", content)

    assert "Город не найден" in content
