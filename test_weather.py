import os
import sqlite3
import pytest
from weather_api import get_weather
from bott import connect, init_db, get_or_create_city_id

API_KEY = "6596f316a56103539735bd87c6246997"


def test_get_weather_valid_city():
    result = get_weather("Almaty", API_KEY)
    assert "city" in result
    assert result["city"] == "Алматы"
    assert "temperature" in result
    assert "description" in result


def test_get_weather_invalid_city():
    result = get_weather("NarniaRandomFake", API_KEY)
    assert "error" in result
    assert "Город не найден" in result["error"]


def test_db_connection():
    conn = connect()
    assert isinstance(conn, sqlite3.Connection)
    conn.close()


def test_city_insert_and_fetch():
    conn = connect()
    cursor = conn.cursor()
    init_db()

    city_name = "TestCity123"
    city_id = get_or_create_city_id(cursor, city_name)
    conn.commit()

    cursor.execute("SELECT name FROM cities WHERE id = ?", (city_id,))
    result = cursor.fetchone()

    assert result is not None
    assert result[0] == city_name

    # очистка
    cursor.execute("DELETE FROM cities WHERE id = ?", (city_id,))
    conn.commit()
    conn.close()
