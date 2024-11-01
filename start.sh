# Configure Poetry to use Python 3.11
(cd ./computer_use_demo && poetry env use python3.11)

# Install project dependencies defined in ./computer_use_demo/pyproject.toml
poetry install --no-root --directory ./computer_use_demo

# Run the Streamlit application using Poetry in ./computer_use_demo
poetry run --directory ./computer_use_demo bash -c "
  # Export required variables for the demo
  export DISPLAY_NUM=99
  export HEIGHT=768
  export WIDTH=1024
  export STREAMLIT_SERVER_PORT=8501

  # Export all variables defined in .env file
  set -a
  source .env
  set +a

  # Launch the Streamlit application
  python -m streamlit run computer_use_demo/streamlit.py
"