document.addEventListener('DOMContentLoaded', () => {
    const chatLog = document.getElementById('chat-log');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const micButton = document.getElementById('mic-button');
    const synth = window.speechSynthesis;
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
    let conversationState = 'idle';
    let tempLeadData = {
        name: "",
        phone: "",
        email: "",
        legal_category: "",
        short_description: "",
        details_collected: "",
        urgency: "",
        preferred_consultation_time: ""
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
        handleConversationFlow(text.toLowerCase());
    };
    const handleConversationFlow = (text) => {
        switch (conversationState) {
            case 'idle':
                tempLeadData.short_description = text;
                conversationState = 'awaiting_legal_category';
                speak("I am an AI Receptionist Assistant for a law firm. Your information is confidential, and I am not providing legal advice. I have noted your issue. Which of the following legal categories does it belong to: contract, corporate, family, civil litigation, criminal, real estate, intellectual property, immigration, debt recovery, or other?");
                break;
            case 'awaiting_legal_category':
                tempLeadData.legal_category = text;
                conversationState = 'awaiting_name';
                speak("Got it. May I have your full name?");
                break;
            case 'awaiting_name':
                tempLeadData.name = text;
                conversationState = 'awaiting_phone';
                speak(`Thank you, ${text}. What is your phone number?`);
                break;
            case 'awaiting_phone':
                tempLeadData.phone = text;
                conversationState = 'awaiting_email';
                speak("And your email address?");
                break;
            case 'awaiting_email':
                tempLeadData.email = text;
                conversationState = 'awaiting_urgency';
                speak("How urgent is this matter?");
                break;
            case 'awaiting_urgency':
                tempLeadData.urgency = text;
                conversationState = 'awaiting_consultation_time';
                speak("What is your preferred consultation time?");
                break;
            case 'awaiting_consultation_time':
                tempLeadData.preferred_consultation_time = text;
                tempLeadData.details_collected = "all";
                saveLead(tempLeadData);
                resetConversation();
                break;
        }
    };
    const resetConversation = () => {
        conversationState = 'idle';
        tempLeadData = {
            name: "",
            phone: "",
            email: "",
            legal_category: "",
            short_description: "",
            details_collected: "",
            urgency: "",
            preferred_consultation_time: ""
        };
    };
    const saveLead = (data) => {
        const jsonOutput = JSON.stringify(data, null, 2);
        addAiMessage(`Thank you for contacting us. Your request will be forwarded to the legal team. Here is a summary of your intake:\n${jsonOutput}`);
        const key = 'leads';
        const existingData = JSON.parse(localStorage.getItem(key)) || [];
        existingData.push({ ...data, timestamp: new Date().toISOString() });
        localStorage.setItem(key, JSON.stringify(existingData));
    };
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
        speak("Welcome! To start, please type your message or use the microphone.");
        conversationState = 'idle';
    }, 500);
});
