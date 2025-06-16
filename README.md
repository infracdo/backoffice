# Zeep Backend

FastAPI app connected to a PostgreSQL database.

---

## Requirements

- Python 3.10+
- PostgreSQL
- (Optional) Docker

---

## Setup and Run

### 1. Clone the project

```bash
git clone git@gitlabv3.thousandminds.com:frencys/zeep-backend.git
cd zeep-backend
```

### 2. Create a virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Set up environment variables

Duplicate the `.env.example` file and rename it to `.env`:

```bash
cp .env.example .env
```

Then open `.env` and **update the values**:

> Make sure your PostgreSQL database is running and matches the credentials.

---

### 5. Run the app

```bash
uvicorn app:app --reload --port=5050
```

or 
```bash
sh dev.sh
```

Visit: [http://localhost:5050/docs](http://localhost:5050/docs) for the interactive API docs.

---

## Optional: Run with Docker

```bash
docker-compose up --build
```

---
