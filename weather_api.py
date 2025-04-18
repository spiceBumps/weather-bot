import logging
import requests

logger = logging.getLogger("weather_logger")
logger.setLevel(logging.ERROR)

# Создаём handler только один раз
file_handler = logging.FileHandler("error.log", mode='w', encoding="utf-8")
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
file_handler.setFormatter(formatter)

if not any(isinstance(h, logging.FileHandler) and h.baseFilename == file_handler.baseFilename for h in logger.handlers):
    logger.addHandler(file_handler)

def get_weather(city, api_key):
    base_url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key,
        "units": "metric",
        "lang": "ru"
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        data = response.json()

        if response.status_code == 404:
            logger.error(f"[Город не найден] Город: {city}")
            for handler in logger.handlers:
                handler.flush()
            return {"error": "Город не найден"}

        return {
            "city": data["name"],
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"]
        }

    except requests.exceptions.RequestException as e:
        logger.error(f"[RequestException] Город: {city} — {e}")
        for handler in logger.handlers:
            handler.flush()
        return {"error": "Ошибка сети"}

def close_logger():
    for handler in logger.handlers:
        handler.flush()
        handler.close()
    logger.handlers.clear()
