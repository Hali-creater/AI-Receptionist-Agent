document.addEventListener('DOMContentLoaded', () => {
    const chatLog = document.getElementById('chat-log');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const micButton = document.getElementById('mic-button');

    const synth = window.speechSynthesis;
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    let conversationState = 'idle';
    let tempUserData = {};

    const config = {
        companyInfo: {
            hours: "9 AM to 5 PM, Monday through Friday",
            location: "123 Business Street, Suite 100",
            contact: "Phone: 555-0123, Email: hello@company.com",
            wifi: "Network: Company-Guest, Password: Welcome123",
            services: "We offer consulting, development, and support services"
        },
        keywords: {
            emergency: ['emergency', 'help', 'urgent', 'accident', 'fire', 'medical'],
            appointment: ['appointment', 'schedule', 'meeting'],
            registration: ['register', 'check in', 'sign in'],
            information: ['information', 'tell me', 'where is', 'hours', 'location', 'contact', 'wifi', 'services'],
            greeting: ['hello', 'hi', 'good morning'],
            farewell: ['bye', 'thanks', 'goodbye']
        }
    };

    recognition.lang = 'en-US';
    recognition.interimResults = false;
    recognition.maxAlternatives = 1;

    const speak = (text) => {
        addAiMessage(text);
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.rate = 1;
        utterance.pitch = 1;
        synth.speak(utterance);
    };

    const addMessage = (text, sender) => {
        const message = document.createElement('div');
        message.classList.add('message', `${sender}-message`);
        message.textContent = text;
        chatLog.appendChild(message);
        chatLog.scrollTop = chatLog.scrollHeight;
    };

    const addUserMessage = (text) => addMessage(text, 'user');
    const addAiMessage = (text) => addMessage(text, 'ai');

    const processUserInput = (text) => {
        addUserMessage(text);
        const lowerCaseText = text.toLowerCase();

        if (conversationState !== 'idle') {
            handleConversationFlow(lowerCaseText);
            return;
        }

        if (config.keywords.emergency.some(k => lowerCaseText.includes(k))) {
            handleEmergency();
        } else if (config.keywords.appointment.some(k => lowerCaseText.includes(k))) {
            startAppointment();
        } else if (config.keywords.registration.some(k => lowerCaseText.includes(k))) {
            startRegistration();
        } else if (config.keywords.information.some(k => lowerCaseText.includes(k))) {
            handleInformation(lowerCaseText);
        } else if (config.keywords.greeting.some(k => lowerCaseText.includes(k))) {
            speak("Hello! How can I help you today?");
        } else if (config.keywords.farewell.some(k => lowerCaseText.includes(k))) {
            speak("Thank you for visiting! Have a great day!");
        } else {
            speak("I'm here to help with appointments, visitor registration, or general information. What would you like to do?");
        }
    };

    const handleConversationFlow = (text) => {
        switch (conversationState) {
            case 'awaiting_appointment_name':
                tempUserData.name = text;
                conversationState = 'awaiting_appointment_date';
                speak(`Nice to meet you ${text}. What day would work best?`);
                break;
            case 'awaiting_appointment_date':
                tempUserData.date = text;
                conversationState = 'awaiting_appointment_time';
                speak("And what time would you prefer?");
                break;
            case 'awaiting_appointment_time':
                tempUserData.time = text;
                saveAppointment(tempUserData);
                speak(`Perfect! I've scheduled you for ${tempUserData.date} at ${tempUserData.time}.`);
                resetConversation();
                break;
            case 'awaiting_registration_name':
                tempUserData.name = text;
                conversationState = 'awaiting_registration_company';
                speak("What company are you from?");
                break;
            case 'awaiting_registration_company':
                tempUserData.company = text;
                conversationState = 'awaiting_registration_contact';
                speak("Who are you here to see today?");
                break;
            case 'awaiting_registration_contact':
                tempUserData.contact = text;
                saveRegistration(tempUserData);
                speak(`Thank you, ${tempUserData.name}. I've notified ${tempUserData.contact} that you've arrived.`);
                resetConversation();
                break;
        }
    };

    const startAppointment = () => {
        conversationState = 'awaiting_appointment_name';
        tempUserData = {};
        speak("I can help you schedule an appointment. What's your name?");
    };

    const startRegistration = () => {
        conversationState = 'awaiting_registration_name';
        tempUserData = {};
        speak("Let me get you registered. What's your full name?");
    };

    const handleInformation = (text) => {
        if (text.includes('hour')) {
            speak(`Our office hours are ${config.companyInfo.hours}.`);
        } else if (text.includes('location') || text.includes('address')) {
            speak(`We are located at ${config.companyInfo.location}.`);
        } else if (text.includes('contact')) {
            speak(`You can reach us at ${config.companyInfo.contact}.`);
        } else if (text.includes('wifi')) {
            speak(`The WiFi details are: ${config.companyInfo.wifi}.`);
        } else if (text.includes('service')) {
            speak(`We offer the following services: ${config.companyInfo.services}.`);
        } else {
            speak("I can provide information about office hours, location, contact details, WiFi, and services.");
        }
    };

    const handleEmergency = () => {
        speak("I've detected this might be an emergency. I am connecting you with security immediately.");
    };

    const resetConversation = () => {
        conversationState = 'idle';
        tempUserData = {};
    };

    const saveData = (key, data) => {
        const existingData = JSON.parse(localStorage.getItem(key)) || [];
        existingData.push(data);
        localStorage.setItem(key, JSON.stringify(existingData));
    };

    const saveAppointment = (data) => saveData('appointments', { ...data, timestamp: new Date().toISOString() });
    const saveRegistration = (data) => saveData('registrations', { ...data, checkInTime: new Date().toISOString() });

    sendButton.addEventListener('click', () => {
        const text = userInput.value.trim();
        if (text) {
            processUserInput(text);
            userInput.value = '';
        }
    });

    userInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            sendButton.click();
        }
    });

    micButton.addEventListener('click', () => {
        recognition.start();
    });

    recognition.onresult = (event) => {
        const speechToText = event.results[0][0].transcript;
        processUserInput(speechToText);
    };

    recognition.onerror = (event) => {
        speak("I'm sorry, I couldn't understand that. Please try again.");
    };

    // Initial greeting
    setTimeout(() => {
        speak("Hello! Welcome to our office. How can I help you today?");
    }, 500);
});
