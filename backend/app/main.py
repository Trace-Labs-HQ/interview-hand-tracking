import os
from dataclasses import dataclass
from pathlib import Path
from typing import Annotated, Protocol

import boto3
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

load_dotenv(Path(__file__).parents[2] / ".env")

VIDEO_KEY = "video.mp4"
HAND_TRACKS_KEY = "hand_tracks.ndjson"


@dataclass(frozen=True)
class Settings:
    region: str = os.environ.get("AWS_REGION", "us-east-2")
    bucket: str = os.environ["S3_BUCKET"]
    prefix: str = os.environ["S3_PREFIX"].rstrip("/") + "/"
    expiry_seconds: int = int(os.environ.get("PRESIGNED_URL_EXPIRY_SECONDS", "900"))
    frontend_origin: str = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")


settings = Settings()


class S3Client(Protocol):
    def generate_presigned_url(
        self, client_method: str, *, Params: dict[str, str], ExpiresIn: int
    ) -> str: ...


def get_s3_client() -> S3Client:
    return boto3.client("s3", region_name=settings.region)


S3ClientDependency = Annotated[S3Client, Depends(get_s3_client)]


class AssetUrls(BaseModel):
    video_url: str
    hand_tracks_url: str
    expires_in_seconds: int


app = FastAPI(title="Video assets API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.frontend_origin],
    allow_credentials=False,
    allow_methods=["GET"],
    allow_headers=["*"],
)


def presign_get(client: S3Client, object_name: str) -> str:
    return client.generate_presigned_url(
        "get_object",
        Params={"Bucket": settings.bucket, "Key": f"{settings.prefix}{object_name}"},
        ExpiresIn=settings.expiry_seconds,
    )


@app.get("/api/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/api/assets", response_model=AssetUrls)
def assets(client: S3ClientDependency) -> AssetUrls:
    return AssetUrls(
        video_url=presign_get(client, VIDEO_KEY),
        hand_tracks_url=presign_get(client, HAND_TRACKS_KEY),
        expires_in_seconds=settings.expiry_seconds,
    )
