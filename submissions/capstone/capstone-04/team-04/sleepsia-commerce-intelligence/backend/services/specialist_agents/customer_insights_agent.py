"""
Customer Insights Specialist Agent - Analyzes customer behavior and segments
"""

import time
import logging
from typing import Dict, Any

from backend.services.specialist_agents.base_agent import BaseAgent, AgentResult

logger = logging.getLogger(__name__)


class CustomerInsightsAgent(BaseAgent):
    """
    Analyzes customer data for insights and segmentation.

    Input:
    {
        "merchant_id": "merchant_123",
        "customers": [
            {"customer_id": "c1", "lifetime_value": 5000, "days_since_purchase": 10},
            ...
        ]
    }

    Output:
    {
        "total_customers": 100,
        "avg_ltv": 2500,
        "high_value_count": 20,
        "at_risk_count": 5
    }
    """

    def __init__(self):
        """Initialize Customer Insights Agent"""
        super().__init__("CustomerInsightsAgent")

    def validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate customer data has required fields"""
        required = ['merchant_id', 'customers']
        return all(k in data for k in required) and isinstance(data['customers'], list)

    async def execute(self, data: Dict[str, Any]) -> AgentResult:
        """Analyze customer data and return insights"""
        start_time = time.time()

        try:
            if not self.validate_input(data):
                raise ValueError("Missing required fields: merchant_id, customers")

            customers = data['customers']
            insights = self._analyze_customers(customers)

            execution_time = (time.time() - start_time) * 1000

            return AgentResult(
                success=True,
                agent_name=self.name,
                output=insights,
                reasoning=f"Analyzed {len(customers)} customers",
                confidence=0.92,
                execution_time_ms=execution_time,
            )

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000
            self.logger.error(f"Customer insights analysis failed: {e}")

            return AgentResult(
                success=False,
                agent_name=self.name,
                output={},
                reasoning=str(e),
                confidence=0.0,
                execution_time_ms=execution_time,
            )

    def _analyze_customers(self, customers: list) -> Dict[str, Any]:
        """Pure function - analyze customer metrics"""
        if not customers:
            return {
                'total_customers': 0,
                'avg_ltv': 0,
                'high_value_count': 0,
                'at_risk_count': 0,
            }

        # Calculate LTV metrics
        total_ltv = sum(c.get('lifetime_value', 0) for c in customers)
        avg_ltv = total_ltv / len(customers) if customers else 0

        # Segment customers
        high_value = len([c for c in customers if c.get('lifetime_value', 0) > avg_ltv * 2])
        at_risk = len([c for c in customers if c.get('days_since_purchase', 999) > 90])
        loyal = len([c for c in customers if c.get('purchase_count', 0) > 5])

        return {
            'total_customers': len(customers),
            'avg_ltv': float(avg_ltv),
            'high_value_count': high_value,
            'at_risk_count': at_risk,
            'loyal_count': loyal,
            'total_ltv': float(total_ltv),
        }
