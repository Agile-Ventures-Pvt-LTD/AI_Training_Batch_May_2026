import os
import requests
from dotenv import load_dotenv

load_dotenv()

PRIMARY = os.getenv("WTTR_PRIMARY_URL", "https://wttr.in")
FALLBACK = os.getenv("WTTR_FALLBACK_URL", "https://wttr.is")


def get_weather_from_wttr(city_name: str):
    urls = [
        f"{PRIMARY}/{city_name}?format=j1",
        f"{FALLBACK}/{city_name}?format=j1"
    ]

    last_error = None

    for url in urls:
        try:
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                return {
                    "success": True,
                    "raw_weather_data": r.json()
                }
        except Exception as e:
            last_error = str(e)

    return {
        "success": False,
        "message": f"Unable to fetch weather data: {last_error}"
    }
# # from mcp_use import MCPClient
# # from dotenv import load_dotenv
# # import os
# # import requests

# # load_dotenv()

# # PRIMARY = os.getenv("WTTR_PRIMARY_URL", "https://wttr.in")
# # FALLBACK = os.getenv("WTTR_FALLBACK_URL", "https://wttr.is")


# # def get_weather_from_wttr(city_name: str):
# #     urls = [
# #         f"{PRIMARY}/{city_name}?format=j1",
# #         f"{FALLBACK}/{city_name}?format=j1"
# #     ]

# #     last_error = None

# #     for url in urls:
# #         try:
# #             r = requests.get(url, timeout=10)
# #             if r.status_code == 200:
# #                 return {
# #                     "success": True,
# #                     "raw_weather_data": r.json()
# #                 }
# #         except Exception as e:
# #             last_error = str(e)

# #     return {
# #         "success": False,
# #         "message": f"Unable to fetch weather data: {last_error}"
# #     }


# # # ✅ helper to fix response format
# # def extract_output(res):
# #     if isinstance(res, dict) and "output" in res:
# #         return res["output"]
# #     return res


# # # ---------------- MCP CLIENT FLOW ---------------- #

# # def run(city: str):

# #     client = MCPClient({
# #         "mcpServers": {
# #             "weather-server": {
# #                 "command": "python",
# #                 "args": ["src/server.py"]
# #             }
# #         }
# #     })

# #     # ✅ IMPORTANT
# #     # client.start()

# #     # ---------------- STEP 1 ---------------- #
# #     step1 = client.request({
# #         "type": "tool",
# #         "name": "validate_city_input_tool_wrapper",
# #         "input": {"city_name": city}
# #     })
# #     step1 = extract_output(step1)

# #     if not step1.get("success"):
# #         print("Error:", step1.get("message"))
# #         return

# #     # ---------------- STEP 2 ---------------- #
# #     step2 = client.request({
# #         "type": "tool",
# #         "name": "get_weather_forecast_tool_wrapper",
# #         "input": {
# #             "normalized_city_name": step1["normalized_city_name"]
# #         }
# #     })
# #     step2 = extract_output(step2)

# #     if not step2.get("success"):
# #         print("Error:", step2.get("message"))
# #         return

# #     # ---------------- STEP 3 ---------------- #
# #     step3 = client.request({
# #         "type": "tool",
# #         "name": "normalize_weather_data_tool_wrapper",
# #         "input": {
# #             "raw_weather_data": step2["raw_weather_data"]
# #         }
# #     })
# #     step3 = extract_output(step3)

# #     if not step3.get("success"):
# #         print("Error: normalization failed")
# #         return

# #     # ---------------- STEP 4 ---------------- #
# #     step4 = client.request({
# #         "type": "tool",
# #         "name": "calculate_weather_risk_tool_wrapper",
# #         "input": {
# #             "normalized_weather_data": step3
# #         }
# #     })
# #     step4 = extract_output(step4)

# #     # ---------------- STEP 5 ---------------- #
# #     from src.report_writer import build_report
# #     report = build_report(step3, step4)

# #     # ---------------- STEP 6 ---------------- #
# #     client.request({
# #         "type": "tool",
# #         "name": "save_travel_advisory_tool_wrapper",
# #         "input": {"report": report}
# #     })

# #     print("✅ Travel advisory generated successfully")
# #     print("📁 Check: outputs/travel_advisory_report.json")


# # # ---------------- ENTRY POINT ---------------- #

# # if __name__ == "__main__":
# #     run("Jaipur")

# from tools import (
#     validate_city_input_tool,
#     get_weather_forecast_tool,
#     normalize_weather_data_tool,
#     calculate_weather_risk_tool,
#     save_travel_advisory_tool
# )

# from report_writer import build_report


# def run(city: str):

#     # ---------------- STEP 1 ---------------- #
#     step1 = validate_city_input_tool({
#         "city_name": city
#     })

#     if not step1.get("success"):
#         print("Error:", step1.get("message"))
#         return

#     # ---------------- STEP 2 ---------------- #
#     step2 = get_weather_forecast_tool({
#         "normalized_city_name": step1["normalized_city_name"]
#     })

#     if not step2.get("success"):
#         print("Error:", step2.get("message"))
#         return

#     # ---------------- STEP 3 ---------------- #
#     step3 = normalize_weather_data_tool({
#         "raw_weather_data": step2["raw_weather_data"]
#     })

#     if not step3.get("success"):
#         print("Error: normalization failed")
#         return

#     # ---------------- STEP 4 ---------------- #
#     step4 = calculate_weather_risk_tool({
#         "normalized_weather_data": step3
#     })

#     # ---------------- STEP 5 ---------------- #
#     report = build_report(step3, step4)

#     # ---------------- STEP 6 ---------------- #
#     save_travel_advisory_tool({
#         "report": report
#     })

#     print("✅ Travel advisory generated successfully")
#     print("📁 Check: outputs/travel_advisory_report.json")


# if __name__ == "__main__":
#     run("Jaipur")