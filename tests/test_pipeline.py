"""
Basic tests for the pipeline. Requires GEMINI_API_KEY and a built vector store
to run fully — these are structured so you can mock the agents for CI later.
"""

import pytest
from app.orchestrator.pipeline import run_pipeline


def test_pipeline_returns_expected_keys():
    result = run_pipeline("What is paracetamol used for?")
    assert "answer" in result
    assert "sources" in result
    assert "grounded" in result
    assert "route_used" in result


def test_pipeline_handles_no_context_gracefully():
    result = run_pipeline("asdkjaslkdjaslkdj nonsense query xyzabc")
    assert isinstance(result["answer"], str)
    assert len(result["answer"]) > 0
