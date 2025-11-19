import speech_recognition as sr
import pyttsx3
import time
import json
import requests
from datetime import datetime
import threading
import queue

class ReceptionistAI:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        # Conversation state
        self.conversation_active = False
        self.user_data = {}
        self.appointments = []
        
        # Calibration for microphone
        print("Calibrating microphone for ambient noise...")
        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)
        print("Microphone calibrated!")
    
    def setup_tts(self):
        """Configure text-to-speech settings"""
        voices = self.tts_engine.getProperty('voices')
        if voices:
            self.tts_engine.setProperty('voice', voices[1].id)  # Female voice
        self.tts_engine.setProperty('rate', 150)
        self.tts_engine.setProperty('volume', 0.8)
    
    def speak(self, text):
        """Convert text to speech"""
        print(f"AI: {text}")
        self.tts_engine.say(text)
        self.tts_engine.runAndWait()
    
    def listen(self):
        """Listen for user input and convert to text"""
        try:
            with self.microphone as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
            text = self.recognizer.recognize_google(audio)
            print(f"User: {text}")
            return text.lower()
        
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            self.speak("I'm sorry, I didn't catch that. Could you please repeat?")
            return ""
        except sr.RequestError as e:
            self.speak("There seems to be a problem with the speech recognition service.")
            return ""
    
    def greet_visitor(self):
        """Initial greeting"""
        greetings = [
            "Hello! Welcome to our office. How can I help you today?",
            "Good day! I'm your virtual receptionist. What brings you here?",
            "Welcome! How may I assist you today?"
        ]
        import random
        self.speak(random.choice(greetings))
    
    def handle_appointment(self):
        """Handle appointment scheduling"""
        self.speak("I can help you schedule an appointment. What's your name?")
        name = self.listen()
        
        if not name:
            return
        
        self.speak(f"Nice to meet you {name}. What day would you like to schedule the appointment?")
        date = self.listen()
        
        self.speak("And what time works best for you?")
        time_slot = self.listen()
        
        # Create appointment
        appointment = {
            'name': name,
            'date': date,
            'time': time_slot,
            'timestamp': datetime.now().isoformat()
        }
        self.appointments.append(appointment)
        
        self.speak(f"Perfect! I've scheduled your appointment for {date} at {time_slot}. Is there anything else I can help with?")
    
    def handle_visitor_registration(self):
        """Register new visitors"""
        self.speak("Let me get you registered. What's your full name?")
        name = self.listen()
        
        self.speak("What company are you from?")
        company = self.listen()
        
        self.speak("Who are you here to see?")
        contact_person = self.listen()
        
        visitor_data = {
            'name': name,
            'company': company,
            'contact_person': contact_person,
            'check_in_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
        self.user_data = visitor_data
        
        self.speak(f"Thank you {name}. I've registered you from {company} to see {contact_person}. They've been notified of your arrival.")
    
    def provide_information(self):
        """Provide general information"""
        information_options = {
            'hours': "Our office hours are Monday through Friday, 9 AM to 5 PM.",
            'location': "We're located at 123 Business Street, Suite 100.",
            'services': "We offer consulting, development, and support services.",
            'contact': "You can reach us at 555-0123 or email hello@company.com.",
            'wifi': "The WiFi network is 'Company-Guest' and the password is 'Welcome123'."
        }
        
        self.speak("What information would you like? I can tell you about our hours, location, services, contact info, or WiFi.")
        info_request = self.listen()
        
        for key, value in information_options.items():
            if key in info_request:
                self.speak(value)
                return
        
        self.speak("I'm not sure what information you're looking for. Please ask about hours, location, services, contact info, or WiFi.")
    
    def handle_emergency(self):
        """Handle emergency situations"""
        self.speak("I've detected this might be an emergency. Let me connect you with security immediately.")
        # In a real implementation, this would trigger alerts or calls
        self.speak("Security has been notified and help is on the way.")
    
    def process_conversation(self, user_input):
        """Main conversation processing logic"""
        user_input = user_input.lower()
        
        # Emergency detection
        emergency_keywords = ['emergency', 'help', 'urgent', 'accident', 'fire', 'medical']
        if any(keyword in user_input for keyword in emergency_keywords):
            self.handle_emergency()
            return True
        
        # Appointment scheduling
        appointment_keywords = ['appointment', 'schedule', 'meeting', 'book']
        if any(keyword in user_input for keyword in appointment_keywords):
            self.handle_appointment()
            return True
        
        # Visitor registration
        registration_keywords = ['register', 'check in', 'sign in', 'visitor']
        if any(keyword in user_input for keyword in registration_keywords):
            self.handle_visitor_registration()
            return True
        
        # Information requests
        info_keywords = ['information', 'tell me', 'what are', 'where is', 'hours', 'location']
        if any(keyword in user_input for keyword in info_keywords):
            self.provide_information()
            return True
        
        # Greeting responses
        greeting_keywords = ['hello', 'hi', 'hey', 'good morning', 'good afternoon']
        if any(keyword in user_input for keyword in greeting_keywords):
            self.speak("Hello! How can I help you today?")
            return True
        
        # Farewell
        farewell_keywords = ['bye', 'goodbye', 'thanks', 'thank you', 'see you']
        if any(keyword in user_input for keyword in farewell_keywords):
            self.speak("Thank you for visiting! Have a great day!")
            return False
        
        # Default response
        self.speak("I'm here to help with appointments, visitor registration, or general information. What would you like to do?")
        return True
    
    def run(self):
        """Main execution loop"""
        self.speak("Virtual receptionist system activated.")
        self.greet_visitor()
        
        self.conversation_active = True
        while self.conversation_active:
            user_input = self.listen()
            
            if user_input:
                self.conversation_active = self.process_conversation(user_input)
            
            # Small delay between interactions
            time.sleep(1)
        
        self.speak("Receptionist system going offline. Goodbye!")

# Enhanced version with additional features
class AdvancedReceptionistAI(ReceptionistAI):
    def __init__(self):
        super().__init__()
        self.daily_visitors = []
        self.scheduled_appointments = []
    
    def save_visitor_data(self):
        """Save visitor data to file"""
        try:
            with open('visitors.json', 'w') as f:
                json.dump(self.daily_visitors, f, indent=2)
        except Exception as e:
            print(f"Error saving data: {e}")
    
    def load_visitor_data(self):
        """Load visitor data from file"""
        try:
            with open('visitors.json', 'r') as f:
                self.daily_visitors = json.load(f)
        except FileNotFoundError:
            self.daily_visitors = []
    
    def handle_visitor_registration(self):
        """Enhanced visitor registration"""
        super().handle_visitor_registration()
        self.daily_visitors.append(self.user_data)
        self.save_visitor_data()
    
    def get_daily_stats(self):
        """Provide daily statistics"""
        visitor_count = len(self.daily_visitors)
        appointment_count = len(self.appointments)
        
        stats_message = f"Today we have {visitor_count} visitors and {appointment_count} scheduled appointments."
        self.speak(stats_message)
    
    def process_conversation(self, user_input):
        """Enhanced conversation processing"""
        user_input = user_input.lower()
        
        # Add stats request
        if 'statistics' in user_input or 'how many visitors' in user_input:
            self.get_daily_stats()
            return True
        
        return super().process_conversation(user_input)

# Text-based version (if speech doesn't work)
class TextReceptionistAI:
    def __init__(self):
        self.conversation_active = False
        self.user_data = {}
        self.appointments = []
    
    def get_text_input(self):
        """Get input from text instead of speech"""
        return input("You: ").strip().lower()
    
    def speak(self, text):
        """Text-based output"""
        print(f"AI: {text}")
    
    def run(self):
        """Text-based execution"""
        self.speak("Virtual receptionist system activated.")
        self.speak("Hello! Welcome to our office. How can I help you today?")
        
        self.conversation_active = True
        while self.conversation_active:
            user_input = self.get_text_input()
            
            if user_input:
                # Use the same conversation logic
                receptionist = ReceptionistAI()
                self.conversation_active = receptionist.process_conversation(user_input)

# Main execution
if __name__ == "__main__":
    print("Starting Virtual Receptionist AI Agent...")
    
    try:
        # Try to start the speech-based version
        ai_receptionist = AdvancedReceptionistAI()
        ai_receptionist.run()
    
    except Exception as e:
        print(f"Speech recognition not available: {e}")
        print("Starting text-based version...")
        
        # Fallback to text-based version
        text_ai = TextReceptionistAI()
        text_ai.run()
