import streamlit as st
import json
import re

def main():
    st.set_page_config(layout="centered", page_title="AvaDesk")

    # Load CSS
    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title("AvaDesk")

    # Initialize session state
    if 'conversation_state' not in st.session_state:
        st.session_state.conversation_state = 'idle'
    if 'temp_lead_data' not in st.session_state:
        st.session_state.temp_lead_data = {
            "name": "",
            "phone": "",
            "email": "",
            "legal_category": "",
            "case_description": "",
            "desired_outcome": "",
            "incident_date": "",
            "deadlines": "",
            "urgency": "",
            "incident_location": "",
            "other_party": "",
            "previous_representation": "",
            "conflict_check_parties": "",
            "preferred_consultation_method": ""
        }
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(f'<div class="{message["role"]}-message">{message["content"]}</div>', unsafe_allow_html=True)

    # Get user input
    user_input = st.chat_input("Type your message...")

    if user_input:
        # Add user message to chat history
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        with st.chat_message("user"):
            st.markdown(f'<div class="user-message">{user_input}</div>', unsafe_allow_html=True)

        # Process user input
        handle_conversation_flow(user_input)

def handle_conversation_flow(text):
    state = st.session_state.conversation_state

    if state == 'idle':
        st.session_state.temp_lead_data['case_description'] = text
        st.session_state.conversation_state = 'awaiting_name'
        ai_response = "Welcome to AvaDesk. I am an AI Receptionist Assistant. Your information is confidential, and I am not providing legal advice. I have noted your issue. May I have your full name, please?"
    elif state == 'awaiting_name':
        st.session_state.temp_lead_data['name'] = text
        st.session_state.conversation_state = 'awaiting_contact'
        ai_response = f"Thank you, {text}. What is the best phone number and email address to reach you?"
    elif state == 'awaiting_contact':
        phone_regex = r"(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})"
        email_regex = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"

        phone_match = re.search(phone_regex, text)
        email_match = re.search(email_regex, text)

        st.session_state.temp_lead_data['phone'] = phone_match.group(0) if phone_match else "Not provided"
        st.session_state.temp_lead_data['email'] = email_match.group(0) if email_match else "Not provided"

        st.session_state.conversation_state = 'awaiting_legal_category'
        ai_response = "Thank you. What type of legal issue are you facing? (e.g., Criminal, Family Law, Traffic, etc.)"
    elif state == 'awaiting_legal_category':
        st.session_state.temp_lead_data['legal_category'] = text
        st.session_state.conversation_state = 'awaiting_case_description'
        ai_response = "Could you briefly describe what happened?"
    elif state == 'awaiting_case_description':
        st.session_state.temp_lead_data['case_description'] = text
        st.session_state.conversation_state = 'awaiting_desired_outcome'
        ai_response = "What is the main outcome you are hoping for?"
    elif state == 'awaiting_desired_outcome':
        st.session_state.temp_lead_data['desired_outcome'] = text
        st.session_state.conversation_state = 'awaiting_incident_date'
        ai_response = "When did this incident occur?"
    elif state == 'awaiting_incident_date':
        st.session_state.temp_lead_data['incident_date'] = text
        st.session_state.conversation_state = 'awaiting_deadlines'
        ai_response = "Are there any upcoming deadlines, like a court date or a hearing?"
    elif state == 'awaiting_deadlines':
        st.session_state.temp_lead_data['deadlines'] = text
        st.session_state.conversation_state = 'awaiting_urgency'
        ai_response = "How time-sensitive would you say your situation is?"
    elif state == 'awaiting_urgency':
        st.session_state.temp_lead_data['urgency'] = text
        st.session_state.conversation_state = 'awaiting_incident_location'
        ai_response = "What city and state did this occur in?"
    elif state == 'awaiting_incident_location':
        st.session_state.temp_lead_data['incident_location'] = text
        st.session_state.conversation_state = 'awaiting_other_party'
        ai_response = "Who is the other party involved? (e.g., a specific person, a company, the police)"
    elif state == 'awaiting_other_party':
        st.session_state.temp_lead_data['other_party'] = text
        st.session_state.conversation_state = 'awaiting_previous_representation'
        ai_response = "Have you already spoken to or hired another lawyer about this matter?"
    elif state == 'awaiting_previous_representation':
        st.session_state.temp_lead_data['previous_representation'] = text
        st.session_state.conversation_state = 'awaiting_conflict_check'
        ai_response = "May I have the full names of the other parties involved so I can ensure there's no conflict of interest?"
    elif state == 'awaiting_conflict_check':
        st.session_state.temp_lead_data['conflict_check_parties'] = text
        st.session_state.conversation_state = 'awaiting_consultation_method'
        ai_response = "What is the best way to schedule a consultation: a phone call or a video meeting?"
    elif state == 'awaiting_consultation_method':
        st.session_state.temp_lead_data['preferred_consultation_method'] = text
        st.session_state.conversation_state = 'finished'
        json_output = json.dumps(st.session_state.temp_lead_data, indent=2)
        ai_response = f"Thank you for contacting us. Your request will be forwarded to the legal team. Here is a summary of your intake:\n```json\n{json_output}\n```"
        reset_conversation()
    else:
        ai_response = "I'm sorry, I'm not sure how to handle that."

    # Add AI response to chat history
    st.session_state.chat_history.append({"role": "assistant", "content": ai_response})
    with st.chat_message("assistant"):
        st.markdown(f'<div class="ai-message">{ai_response}</div>', unsafe_allow_html=True)

def reset_conversation():
    st.session_state.conversation_state = 'idle'
    st.session_state.temp_lead_data = {
            "name": "",
            "phone": "",
            "email": "",
            "legal_category": "",
            "case_description": "",
            "desired_outcome": "",
            "incident_date": "",
            "deadlines": "",
            "urgency": "",
            "incident_location": "",
            "other_party": "",
            "previous_representation": "",
            "conflict_check_parties": "",
            "preferred_consultation_method": ""
        }

if __name__ == "__main__":
    main()
