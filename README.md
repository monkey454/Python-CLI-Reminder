# 🕒Python-CLI-Reminder


A **text-based reminder application** built with Python that sends both **desktop notifications** and **email alerts** at scheduled times. It supports saving and loading reminders using a JSON file, and runs in the background using threading.

---

## ✨ Features

- ✅ Add reminders with a title, date/time, and email
- 📨 Sends **email alerts** using Gmail SMTP
- 🔔 Shows **desktop notifications** using Plyer
- 💾 Save/load reminders to/from `reminder.json`
- 🔁 Background thread checks reminders every minute
- 🛡 Validates email format and prevents past time reminders

---

## 📦 Requirements

Install the required packages using pip:

```bash
pip install plyer

