import json
import csv
from crewai import Crew, Process
from src.agents import ALL_AGENTS
from src.tasks import build_tasks
from src.config import RESUMES_DIR, CANDIDATE_INDEX_PATH
from src.output_writer import append_execution_log

class ResumeScreeningCrew:
    def __init__(self):
        self.agents = ALL_AGENTS

    def _resolve_resume_path(self, candidate_id: str) -> str:
        with open(CANDIDATE_INDEX_PATH, mode="r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                if row.get("candidate_id") == candidate_id:
                    return str(RESUMES_DIR / row["resume_file"])
        raise ValueError(f"Candidate ID not found: {candidate_id}")

    def run(self, candidate_id: str) -> dict:
        append_execution_log(f"Starting screening for {candidate_id}")
        
        resume_path = self._resolve_resume_path(candidate_id)
        tasks = build_tasks(candidate_id, resume_path)
        
        crew = Crew(
            agents=self.agents,
            tasks=tasks,
            process=Process.sequential,
            verbose=True,
            memory=False
        )
        
        result = crew.kickoff()
        append_execution_log(f"Screening complete for {candidate_id}")
        
        if hasattr(result, "model_dump"):
            return result.model_dump()
        if isinstance(result, str):
            try:
                return json.loads(result)
            except json.JSONDecodeError:
                pass
        return {"raw_output": str(result)}

    def run_batch(self, candidate_ids: list) -> dict:
        results = {}
        for cid in candidate_ids:
            try:
                results[cid] = self.run(cid)
            except Exception as e:
                append_execution_log(f"Failed {cid}: {e}")
                results[cid] = {"error": str(e)}
        return results

    def run_sample_screening(self) -> dict:
        return self.run_batch(["CAND-001", "CAND-002", "CAND-003"])