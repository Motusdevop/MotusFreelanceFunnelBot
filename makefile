up-dev:
	ENV_FILE=.env.dev docker compose up --build

up-prod:
	ENV_FILE=.env.prod docker compose up --build -d