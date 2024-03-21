.DEFAULT_GOAL := default

install_requirements:
	@pip install -r requirements.txt

run_api:
	@uvicorn btm.api.fast:app --reload
