DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker-compose.yml
APP_CONTAINER = fastapi_app
ALEMBIC_REVISION_CMD = alembic revision -m
ALEMBIC_UPGRADE_CMD = alembic upgrade head

.PHONY: app
app:
	${DC} -f ${APP_FILE} ${ENV} up --build -d

.PHONY: app-down
app-down:
	${DC} -f ${APP_FILE} down

.PHONY: app-shell
app-shell:
	${EXEC} ${APP_CONTAINER} bash

.PHONY: app-logs
app-logs:
	${LOGS} ${APP_CONTAINER} -f

.PHONY: alembic-rev
alembic-rev:
ifeq ($(words $(MAKECMDGOALS)),1)
	$(error Usage: make alembic-rev "your message")
endif
	${EXEC} ${APP_CONTAINER} ${ALEMBIC_REVISION_CMD} "$(word 2,$(MAKECMDGOALS))"
%:
	@:

.PHONY: alembic-upgrade
alembic-upgrade:
	${EXEC} ${APP_CONTAINER} ${ALEMBIC_UPGRADE_CMD}

.PHONY: test
test:
	${EXEC} ${APP_CONTAINER} pytest