run:
	uvicorn main:app --reload

migrations:
	alembic revision --m="$(NAME)" --autogenerate

migrate:
	alembic upgrade head