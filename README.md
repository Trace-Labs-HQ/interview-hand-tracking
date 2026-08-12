# Video app

Trace is building an internal web-based data explorer. Engineers currently debug hand-tracking
results locally by viewing hand overlays in Foxglove, but Foxglove is not available in the
production web explorer. We need a browser-native way to inspect those results.

The source video and its projected 2D hand tracks are in the S3 location configured in `.env`.

The goal is to:

1. Overlay the projected hand tracks correctly on the video in the browser.
2. Make the approach scale to long videos with more than 100,000 overlay frames.

## Setup

Requirements: Node.js 22+, Python 3.13+, [`uv`](https://docs.astral.sh/uv/), and `make`.

```bash
cp .env.example .env
# Fill in the AWS credentials and S3 prefix supplied for the interview.
make sync
```

## Run

In separate terminals:

```bash
make backend
make frontend
```

Open http://localhost:5173. The backend runs at http://localhost:8000.

## Test

```bash
make test
```
