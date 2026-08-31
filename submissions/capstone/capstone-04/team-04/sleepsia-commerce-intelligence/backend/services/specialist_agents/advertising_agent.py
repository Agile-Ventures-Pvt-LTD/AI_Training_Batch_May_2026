"""
Advertising Specialist Agent - Analyzes advertising campaigns and ROI
"""

import time
import logging
from typing import Dict, Any

from backend.services.specialist_agents.base_agent import BaseAgent, AgentResult

logger = logging.getLogger(__name__)


class AdvertisingAgent(BaseAgent):
    """
    Analyzes advertising campaigns and ROI.

    Input:
    {
        "merchant_id": "merchant_123",
        "campaigns": [
            {"name": "Summer Sale", "spend": 1000, "impressions": 50000, "clicks": 500, "sales": 5000}
        ]
    }

    Output:
    {
        "total_spend": 5000,
        "total_impressions": 250000,
        "total_clicks": 2500,
        "average_ctr": 1.0,
        "average_cpc": 2.0,
        "roas": 5.0
    }
    """

    def __init__(self):
        """Initialize Advertising Agent"""
        super().__init__("AdvertisingAgent")

    def validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate advertising data has required fields"""
        required = ['merchant_id', 'campaigns']
        return all(k in data for k in required) and isinstance(data['campaigns'], list)

    async def execute(self, data: Dict[str, Any]) -> AgentResult:
        """Analyze advertising data and return insights"""
        start_time = time.time()

        try:
            if not self.validate_input(data):
                raise ValueError("Missing required fields: merchant_id, campaigns")

            campaigns = data['campaigns']
            analysis = self._analyze_campaigns(campaigns)

            execution_time = (time.time() - start_time) * 1000

            return AgentResult(
                success=True,
                agent_name=self.name,
                output=analysis,
                reasoning=f"Analyzed {len(campaigns)} ad campaigns",
                confidence=0.90,
                execution_time_ms=execution_time,
            )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self.logger.error(f"Advertising analysis failed: {e}")

            return AgentResult(
                success=False,
                agent_name=self.name,
                output={},
                reasoning=str(e),
                confidence=0.0,
                execution_time_ms=execution_time,
            )

    def _analyze_campaigns(self, campaigns: list) -> Dict[str, Any]:
        """Pure function - analyze ad performance"""
        if not campaigns:
            return {
                'total_spend': 0,
                'total_impressions': 0,
                'total_clicks': 0,
                'average_ctr': 0,
                'average_cpc': 0,
                'roas': 0,
                'campaign_count': 0,
            }

        total_spend = sum(c.get('spend', 0) for c in campaigns)
        total_impressions = sum(c.get('impressions', 0) for c in campaigns)
        total_clicks = sum(c.get('clicks', 0) for c in campaigns)
        total_sales = sum(c.get('sales', 0) for c in campaigns)

        # Calculate metrics
        avg_ctr = (total_clicks / total_impressions * 100) if total_impressions > 0 else 0
        avg_cpc = (total_spend / total_clicks) if total_clicks > 0 else 0
        roas = (total_sales / total_spend) if total_spend > 0 else 0

        return {
            'total_spend': float(total_spend),
            'total_impressions': total_impressions,
            'total_clicks': total_clicks,
            'average_ctr': float(avg_ctr),
            'average_cpc': float(avg_cpc),
            'roas': float(roas),
            'campaign_count': len(campaigns),
            'total_sales': float(total_sales),
        }
