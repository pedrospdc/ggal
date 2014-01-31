clean:
	@find . -iname '*.pyc' -delete
	@find . -iname '*.pyo' -delete

run:
	python setup.py;
	python manage.py runserver;
