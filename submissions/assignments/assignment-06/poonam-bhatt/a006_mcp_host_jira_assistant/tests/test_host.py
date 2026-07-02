import pytest
import asyncio
from unittest.mock import AsyncMock, patch, MagicMock
from src.host import JiraIssueAssistantHost

# Define mock Tool class since list_tools returns custom Tool structures
class MockTool:
    def __init__(self, name, description, input_schema):
        self.name = name
        self.description = description
        self.inputSchema = input_schema

class MockContent:
    def __init__(self, text):
        self.text = text

class MockCallResult:
    def __init__(self, content):
        self.content = content

@pytest.mark.asyncio
async def test_tool_discovery():
    """Verify tool discovery phase in host coordinates correctly."""
    # We will mock JiraMCPClient methods
    with patch("src.host.JiraMCPClient") as MockClient:
        instance = MockClient.return_value
        instance.connect = AsyncMock()
        instance.disconnect = AsyncMock()
        instance.list_available_tools = AsyncMock(return_value=[
            MockTool("list_projects", "List projects", {}),
            MockTool("search_issues", "Search issues", {})
        ])
        
        # Instantiate host
        host = JiraIssueAssistantHost()
        
        # Test connect and discovery
        await host.mcp_client.connect()
        tools = await host.mcp_client.list_available_tools()
        await host.mcp_client.disconnect()
        
        assert len(tools) == 2
        assert tools[0].name == "list_projects"
        assert tools[1].name == "search_issues"
        instance.connect.assert_called_once()
        instance.disconnect.assert_called_once()

@pytest.mark.asyncio
@patch("src.host.GroqLLMClient")
@patch("src.host.JiraMCPClient")
async def test_query_execution(MockClient, MockLLM):
    """Test that a simple query runs end-to-end with tool calling and final answers."""
    # 1. Setup client mock
    client_instance = MockClient.return_value
    client_instance.connect = AsyncMock()
    client_instance.disconnect = AsyncMock()
    
    # Tool definitions returned by discovery
    mock_tools = [
        MockTool("list_projects", "List projects", {})
    ]
    client_instance.list_available_tools = AsyncMock(return_value=mock_tools)
    
    # Tool call response from the server
    mock_mcp_result = MockCallResult([MockContent('[{"key": "DEMO", "name": "Demo"}]')])
    client_instance.call_server_tool = AsyncMock(return_value=mock_mcp_result)
    
    # 2. Setup LLM mock
    llm_instance = MockLLM.return_value
    llm_instance.convert_mcp_tools_to_groq.return_value = [{"type": "function", "function": {"name": "list_projects"}}]
    
    # Construct mock completions responses:
    # First response: Ask for tool call
    mock_tool_call = MagicMock()
    mock_tool_call.id = "call_1"
    mock_tool_call.function.name = "list_projects"
    mock_tool_call.function.arguments = "{}"
    
    mock_msg_1 = MagicMock()
    mock_msg_1.content = None
    mock_msg_1.tool_calls = [mock_tool_call]
    
    mock_choice_1 = MagicMock()
    mock_choice_1.message = mock_msg_1
    
    mock_resp_1 = MagicMock()
    mock_resp_1.choices = [mock_choice_1]
    
    # Second response: Formulate final answer based on tool output
    mock_msg_2 = MagicMock()
    mock_msg_2.content = "Here is the list of projects: DEMO"
    mock_msg_2.tool_calls = None
    
    mock_choice_2 = MagicMock()
    mock_choice_2.message = mock_msg_2
    
    mock_resp_2 = MagicMock()
    mock_resp_2.choices = [mock_choice_2]
    
    # Side effects to return tool call first, then text response
    llm_instance.get_chat_response.side_effect = [mock_resp_1, mock_resp_2]
    
    # 3. Instantiate and run Host query
    host = JiraIssueAssistantHost()
    result = await host.run_query("List all projects")
    
    # Assertions
    assert result["user_query"] == "List all projects"
    assert "list_projects" in result["tools_used"]
    assert "DEMO" in result["final_answer"]
    assert result["write_action_performed"] is False
    
    # Verify mock interactions
    client_instance.connect.assert_called_once()
    client_instance.list_available_tools.assert_called_once()
    client_instance.call_server_tool.assert_called_once_with("list_projects", {})
    client_instance.disconnect.assert_called_once()

@pytest.mark.asyncio
@patch("src.host.GroqLLMClient")
@patch("src.host.JiraMCPClient")
async def test_multi_tool_flow(MockClient, MockLLM):
    """Test sequential multi-step tool calls flow (e.g. details then comments)."""
    client_instance = MockClient.return_value
    client_instance.connect = AsyncMock()
    client_instance.disconnect = AsyncMock()
    client_instance.list_available_tools = AsyncMock(return_value=[
        MockTool("get_issue_details", "", {}),
        MockTool("get_issue_comments", "", {})
    ])
    
    # Mock sequential calls: first get_issue_details, second get_issue_comments
    mock_details_result = MockCallResult([MockContent('{"key": "ABC-12", "summary": "Bad Bug"}')])
    mock_comments_result = MockCallResult([MockContent('[{"author": "Bob", "body": "QA pending"}]')])
    client_instance.call_server_tool.side_effect = [mock_details_result, mock_comments_result]
    
    # Setup LLM response sequential logic
    # Step 1: Request get_issue_details
    tc1 = MagicMock()
    tc1.id = "c1"
    tc1.function.name = "get_issue_details"
    tc1.function.arguments = '{"issue_key": "ABC-12"}'
    m1 = MagicMock()
    m1.content = None
    m1.tool_calls = [tc1]
    r1 = MagicMock(choices=[MagicMock(message=m1)])
    
    # Step 2: Request get_issue_comments
    tc2 = MagicMock()
    tc2.id = "c2"
    tc2.function.name = "get_issue_comments"
    tc2.function.arguments = '{"issue_key": "ABC-12"}'
    m2 = MagicMock()
    m2.content = None
    m2.tool_calls = [tc2]
    r2 = MagicMock(choices=[MagicMock(message=m2)])
    
    # Step 3: Return summary combining both
    m3 = MagicMock()
    m3.content = "Summary: Bad Bug. Comment by Bob: QA pending."
    m3.tool_calls = None
    r3 = MagicMock(choices=[MagicMock(message=m3)])
    
    llm_instance = MockLLM.return_value
    llm_instance.convert_mcp_tools_to_groq.return_value = [
        {"type": "function", "function": {"name": "get_issue_details"}},
        {"type": "function", "function": {"name": "get_issue_comments"}}
    ]
    llm_instance.get_chat_response.side_effect = [r1, r2, r3]
    
    host = JiraIssueAssistantHost()
    result = await host.run_query("Summarize ABC-12 including comments")
    
    assert "get_issue_details" in result["tools_used"]
    assert "get_issue_comments" in result["tools_used"]
    assert "QA pending" in result["final_answer"]
    assert result["write_action_performed"] is False

@pytest.mark.asyncio
@patch("src.host.GroqLLMClient")
@patch("src.host.JiraMCPClient")
async def test_write_operation(MockClient, MockLLM):
    """Test that a write tool sets write_action_performed to True."""
    client_instance = MockClient.return_value
    client_instance.connect = AsyncMock()
    client_instance.disconnect = AsyncMock()
    client_instance.list_available_tools = AsyncMock(return_value=[
        MockTool("add_issue_comment", "", {})
    ])
    
    mock_mcp_result = MockCallResult([MockContent('{"status": "Comment added successfully"}')])
    client_instance.call_server_tool.return_value = mock_mcp_result
    
    # Setup LLM response: first call add_issue_comment, second return message text
    tc1 = MagicMock()
    tc1.id = "c1"
    tc1.function.name = "add_issue_comment"
    tc1.function.arguments = '{"issue_key": "ABC-5", "comment_text": "QA validation is pending"}'
    m1 = MagicMock(content=None, tool_calls=[tc1])
    r1 = MagicMock(choices=[MagicMock(message=m1)])
    
    m2 = MagicMock(content="Comment successfully added to ABC-5.", tool_calls=None)
    r2 = MagicMock(choices=[MagicMock(message=m2)])
    
    llm_instance = MockLLM.return_value
    llm_instance.convert_mcp_tools_to_groq.return_value = [{"type": "function", "function": {"name": "add_issue_comment"}}]
    llm_instance.get_chat_response.side_effect = [r1, r2]
    
    host = JiraIssueAssistantHost()
    result = await host.run_query("Add a comment to ABC-5 saying QA validation is pending")
    
    assert "add_issue_comment" in result["tools_used"]
    assert result["write_action_performed"] is True
    assert "successfully added" in result["final_answer"]
