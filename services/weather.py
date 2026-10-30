"""Consulta de dados atuais pela API pública Open-Meteo."""
import httpx


def get_weather(city):
    if not city.strip():
        raise ValueError("Informe o nome de uma cidade.")
    with httpx.Client(timeout=12.0) as client:
        geo = client.get("https://geocoding-api.open-meteo.com/v1/search", params={
            "name": city.strip(), "count": 1, "language": "pt", "format": "json", "countryCode": "BR"
        })
        geo.raise_for_status()
        locations = geo.json().get("results", [])
        if not locations:
            raise ValueError("Cidade brasileira não encontrada.")
        location = locations[0]
        response = client.get("https://api.open-meteo.com/v1/forecast", params={
            "latitude": location["latitude"], "longitude": location["longitude"],
            "current": "temperature_2m,relative_humidity_2m,wind_speed_10m", "timezone": "auto"
        })
        response.raise_for_status()
        current = response.json()["current"]
    return {
        "cidade": location["name"], "estado": location.get("admin1", ""),
        "pais": location.get("country", ""), "horario_medicao": current["time"],
        "temperatura_c": current["temperature_2m"],
        "umidade_percentual": current["relative_humidity_2m"],
        "vento_kmh": current["wind_speed_10m"], "fonte": "Open-Meteo",
    }
