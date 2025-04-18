import sqlite3
import os
from weather_api import get_weather
from bott import connect, init_db, get_or_create_city_id, update_weather

API_KEY = "6596f316a56103539735bd87c6246997"
TEST_CITY = "Almaty"


def test_full_weather_flow():
    # шаг 1: получить данные из API
    weather = get_weather(TEST_CITY, API_KEY)
    assert "temperature" in weather
    assert "description" in weather

    # шаг 2: сохранить в БД
    update_weather(TEST_CITY, API_KEY)

    # шаг 3: проверить, что данные записаны
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT c.name, w.temperature, w.description
        FROM weather_data w
        JOIN cities c ON c.id = w.city_id
        WHERE c.name = ?
        ORDER BY w.updated_at DESC
        LIMIT 1
    """,
        (TEST_CITY,),
    )
    result = cursor.fetchone()
    conn.close()

    assert result is not None
    assert result[0] == TEST_CITY
    assert isinstance(result[1], float)  # температура
    assert isinstance(result[2], str)  # описание


print("Тесты прошли успешно!")
