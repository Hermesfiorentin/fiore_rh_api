
#!/bin/bash
cd "$(dirname "$0")"
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
