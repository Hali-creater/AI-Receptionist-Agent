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
        case_description: "",
        desired_outcome: "",
        incident_date: "",
        deadlines: "",
        urgency: "",
        incident_location: "",
        other_party: "",
        previous_representation: "",
        conflict_check_parties: "",
        preferred_consultation_method: ""
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
        handleConversationFlow(text);
    };

    const handleConversationFlow = (text) => {
        if (conversationState === 'idle') {
            tempLeadData.case_description = text;
            conversationState = 'awaiting_name';
            speak("Welcome to AvaDesk. I am an AI Receptionist Assistant. Your information is confidential, and I am not providing legal advice. I have noted your issue. May I have your full name, please?");
            return;
        }

        switch (conversationState) {
            case 'awaiting_name':
                tempLeadData.name = text;
                conversationState = 'awaiting_contact';
                speak(`Thank you, ${text}. What is the best phone number and email address to reach you?`);
                break;
            case 'awaiting_contact':
                // Simple parsing for phone and email. A more robust solution would use regex.
                const parts = text.split(' ');
                tempLeadData.phone = parts.find(p => p.match(/^[0-9-()+]+$/)) || "Not provided";
                tempLeadData.email = parts.find(p => p.includes('@')) || "Not provided";
                conversationState = 'awaiting_legal_category';
                speak("Thank you. What type of legal issue are you facing? (e.g., Criminal, Family Law, Traffic, etc.)");
                break;
            case 'awaiting_legal_category':
                tempLeadData.legal_category = text;
                conversationState = 'awaiting_case_description';
                speak("Could you briefly describe what happened?");
                break;
            case 'awaiting_case_description':
                tempLeadData.case_description = text;
                conversationState = 'awaiting_desired_outcome';
                speak("What is the main outcome you are hoping for?");
                break;
            case 'awaiting_desired_outcome':
                tempLeadData.desired_outcome = text;
                conversationState = 'awaiting_incident_date';
                speak("When did this incident occur?");
                break;
            case 'awaiting_incident_date':
                tempLeadData.incident_date = text;
                conversationState = 'awaiting_deadlines';
                speak("Are there any upcoming deadlines, like a court date or a hearing?");
                break;
            case 'awaiting_deadlines':
                tempLeadData.deadlines = text;
                conversationState = 'awaiting_urgency';
                speak("How time-sensitive would you say your situation is?");
                break;
            case 'awaiting_urgency':
                tempLeadData.urgency = text;
                conversationState = 'awaiting_incident_location';
                speak("What city and state did this occur in?");
                break;
            case 'awaiting_incident_location':
                tempLeadData.incident_location = text;
                conversationState = 'awaiting_other_party';
                speak("Who is the other party involved? (e.g., a specific person, a company, the police)");
                break;
            case 'awaiting_other_party':
                tempLeadData.other_party = text;
                conversationState = 'awaiting_previous_representation';
                speak("Have you already spoken to or hired another lawyer about this matter?");
                break;
            case 'awaiting_previous_representation':
                tempLeadData.previous_representation = text;
                conversationState = 'awaiting_conflict_check';
                speak("May I have the full names of the other parties involved so I can ensure there's no conflict of interest?");
                break;
            case 'awaiting_conflict_check':
                tempLeadData.conflict_check_parties = text;
                conversationState = 'awaiting_consultation_method';
                speak("What is the best way to schedule a consultation: a phone call or a video meeting?");
                break;
            case 'awaiting_consultation_method':
                tempLeadData.preferred_consultation_method = text;
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
            case_description: "",
            desired_outcome: "",
            incident_date: "",
            deadlines: "",
            urgency: "",
            incident_location: "",
            other_party: "",
            previous_representation: "",
            conflict_check_parties: "",
            preferred_consultation_method: ""
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

    // No initial greeting on page load, wait for user to start the conversation.
});
