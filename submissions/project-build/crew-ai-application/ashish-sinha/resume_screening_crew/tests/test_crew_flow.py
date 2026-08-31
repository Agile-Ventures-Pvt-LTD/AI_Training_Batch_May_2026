import pytest
from unittest.mock import MagicMock, patch
from src.crew import ResumeScreeningCrew

class TestCrewFlow:
    @patch('src.crew.candidate_index_lookup_tool')
    @patch('src.crew.score_calculator_tool')
    @patch('src.crew.save_report_tool')
    @patch('src.crew.Crew')
    def test_crew_kickoff_orchestration_flow(self, mock_crew_class, mock_save, mock_calc, mock_lookup):
        mock_lookup._run.return_value = {
            "found": True,
            "candidate_id": "CAND-001",
            "candidate_name": "Test Candidate",
            "resume_file": "resume_01.md"
        }
        
        mock_calc._run.return_value = {
            "overall_score": 32,
            "max_score": 40,
            "percentage": 80.0,
            "recommendation_band": "STRONG_MATCH"
        }
        
        mock_crew_instance = MagicMock()
        mock_crew_class.return_value = mock_crew_instance
        mock_crew_instance.kickoff.return_value = "Finished Successfully"

        crew_pipeline = ResumeScreeningCrew()
        

        with patch.object(crew_pipeline.tasks_factory, 'final_recommendation_task') as mock_rec_task, \
             patch.object(crew_pipeline.tasks_factory, 'skill_matching_task') as mock_match_task:
            
            mock_rec_task.return_value.output.json_dict = {
                "candidate_id": "CAND-001",
                "candidate_name": "Test Candidate",
                "role_title": "AI Engineer",
                "category_scores": {"python_programming": 4},
                "executive_summary": "Excellent fit",
                "strengths": ["Python"],
                "gaps": [],
                "interview_focus_areas": ["Architecture"],
                "interview_questions": {"technical": ["Q1"]},
                "evidence": ["Github link"]
            }
            mock_match_task.return_value.output.json_dict = {"category_scores": {"python_programming": 4}}
            result = crew_pipeline.kickoff(candidate_id="CAND-001")

            assert result["candidate_id"] == "CAND-001"
            assert "human_review_note" in result
            assert "AI-assisted screening report" in result["human_review_note"]
            
            mock_save._run.assert_called_once()
