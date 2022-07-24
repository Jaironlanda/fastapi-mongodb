# Basic CRUD `mongodb` and `fastapi`

## Setup
Require python version >=3.9

### 1. Create environment
`python3 -m venv venv`

### 2. Activate environment
- `source venv/bin/activate` (Linux/MacOS)
- `venv\scripts\activate` (Windows)

### 3. Install package
`pip install -r requirements.txt`

### 4. Run
`uvicorn app.main:app --reload`

### API Documentation
- `http://127.0.0.1:8000/docs`
- `http://127.0.0.1:8000/redoc`