.PHONY: sync frontend backend test

sync:
	npm install
	cd backend && uv sync

frontend:
	npm run dev

backend:
	cd backend && uv run uvicorn app.main:app --reload

test:
	npm run lint
	npm run test
	npm run build
	cd backend && uv run pytest
