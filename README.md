docker compose up
docker compose exec backend uv run python manage.py generate_data
docker compose exec backend uv run python manage.py create_intervals
