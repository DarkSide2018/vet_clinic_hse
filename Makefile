install:
	pip install -r requirements.txt

start:
	uvicorn main:app --reload