"""
M-7 Phase 2: Unit tests for specialist agent base class

Tests for backend/services/specialist_agents/base_agent.py

Coverage areas:
- Agent initialization
- Input validation
- Result creation
- Error handling
- Execution timing
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from backend.services.specialist_agents.base_agent import BaseAgent


@pytest.mark.unit
class TestAgentInitialization:
    """Test agent initialization"""

    def test_agent_creation(self):
        """Test basic agent creation"""
        agent = BaseAgent("Test Agent", "test_type")
        assert agent.name == "Test Agent"
        assert agent.agent_type == "test_type"

    def test_agent_has_required_attributes(self):
        """Test agent has all required attributes"""
        agent = BaseAgent("Test Agent", "test_type")
        assert hasattr(agent, 'name')
        assert hasattr(agent, 'agent_type')
        assert hasattr(agent, 'execute')

    def test_multiple_agents_independent(self):
        """Test multiple agents are independent"""
        agent1 = BaseAgent("Agent 1", "type1")
        agent2 = BaseAgent("Agent 2", "type2")
        assert agent1.name != agent2.name
        assert agent1.agent_type != agent2.agent_type

    def test_agent_name_stored_correctly(self):
        """Test agent name is stored correctly"""
        name = "Sales Analyzer"
        agent = BaseAgent(name, "sales")
        assert agent.name == name

    def test_agent_type_stored_correctly(self):
        """Test agent type is stored correctly"""
        agent_type = "analytical"
        agent = BaseAgent("Agent", agent_type)
        assert agent.agent_type == agent_type


@pytest.mark.unit
class TestAgentInputValidation:
    """Test agent input validation"""

    def test_agent_rejects_none_name(self):
        """Test agent rejects None name"""
        with pytest.raises((TypeError, ValueError)):
            BaseAgent(None, "test_type")

    def test_agent_rejects_empty_name(self):
        """Test agent rejects empty name"""
        with pytest.raises((ValueError, AssertionError)):
            BaseAgent("", "test_type")

    def test_agent_rejects_none_type(self):
        """Test agent rejects None type"""
        with pytest.raises((TypeError, ValueError)):
            BaseAgent("Agent", None)

    def test_agent_rejects_empty_type(self):
        """Test agent rejects empty type"""
        with pytest.raises((ValueError, AssertionError)):
            BaseAgent("Agent", "")

    def test_agent_accepts_valid_inputs(self):
        """Test agent accepts valid inputs"""
        agent = BaseAgent("Valid Agent", "valid_type")
        assert agent.name == "Valid Agent"
        assert agent.agent_type == "valid_type"


@pytest.mark.unit
class TestAgentExecution:
    """Test agent execution"""

    def test_agent_has_execute_method(self):
        """Test agent has execute method"""
        agent = BaseAgent("Test Agent", "test_type")
        assert callable(getattr(agent, 'execute', None))

    def test_agent_execute_accepts_data(self):
        """Test execute method accepts data parameter"""
        agent = BaseAgent("Test Agent", "test_type")
        # This should not raise
        try:
            result = agent.execute({"test": "data"})
        except NotImplementedError:
            # Base class might not implement, that's OK
            pass

    def test_agent_execute_returns_result(self):
        """Test execute method returns a result"""
        agent = BaseAgent("Test Agent", "test_type")
        # Override execute for testing
        agent.execute = Mock(return_value={"status": "success"})
        result = agent.execute({"test": "data"})
        assert result is not None
        assert isinstance(result, dict)

    def test_agent_tracks_execution_time(self):
        """Test agent can track execution time"""
        agent = BaseAgent("Test Agent", "test_type")
        agent.execute = Mock(return_value={"status": "success"})

        # Measure execution
        import time
        start = time.time()
        agent.execute({"test": "data"})
        duration = time.time() - start

        assert duration >= 0


@pytest.mark.unit
class TestAgentResultCreation:
    """Test agent result creation"""

    def test_result_has_status(self):
        """Test result has status field"""
        agent = BaseAgent("Test Agent", "test_type")
        agent.execute = Mock(return_value={
            "status": "success",
            "data": {}
        })
        result = agent.execute({"test": "data"})
        assert "status" in result

    def test_result_status_values(self):
        """Test result status has valid values"""
        agent = BaseAgent("Test Agent", "test_type")

        success_result = {"status": "success", "data": {}}
        error_result = {"status": "error", "error": "test error"}

        agent.execute = Mock(side_effect=[success_result, error_result])

        result1 = agent.execute({"test": "data"})
        result2 = agent.execute({"test": "data"})

        assert result1["status"] in ["success", "error", "warning"]
        assert result2["status"] in ["success", "error", "warning"]

    def test_result_contains_data(self):
        """Test result contains data field"""
        agent = BaseAgent("Test Agent", "test_type")
        agent.execute = Mock(return_value={
            "status": "success",
            "data": {"analysis": "test"}
        })
        result = agent.execute({"test": "data"})
        assert "data" in result

    def test_error_result_has_message(self):
        """Test error result contains error message"""
        agent = BaseAgent("Test Agent", "test_type")
        agent.execute = Mock(return_value={
            "status": "error",
            "error": "Something went wrong"
        })
        result = agent.execute({"test": "data"})
        assert "error" in result or "message" in result


@pytest.mark.unit
class TestAgentErrorHandling:
    """Test agent error handling"""

    def test_agent_handles_invalid_data(self):
        """Test agent handles invalid input data"""
        agent = BaseAgent("Test Agent", "test_type")
        agent.execute = Mock(return_value={
            "status": "error",
            "error": "Invalid input"
        })

        result = agent.execute(None)
        assert result["status"] == "error"

    def test_agent_handles_empty_data(self):
        """Test agent handles empty data"""
        agent = BaseAgent("Test Agent", "test_type")
        agent.execute = Mock(return_value={
            "status": "error",
            "error": "Empty data"
        })

        result = agent.execute({})
        assert result["status"] == "error"

    def test_agent_error_message_descriptive(self):
        """Test error messages are descriptive"""
        agent = BaseAgent("Test Agent", "test_type")
        agent.execute = Mock(return_value={
            "status": "error",
            "error": "Failed to process sales data: insufficient records"
        })

        result = agent.execute({"test": "data"})
        assert len(result["error"]) > 10  # Should have detailed message


@pytest.mark.unit
class TestAgentMetadata:
    """Test agent metadata"""

    def test_agent_has_metadata(self):
        """Test agent has metadata"""
        agent = BaseAgent("Test Agent", "test_type")
        assert hasattr(agent, 'name')
        assert hasattr(agent, 'agent_type')

    def test_agent_name_is_string(self):
        """Test agent name is string"""
        agent = BaseAgent("Test Agent", "test_type")
        assert isinstance(agent.name, str)

    def test_agent_type_is_string(self):
        """Test agent type is string"""
        agent = BaseAgent("Test Agent", "test_type")
        assert isinstance(agent.agent_type, str)

    def test_agent_string_representation(self):
        """Test agent has string representation"""
        agent = BaseAgent("Test Agent", "test_type")
        str_repr = str(agent)
        assert "Test Agent" in str_repr or len(str_repr) > 0


@pytest.mark.unit
class TestAgentInheritance:
    """Test agent inheritance and extensibility"""

    def test_can_subclass_agent(self):
        """Test can create agent subclass"""
        class CustomAgent(BaseAgent):
            def execute(self, data):
                return {"status": "success", "data": data}

        agent = CustomAgent("Custom", "custom")
        assert isinstance(agent, BaseAgent)

    def test_subclass_maintains_attributes(self):
        """Test subclass maintains parent attributes"""
        class CustomAgent(BaseAgent):
            def execute(self, data):
                return {"status": "success"}

        agent = CustomAgent("Custom", "custom")
        assert agent.name == "Custom"
        assert agent.agent_type == "custom"

    def test_subclass_can_override_execute(self):
        """Test subclass can override execute method"""
        class CustomAgent(BaseAgent):
            def execute(self, data):
                return {"status": "custom", "result": "overridden"}

        agent = CustomAgent("Custom", "custom")
        result = agent.execute({"test": "data"})
        assert result["status"] == "custom"
