import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from math import pi
import base64

# Configure page
st.set_page_config(
    page_title="AI Development Risk Assessment",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with HCL Tech branding
st.markdown("""
<style>
    /* HCL Tech gradient background */
    .main {
        background: linear-gradient(135deg, #6B46C1 0%, #3B82F6 100%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #6B46C1 0%, #3B82F6 100%);
    }
    
    /* Header styling */
    .header-container {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .hcl-title {
        color: white;
        font-size: 3rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
    }
    
    .hcl-subtitle {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.2rem;
    }
    
    /* Card styling */
    .assessment-card {
        background: rgba(255, 255, 255, 0.95);
        padding: 2rem;
        border-radius: 15px;
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        margin-bottom: 1rem;
    }
    
    .risk-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 15px;
        margin-bottom: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Risk level styling */
    .risk-high {
        background: linear-gradient(135deg, #ef4444, #dc2626);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 1.5rem;
    }
    
    .risk-medium {
        background: linear-gradient(135deg, #f59e0b, #d97706);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 1.5rem;
    }
    
    .risk-low {
        background: linear-gradient(135deg, #10b981, #059669);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        font-weight: bold;
        font-size: 1.5rem;
    }
    
    /* Question styling */
    .question-container {
        background: #f8fafc;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #6B46C1;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #6B46C1, #3B82F6);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: bold;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(107, 70, 193, 0.4);
    }
    
    /* Recommendation cards */
    .recommendation-card {
        background: rgba(255, 255, 255, 0.1);
        backdrop-filter: blur(10px);
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        border-left: 4px solid #3B82F6;
        color: white;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background: rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Assessment data structure
ASSESSMENT_DATA = {
    "Governance & Oversight Controls": {
        "description": "Formal organizational structures and policy frameworks that establish human oversight mechanisms and decision protocols to ensure human accountability, ethical conduct, and risk management throughout AI development and deployment.",
        "tenet": "Governance",
        "hover_description": "Establishes accountability frameworks and decision-making processes for responsible AI development and deployment oversight.",
        "questions": [
            {
                "text": "Does your development team have established governance protocols for reviewing and approving AI model selections and prompt engineering decisions before production deployment?",
                "options": [
                    {"text": "Yes, we have formal review boards and documented approval processes", "risk": 0},
                    {"text": "Yes, but it's mostly informal peer review", "risk": 1},
                    {"text": "No, developers make these decisions independently", "risk": 2}
                ]
            },
            {
                "text": "How does your organization handle conflict of interest when selecting foundation models or AI services from vendors?",
                "options": [
                    {"text": "We have clear policies and disclosure requirements for vendor relationships", "risk": 0},
                    {"text": "We're aware of potential conflicts but don't have formal policies", "risk": 1},
                    {"text": "We haven't considered this as a potential issue", "risk": 2}
                ]
            }
        ]
    },
    "Technical & Security Controls": {
        "description": "Technical, physical, and engineering safeguards that secure AI systems and constrain model behaviors to ensure security, safety, alignment with human values, and content integrity.",
        "tenet": "Technical",
        "hover_description": "Implements security measures, model alignment techniques, and technical safeguards to ensure AI system integrity and safety.",
        "questions": [
            {
                "text": "What security measures do you implement when integrating foundation models and APIs into your SDLC pipeline?",
                "options": [
                    {"text": "API key rotation, encrypted communications, access logging, and secure prompt storage", "risk": 0},
                    {"text": "Basic API security but limited logging and monitoring", "risk": 1},
                    {"text": "Minimal security - mainly relying on vendor security", "risk": 2}
                ]
            },
            {
                "text": "How do you ensure model alignment and prevent prompt injection attacks in your automated development workflows?",
                "options": [
                    {"text": "Input validation, prompt sanitization, and output filtering with regular security testing", "risk": 0},
                    {"text": "Some input validation but limited prompt security measures", "risk": 1},
                    {"text": "We trust the foundation model's built-in safety measures", "risk": 2}
                ]
            }
        ]
    },
    "Operational Process Controls": {
        "description": "Processes and management frameworks governing AI system deployment, usage, monitoring, incident handling, and validation, which promote safety, security, and accountability throughout the system lifecycle.",
        "tenet": "Operational",
        "hover_description": "Manages AI system lifecycle processes including testing, monitoring, incident response, and continuous validation procedures.",
        "questions": [
            {
                "text": "What testing and validation processes do you have for AI-generated code and automated development outputs?",
                "options": [
                    {"text": "Multi-stage testing including unit tests, security scans, and human code review", "risk": 0},
                    {"text": "Standard testing but limited AI-specific validation", "risk": 1},
                    {"text": "Minimal testing - we mostly trust the AI outputs", "risk": 2}
                ]
            },
            {
                "text": "How do you monitor and respond to incidents involving AI model failures, data leakage or unexpected behaviors in your development pipeline?",
                "options": [
                    {"text": "Formal incident response plan with AI-specific procedures and rollback capabilities", "risk": 0},
                    {"text": "Informal incident handling with some monitoring in place", "risk": 1},
                    {"text": "We handle issues reactively as they arise", "risk": 2}
                ]
            }
        ]
    },
    "Transparency & Accountability Controls": {
        "description": "Formal disclosure practices and verification mechanisms that communicate AI system information and enable external scrutiny to build trust, facilitate oversight, and ensure accountability to users, regulators, and the public.",
        "tenet": "Transparency",
        "hover_description": "Ensures open communication about AI systems through documentation, disclosure practices, and external verification mechanisms.",
        "questions": [
            {
                "text": "How do you document and disclose the use of AI models and automated processes in your software development to stakeholders?",
                "options": [
                    {"text": "Detailed documentation including model versions, prompts used, and AI contribution tracking", "risk": 0},
                    {"text": "Basic documentation of AI tool usage but limited detail", "risk": 1},
                    {"text": "No specific documentation of AI usage in development", "risk": 2}
                ]
            },
            {
                "text": "What mechanisms do you have for external audit and verification of your AI-assisted development practices?",
                "options": [
                    {"text": "Regular third-party audits and compliance assessments", "risk": 0},
                    {"text": "Limited external review, mainly through client requirements", "risk": 1},
                    {"text": "No external audit mechanisms in place", "risk": 2}
                ]
            }
        ]
    },
    "Data Privacy & Protection Controls": {
        "description": "Safeguards and protocols that protect intellectual property, personal data, and sensitive information when using AI systems in development processes, ensuring compliance with privacy regulations and preventing unauthorized data exposure.",
        "tenet": "Privacy",
        "hover_description": "Protects intellectual property and personal data through comprehensive privacy controls and secure AI implementation practices.",
        "questions": [
            {
                "text": "What measures do you have in place to prevent intellectual property infringement when creating or using AI models for content generation and code development assistance?",
                "options": [
                    {"text": "Comprehensive IP scanning, license compliance checks, and legal review of AI-generated code", "risk": 0},
                    {"text": "Basic awareness of IP issues but limited systematic checking", "risk": 1},
                    {"text": "No specific IP protection measures for AI-generated content", "risk": 2}
                ]
            },
            {
                "text": "How do you handle personally identifiable information (PII) and sensitive data when using AI tools in your development and testing processes?",
                "options": [
                    {"text": "Data anonymization, PII detection tools, and strict data handling policies with AI providers", "risk": 0},
                    {"text": "Some PII protection measures but inconsistent application", "risk": 1},
                    {"text": "No specific PII protection protocols for AI tool usage", "risk": 2}
                ]
            }
        ]
    }
}

RECOMMENDATIONS = [
    {
        "title": "Implement AI Governance Framework",
        "description": "Establish formal review processes for AI model selection and prompt engineering decisions. Create an AI steering committee with representatives from development, security, and compliance teams to approve AI integrations before production deployment.",
        "sources": "Aligned with NIST AI RMF GOVERN function and EU AI Act Article 16 (Quality Management System)"
    },
    {
        "title": "Enhance Security Controls",
        "description": "Implement comprehensive API security measures including regular key rotation, encrypted communications, and detailed access logging. Deploy input validation and prompt sanitization to prevent injection attacks, and establish secure storage for prompt templates and AI configurations.",
        "sources": "Based on NIST AI RMF MANAGE function and EU AI Act Article 15 (Accuracy, Robustness and Cybersecurity)"
    },
    {
        "title": "Establish AI-Specific Testing Protocols",
        "description": "Create multi-stage validation processes for AI-generated code including automated security scans, bias detection, and mandatory human code review. Implement continuous monitoring of AI outputs and establish baseline performance metrics to detect model drift or degradation.",
        "sources": "Supports NIST AI RMF MEASURE function and EU AI Act Article 14 (Human Oversight)"
    },
    {
        "title": "Develop Incident Response Plan",
        "description": "Create formal incident response procedures specifically for AI-related failures including model hallucinations, prompt injection attempts, and unexpected behaviors. Establish rollback capabilities and maintain audit trails of all AI interactions for forensic analysis.",
        "sources": "Implements NIST AI RMF MANAGE-2.4 and EU AI Act Article 62 (Reporting of Serious Incidents)"
    },
    {
        "title": "Improve Documentation and Transparency",
        "description": "Maintain comprehensive documentation of all AI models used, including versions, training data sources, known limitations, and contribution tracking in code repositories. Establish regular third-party security assessments and create clear disclosure policies for stakeholders about AI usage in your development process.",
        "sources": "Addresses NIST AI RMF MAP function and EU AI Act Article 11 (Technical Documentation)"
    },
    {
        "title": "Implement Data Privacy and IP Protection",
        "description": "Deploy comprehensive data protection measures including PII detection and anonymization tools, IP scanning for AI-generated code, and strict data handling agreements with AI service providers. Establish clear policies for handling sensitive information in AI workflows and implement automated compliance monitoring.",
        "sources": "Complies with NIST AI RMF GOVERN-1.6 (Privacy) and EU AI Act Article 10 (Data and Data Governance)"
    }
]

def initialize_session_state():
    """Initialize session state variables"""
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    if 'current_category' not in st.session_state:
        st.session_state.current_category = 0
    if 'assessment_complete' not in st.session_state:
        st.session_state.assessment_complete = False

def calculate_risk_level(responses):
    """Calculate overall risk level based on responses"""
    if not responses:
        return None
    
    total_risk = sum(responses.values())
    max_possible_risk = len(responses) * 2
    risk_percentage = (total_risk / max_possible_risk) * 100
    
    if risk_percentage <= 25:
        return {"level": "LOW", "color": "#10b981", "percentage": risk_percentage}
    elif risk_percentage <= 60:
        return {"level": "MEDIUM", "color": "#f59e0b", "percentage": risk_percentage}
    else:
        return {"level": "HIGH", "color": "#ef4444", "percentage": risk_percentage}

def create_radar_chart(responses):
    """Create radar chart for risk assessment results"""
    categories = list(ASSESSMENT_DATA.keys())
    
    # Calculate average risk for each category
    category_risks = []
    category_labels = []
    for i, category in enumerate(categories):
        category_responses = [responses.get(f"{i}_{j}", 0) for j in range(2)]
        avg_risk = sum(category_responses) / len(category_responses) if category_responses else 0
        category_risks.append(avg_risk)
        category_labels.append(ASSESSMENT_DATA[category]['tenet'])
    
    # Convert to performance scale (higher is better, inverted from risk)
    performance_scores = [(2 - risk) / 2 * 100 for risk in category_risks]
    
    # Add first point at the end to close the polygon
    performance_scores_closed = performance_scores + [performance_scores[0]]
    category_labels_closed = category_labels + [category_labels[0]]
    
    fig = go.Figure()
    
    # Add the main trace
    fig.add_trace(go.Scatterpolar(
        r=performance_scores_closed,
        theta=category_labels_closed,
        fill='toself',
        name='Performance Score',
        line=dict(color='#3B82F6', width=3),
        fillcolor='rgba(59, 130, 246, 0.3)',
        hovertemplate='<b>%{theta}</b><br>Performance: %{r:.1f}%<br>' +
                     '<i>%{customdata}</i><extra></extra>',
        customdata=[ASSESSMENT_DATA[cat]['hover_description'] for cat in categories] + [ASSESSMENT_DATA[categories[0]]['hover_description']]
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                gridcolor='rgba(255, 255, 255, 0.3)',
                linecolor='rgba(255, 255, 255, 0.3)',
                tickfont=dict(color='white', size=10)
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.3)',
                linecolor='rgba(255, 255, 255, 0.3)',
                tickfont=dict(color='white', size=12, family='Arial Black')
            )
        ),
        showlegend=False,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=12),
        height=400,
        margin=dict(l=80, r=80, t=80, b=80)
    )
    
    return fig

def create_classification_levels_chart(responses):
    """Create classification levels visualization"""
    categories = ["Governance", "Technical", "Operational", "Transparency", "Privacy"]
    
    # Calculate risk levels for each category
    category_data = []
    for i, category in enumerate(categories):
        category_responses = [responses.get(f"{i}_{j}", 0) for j in range(2)]
        avg_risk = sum(category_responses) / len(category_responses) if category_responses else 0
        
        # Get hover description from ASSESSMENT_DATA
        full_category_name = list(ASSESSMENT_DATA.keys())[i]
        hover_desc = ASSESSMENT_DATA[full_category_name]['hover_description']
        
        # Fix the risk level calculation and positioning
        if avg_risk <= 0.5:
            level = "Low"
            position = 25
            color = "#10B981"  # Green
        elif avg_risk <= 1.5:
            level = "Medium"
            position = 50
            color = "#F59E0B"  # Orange
        else:
            level = "High"
            position = 75
            color = "#EF4444"  # Red
            
        category_data.append({
            "category": category,
            "level": level,
            "position": position,
            "color": color,
            "hover_description": hover_desc,
            "risk_score": avg_risk
        })
    
    return category_data

def display_header():
    """Display the header with HCL Tech branding"""
    st.markdown("""
    <div class="header-container">
        <div class="hcl-title">HCLTech | Engineering Progress</div>
        <div class="hcl-subtitle">AI Development Risk Assessment</div>
        <p style="color: rgba(255, 255, 255, 0.7); margin-top: 1rem;">
            Assess and visualize the key pillars of responsible AI implementation
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_assessment_form():
    """Display the assessment form"""
    categories = list(ASSESSMENT_DATA.keys())
    current_cat = categories[st.session_state.current_category]
    
    st.markdown(f"""
    <div class="assessment-card">
        <h2 style="color: #1f2937; margin-bottom: 1rem;">{current_cat}</h2>
        <p style="color: #6b7280; margin-bottom: 2rem;">{ASSESSMENT_DATA[current_cat]['description']}</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display questions for current category
    for q_idx, question in enumerate(ASSESSMENT_DATA[current_cat]['questions']):
        st.markdown(f"""
        <div class="question-container">
            <h4 style="color: #374151; margin-bottom: 1rem;">Question {q_idx + 1}:</h4>
            <p style="color: #4b5563; margin-bottom: 1rem;">{question['text']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        question_key = f"{st.session_state.current_category}_{q_idx}"
        
        # Radio button options
        selected_option = st.radio(
            "Select your answer:",
            options=range(len(question['options'])),
            format_func=lambda x: question['options'][x]['text'],
            key=f"q_{question_key}",
            index=st.session_state.responses.get(question_key, None)
        )
        
        if selected_option is not None:
            st.session_state.responses[question_key] = question['options'][selected_option]['risk']
    
    # Navigation buttons
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        if st.session_state.current_category > 0:
            if st.button("← Previous"):
                st.session_state.current_category -= 1
                st.rerun()
    
    with col3:
        if st.session_state.current_category < len(categories) - 1:
            # Check if all questions in current category are answered
            current_questions_answered = all(
                f"{st.session_state.current_category}_{q_idx}" in st.session_state.responses
                for q_idx in range(len(ASSESSMENT_DATA[current_cat]['questions']))
            )
            
            if current_questions_answered:
                if st.button("Next →"):
                    st.session_state.current_category += 1
                    st.rerun()
            else:
                st.button("Next →", disabled=True, help="Please answer all questions to continue")
        else:
            # Check if all questions are answered
            total_questions = sum(len(cat_data['questions']) for cat_data in ASSESSMENT_DATA.values())
            if len(st.session_state.responses) == total_questions:
                if st.button("View Results"):
                    st.session_state.assessment_complete = True
                    st.rerun()
            else:
                st.button("View Results", disabled=True, help="Please answer all questions to see results")

def display_results():
    """Display the assessment results with visualizations"""
    risk_result = calculate_risk_level(st.session_state.responses)
    
    if not risk_result:
        st.error("No assessment data available")
        return
    
    # Display risk level
    risk_class = f"risk-{risk_result['level'].lower()}"
    st.markdown(f"""
    <div class="{risk_class}">
        🎯 Overall Risk Level: {risk_result['level']} 
        ({risk_result['percentage']:.1f}% Risk Score)
    </div>
    """, unsafe_allow_html=True)
    
    # Create two columns for visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="risk-card">
            <h3 style="color: white; margin-bottom: 1rem;">📊 Tenets Overview</h3>
        </div>
        """, unsafe_allow_html=True)
        
        radar_fig = create_radar_chart(st.session_state.responses)
        st.plotly_chart(radar_fig, use_container_width=True, config={'displayModeBar': False})
    
    with col2:
        st.markdown("""
        <div class="risk-card">
            <h3 style="color: white; margin-bottom: 1rem;">📈 Classification Levels</h3>
        </div>
        """, unsafe_allow_html=True)
        
        category_data = create_classification_levels_chart(st.session_state.responses)
        
        for cat_data in category_data:
            st.markdown(f"""
            <div style="margin-bottom: 1rem;" title="{cat_data['hover_description']}">
                <div style="color: white; margin-bottom: 0.5rem; display: flex; align-items: center;">
                    <div style="width: 12px; height: 12px; background: {cat_data['color']}; border-radius: 50%; margin-right: 8px;"></div>
                    <span style="cursor: help;" title="Risk Score: {cat_data['risk_score']:.1f}/2.0 - {cat_data['hover_description']}">{cat_data['category']}</span>
                    <span style="margin-left: auto; font-weight: bold;" title="{cat_data['level']} Risk Level">{cat_data['level']}</span>
                </div>
                <div style="background: rgba(255, 255, 255, 0.2); height: 8px; border-radius: 4px; overflow: hidden;" title="Performance Level: {100 - (cat_data['risk_score']/2*100):.0f}%">
                    <div style="background: {cat_data['color']}; height: 100%; width: {cat_data['position']}%; border-radius: 4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Show recommendations if medium or high risk
    if risk_result['level'] in ['MEDIUM', 'HIGH']:
        st.markdown("""
        <div class="risk-card">
            <h3 style="color: white; margin-bottom: 1rem;">💡 Recommended Actions to Reduce Risk</h3>
        </div>
        """, unsafe_allow_html=True)
        
        for i, recommendation in enumerate(RECOMMENDATIONS, 1):
            st.markdown(f"""
            <div class="recommendation-card">
                <h4 style="color: white; margin-bottom: 0.5rem;">{i}. {recommendation['title']}</h4>
                <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem; margin-bottom: 0.5rem;">{recommendation['description']}</p>
                <p style="color: rgba(255, 255, 255, 0.6); font-size: 0.8rem; font-style: italic;"><strong>Sources:</strong> {recommendation['sources']}</p>
            </div>
            """, unsafe_allow_html=True)
        
        # Priority implementation guidance
        priority_text = (
            "High Risk: Implement recommendations 1, 2, and 4 immediately. These address critical governance and security gaps that could lead to significant incidents."
            if risk_result['level'] == 'HIGH' else
            "Medium Risk: Start with recommendations 1 and 3 to establish foundational controls, then gradually implement the remaining recommendations over the next quarter."
        )
        
        st.markdown(f"""
        <div style="background: rgba(251, 191, 36, 0.2); border: 1px solid rgba(251, 191, 36, 0.4); padding: 1rem; border-radius: 10px; margin-top: 1rem;">
            <h4 style="color: #fbbf24; margin-bottom: 0.5rem;">🎯 Priority Implementation</h4>
            <p style="color: rgba(251, 191, 36, 0.9); font-size: 0.9rem;">{priority_text}</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Reset button
    if st.button("🔄 Take Assessment Again"):
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def main():
    """Main application function"""
    initialize_session_state()
    display_header()
    
    # Sidebar with progress
    with st.sidebar:
        st.markdown("""
        <div style="color: white; padding: 1rem;">
            <h3>📊 Assessment Progress</h3>
        </div>
        """, unsafe_allow_html=True)
        
        categories = list(ASSESSMENT_DATA.keys())
        total_questions = sum(len(cat_data['questions']) for cat_data in ASSESSMENT_DATA.values())
        answered_questions = len(st.session_state.responses)
        
        progress = answered_questions / total_questions if total_questions > 0 else 0
        st.progress(progress)
        st.write(f"**{answered_questions}/{total_questions}** questions answered")
        
        st.markdown("---")
        
        # Category overview
        for i, category in enumerate(categories):
            cat_questions = len(ASSESSMENT_DATA[category]['questions'])
            cat_answered = sum(1 for q_idx in range(cat_questions) if f"{i}_{q_idx}" in st.session_state.responses)
            
            status = "✅" if cat_answered == cat_questions else "⏳" if cat_answered > 0 else "⭕"
            current_indicator = "👉" if i == st.session_state.current_category and not st.session_state.assessment_complete else ""
            
            st.write(f"{status} {current_indicator} **{category.split()[0]}** ({cat_answered}/{cat_questions})")
    
    # Main content area
    if not st.session_state.assessment_complete:
        display_assessment_form()
    else:
        display_results()

if __name__ == "__main__":
    main()
