from tools.reader_tools import (
    batch_candidate_loader_tool,
    candidate_index_lookup_tool,
    read_job_description_tool,
    read_resume_tool,
)


def test_read_job_description():
    result = read_job_description_tool.run()
    assert result["success"] is True


def test_candidate_lookup():
    result = candidate_index_lookup_tool.run(
        candidate_id="CAND-001"
    )
    assert result["found"] is True


def test_batch_loader():
    result = batch_candidate_loader_tool.run()
    assert len(result) > 0


def test_resume_reader():
    result = read_resume_tool.run(
        resume_file="candidate_001.md"
    )
    assert result["success"] is True