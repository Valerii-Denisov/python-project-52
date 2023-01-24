install:
	poetry install

uninstall:
	python3 -m pip uninstall hexlet-code

lint:
	poetry run flake8 task_manager

test:
	poetry run python manage.py test

test-coverage:
	poetry run coverage run manage.py test
	poetry run coverage xml
	poetry run coverage report

requir:
	poetry export --without-hashes --format=requirements.txt > requirements.txt


messages:
	poetry run django-admin makemessages --ignore="static" --ignore=".env"  -l ru


compille_mess:
	poetry run django-admin compilemessages


runserver:
	poetry run python manage.py runserver
