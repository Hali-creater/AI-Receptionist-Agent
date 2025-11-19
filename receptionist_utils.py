import json
from datetime import datetime, timedelta
import smtplib
from email.mime.text import MIMEText

class NotificationSystem:
    def __init__(self):
        self.notifications = []
    
    def send_email_notification(self, subject, message, to_email):
        """Send email notifications (configure with your SMTP settings)"""
        try:
            # This is a template - configure with your email settings
            msg = MimeText(message)
            msg['Subject'] = subject
            msg['From'] = 'receptionist@company.com'
            msg['To'] = to_email
            
            # Example with Gmail (you'll need to enable app passwords)
            # with smtplib.SMTP_SSL('smtp.gmail.com', 465) as server:
            #     server.login('your_email@gmail.com', 'your_app_password')
            #     server.send_message(msg)
            
            print(f"Email notification sent to {to_email}: {subject}")
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def notify_staff(self, visitor_name, contact_person):
        """Notify staff about visitor arrival"""
        message = f"Visitor {visitor_name} has arrived and is waiting to see {contact_person}."
        self.send_email_notification(
            "Visitor Arrival Notification",
            message,
            f"{contact_person}@company.com"  # This would be looked up from a directory
        )

class DataManager:
    def __init__(self):
        self.visitors_file = 'visitors.json'
        self.appointments_file = 'appointments.json'
    
    def save_data(self, filepath, data):
        """Generic data saving method"""
        try:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            return True
        except Exception as e:
            print(f"Error saving data to {filepath}: {e}")
            return False

    def load_data(self, filepath):
        """Generic data loading method"""
        try:
            with open(filepath, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
        except json.JSONDecodeError:
            return []

    def save_visitor(self, visitor_data):
        """Save visitor data"""
        visitors = self.load_data(self.visitors_file)
        visitors.append(visitor_data)
        return self.save_data(self.visitors_file, visitors)

    def load_visitors(self):
        """Load all visitors"""
        return self.load_data(self.visitors_file)
    
    def save_appointment(self, appointment_data):
        """Save appointment data"""
        appointments = self.load_data(self.appointments_file)
        appointments.append(appointment_data)
        return self.save_data(self.appointments_file, appointments)

    def load_appointments(self):
        """Load all appointments"""
        return self.load_data(self.appointments_file)

    def get_todays_visitors(self):
        """Get today's visitors"""
        visitors = self.load_visitors()
        today = datetime.now().strftime("%Y-%m-%d")
        
        return [v for v in visitors if v.get('check_in_time', '').startswith(today)]
