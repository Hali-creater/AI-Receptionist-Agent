import streamlit as st
import json

QUESTIONS = [
    # Phase 1: Foundation & Identity
    {"key": "full_legal_name", "phase": 1, "question": "What is your full legal name, and what should I call you?"},
    {"key": "contact_info", "phase": 1, "question": "What is the best mailing address, email, and phone number to reach you?"},
    {"key": "previous_representation", "phase": 1, "question": "Have you spoken to or hired another lawyer about this matter before?"},
    {"key": "referral_source", "phase": 1, "question": "How did you hear about me or our firm?"},
    {"key": "deadlines", "phase": 1, "question": "Do you have any time-sensitive deadlines we need to be aware of? (e.g., court dates, statute of limitations)"},
    # Phase 2: Core Narrative & Facts
    {"key": "case_summary", "phase": 2, "question": "In your own words, please tell me what brings you here today."},
    {"key": "timeline", "phase": 2, "question": "When did this situation first begin? Please walk me through the key events in chronological order."},
    {"key": "involved_parties", "phase": 2, "question": "Who else is involved? (Full names, relationships, companies)"},
    {"key": "location", "phase": 2, "question": "Where did the key events take place?"},
    {"key": "turning_point", "phase": 2, "question": "What was the single most important event or turning point?"},
    {"key": "current_status", "phase": 2, "question": "What is the situation right now? What is the latest development?"},
    # Phase 3: Objectives & Strategy
    {"key": "ideal_outcome", "phase": 3, "question": "What is your ideal outcome from this situation?"},
    {"key": "minimum_resolution", "phase": 3, "question": "What is the minimum result you would accept to resolve this?"},
    {"key": "motivation", "phase": 3, "question": "Is this more about financial compensation, a specific action (like getting a contract enforced), or a matter of principle?"},
    {"key": "risk_tolerance", "phase": 3, "question": "How do you feel about the risks, costs, and potential stress of going to court versus trying to settle?"},
    {"key": "past_resolution_attempts", "phase": 3, "question": "Have you taken any steps to resolve this already? (e.g., sent a demand letter, filed a report, had a direct conversation)"},
    # Phase 4: Case-Specific Deep Dive (Civil Litigation / Disputes)
    {"key": "damages", "phase": 4, "question": "What specific financial losses or harms have you suffered? Do you have records, receipts, or calculations?"},
    {"key": "evidence", "phase": 4, "question": "What documentation do you have? (Contracts, emails, text messages, photos, videos, invoices)"},
    {"key": "witnesses", "phase": 4, "question": "Who else witnessed the events? Are they willing to speak on your behalf?"},
    # Phase 4: Case-Specific Deep Dive (Family Law)
    {"key": "relationship_history", "phase": 4, "question": "What is the history of your relationship/marriage? (Date of marriage, separation)"},
    {"key": "children_arrangements", "phase": 4, "question": "What are the current living arrangements for the children? What do you believe is in their best interest?"},
    {"key": "assets_and_debts", "phase": 4, "question": "Can you list all significant assets (home, cars, accounts) and debts you own, jointly or separately?"},
    # Phase 4: Case-Specific Deep Dive (Criminal Defense)
    {"key": "charges_investigation", "phase": 4, "question": "Have you been charged? If so, with what? Or are you under investigation?"},
    {"key": "official_contact_details", "phase": 4, "question": "What have you already said to the police or investigators?"},
    {"key": "case_details_criminal", "phase": 4, "question": "Do you know the names of any arresting officers, detectives, or witnesses the prosecution might have?"},
    # Phase 4: Case-Specific Deep Dive (Business/Contract Law)
    {"key": "agreement_details", "phase": 4, "question": "Do you have a written contract or agreement? What were the key terms?"},
    {"key": "breach_details", "phase": 4, "question": "What specific part of the agreement do you believe was broken, and how?"},
    {"key": "business_impact", "phase": 4, "question": "How has this dispute affected your business operations or finances?"},
    # Phase 5: Practical & Financial Considerations
    {"key": "budget", "phase": 5, "question": "What is your understanding or expectation regarding the costs and fees for my services?"},
    {"key": "communication_preferences", "phase": 5, "question": "How often would you like updates, and what is your preferred method of communication?"},
    {"key": "decision_maker", "phase": 5, "question": "Are you the sole decision-maker, or do you need to consult with anyone else (like a spouse or partner)?"},
    # Phase 6: Critical Closing Questions
    {"key": "case_weaknesses", "phase": 6, "question": "What do you think is the weakest part of your position or story?"},
    {"key": "opponent_argument", "phase": 6, "question": "What do you think the other side would say is their strongest argument?"},
    {"key": "personal_context", "phase": 6, "question": "Is there anything in your personal history, background, or past conduct that you think the other side might try to use against you?"},
    {"key": "final_check", "phase": 6, "question": "Is there anything important I haven't asked about that you think I need to know?"}
]

def main():
    st.set_page_config(layout="centered", page_title="AvaDesk")

    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title("AvaDesk")

    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'lead_data' not in st.session_state:
        st.session_state.lead_data = {q["key"]: "" for q in QUESTIONS}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = [{"role": "assistant", "content": "Welcome to AvaDesk. I am an AI Receptionist Assistant. Your information is confidential, and I am not providing legal advice. To start, please answer the following questions."}]
        st.session_state.chat_history.append({"role": "assistant", "content": QUESTIONS[0]['question']})

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(f'<div class="{message["role"]}-message">{message["content"]}</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Type your message...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        handle_conversation_flow(user_input)
        st.rerun()


def handle_conversation_flow(user_answer):
    current_index = st.session_state.current_question_index

    question_key = QUESTIONS[current_index]["key"]
    st.session_state.lead_data[question_key] = user_answer

    st.session_state.current_question_index += 1
    next_index = st.session_state.current_question_index

    if next_index < len(QUESTIONS):
        next_question = QUESTIONS[next_index]["question"]
        st.session_state.chat_history.append({"role": "assistant", "content": next_question})
    else:
        summary = "Thank you for providing all the information. Here is a summary of your intake:"
        json_output = json.dumps(st.session_state.lead_data, indent=2)
        final_message = f"{summary}\n```json\n{json_output}\n```"

        st.session_state.chat_history.append({"role": "assistant", "content": final_message})

        st.session_state.current_question_index = 0
        st.session_state.lead_data = {q["key"]: "" for q in QUESTIONS}


if __name__ == "__main__":
    main()
