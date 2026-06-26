import os
import json
import csv
import pytest
from deepeval.test_case import LLMTestCase, ToolCall
from deepeval.metrics import AnswerRelevancyMetric, FaithfulnessMetric, ToolCorrectnessMetric
from deepeval.models import GPTModel
from src.config import GROQ_MODEL, GROQ_API_KEY
from src.scoring import calculate_recommendation_band

eval_model = GPTModel(
    model=GROQ_MODEL,
    api_key=GROQ_API_KEY,
    base_url="https://api.groq.com/openai/v1"
)

evaluation_results = []

def teardown_module(module):
    evals_dir = os.path.dirname(os.path.abspath(__file__))
    report_path = os.path.join(evals_dir, "evaluation_report.md")
    
    md_content = "# DeepEval Evaluation Report Summary\n\n"
    md_content += "This report summarizes the DeepEval test results for candidates.\n\n"
    md_content += "| Candidate ID | Answer Relevancy | Faithfulness | Tool Correctness |\n"
    md_content += "|---|---|---|---|\n"
    
    for res in evaluation_results:
        md_content += f"| {res['candidate_id']} | {res['relevancy']} | {res['faithfulness']} | {res['tool_correctness']} |\n"
        
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(md_content)

def get_paths(candidate_id):
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    report_path = os.path.join(base_dir, "outputs", f"{candidate_id}_screening_report.json")
    
    csv_path = os.path.join(base_dir, "data", "p004_resume_screening_crew_dataset", "metadata", "candidate_index.csv")
    resume_file = ""
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row["candidate_id"].strip().upper() == candidate_id.upper():
                resume_file = row["resume_file"]
                break
                
    resume_path = os.path.join(base_dir, "data", "p004_resume_screening_crew_dataset", "resumes", resume_file)
    return report_path, resume_path

def parse_tools_called_from_logs(base_dir):
    log_path = os.path.join(base_dir, "outputs", "execution_log.txt")
    all_tools = [
        "read_job_description_tool",
        "read_resume_tool",
        "candidate_index_lookup_tool",
        "load_screening_rubric_tool",
        "score_calculator_tool",
        "save_report_tool",
        "skill_matcher_tool",
        "validate_report_schema_tool"
    ]
    if os.path.exists(log_path):
        with open(log_path, "r", encoding="utf-8") as f:
            log_content = f.read()
        return [ToolCall(name=tool) for tool in all_tools if tool in log_content]
    return []

@pytest.mark.parametrize("candidate_id", ["CAND-001", "CAND-002", "CAND-003"])
def test_candidate_screening_report(candidate_id):
    report_path, resume_path = get_paths(candidate_id)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
    with open(report_path, "r", encoding="utf-8") as f:
        report = json.load(f)
        
    with open(resume_path, "r", encoding="utf-8") as f:
        resume_content = f.read()

    tools_called = parse_tools_called_from_logs(base_dir)
    expected_tools = [ToolCall(name=tool) for tool in [
        "read_job_description_tool",
        "read_resume_tool",
        "load_screening_rubric_tool",
        "score_calculator_tool",
        "skill_matcher_tool",
        "validate_report_schema_tool",
        "save_report_tool"
    ]]

    test_case = LLMTestCase(
        input="Screen candidate resume against job description and generate screening report.",
        actual_output=report.get("executive_summary", ""),
        retrieval_context=[resume_content],
        tools_called=tools_called,
        expected_tools=expected_tools
    )
    
    relevancy_metric = AnswerRelevancyMetric(threshold=0.5, model=eval_model)
    faithfulness_metric = FaithfulnessMetric(threshold=0.5, model=eval_model)
    tool_correctness_metric = ToolCorrectnessMetric(threshold=0.5, model=eval_model)
    
    try:
        relevancy_metric.measure(test_case)
        faithfulness_metric.measure(test_case)
        tool_correctness_metric.measure(test_case)
        
        assert relevancy_metric.is_successful(), f"Answer Relevancy failed: {relevancy_metric.reason}"
        assert faithfulness_metric.is_successful(), f"Faithfulness failed: {faithfulness_metric.reason}"
        assert tool_correctness_metric.is_successful(), f"Tool Correctness failed: {tool_correctness_metric.reason}"
    finally:
        rel_score = f"{relevancy_metric.score:.2f}" if relevancy_metric.score is not None else "N/A"
        faith_score = f"{faithfulness_metric.score:.2f}" if faithfulness_metric.score is not None else "N/A"
        tool_score = f"{tool_correctness_metric.score:.2f}" if tool_correctness_metric.score is not None else "N/A" 
        
        evaluation_results.append({
            "candidate_id": candidate_id,
            "relevancy": rel_score,
            "faithfulness": faith_score,
            "tool_correctness": tool_score
        })
    
    assert report.get("recommendation") == calculate_recommendation_band(report.get("percentage", 0))
        
    questions = report.get("interview_questions", {})
    assert len(questions.get("technical_questions", [])) >= 3
    assert len(questions.get("project_deep_dive_questions", [])) >= 2
    assert len(questions.get("scenario_questions", [])) >= 2
    assert len(questions.get("gap_validation_questions", [])) >= 2
