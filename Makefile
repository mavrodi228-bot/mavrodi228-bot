up:
	docker compose up --build

down:
	docker compose down -v

backend-test:
	docker compose run --rm backend sh -c "pytest"

frontend-build:
	docker compose run --rm frontend sh -c "npm run build"
