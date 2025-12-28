import streamlit as st
import json
import smtplib
from email.mime.text import MIMEText

LAW_QUESTIONS = {
    "Commercial Law": [
        {"key": "business_type", "question": "What type of business do you operate?"},
        {"key": "business_duration", "question": "How long has your business been running?"},
        {"key": "dispute_nature", "question": "What is the nature of the dispute or issue?"},
        {"key": "contract_related", "question": "Is this related to a contract?"},
        {"key": "other_parties", "question": "Who are the other parties involved?"},
        {"key": "issue_arose_date", "question": "When did the issue first arise?"},
        {"key": "resolution_attempts", "question": "Have you attempted to resolve it outside of court?"},
        {"key": "written_agreements", "question": "Do you have written agreements related to this matter?"},
        {"key": "goods_or_services", "question": "Is this about goods or services?"},
        {"key": "outstanding_payments", "question": "Are there outstanding payments involved?"},
        {"key": "breach_of_contract", "question": "Is there a breach of contract claim?"},
        {"key": "claimant_or_defendant", "question": "Are you the claimant or defendant?"},
        {"key": "legal_notices", "question": "Have you received any legal notices?"},
        {"key": "dispute_location", "question": "Is this dispute local or international?"},
        {"key": "supporting_documents", "question": "Do you have supporting documents?"},
        {"key": "is_urgent", "question": "Is this urgent?"},
        {"key": "deadlines", "question": "Are there deadlines approaching?"},
        {"key": "previous_lawyers", "question": "Have you worked with lawyers before on this matter?"},
        {"key": "financial_value", "question": "What is the financial value of the dispute?"},
        {"key": "intellectual_property", "question": "Is this related to intellectual property?"},
        {"key": "franchising", "question": "Is this related to franchising?"},
        {"key": "supply_chain", "question": "Is this related to supply chain issues?"},
        {"key": "multiple_parties", "question": "Are there multiple parties involved?"},
        {"key": "business_competition", "question": "Is this related to business competition?"},
        {"key": "consumer_complaints", "question": "Is this related to consumer complaints?"},
        {"key": "regulatory_compliance", "question": "Is this related to regulatory compliance?"},
        {"key": "previous_sued", "question": "Have you been sued before?"},
        {"key": "mediation_or_litigation", "question": "Do you want mediation or litigation?"},
        {"key": "insurance_coverage", "question": "Do you have insurance coverage for this?"},
        {"key": "desired_outcome", "question": "What outcome are you hoping for?"}
    ],
    "Corporate Law": [
        {"key": "company_structure", "question": "What type of company structure do you have?"},
        {"key": "role_in_company", "question": "Are you a shareholder, director, or officer?"},
        {"key": "company_formation", "question": "Is this about company formation?"},
        {"key": "governance_issues", "question": "Is this about governance issues?"},
        {"key": "shareholder_disputes", "question": "Is this about shareholder disputes?"},
        {"key": "mergers_acquisitions", "question": "Is this about mergers or acquisitions?"},
        {"key": "corporate_law_compliance", "question": "Is this about compliance with corporate law?"},
        {"key": "board_decisions", "question": "Is this about board decisions?"},
        {"key": "minority_shareholder_rights", "question": "Is this about minority shareholder rights?"},
        {"key": "director_liability", "question": "Is this about director liability?"},
        {"key": "company_dissolution", "question": "Is this about company dissolution?"},
        {"key": "restructuring", "question": "Is this about restructuring?"},
        {"key": "corporate_fraud", "question": "Is this about corporate fraud?"},
        {"key": "corporate_financing", "question": "Is this about corporate financing?"},
        {"key": "securities_regulation", "question": "Is this about securities regulation?"},
        {"key": "shareholder_agreements", "question": "Is this about shareholder agreements?"},
        {"key": "dividend_disputes", "question": "Is this about dividend disputes?"},
        {"key": "hostile_takeovers", "question": "Is this about hostile takeovers?"},
        {"key": "corporate_governance_policies", "question": "Is this about corporate governance policies?"},
        {"key": "executive_compensation", "question": "Is this about executive compensation?"},
        {"key": "voting_rights", "question": "Is this about voting rights?"},
        {"key": "fiduciary_duties", "question": "Is this about fiduciary duties?"},
        {"key": "conflicts_of_interest", "question": "Is this about conflicts of interest?"},
        {"key": "compliance_audits", "question": "Is this about compliance audits?"},
        {"key": "regulatory_filings", "question": "Is this about regulatory filings?"},
        {"key": "corporate_tax_issues", "question": "Is this about corporate tax issues?"},
        {"key": "cross_border_matters", "question": "Is this about cross-border corporate matters?"},
        {"key": "corporate_contracts", "question": "Is this about corporate contracts?"},
        {"key": "corporate_liability", "question": "Is this about corporate liability?"},
        {"key": "desired_resolution", "question": "What resolution are you seeking?"}
    ],
    "Employment Law": [
        {"key": "employer_or_employee", "question": "Are you an employer or employee?"},
        {"key": "wrongful_termination", "question": "Is this about wrongful termination?"},
        {"key": "workplace_discrimination", "question": "Is this about workplace discrimination?"},
        {"key": "harassment", "question": "Is this about harassment?"},
        {"key": "wages_overtime", "question": "Is this about wages or overtime?"},
        {"key": "employment_contracts", "question": "Is this about employment contracts?"},
        {"key": "workplace_safety", "question": "Is this about workplace safety?"},
        {"key": "benefits_pensions", "question": "Is this about benefits or pensions?"},
        {"key": "maternity_paternity_leave", "question": "Is this about maternity or paternity leave?"},
        {"key": "redundancy", "question": "Is this about redundancy?"},
        {"key": "unfair_dismissal", "question": "Is this about unfair dismissal?"},
        {"key": "workplace_retaliation", "question": "Is this about workplace retaliation?"},
        {"key": "whistleblowing", "question": "Is this about whistleblowing?"},
        {"key": "workplace_policies", "question": "Is this about workplace policies?"},
        {"key": "union_disputes", "question": "Is this about union disputes?"},
        {"key": "collective_bargaining", "question": "Is this about collective bargaining?"},
        {"key": "disciplinary_action", "question": "Is this about disciplinary action?"},
        {"key": "workplace_injury", "question": "Is this about workplace injury?"},
        {"key": "disability_rights", "question": "Is this about disability rights?"},
        {"key": "equal_pay", "question": "Is this about equal pay?"},
        {"key": "contract_breaches", "question": "Is this about contract breaches?"},
        {"key": "probationary_periods", "question": "Is this about probationary periods?"},
        {"key": "non_compete_clauses", "question": "Is this about non-compete clauses?"},
        {"key": "confidentiality_agreements", "question": "Is this about confidentiality agreements?"},
        {"key": "workplace_bullying", "question": "Is this about workplace bullying?"},
        {"key": "grievance_procedures", "question": "Is this about grievance procedures?"},
        {"key": "retirement_disputes", "question": "Is this about retirement disputes?"},
        {"key": "severance_packages", "question": "Is this about severance packages?"},
        {"key": "workplace_investigations", "question": "Is this about workplace investigations?"},
        {"key": "desired_outcome", "question": "What outcome do you want?"}
    ],
    "Real Estate Law": [
        {"key": "role", "question": "Are you a buyer, seller, landlord, or tenant?"},
        {"key": "property_purchase", "question": "Is this about property purchase?"},
        {"key": "property_sale", "question": "Is this about property sale?"},
        {"key": "lease_agreements", "question": "Is this about lease agreements?"},
        {"key": "rental_disputes", "question": "Is this about rental disputes?"},
        {"key": "eviction", "question": "Is this about eviction?"},
        {"key": "mortgage_issues", "question": "Is this about mortgage issues?"},
        {"key": "foreclosure", "question": "Is this about foreclosure?"},
        {"key": "property_boundaries", "question": "Is this about property boundaries?"},
        {"key": "land_use", "question": "Is this about land use?"},
        {"key": "zoning_laws", "question": "Is this about zoning laws?"},
        {"key": "construction_disputes", "question": "Is this about construction disputes?"},
        {"key": "property_development", "question": "Is this about property development?"},
        {"key": "title_deeds", "question": "Is this about title deeds?"},
        {"key": "easements", "question": "Is this about easements?"},
        {"key": "property_fraud", "question": "Is this about property fraud?"},
        {"key": "co_ownership_disputes", "question": "Is this about co-ownership disputes?"},
        {"key": "inheritance_of_property", "question": "Is this about inheritance of property?"},
        {"key": "commercial_property", "question": "Is this about commercial property?"},
        {"key": "residential_property", "question": "Is this about residential property?"},
        {"key": "landlord_obligations", "question": "Is this about landlord obligations?"},
        {"key": "tenant_rights", "question": "Is this about tenant rights?"},
        {"key": "property_valuation", "question": "Is this about property valuation?"},
        {"key": "property_insurance", "question": "Is this about property insurance?"},
        {"key": "environmental_compliance", "question": "Is this about environmental compliance?"},
        {"key": "building_permits", "question": "Is this about building permits?"},
        {"key": "property_taxes", "question": "Is this about property taxes?"},
        {"key": "real_estate_agents", "question": "Is this about real estate agents?"},
        {"key": "property_investment", "question": "Is this about property investment?"},
        {"key": "desired_resolution", "question": "What resolution are you seeking?"}
    ],
    "Contentious & Litigation": [
        {"key": "filing_or_defending", "question": "Are you filing a lawsuit or defending one?"},
        {"key": "dispute_type", "question": "What type of dispute is this?"},
        {"key": "parties_involved", "question": "Who are the parties involved?"},
        {"key": "financial_value", "question": "What is the financial value of the dispute?"},
        {"key": "civil_or_commercial", "question": "Is this civil or commercial litigation?"},
        {"key": "breach_of_contract", "question": "Is this about breach of contract?"},
        {"key": "negligence", "question": "Is this about negligence?"},
        {"key": "fraud", "question": "Is this about fraud?"},
        {"key": "property_disputes", "question": "Is this about property disputes?"},
        {"key": "employment_disputes", "question": "Is this about employment disputes?"},
        {"key": "family_disputes", "question": "Is this about family disputes?"},
        {"key": "debt_recovery", "question": "Is this about debt recovery?"},
        {"key": "intellectual_property", "question": "Is this about intellectual property?"},
        {"key": "defamation", "question": "Is this about defamation?"},
        {"key": "insurance_claims", "question": "Is this about insurance claims?"},
        {"key": "partnership_disputes", "question": "Is this about partnership disputes?"},
        {"key": "shareholder_disputes", "question": "Is this about shareholder disputes?"},
        {"key": "landlord_tenant_disputes", "question": "Is this about landlord-tenant disputes?"},
        {"key": "construction_disputes", "question": "Is this about construction disputes?"},
        {"key": "consumer_complaints", "question": "Is this about consumer complaints?"},
        {"key": "regulatory_compliance", "question": "Is this about regulatory compliance?"},
        {"key": "arbitration", "question": "Is this about arbitration?"},
        {"key": "mediation", "question": "Is this about mediation?"},
        {"key": "settlement_negotiations", "question": "Is this about settlement negotiations?"},
        {"key": "appeals", "question": "Is this about appeals?"},
        {"key": "enforcement_of_judgments", "question": "Is this about enforcement of judgments?"},
        {"key": "cross_border_disputes", "question": "Is this about cross-border disputes?"},
        {"key": "is_urgent", "question": "Is this urgent?"},
        {"key": "supporting_documents", "question": "Do you have supporting documents?"},
        {"key": "desired_outcome", "question": "What outcome are you seeking?"}
    ],
    "Competition Law": [
        {"key": "anti_competitive_practices", "question": "Is this about anti-competitive practices?"},
        {"key": "price_fixing", "question": "Is this about price fixing?"},
        {"key": "market_dominance", "question": "Is this about market dominance?"},
        {"key": "abuse_of_power", "question": "Is this about abuse of power?"},
        {"key": "mergers_acquisitions", "question": "Is this about mergers or acquisitions?"},
        {"key": "cartel_investigations", "question": "Is this about cartel investigations?"},
        {"key": "unfair_trade_practices", "question": "Is this about unfair trade practices?"},
        {"key": "predatory_pricing", "question": "Is this about predatory pricing?"},
        {"key": "exclusive_dealing", "question": "Is this about exclusive dealing?"},
        {"key": "bid_rigging", "question": "Is this about bid rigging?"},
        {"key": "resale_price_maintenance", "question": "Is this about resale price maintenance?"},
        {"key": "monopolies", "question": "Is this about monopolies?"},
        {"key": "restrictive_agreements", "question": "Is this about restrictive agreements?"},
        {"key": "consumer_protection", "question": "Is this about consumer protection?"},
        {"key": "regulatory_compliance", "question": "Is this about regulatory compliance?"},
        {"key": "unfair_competition", "question": "Is this about unfair competition?"},
        {"key": "intellectual_property_misuse", "question": "Is this about intellectual property misuse?"},
        {"key": "market_entry_barriers", "question": "Is this about market entry barriers?"},
        {"key": "supply_chain_restrictions", "question": "Is this about supply chain restrictions?"},
        {"key": "distribution_agreements", "question": "Is this about distribution agreements?"},
        {"key": "advertising_practices", "question": "Is this about advertising practices?"},
        {"key": "merger_clearance", "question": "Is this about merger clearance?"},
        {"key": "competition_authority_investigations", "question": "Is this about competition authority investigations?"},
        {"key": "penalties_fines", "question": "Is this about penalties or fines?"},
        {"key": "compliance_programs", "question": "Is this about compliance programs?"},
        {"key": "whistleblowing", "question": "Is this about whistleblowing?"},
        {"key": "cross_border_competition_issues", "question": "Is this about cross-border competition issues?"},
        {"key": "is_urgent", "question": "Is this urgent?"},
        {"key": "supporting_documents", "question": "Do you have supporting documents?"},
        {"key": "desired_resolution", "question": "What resolution are you seeking?"}
    ],
    "Aviation Law": [
        {"key": "party_type", "question": "Are you a passenger, airline, employee, or another party?"},
        {"key": "flight_delay_cancellation", "question": "Is this about a flight delay or cancellation?"},
        {"key": "denied_boarding", "question": "Is this about denied boarding?"},
        {"key": "lost_damaged_luggage", "question": "Is this about lost or damaged luggage?"},
        {"key": "compensation_claims", "question": "Is this about compensation claims?"},
        {"key": "ticket_refunds", "question": "Is this about ticket refunds?"},
        {"key": "airline_contracts", "question": "Is this about airline contracts?"},
        {"key": "aviation_safety_concerns", "question": "Is this about aviation safety concerns?"},
        {"key": "aircraft_leasing", "question": "Is this about aircraft leasing?"},
        {"key": "aircraft_financing", "question": "Is this about aircraft financing?"},
        {"key": "pilot_licensing_certification", "question": "Is this about pilot licensing or certification?"},
        {"key": "crew_employment_disputes", "question": "Is this about crew employment disputes?"},
        {"key": "passenger_rights", "question": "Is this about passenger rights?"},
        {"key": "regulatory_compliance", "question": "Is this about regulatory compliance?"},
        {"key": "airport_operations", "question": "Is this about airport operations?"},
        {"key": "aviation_insurance", "question": "Is this about aviation insurance?"},
        {"key": "aviation_accidents", "question": "Is this about aviation accidents?"},
        {"key": "liability_claims", "question": "Is this about liability claims?"},
        {"key": "international_aviation_law", "question": "Is this about international aviation law?"},
        {"key": "cargo_disputes", "question": "Is this about cargo disputes?"},
        {"key": "charter_flight_agreements", "question": "Is this about charter flight agreements?"},
        {"key": "air_traffic_control_issues", "question": "Is this about air traffic control issues?"},
        {"key": "aviation_security", "question": "Is this about aviation security?"},
        {"key": "aircraft_maintenance_disputes", "question": "Is this about aircraft maintenance disputes?"},
        {"key": "environmental_regulations", "question": "Is this about environmental regulations in aviation?"},
        {"key": "government_aviation_policies", "question": "Is this about government aviation policies?"},
        {"key": "cross_border_aviation_disputes", "question": "Is this about cross-border aviation disputes?"},
        {"key": "aviation_licensing_authorities", "question": "Is this about aviation licensing authorities?"},
        {"key": "supporting_documents", "question": "Do you have supporting documents (tickets, contracts, notices)?"},
        {"key": "desired_resolution", "question": "What resolution or outcome are you seeking?"}
    ],
    "Shipping Law": [
        {"key": "party_type", "question": "Are you a ship owner, charterer, cargo owner, or crew member?"},
        {"key": "cargo_damage_loss", "question": "Is this about cargo damage or loss?"},
        {"key": "late_delivery_goods", "question": "Is this about late delivery of goods?"},
        {"key": "freight_payment_disputes", "question": "Is this about freight payment disputes?"},
        {"key": "charter_party_agreements", "question": "Is this about charter party agreements?"},
        {"key": "bills_of_lading", "question": "Is this about bills of lading?"},
        {"key": "ship_collisions", "question": "Is this about ship collisions?"},
        {"key": "salvage_claims", "question": "Is this about salvage claims?"},
        {"key": "marine_insurance", "question": "Is this about marine insurance?"},
        {"key": "crew_employment_disputes", "question": "Is this about crew employment disputes?"},
        {"key": "ship_registration", "question": "Is this about ship registration?"},
        {"key": "ship_financing", "question": "Is this about ship financing?"},
        {"key": "shipbuilding_contracts", "question": "Is this about shipbuilding contracts?"},
        {"key": "repairs_maintenance_disputes", "question": "Is this about repairs or maintenance disputes?"},
        {"key": "port_regulations", "question": "Is this about port regulations?"},
        {"key": "customs_clearance_issues", "question": "Is this about customs clearance issues?"},
        {"key": "environmental_compliance_at_sea", "question": "Is this about environmental compliance at sea?"},
        {"key": "pollution_oil_spills", "question": "Is this about pollution or oil spills?"},
        {"key": "maritime_safety", "question": "Is this about maritime safety?"},
        {"key": "piracy_security_concerns", "question": "Is this about piracy or security concerns?"},
        {"key": "international_shipping_regulations", "question": "Is this about international shipping regulations?"},
        {"key": "cabotage_laws", "question": "Is this about cabotage laws (domestic shipping restrictions)?"},
        {"key": "demurrage_detention_charges", "question": "Is this about demurrage or detention charges?"},
        {"key": "ship_arrest_detention", "question": "Is this about ship arrest or detention?"},
        {"key": "limitation_of_liability", "question": "Is this about limitation of liability?"},
        {"key": "arbitration_shipping_disputes", "question": "Is this about arbitration in shipping disputes?"},
        {"key": "cross_border_shipping_disputes", "question": "Is this about cross-border shipping disputes?"},
        {"key": "government_maritime_policies", "question": "Is this about government maritime policies?"},
        {"key": "supporting_documents", "question": "Do you have supporting documents (contracts, bills of lading, notices)?"},
        {"key": "desired_resolution", "question": "What resolution or outcome are you seeking?"}
    ]
}

def send_email(subject, body):
    """Sends an email using credentials from Streamlit's secrets."""
    try:
        email_config = st.secrets["email"]
        sender_email = email_config["address"]
        password = email_config["password"]
        recipient_email = email_config["recipient_address"]
        smtp_server = email_config["smtp_server"]
        smtp_port = email_config["smtp_port"]

        msg = MIMEText(body)
        msg['Subject'] = subject
        msg['From'] = sender_email
        msg['To'] = recipient_email

        with smtplib.SMTP(smtp_server, smtp_port) as server:
            server.starttls()
            server.login(sender_email, password)
            server.send_message(msg)
        return True
    except Exception as e:
        st.error(f"Error sending email: {e}")
        return False

def main():
    st.set_page_config(layout="centered", page_title="AvaDesk")

    with open("style.css") as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

    st.title("AvaDesk")

    if 'current_question_index' not in st.session_state:
        st.session_state.current_question_index = 0
    if 'lead_data' not in st.session_state:
        st.session_state.lead_data = {}
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'selected_specialty' not in st.session_state:
        st.session_state.selected_specialty = None

    if not st.session_state.chat_history:
        # Initial state: asking for specialty
        specialties = "\n".join([f"- {key}" for key in LAW_QUESTIONS.keys()])
        welcome_message = (
            "Welcome to AvaDesk. I am an AI Receptionist Assistant. "
            "Your information is confidential, and I am not providing legal advice.\n\n"
            "Please select the area of law that best fits your needs:\n"
            f"{specialties}"
        )
        st.session_state.chat_history.append({"role": "assistant", "content": welcome_message})

    for message in st.session_state.chat_history:
        role = message["role"]
        display_role = "Client" if role == "user" else role
        with st.chat_message(display_role):
            st.markdown(f'<div class="{role}-message">{message["content"]}</div>', unsafe_allow_html=True)

    user_input = st.chat_input("Type your response...")

    if user_input:
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        handle_conversation_flow(user_input)
        st.rerun()


def handle_conversation_flow(user_answer):
    if not st.session_state.selected_specialty:
        # User has just selected a specialty
        if user_answer in LAW_QUESTIONS:
            st.session_state.selected_specialty = user_answer
            st.session_state.current_question_index = 0
            questions = LAW_QUESTIONS[st.session_state.selected_specialty]
            st.session_state.lead_data = {q["key"]: "" for q in questions}
            st.session_state.chat_history.append({"role": "assistant", "content": questions[0]['question']})
        else:
            st.session_state.chat_history.append({"role": "assistant", "content": "Please select a valid area of law from the list."})
        return

    current_index = st.session_state.current_question_index
    questions = LAW_QUESTIONS[st.session_state.selected_specialty]

    if current_index >= len(questions):
        return

    question_key = questions[current_index]["key"]
    st.session_state.lead_data[question_key] = user_answer

    st.session_state.current_question_index += 1
    next_index = st.session_state.current_question_index

    if next_index < len(questions):
        next_question = questions[next_index]["question"]
        st.session_state.chat_history.append({"role": "assistant", "content": next_question})
    else:
        summary = "Thank you for providing all the information. Here is a summary of your intake:"
        json_output = json.dumps(st.session_state.lead_data, indent=2)
        final_message = f"{summary}\n```json\n{json_output}\n```"
        st.session_state.chat_history.append({"role": "assistant", "content": final_message})

        email_subject = f"New Client Intake: {st.session_state.selected_specialty}"
        email_body = f"A new client has completed the intake process for {st.session_state.selected_specialty}. Below is the summary of their information:\n\n{json_output}"

        if send_email(email_subject, email_body):
            st.session_state.chat_history.append({"role": "assistant", "content": "Your information has been securely sent to the legal team. They will review your case and get back to you shortly."})
        else:
            st.session_state.chat_history.append({"role": "assistant", "content": "There was an issue sending your information to the legal team. Please copy the summary above and send it to them directly."})


if __name__ == "__main__":
    main()
