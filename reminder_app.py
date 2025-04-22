import datetime
import json
import os
import time
import threading
import smtplib
from email.message import EmailMessage
from plyer import notification
import re
import requests
reminders = []

# Function to show desktop notification
def send_notification(title, message):
    notification.notify(
        title=title,
        message=message,
        timeout=10
    )

# Function to send email (using Gmail SMTP)
def send_email(subject, body, to_email):
    try:
        sender_email = "xyz0123@gmail.com"         # <-- Change this
        sender_password = ".................."         # <-- Use app password, not your real one

        msg = EmailMessage()
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = to_email
        msg.set_content(body)

        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(sender_email, sender_password)
            smtp.send_message(msg)
        print(f"Email sent to {to_email}")
    except Exception as e:
        print("Error sending email:", e)
# function to send sms
def send_sms(to,message):
    url = "https://sms.xyz.com/sms/xx/sendxx/"  # with actual URL

    data = {
        "auth_token": "012#$xyzabc", #enter the toke
        "to": to,
        "text": message
    }

    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=data, headers=headers)

    print("Status Code:", response.status_code)
    print("Response JSON:", response.json())

# Background thread to check reminders
def reminder_checker():
    while True:
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        for reminder in reminders[:]:  # Use slice to avoid modifying_list during iteration
            if reminder["Date_Time"] == now:
                send_notification(reminder["Title"], f"Reminder: {reminder['Title']} at {reminder['Date_Time']}")
                send_email("Reminder Alert", f"Reminder: {reminder['Title']} at {reminder['Date_Time']}", reminder["Email"])
                send_sms(reminder["Phone_Number"], f"Reminder: {reminder['Title']} at {reminder['Date_Time']}")
                print(f"\nReminder: {reminder['Title']} at {reminder['Date_Time']}")
                reminders.remove(reminder)
        time.sleep(60)  # Wait 1 minute

def is_valid_email(email):
    # Simple regex for basic email format checking
    pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    return re.match(pattern, email) is not None

def is_valid_phone(phone):
    # Allows optional +, followed by 10 to 15 digits
    pattern = r'^9779\d{9}$'
    return re.match(pattern, phone) is not None

def add_reminder():
    try:
        title = input("Enter the title of the reminder: ")

        while True:
            date_time = input("Enter the date and time (YYYY-MM-DD HH:MM): ")
            dt = datetime.datetime.strptime(date_time, "%Y-%m-%d %H:%M")
            # Parse and check if date is in the future
            if dt <= datetime.datetime.now():
                print("You can't set a reminder in the past. Please enter a future date and time.")
            else:
                break
        except ValueError as e:
            print("Invalid date/time format. Please follow YYYY-MM-DD HH:MM",e)
            
        date_time_str = dt.strftime("%Y-%m-%d %H:%M")
        while True:
            email = input("Enter your email for reminder alert: ")

            # Check for valid email
            if not is_valid_email(email):
                print("Invalid email format. Please try again.")
            else: 
                break
        
            
        while True:
            phone_number = input("Enter your mobile number for reminder alert: ")
            # check for valid phone number
            if not is_valid_phone(phone_number):
                print("Invalid email format. Please try again.")
            else:
                break


        reminder = {
            "Title": title,
            "Date_Time": date_time_str,
            "Email": email,
            "Phone_Number":phone_number
        }
        reminders.append(reminder)
        print("Reminder added successfully!")
   

def view_reminder():
    if not reminders:
        print("No reminders found.")
        return
    for i, r in enumerate(reminders, 1):
        print(f"{i}. {r['Title']} at {r['Date_Time']} | Email: {r['Email']}")

def delete_reminder():
    if not reminders:
        print("No reminders to delete.")
        return
    view_reminder()
    while True:
        try:
            choice = int(input("Enter the number of reminder to delete: "))
            if 1 <= choice <= len(reminders):
                removed = reminders.pop(choice - 1)
                save_to_file()

                print(f"Deleted reminder: {removed['Title']}")
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Please enter a valid number.")

def save_to_file():
    try:
        with open("reminder.json", "w") as f:
            json.dump(reminders, f, indent=4)
        print("Reminders saved.")
    except Exception as e:
        print("Error saving:", e)

def load_from_file():
    if os.path.exists("reminder.json"):
        try:
            with open("reminder.json", "r") as f:
                data = json.load(f)
                if isinstance(data, list):
                    reminders.clear()
                    reminders.extend(data)
                    print("Reminders loaded.")
        except Exception as e:
            print("Error loading reminders:", e)

def main():
    print("=== Reminder App ===")
    print("1. Add Reminder\n2. View Reminders\n3. Delete Reminder\n4. Save to File\n5. Load from File\n6. Exit")
    while True:
        try:
            choice = int(input("Enter choice (1-6): "))
            if choice == 1:
                add_reminder()
            elif choice == 2:
                view_reminder()
            elif choice == 3:
                delete_reminder()
            elif choice == 4:
                save_to_file()
            elif choice == 5:
                load_from_file()
            elif choice == 6:
                print("Goodbye!")
                break
            else:
                print("Invalid choice.")
        except ValueError:
            print("Enter a number from 1 to 6.")

if __name__ == "__main__":
    load_from_file()
    threading.Thread(target=reminder_checker, daemon=True).start()
    main()
