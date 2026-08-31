"""
Base Agent Class - Abstract interface for all specialist agents

Each specialist agent is a pure function that:
1. Takes structured input
2. Performs specific analysis/task
3. Returns structured output
4. Has no side effects
"""

import time
import logging
from abc import ABC, abstractmethod
from typing import Dict, Any
from dataclasses import dataclass
from datetime import datetime

logger = logging.getLogger(__name__)


@dataclass
class AgentResult:
    """Standardized result from agent execution"""

    success: bool
    agent_name: str
    output: Dict[str, Any]
    reasoning: str
    confidence: float  # 0.0 to 1.0
    execution_time_ms: float
    timestamp: str = None

    def __post_init__(self):
        """Initialize timestamp if not provided"""
        if self.timestamp is None:
            self.timestamp = datetime.utcnow().isoformat()

    def to_dict(self) -> Dict[str, Any]:
        """Convert result to dictionary"""
        return {
            'success': self.success,
            'agent_name': self.agent_name,
            'output': self.output,
            'reasoning': self.reasoning,
            'confidence': self.confidence,
            'execution_time_ms': self.execution_time_ms,
            'timestamp': self.timestamp,
        }


class BaseAgent(ABC):
    """
    Abstract base class for all specialist agents.

    Each agent is a pure function that:
    - Takes structured input
    - Performs specific analysis/task
    - Returns structured output with reasoning
    - Has no side effects
    """

    def __init__(self, name: str):
        """Initialize agent with name"""
        self.name = name
        self.logger = logging.getLogger(f"agent.{name}")

    @abstractmethod
    async def execute(self, data: Dict[str, Any]) -> AgentResult:
        """
        Execute the agent's primary task.

        Args:
            data: Input data for the agent

        Returns:
            AgentResult with output and reasoning

        Raises:
            ValueError: If input data is invalid
            RuntimeError: If execution fails
        """
        pass

    @abstractmethod
    def validate_input(self, data: Dict[str, Any]) -> bool:
        """
        Validate input data is in expected format.

        Args:
            data: Input data to validate

        Returns:
            True if valid, False otherwise
        """
        pass

    def _log_execution(self, result: AgentResult) -> None:
        """
        Log agent execution for monitoring.

        Args:
            result: Agent execution result
        """
        self.logger.info(
            f"Agent {self.name} executed: success={result.success}, "
            f"confidence={result.confidence:.2f}, time={result.execution_time_ms:.1f}ms"
        )

    async def execute_safe(self, data: Dict[str, Any]) -> AgentResult:
        """
        Execute agent with error handling and timing.

        Args:
            data: Input data for the agent

        Returns:
            AgentResult with error information if execution fails
        """
        start_time = time.time()

        try:
            # Validate input
            if not self.validate_input(data):
                raise ValueError("Input validation failed")

            # Execute agent logic
            result = await self.execute(data)

            # Log successful execution
            self._log_execution(result)

            return result

        except Exception as e:
            execution_time = (time.time() - start_time) * 1000

            self.logger.error(f"{self.name} execution failed: {e}", exc_info=True)

            return AgentResult(
                success=False,
                agent_name=self.name,
                output={},
                reasoning=f"Error: {str(e)}",
                confidence=0.0,
                execution_time_ms=execution_time,
            )
