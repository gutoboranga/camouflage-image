setup:
	pip install numpy
	pip install opencv-python

run:
	@echo "> choose the images"
	@python src/run.py

run_and_save:
	@echo "> choose the images"
	@python src/run.py "save"

