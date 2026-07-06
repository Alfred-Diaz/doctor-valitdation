# Doctor Validation

Local web app for consolidating doctor affiliation PDF files into the PPS Final Template.

## What this app does

- Upload multiple medical society PDF files
- Upload the PPS Final Template Excel file
- Extract doctor names and medical society information
- Remove duplicate records
- Generate a consolidated Excel output
- Download the completed file from the browser

## Supported source files

The app is designed for these medical society file types:

- PPAG
- PCP
- PCS
- POGS
- PAFP

The medical society is detected from the uploaded PDF filename.

## Quick local run

```powershell
git clone https://github.com/Alfred-Diaz/doctor-valitdation.git
cd doctor-valitdation
python -m venv .venv
.venv\Scripts\activate
python -m pip install -r requirements.txt
python app.py
```

Open:

```text
http://localhost:8080
```

## Local network hosting

Run:

```powershell
waitress-serve --host=0.0.0.0 --port=8080 app:app
```

Then users can access:

```text
http://SERVER-IP:8080
```

Full instructions are in:

```text
DEPLOYMENT_LOCAL_SERVER.md
```

## Security note

Do not commit actual PDF files or Excel output files. The repository ignores:

```text
uploads/*
output/*
logs/*
*.pdf
*.xlsx
```
