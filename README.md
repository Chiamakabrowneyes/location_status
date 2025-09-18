# Clinician Geofence Monitoring Service
This project monitors clinician locations using the provided API and raises alerts if a clinician leaves their designated safety zone.
It also sends periodic summary updates of all clinicians’ statuses.

**Features**

- Polls the Clinician Status API at fixed intervals.

- Detects when clinicians leave their expected zone.

- Sends immediate alerts via email.

- Sends a summary update every 10 minutes during monitoring.

- Configurable runtime (e.g., run for 1 hour).

### SetUp Instructions

**Clone the repository and create a virtual environment:**

`python3 -m venv .venv `

`source .venv/bin/activate`

**Install Python dependencies via pip:**

`pip install -r requirements.txt`

**Configure SMTP for email alerts in Constants.py file:**
1. [ ] SMTP_HOST = "smtp.gmail.com"
2. [ ] SMTP_PORT = 587
3. [ ] SMTP_USER = "your_email@gmail.com"
4. [ ] SMTP_PASS = "your_16_char_app_password"  # Google App Password, not your real password
5. [ ] 
6. [ ] ALERT_SENDER = "your_email@gmail.com"
7. [ ] ALERT_RECIPIENT = "recipient_email@example.com"

**Run the service:**

`python3 monitor.py`



