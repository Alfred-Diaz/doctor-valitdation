# Local Server Deployment Guide

This guide sets up Doctor Validation as a local web app on a Windows server or office workstation.

## 1. Clone the repository

```powershell
git clone https://github.com/Alfred-Diaz/doctor-valitdation.git
cd doctor-valitdation
```

## 2. Create a virtual environment

```powershell
python -m venv .venv
.venv\Scripts\activate
```

If activation is blocked, run this once:

```powershell
Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
```

Then activate again:

```powershell
.venv\Scripts\activate
```

## 3. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## 4. Test locally

```powershell
python app.py
```

Open this on the server browser:

```text
http://localhost:8080
```

## 5. Run for local network users

For production-style local hosting, use Waitress:

```powershell
waitress-serve --host=0.0.0.0 --port=8080 app:app
```

Users on the same network can open:

```text
http://SERVER-IP:8080
```

Example:

```text
http://192.168.1.50:8080
```

## 6. Firewall rule

If users cannot access the site, allow port 8080 in Windows Firewall.

```powershell
New-NetFirewallRule -DisplayName "Doctor Validation App 8080" -Direction Inbound -Protocol TCP -LocalPort 8080 -Action Allow
```

## 7. Daily use

1. Open the web app.
2. Upload one or more PDF files.
3. Upload `PPS FINAL TEMPLATE.xlsx`.
4. Click Generate.
5. Download the consolidated Excel file.

## 8. Data privacy

PDFs and generated Excel files are ignored by Git and should remain only on the local server.

Folders used by the app:

```text
uploads/
output/
logs/
```

## 9. Optional: create a start script

Create `start_server.bat` with:

```bat
@echo off
cd /d C:\path\to\doctor-valitdation
call .venv\Scripts\activate
waitress-serve --host=0.0.0.0 --port=8080 app:app
pause
```
