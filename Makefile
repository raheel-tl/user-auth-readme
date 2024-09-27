push:
	git add . \
	&& git commit -m "Improvements push" \
	&& git push origin HEAD

server:
	fastapi dev main.py

migrate:
	alembic upgrade head

migrations:
	alembic revision --autogenerate -m "Initial migration user"
