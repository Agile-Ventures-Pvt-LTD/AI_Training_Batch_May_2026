## mock raw data for weather jaipur.

MOCK_RAW_WEATHER = {
    "request": [
        {
            "query": "Jaipur",
            "type": "City"
        }
    ],
    "nearest_area": [
        {
            "areaName": [{"value": "Jaipur"}],
            "region": [{"value": "Rajasthan"}],
            "country": [{"value": "India"}]
        }
    ],
    "current_condition": [
        {
            "temp_C": "31",
            "humidity": "48",
            "precipMM": "0.0",
            "windspeedKmph": "12",
            "weatherDesc": [{"value": "Sunny"}]
        }
    ],
    "weather": [
        {
            "date": "2026-06-26",
            "maxtempC": "37",
            "mintempC": "27",
            "avgtempC": "32",
            "totalSnow_cm": "0.0",
            "hourly": [
                {
                    "time": "0",
                    "tempC": "27",
                    "windspeedKmph": "10",
                    "chanceofrain": "10",
                    "precipMM": "0.0",
                    "weatherDesc": [{"value": "Clear"}]
                },
                {
                    "time": "1200",
                    "tempC": "37",
                    "windspeedKmph": "28",
                    "chanceofrain": "60",
                    "precipMM": "1.2",
                    "weatherDesc": [{"value": "Partly cloudy"}]
                }
            ]
        }
    ]
}
