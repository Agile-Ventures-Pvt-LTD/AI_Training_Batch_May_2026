from main import get_resume_file


def test_resume_lookup():
    file = get_resume_file("CAND-001")
    assert file is not None