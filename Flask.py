import json
import urllib.parse
import urllib.request
from datetime import datetime

from flask import Flask, render_template, request

app = Flask(__name__)


def weather_code_info(code: int):
    mapping = {
        0: ("☀️", "Clear sky"),
        1: ("🌤️", "Mainly clear"),
        2: ("⛅", "Partly cloudy"),
        3: ("☁️", "Overcast"),
        45: ("🌫️", "Fog"),
        48: ("🌫️", "Depositing rime fog"),
        51: ("🌦️", "Light drizzle"),
        53: ("🌦️", "Moderate drizzle"),
        55: ("🌧️", "Dense drizzle"),
        56: ("🌧️", "Light freezing drizzle"),
        57: ("🌧️", "Dense freezing drizzle"),
        61: ("🌦️", "Slight rain"),
        63: ("🌧️", "Moderate rain"),
        65: ("🌧️", "Heavy rain"),
        66: ("🌧️", "Light freezing rain"),
        67: ("🌧️", "Heavy freezing rain"),
        71: ("🌨️", "Slight snow"),
        73: ("❄️", "Moderate snow"),
        75: ("❄️", "Heavy snow"),
        77: ("❄️", "Snow grains"),
        80: ("🌦️", "Rain showers"),
        81: ("🌧️", "Moderate showers"),
        82: ("🌧️", "Violent showers"),
        85: ("🌨️", "Snow showers"),
        86: ("🌨️", "Heavy snow showers"),
        95: ("⛈️", "Thunderstorm"),
        96: ("⛈️", "Thunderstorm with hail"),
        99: ("⛈️", "Heavy thunderstorm with hail"),
    }
    return mapping.get(code, ("🌤️", "Weather conditions"))


def fetch_json(url: str):
    request = urllib.request.Request(url, headers={"User-Agent": "WeatherApp/1.0"})
    with urllib.request.urlopen(request, timeout=12) as response:
        return json.loads(response.read().decode("utf-8"))


def build_forecast(daily_data):
    if not daily_data:
        return []

    forecast = []
    times = daily_data.get("time") or []
    codes = daily_data.get("weather_code") or []
    max_temps = daily_data.get("temperature_2m_max") or []
    min_temps = daily_data.get("temperature_2m_min") or []
    precip_probs = daily_data.get("precipitation_probability_max") or []

    for index, day in enumerate(times):
        try:
            code = int(codes[index]) if index < len(codes) else 0
            max_temp = round(float(max_temps[index]), 1) if index < len(max_temps) else 0.0
            min_temp = round(float(min_temps[index]), 1) if index < len(min_temps) else 0.0
            precip = int(precip_probs[index]) if index < len(precip_probs) else 0
            icon, description = weather_code_info(code)
            forecast_date = datetime.fromisoformat(str(day))
            forecast.append(
                {
                    "date": day,
                    "day": forecast_date.strftime("%a"),
                    "icon": icon,
                    "description": description,
                    "max_temp": max_temp,
                    "min_temp": min_temp,
                    "precipitation": precip,
                }
            )
        except (TypeError, ValueError, IndexError):
            continue

    return forecast


@app.route("/", methods=["GET", "POST"])
def home():
    city = ""
    result = None
    error = None

    if request.method == "POST":
        city = (request.form.get("city") or "").strip()

        if not city:
            error = "Please enter a city name."
            return render_template("index.html", city=city, result=result, error=error)

        try:
            geo_url = (
                "https://geocoding-api.open-meteo.com/v1/search?"
                f"name={urllib.parse.quote(city)}&count=1&language=en&format=json"
            )
            geo_data = fetch_json(geo_url)
            locations = geo_data.get("results") or []

            if not locations:
                error = f"No weather data found for '{city}'."
                return render_template("index.html", city=city, result=result, error=error)

            place = locations[0]
            lat = place["latitude"]
            lon = place["longitude"]

            weather_url = (
                "https://api.open-meteo.com/v1/forecast?"
                f"latitude={lat}&longitude={lon}&current=temperature_2m,relative_humidity_2m,"
                "wind_speed_10m,weather_code&daily=weather_code,temperature_2m_max,temperature_2m_min,"
                "precipitation_probability_max&timezone=auto&forecast_days=10"
            )
            weather_data = fetch_json(weather_url)
            current = weather_data.get("current", {})
            daily = weather_data.get("daily", {})

            code = int(current.get("weather_code", 0))
            icon, description = weather_code_info(code)

            result = {
                "city": place.get("name", city),
                "country": place.get("country", ""),
                "temperature": round(float(current.get("temperature_2m", 0)), 1),
                "humidity": int(current.get("relative_humidity_2m", 0)),
                "wind": round(float(current.get("wind_speed_10m", 0)), 1),
                "description": description,
                "icon": icon,
                "forecast": build_forecast(daily),
            }

        except Exception:
            error = f"Unable to fetch weather for '{city}'. Please try another city."

    return render_template("index.html", city=city, result=result, error=error)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
