from app.agents.router_agent import router_agent, VALID_ROUTES


def test_router_returns_valid_route():
    route = router_agent("What is the capital of France?")
    assert route in VALID_ROUTES
