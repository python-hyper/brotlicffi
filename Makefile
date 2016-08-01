publish:
	rm -rf dist/
	python setup.py sdist
	twine upload -s dist/*

