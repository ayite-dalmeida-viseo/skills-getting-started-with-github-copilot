import copy

import pytest
from fastapi.testclient import TestClient

import src.app as app_module
from src.app import app

# Snapshot of the seeded in-memory activities, taken before any test mutates it
_original_activities = copy.deepcopy(app_module.activities)


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture(autouse=True)
def reset_activities():
    # Restore the in-memory activities dict so tests don't leak state into each other
    app_module.activities.clear()
    app_module.activities.update(copy.deepcopy(_original_activities))
    yield
