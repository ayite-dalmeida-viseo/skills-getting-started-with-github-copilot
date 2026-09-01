from src.app import activities

CHESS_CLUB = "Chess Club"
EXISTING_PARTICIPANT = "michael@mergington.edu"
NEW_EMAIL = "new.student@mergington.edu"


def test_root_redirects_to_static_index(client):
    # Arrange
    # (no extra setup needed)

    # Act
    response = client.get("/", follow_redirects=False)

    # Assert
    assert response.status_code in (307, 308)
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_seeded_data(client):
    # Arrange
    # (activities dict is seeded by the reset_activities fixture)

    # Act
    response = client.get("/activities")

    # Assert
    assert response.status_code == 200
    body = response.json()
    assert CHESS_CLUB in body
    for details in body.values():
        assert set(["description", "schedule", "max_participants", "participants"]) <= details.keys()


def test_signup_for_activity_success(client):
    # Arrange
    assert NEW_EMAIL not in activities[CHESS_CLUB]["participants"]

    # Act
    response = client.post(f"/activities/{CHESS_CLUB}/signup", params={"email": NEW_EMAIL})

    # Assert
    assert response.status_code == 200
    assert NEW_EMAIL in activities[CHESS_CLUB]["participants"]


def test_signup_for_activity_duplicate_returns_400(client):
    # Arrange
    assert EXISTING_PARTICIPANT in activities[CHESS_CLUB]["participants"]

    # Act
    response = client.post(f"/activities/{CHESS_CLUB}/signup", params={"email": EXISTING_PARTICIPANT})

    # Assert
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]


def test_signup_for_unknown_activity_returns_404(client):
    # Arrange
    unknown_activity = "Nonexistent Club"

    # Act
    response = client.post(f"/activities/{unknown_activity}/signup", params={"email": NEW_EMAIL})

    # Assert
    assert response.status_code == 404


def test_unregister_from_activity_success(client):
    # Arrange
    assert EXISTING_PARTICIPANT in activities[CHESS_CLUB]["participants"]

    # Act
    response = client.post(f"/activities/{CHESS_CLUB}/unregister", params={"email": EXISTING_PARTICIPANT})

    # Assert
    assert response.status_code == 200
    assert EXISTING_PARTICIPANT not in activities[CHESS_CLUB]["participants"]


def test_unregister_not_registered_returns_400(client):
    # Arrange
    assert NEW_EMAIL not in activities[CHESS_CLUB]["participants"]

    # Act
    response = client.post(f"/activities/{CHESS_CLUB}/unregister", params={"email": NEW_EMAIL})

    # Assert
    assert response.status_code == 400
    assert "not signed up" in response.json()["detail"]


def test_unregister_unknown_activity_returns_404(client):
    # Arrange
    unknown_activity = "Nonexistent Club"

    # Act
    response = client.post(f"/activities/{unknown_activity}/unregister", params={"email": EXISTING_PARTICIPANT})

    # Assert
    assert response.status_code == 404
