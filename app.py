import speech_recognition as sr
import pyttsx3
import time
import json
from datetime import datetime
import threading
import queue
import random

from receptionist_utils import DataManager, NotificationSystem
from config import SPEECH_SETTINGS, COMPANY_INFO, GREETINGS, FAREWELLS, KEYWORDS

class ReceptionistAI:
    def __init__(self):
        # Initialize speech recognition
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Initialize text-to-speech
        self.tts_engine = pyttsx3.init()
        self.setup_tts()
        
        # Data and notification managers
        self.data_manager = DataManager()
        self.notification_system = NotificationSystem()

        # Load existing data
        self.appointments = self.data_manager.load_appointments()

        # Conversation state
        self.conversation_active = False
        
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
        self.tts_engine.setProperty('rate', SPEECH_SETTINGS['voice_rate'])
        self.tts_engine.setProperty('volume', SPEECH_SETTINGS['voice_volume'])
    
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
                audio = self.recognizer.listen(
                    source,
                    timeout=SPEECH_SETTINGS['listen_timeout'],
                    phrase_time_limit=SPEECH_SETTINGS['phrase_time_limit']
                )
            
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
        self.speak(random.choice(GREETINGS))
    
    def handle_appointment(self):
        """Handle appointment scheduling"""
        self.speak("I can help you schedule an appointment. What's your name?")
        name = self.listen()
        if not name: return

        self.speak(f"Nice to meet you {name}. What day would you like to schedule?")
        date = self.listen()
        if not date: return

        self.speak("And what time works best for you?")
        time_slot = self.listen()
        if not time_slot: return
        
        appointment = {
            'name': name, 'date': date, 'time': time_slot,
            'timestamp': datetime.now().isoformat()
        }
        self.data_manager.save_appointment(appointment)
        self.appointments.append(appointment)
        
        self.speak(f"Perfect! I've scheduled you for {date} at {time_slot}. Anything else?")
    
    def handle_visitor_registration(self):
        """Register new visitors"""
        self.speak("Let me get you registered. What's your full name?")
        name = self.listen()
        if not name: return

        self.speak("What company are you from?")
        company = self.listen()
        if not company: return

        self.speak("Who are you here to see?")
        contact_person = self.listen()
        if not contact_person: return
        
        visitor_data = {
            'name': name, 'company': company, 'contact_person': contact_person,
            'check_in_time': datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        self.data_manager.save_visitor(visitor_data)
        self.notification_system.notify_staff(name, contact_person)
        
        self.speak(f"Thank you {name}. I've notified {contact_person} of your arrival.")
    
    def provide_information(self):
        """Provide general company information"""
        self.speak("I can provide information about our hours, location, services, contact details, or WiFi. What do you need to know?")
        
        info_request = self.listen()
        
        if any(key in info_request for key in ['hour', 'open', 'close']):
            self.speak(f"Our office hours are {COMPANY_INFO['hours']}.")
        elif any(key in info_request for key in ['location', 'address', 'where']):
            self.speak(f"We are located at {COMPANY_INFO['address']}.")
        elif 'service' in info_request:
            self.speak("We offer consulting, development, and support services.")
        elif any(key in info_request for key in ['contact', 'phone', 'email']):
            self.speak(f"You can reach us at {COMPANY_INFO['phone']} or {COMPANY_INFO['email']}.")
        elif 'wifi' in info_request:
            self.speak("The WiFi network is 'Company-Guest' and the password is 'Welcome123'.")
        else:
            self.speak("I'm not sure about that. I can help with hours, location, services, contact info, or WiFi.")

    def handle_emergency(self):
        """Handle emergency situations"""
        self.speak("I've detected this might be an emergency. Connecting you with security immediately.")
        # This would trigger alerts or calls
        self.speak("Security has been notified and help is on the way.")

    def process_conversation(self, user_input):
        """Main conversation processing logic"""
        if any(keyword in user_input for keyword in KEYWORDS['emergency']):
            self.handle_emergency()
        elif any(keyword in user_input for keyword in KEYWORDS['appointment']):
            self.handle_appointment()
        elif any(keyword in user_input for keyword in KEYWORDS['registration']):
            self.handle_visitor_registration()
        elif any(keyword in user_input for keyword in KEYWORDS['information']):
            self.provide_information()
        elif any(keyword in user_input for keyword in KEYWORDS['greeting']):
            self.speak("Hello! How can I assist you today?")
        elif any(keyword in user_input for keyword in KEYWORDS['farewell']):
            self.speak(random.choice(FAREWELLS))
            return False
        else:
            self.speak("I can help with appointments, registration, or general information. What would you like to do?")
        
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
            time.sleep(1)
        
        self.speak("Receptionist system shutting down. Goodbye!")

class AdvancedReceptionistAI(ReceptionistAI):
    def __init__(self):
        super().__init__()
    
    def get_daily_stats(self):
        """Provide daily statistics"""
        visitor_count = len(self.data_manager.get_todays_visitors())
        appointment_count = len(self.appointments)
        
        stats_message = f"Today we have had {visitor_count} visitors and have {appointment_count} scheduled appointments."
        self.speak(stats_message)
    
    def process_conversation(self, user_input):
        """Enhanced conversation processing"""
        if 'statistics' in user_input or 'how many visitors' in user_input:
            self.get_daily_stats()
            return True
        return super().process_conversation(user_input)

class TextReceptionistAI(ReceptionistAI):
    def __init__(self):
        # Skip speech-related setup
        self.tts_engine = None
        self.recognizer = None
        self.microphone = None

        # Initialize data managers and state
        self.data_manager = DataManager()
        self.notification_system = NotificationSystem()
        self.appointments = self.data_manager.load_appointments()
        self.conversation_active = False
    
    def speak(self, text):
        """Text-based output"""
        print(f"AI: {text}")

    def listen(self):
        """Get input from text instead of speech"""
        return input("You: ").strip().lower()

# Main execution
if __name__ == "__main__":
    print("Starting Virtual Receptionist AI Agent...")
    
    try:
        ai_receptionist = AdvancedReceptionistAI()
        ai_receptionist.run()
    except Exception as e:
        print(f"Speech recognition not available: {e}")
        print("Starting text-based fallback...")
        text_ai = TextReceptionistAI()
        text_ai.run()
