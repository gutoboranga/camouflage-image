setup:
	pip install numpy
	pip install opencv-python

run:
	@echo "> choose the images"
	@python source_code/run.py

run_and_save:
	@echo "> choose the images"
	@python source_code/run.py "save"

