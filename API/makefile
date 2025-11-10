run:
	uvicorn app.main:app --reload

run-docker:
	docker-compose up -d

create-migrations:
	alembic revision --autogenerate -m "$(d)"

run-migrations:
	alembic upgrade head
