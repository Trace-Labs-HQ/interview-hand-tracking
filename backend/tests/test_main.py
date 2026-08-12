from fastapi.testclient import TestClient

from app.main import HAND_TRACKS_KEY, VIDEO_KEY, app, get_s3_client, settings


class FakeS3Client:
    def __init__(self) -> None:
        self.calls: list[tuple[str, dict[str, str], int]] = []

    def generate_presigned_url(
        self, client_method: str, *, Params: dict[str, str], ExpiresIn: int
    ) -> str:
        self.calls.append((client_method, Params, ExpiresIn))
        return f"https://example.test/{Params['Key']}"


def test_assets_presigns_only_the_two_fixed_objects() -> None:
    fake_s3 = FakeS3Client()
    app.dependency_overrides[get_s3_client] = lambda: fake_s3

    try:
        response = TestClient(app).get(
            "/api/assets?bucket=attacker-bucket&key=private-object&expires=604800"
        )
    finally:
        app.dependency_overrides.clear()

    assert response.status_code == 200
    assert [call[0] for call in fake_s3.calls] == ["get_object", "get_object"]
    assert [call[1] for call in fake_s3.calls] == [
        {"Bucket": settings.bucket, "Key": f"{settings.prefix}{VIDEO_KEY}"},
        {"Bucket": settings.bucket, "Key": f"{settings.prefix}{HAND_TRACKS_KEY}"},
    ]
    assert all(call[2] == settings.expiry_seconds for call in fake_s3.calls)
    assert response.json()["expires_in_seconds"] == settings.expiry_seconds


def test_health() -> None:
    assert TestClient(app).get("/api/health").json() == {"status": "ok"}
