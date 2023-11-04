install:
	pip install -r requirements.txt && \
    pip install 'uvicorn[standard]'

start:
	uvicorn main:app --reload