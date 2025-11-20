document.addEventListener('DOMContentLoaded', () => {
    const chatLog = document.getElementById('chat-log');
    const userInput = document.getElementById('user-input');
    const sendButton = document.getElementById('send-button');
    const micButton = document.getElementById('mic-button');

    const synth = window.speechSynthesis;
    const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();

    let conversationState = 'idle';
    let tempLeadData = {};

    const config = {
        companyInfo: {
            name: "Australian Lawyers & Advocates",
            address: "Level 1, 299 Elizabeth Street, Sydney, NSW 2000, Australia",
            phone: "(02) 9159 9833",
            email: "info@lawyersandadvocates.com.au",
            greeting: "Welcome to Australian Lawyers & Advocates. We are a criminal and traffic law firm based in Sydney. How can I help you today?",
            founders: "Our Legal Practice Directors, Jack Leitner and Daniel Shestowsky, are both Accredited Specialists in Criminal Law.",
            values: "We provide high-quality, client-centered legal support. We treat our clients as part of our legal team, ensuring you are not just a number."
        },
        services: {
            "criminal law": ["firearms/weapons", "sexual assault", "drug defence", "murder & manslaughter", "assault", "armed robbery", "fraud", "domestic violence", "self defence"],
            "traffic law": ["drink driving", "reckless driving", "traffic tickets"],
            "family law": ["We offer some family law services. For complex cases, we may refer you to a specialist."]
        },
        keywords: {
            consultation: ['consultation', 'appointment', 'meeting', 'speak to a lawyer', 'legal advice'],
            information: ['information', 'tell me about', 'who are you', 'services', 'lawyers', 'values', 'contact', 'address'],
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

        if (config.keywords.consultation.some(k => lowerCaseText.includes(k))) {
            startLeadQualification();
        } else if (config.keywords.information.some(k => lowerCaseText.includes(k))) {
            handleInformation(lowerCaseText);
        } else if (config.keywords.greeting.some(k => lowerCaseText.includes(k))) {
            speak("Hello! How can I help you?");
        } else if (config.keywords.farewell.some(k => lowerCaseText.includes(k))) {
            speak("Thank you for contacting us. Have a great day!");
        } else {
            speak("I can help you schedule a consultation or provide information about our firm. What would you like to do?");
        }
    };

    const handleConversationFlow = (text) => {
        switch (conversationState) {
            case 'awaiting_issue_type':
                tempLeadData.issueType = text;
                conversationState = 'awaiting_issue_details';
                speak("Thank you. Could you briefly describe your situation?");
                break;
            case 'awaiting_issue_details':
                tempLeadData.details = text;
                conversationState = 'awaiting_charge_status';
                speak("Have you already been charged, or are you seeking advice?");
                break;
            case 'awaiting_charge_status':
                tempLeadData.chargeStatus = text;
                conversationState = 'awaiting_urgency';
                speak("How urgent is this matter? For example, do you have a court date soon?");
                break;
            case 'awaiting_urgency':
                tempLeadData.urgency = text;
                conversationState = 'awaiting_contact_name';
                speak("I see. To schedule your consultation, may I have your full name?");
                break;
            case 'awaiting_contact_name':
                tempLeadData.name = text;
                conversationState = 'awaiting_contact_details';
                speak(`Thank you, ${text}. What is the best phone number or email to reach you at?`);
                break;
            case 'awaiting_contact_details':
                tempLeadData.contact = text;
                saveLead(tempLeadData);
                speak(`Thank you. A specialist from our team will contact you at ${text} shortly. We will be in touch soon.`);
                resetConversation();
                break;
        }
    };

    const startLeadQualification = () => {
        conversationState = 'awaiting_issue_type';
        tempLeadData = {};
        speak("I can help with that. First, what type of legal issue are you facing? (e.g., Criminal, Traffic, or Family law)");
    };

    const handleInformation = (text) => {
        if (text.includes('lawyer') || text.includes('who')) {
            speak(config.companyInfo.founders);
        } else if (text.includes('service') || text.includes('criminal') || text.includes('traffic')) {
            const criminalServices = config.services["criminal law"].join(', ');
            const trafficServices = config.services["traffic law"].join(', ');
            speak(`We specialise in Criminal Law, including: ${criminalServices}. We also handle Traffic Law, such as: ${trafficServices}. We offer some family law services as well.`);
        } else if (text.includes('value') || text.includes('approach')) {
            speak(config.companyInfo.values);
        } else if (text.includes('contact') || text.includes('address') || text.includes('phone') || text.includes('email')) {
            speak(`You can reach us at ${config.companyInfo.phone}, email us at ${config.companyInfo.email}, or visit our office at ${config.companyInfo.address}.`);
        } else {
            speak("I can provide information about our lawyers, our services, our values, or our contact details. What would you like to know?");
        }
    };

    const resetConversation = () => {
        conversationState = 'idle';
        tempLeadData = {};
    };

    const saveLead = (data) => {
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
        speak(config.companyInfo.greeting);
    }, 500);
});
