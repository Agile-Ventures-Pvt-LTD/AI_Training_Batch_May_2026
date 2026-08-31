"""
Sales Specialist Agent - Analyzes sales data and provides performance insights
"""

import time
import logging
from typing import Dict, Any

from backend.services.specialist_agents.base_agent import BaseAgent, AgentResult

logger = logging.getLogger(__name__)


class SalesAgent(BaseAgent):
    """
    Analyzes sales data and provides insights.

    Input:
    {
        "merchant_id": "merchant_123",
        "sales_data": [{"date": "2024-08-01", "amount": 1000}, ...],
        "time_period": "monthly"
    }

    Output:
    {
        "total_sales": 50000,
        "average_daily": 1612.9,
        "growth_rate": 0.15,
        "trend": "upward"
    }
    """

    def __init__(self):
        """Initialize Sales Agent"""
        super().__init__("SalesAgent")

    def validate_input(self, data: Dict[str, Any]) -> bool:
        """Validate sales data has required fields"""
        required = ['merchant_id', 'sales_data']
        return all(k in data for k in required) and isinstance(data['sales_data'], list)

    async def execute(self, data: Dict[str, Any]) -> AgentResult:
        """Analyze sales data and return insights"""
        start_time = time.time()

        try:
            # Validate input
            if not self.validate_input(data):
                raise ValueError("Missing required fields: merchant_id, sales_data")

            # Extract data
            merchant_id = data['merchant_id']
            sales_data = data['sales_data']

            # Analyze
            analysis = self._analyze_sales(sales_data)

            execution_time = (time.time() - start_time) * 1000

            result = AgentResult(
                success=True,
                agent_name=self.name,
                output=analysis,
                reasoning=f"Analyzed {len(sales_data)} sales records for merchant {merchant_id}",
                confidence=0.95,
                execution_time_ms=execution_time,
            )

            self._log_execution(result)
            return result

        except Exception as e:
            self.logger.error(f"Sales analysis failed: {e}")
            execution_time = (time.time() - start_time) * 1000

            return AgentResult(
                success=False,
                agent_name=self.name,
                output={},
                reasoning=f"Error: {str(e)}",
                confidence=0.0,
                execution_time_ms=execution_time,
            )

    def _analyze_sales(self, sales_data: list) -> Dict[str, Any]:
        """Pure function - analyze sales data"""
        if not sales_data:
            return {
                'total_sales': 0,
                'average_daily': 0,
                'growth_rate': 0,
                'trend': 'no_data',
                'record_count': 0,
            }

        # Extract amounts
        amounts = [s.get('amount', 0) for s in sales_data]

        # Calculate metrics
        total = sum(amounts)
        average = total / len(amounts) if amounts else 0

        # Calculate growth
        if len(amounts) >= 2:
            first_half = sum(amounts[:len(amounts)//2])
            second_half = sum(amounts[len(amounts)//2:])
            growth_rate = (second_half - first_half) / (first_half or 1)
        else:
            growth_rate = 0

        # Determine trend
        if growth_rate > 0.1:
            trend = 'upward'
        elif growth_rate < -0.1:
            trend = 'downward'
        else:
            trend = 'stable'

        return {
            'total_sales': float(total),
            'average_daily': float(average),
            'growth_rate': float(growth_rate),
            'trend': trend,
            'record_count': len(sales_data),
        }
