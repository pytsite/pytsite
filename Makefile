all:
	@echo "Please run 'make dist' or 'make upload'"

clean:
	python ./setup.py clean

dist: clean
	python ./setup.py bdist_wheel

upload: dist
	twine upload ./dist/*
