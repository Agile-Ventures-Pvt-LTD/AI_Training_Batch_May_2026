from __future__ import annotations
import json
import logging
from pathlib import Path
from typing import Any, Dict, List
from schemas import (TravelAdvisoryReport,TOOLS_USED,RESOURCES_USED,PROMPTS_USED,)
logger = logging.getLogger(__name__)
class ReportWriter:
    """
    Builds and saves the final travel advisory report.
    """
    def __init__(self,output_directory: str = "outputs",) -> None:
        self.output_directory = Path(output_directory)
        self.output_directory.mkdir(parents=True,exist_ok=True,)
        self.output_file = (self.output_directory/ "travel_advisory_report.json")
    def build_report(self,normalized_weather_data: Dict[str, Any],risk_result: Dict[str, Any],packing_suggestions: List[str],travel_readiness_advisory: str,weather_risk_explanation: str,)->Dict[str, Any]:
        """
        Build final report matching PRD schema.
        """
        report = {"destination":normalized_weather_data.get("destination","",),
            "region":
                normalized_weather_data.get("region","",),
            "country":
                normalized_weather_data.get("country","",),
            "forecast_days":
                normalized_weather_data.get("forecast_days",3,),
            "current_weather":normalized_weather_data.get("current_weather",{},),
            "daily_forecast":normalized_weather_data.get("daily_forecast",[],),
            "weather_risk":risk_result.get("weather_risk","LOW",),
            "risk_factors":
                risk_result.get("risk_factors",[],),
            "recommended_actions":risk_result.get("recommended_actions",[],),
            "packing_suggestions":packing_suggestions,
            "travel_readiness_advisory":travel_readiness_advisory,
            "weather_risk_explanation":weather_risk_explanation,
            "resources_used":RESOURCES_USED,
            "tools_used":TOOLS_USED,
            "prompts_used":PROMPTS_USED,}
        return report
    def validate_report(self,report: Dict[str, Any],)-> TravelAdvisoryReport:
        """
        Validate report using Pydantic schema.
        """
        try:
            return TravelAdvisoryReport(**report)
        except Exception as exc:
            logger.exception("Report validation failed")
            raise ValueError(
                f"Invalid report schema: {exc}"
            ) from exc
    def save_report(self,report: Dict[str, Any],)-> Dict[str, Any]:
        """
        Validate and save report.
        Returns:
            Structured success response.
        """
        try:
            validated_report = (self.validate_report(report))
            with open(self.output_file,"w",encoding="utf-8",) as file:
                json.dump(validated_report.model_dump(),file,indent=4,ensure_ascii=False,)
            logger.info("Travel advisory report saved: %s",self.output_file,)
            return {"success": True,"saved_path":str(self.output_file),}
        except Exception as exc:
            logger.exception("Failed to save report")
            return {"success": False,"message": str(exc),}
def write_travel_advisory_report(normalized_weather_data: Dict[str, Any],risk_result: Dict[str, Any],packing_suggestions: List[str],travel_readiness_advisory: str,weather_risk_explanation: str,)-> Dict[str, Any]:
    """
    One-call report generation helper.
    """
    writer = ReportWriter()
    report = writer.build_report(
        normalized_weather_data=
        normalized_weather_data,
        risk_result=
        risk_result,
        packing_suggestions=
        packing_suggestions,
        travel_readiness_advisory=
        travel_readiness_advisory,
        weather_risk_explanation=
        weather_risk_explanation,
    )
    return writer.save_report(report)
if __name__ == "__main__":
    sample_weather_data = {
        "destination": "Jaipur",
        "region": "Rajasthan",
        "country": "India",
        "forecast_days": 3,

        "current_weather": {
            "temperature_c": 31.0,
            "humidity": 48,
            "precipitation_mm": 0.0,
            "wind_speed_kmph": 12.0,
            "weather_description": "Sunny",
        },

        "daily_forecast": [],
    }
    sample_risk = {
        "weather_risk": "MEDIUM",
        "risk_factors": [
            "Maximum temperature is expected to be above 35°C."
        ],
        "recommended_actions": [
            "Carry water and stay hydrated."
        ],
    }
    result = write_travel_advisory_report(
        normalized_weather_data=
        sample_weather_data,
        risk_result=
        sample_risk,
        packing_suggestions=["Water bottle","Sunscreen","Hat",],
        travel_readiness_advisory="Travel appears manageable with basic precautions.",
        weather_risk_explanation="Moderate heat conditions are expected.",)
    print(result)