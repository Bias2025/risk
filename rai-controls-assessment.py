#!/usr/bin/env python3
"""
AI Development Readiness Assessment Tool
A comprehensive web-based application for evaluating organizational readiness 
in implementing responsible AI practices across software development lifecycle.

Version: 2.0
Author: HCLTech Engineering Progress Team
License: Proprietary
"""

# =============================================================================
# IMPORTS
# =============================================================================

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np
from math import pi
import base64
from typing import Dict, List, Any, Optional

# =============================================================================
# CONFIGURATION
# =============================================================================

# Page configuration
st.set_page_config(
    page_title="AI Development Readiness Assessment",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =============================================================================
# STYLING
# =============================================================================

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
    
    /* Readiness level styling */
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

# =============================================================================
# DATA MODELS
# =============================================================================

# Assessment data structure - Hybrid approach: Tenets with Controls implementation
ASSESSMENT_DATA: Dict[str, Dict[str, Any]] = {
    "Fairness Tenet": {
        "description": "Ensuring AI systems treat all individuals and groups equitably, preventing bias and discrimination in software development processes and AI-generated code.",
        "tenet": "Fairness",
        "hover_description": "Ensures AI development tools and generated code treat all users and groups equitably, preventing discriminatory outcomes through bias monitoring, algorithmic auditing, and fairness-aware development practices.",
        "control_categories": ["Governance Controls", "Technical Controls"],
        "questions": [
            {
                "text": "How does your development team evaluate AI coding assistants and generated code for bias across different user demographics and use cases in your software applications?",
                "control_focus": "Governance & Technical Controls",
                "options": [
                    {"text": "We conduct comprehensive bias testing of AI-generated code with diverse test scenarios and regular algorithmic audits across multiple demographic dimensions", "risk": 0},
                    {"text": "We perform basic bias checks on AI-generated code during development but lack systematic ongoing monitoring", "risk": 1},
                    {"text": "We rely on AI tool vendor assurances and have not implemented specific bias evaluation processes for generated code", "risk": 2}
                ]
            },
            {
                "text": "What processes ensure that AI-assisted software development produces equitable outcomes when your applications make decisions affecting different user groups?",
                "control_focus": "Operational & Transparency Controls",
                "options": [
                    {"text": "We have established fairness metrics for AI-generated features, regular impact assessments, and corrective mechanisms for disparate outcomes in our applications", "risk": 0},
                    {"text": "We monitor some application outcomes but lack formal processes for addressing inequitable treatment in AI-assisted development", "risk": 1},
                    {"text": "We have not implemented specific measures to ensure equitable outcomes from AI-assisted software development", "risk": 2}
                ]
            }
        ]
    },
    "Privacy Tenet": {
        "description": "Protecting personal data and sensitive information through comprehensive privacy controls in AI-assisted development workflows and code generation processes.",
        "tenet": "Privacy",
        "hover_description": "Protects personal data and sensitive information in development environments through privacy-by-design principles, secure coding practices, and comprehensive privacy controls for AI tools.",
        "control_categories": ["Technical Controls", "Operational Controls", "Transparency Controls"],
        "questions": [
            {
                "text": "How do you prevent AI coding assistants from accessing, learning from, or exposing sensitive data, personal information, or proprietary code during development?",
                "control_focus": "Technical & Operational Controls",
                "options": [
                    {"text": "We implement strict data isolation, code sanitization before AI processing, automated PII detection, and privacy-preserving development environments with comprehensive access controls", "risk": 0},
                    {"text": "We limit AI tool access to certain code repositories but lack comprehensive privacy-preserving techniques and automated data protection", "risk": 1},
                    {"text": "We use AI coding tools without specific controls to prevent exposure of sensitive data or proprietary information", "risk": 2}
                ]
            },
            {
                "text": "What measures ensure compliance with data protection regulations when using AI tools in software development and deployment pipelines?",
                "control_focus": "Operational & Transparency Controls",
                "options": [
                    {"text": "We have automated compliance checking in CI/CD pipelines, clear data handling policies for AI tools, and comprehensive audit trails for all AI-assisted development activities", "risk": 0},
                    {"text": "We can track data usage in development but the compliance verification process is mostly manual and inconsistent", "risk": 1},
                    {"text": "We have limited capabilities to ensure regulatory compliance when using AI tools in our development processes", "risk": 2}
                ]
            }
        ]
    },
    "Security Tenet": {
        "description": "Protecting software development processes and AI-generated code from threats, vulnerabilities, and unauthorized access through robust technical safeguards and operational security controls.",
        "tenet": "Security",
        "hover_description": "Implements comprehensive security measures including secure coding practices for AI-generated code, vulnerability scanning, prompt injection protection, and continuous threat monitoring in development environments.",
        "control_categories": ["Technical Controls", "Operational Controls"],
        "questions": [
            {
                "text": "How do you protect your development environment and AI coding tools against prompt injection attacks, code poisoning, and unauthorized model access?",
                "control_focus": "Technical & Security Controls",
                "options": [
                    {"text": "We implement comprehensive prompt sanitization, input validation for AI tools, secure API configurations, code signing for AI-generated content, and regular security assessments of our AI development workflow", "risk": 0},
                    {"text": "We have basic input validation and some security testing but lack comprehensive protection against AI-specific development threats", "risk": 1},
                    {"text": "We rely primarily on standard cybersecurity measures without AI-specific threat protection in our development environment", "risk": 2}
                ]
            },
            {
                "text": "What controls ensure the security and integrity of AI-generated code before it's integrated into your software applications?",
                "control_focus": "Technical & Operational Controls",
                "options": [
                    {"text": "We implement automated security scanning of AI-generated code, vulnerability assessment tools, code review processes, and integrity verification with comprehensive testing before integration", "risk": 0},
                    {"text": "We review AI-generated code and run some security checks but lack comprehensive automated security validation", "risk": 1},
                    {"text": "We use AI-generated code with basic quality checks but no specific security or integrity validation measures", "risk": 2}
                ]
            }
        ]
    },
    "Transparency Tenet": {
        "description": "Ensuring AI-assisted development processes are explainable, interpretable, and their impact on software functionality is documented and communicated to relevant stakeholders.",
        "tenet": "Transparency",
        "hover_description": "Ensures AI development processes are explainable through comprehensive documentation, code attribution, development decision explanations, and transparency controls for AI tool usage.",
        "control_categories": ["Transparency Controls", "Operational Controls"],
        "questions": [
            {
                "text": "How do you provide visibility into which parts of your codebase were generated or modified by AI tools, and explain AI-assisted development decisions to your team?",
                "control_focus": "Technical & Transparency Controls",
                "options": [
                    {"text": "We provide comprehensive code attribution tracking, AI contribution documentation, decision explanations with confidence scores, and clear documentation of all AI-assisted development activities", "risk": 0},
                    {"text": "We track some AI-generated code contributions but lack comprehensive explainability and documentation across all development activities", "risk": 1},
                    {"text": "We provide limited or no tracking of AI contributions to our codebase and development decisions", "risk": 2}
                ]
            },
            {
                "text": "What documentation and disclosure practices do you maintain regarding AI tool usage, capabilities, limitations, and impact on your software development lifecycle?",
                "control_focus": "Transparency & Operational Controls",
                "options": [
                    {"text": "We maintain comprehensive AI tool documentation, development impact assessments, performance metrics, usage guidelines, and clear communication to stakeholders about AI assistance in our development process", "risk": 0},
                    {"text": "We document basic AI tool information but lack comprehensive transparency documentation about development impact", "risk": 1},
                    {"text": "We provide minimal documentation about AI tool capabilities, limitations, and their impact on our development process", "risk": 2}
                ]
            }
        ]
    },
    "Accountability Tenet": {
        "description": "Establishing clear governance frameworks, human oversight mechanisms, and responsibility structures for AI-assisted development outcomes and software quality.",
        "tenet": "Accountability",
        "hover_description": "Establishes clear governance, oversight, and responsibility frameworks through human-in-the-loop development processes, code quality monitoring, and accountability controls for AI-assisted development.",
        "control_categories": ["Governance Controls", "Operational Controls"],
        "questions": [
            {
                "text": "How do you establish and maintain human oversight and intervention capabilities for AI-assisted development decisions and code generation?",
                "control_focus": "Governance & Operational Controls",
                "options": [
                    {"text": "We have mandatory human code review processes, clear escalation procedures for AI-generated code, override capabilities, and trained oversight personnel for all critical development decisions involving AI", "risk": 0},
                    {"text": "We have human oversight for some AI-assisted development but lack comprehensive intervention capabilities and formal review processes", "risk": 1},
                    {"text": "We have limited human oversight and intervention mechanisms for AI-assisted development activities", "risk": 2}
                ]
            },
            {
                "text": "What monitoring and evaluation processes track the performance, quality, and impact of AI-assisted development on your software applications post-deployment?",
                "control_focus": "Operational & Monitoring Controls",
                "options": [
                    {"text": "We implement continuous monitoring of software quality metrics, AI contribution tracking, performance impact assessments, and systematic feedback loops with corrective actions for AI-assisted development", "risk": 0},
                    {"text": "We monitor technical performance metrics but have limited tracking of AI development impact and software quality correlation", "risk": 1},
                    {"text": "We have basic system monitoring but no specific processes for tracking the impact of AI-assisted development on software quality and performance", "risk": 2}
                ]
            }
        ]
    }
}

# Recommendations with regulatory alignment
RECOMMENDATIONS: List[Dict[str, str]] = [
    {
        "title": "Implement AI Development Governance Framework",
        "description": "Establish formal review processes for AI tool selection and AI-assisted development decisions. Create an AI development steering committee with representatives from development, security, and compliance teams to approve AI tool integrations before production use.",
        "sources": "Aligned with NIST AI RMF GOVERN function and EU AI Act Article 16 (Quality Management System)"
    },
    {
        "title": "Enhance Development Environment Security Controls",
        "description": "Implement comprehensive API security measures for AI tools including regular key rotation, encrypted communications, and detailed access logging. Deploy input validation and prompt sanitization to prevent injection attacks, and establish secure storage for AI tool configurations.",
        "sources": "Based on NIST AI RMF MANAGE function and EU AI Act Article 15 (Accuracy, Robustness and Cybersecurity)"
    },
    {
        "title": "Establish AI-Specific Code Review Protocols",
        "description": "Create multi-stage validation processes for AI-generated code including automated security scans, bias detection, vulnerability assessment, and mandatory human code review. Implement continuous monitoring of AI code contributions and establish baseline quality metrics.",
        "sources": "Supports NIST AI RMF MEASURE function and EU AI Act Article 14 (Human Oversight)"
    },
    {
        "title": "Develop AI Development Incident Response Plan",
        "description": "Create formal incident response procedures specifically for AI development failures including model hallucinations, prompt injection attempts, and unexpected code generation behaviors. Establish rollback capabilities and maintain audit trails of all AI development interactions.",
        "sources": "Implements NIST AI RMF MANAGE-2.4 and EU AI Act Article 62 (Reporting of Serious Incidents)"
    },
    {
        "title": "Improve AI Development Documentation and Transparency",
        "description": "Maintain comprehensive documentation of all AI tools used in development, including versions, training data sources, known limitations, and AI contribution tracking in code repositories. Establish regular third-party security assessments of AI development workflows.",
        "sources": "Addresses NIST AI RMF MAP function and EU AI Act Article 11 (Technical Documentation)"
    },
    {
        "title": "Implement Development Data Privacy and IP Protection",
        "description": "Deploy comprehensive data protection measures including PII detection in development environments, IP scanning for AI-generated code, and strict data handling agreements with AI service providers. Establish clear policies for handling sensitive information in AI development workflows.",
        "sources": "Complies with NIST AI RMF GOVERN-1.6 (Privacy) and EU AI Act Article 10 (Data and Data Governance)"
    }
]

# =============================================================================
# CORE FUNCTIONS
# =============================================================================

def initialize_session_state() -> None:
    """Initialize session state variables for the application."""
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    if 'current_category' not in st.session_state:
        st.session_state.current_category = 0
    if 'assessment_complete' not in st.session_state:
        st.session_state.assessment_complete = False

def calculate_readiness_level(responses: Dict[str, int]) -> Optional[Dict[str, Any]]:
    """
    Calculate overall readiness level based on responses.
    
    Args:
        responses: Dictionary of question responses with risk scores
        
    Returns:
        Dictionary with level, color, and percentage or None if no responses
    """
    if not responses:
        return None
    
    total_score = sum(responses.values())
    max_possible_score = len(responses) * 2
    readiness_percentage = ((max_possible_score - total_score) / max_possible_score) * 100
    
    if readiness_percentage >= 75:
        return {"level": "ADVANCED", "color": "#10b981", "percentage": readiness_percentage}
    elif readiness_percentage >= 50:
        return {"level": "DEVELOPING", "color": "#f59e0b", "percentage": readiness_percentage}
    else:
        return {"level": "BASIC", "color": "#ef4444", "percentage": readiness_percentage}

def create_radar_chart(responses: Dict[str, int]) -> go.Figure:
    """
    Create radar chart for responsible AI assessment results.
    
    Args:
        responses: Dictionary of question responses
        
    Returns:
        Plotly figure object for radar chart
    """
    categories = list(ASSESSMENT_DATA.keys())
    
    # Calculate average score for each category
    category_scores = []
    category_labels = []
    for i, category in enumerate(categories):
        category_responses = [responses.get(f"{i}_{j}", 0) for j in range(2)]
        avg_score = sum(category_responses) / len(category_responses) if category_responses else 0
        category_scores.append(avg_score)
        category_labels.append(ASSESSMENT_DATA[category]['tenet'])
    
    # Convert to performance scale (higher is better, inverted from risk)
    performance_scores = [(2 - score) / 2 * 100 for score in category_scores]
    
    # Add first point at the end to close the polygon
    performance_scores_closed = performance_scores + [performance_scores[0]]
    category_labels_closed = category_labels + [category_labels[0]]
    
    fig = go.Figure()
    
    # Add the main trace
    fig.add_trace(go.Scatterpolar(
        r=performance_scores_closed,
        theta=category_labels_closed,
        fill='toself',
        name='Readiness Score',
        line=dict(color='#3B82F6', width=3),
        fillcolor='rgba(59, 130, 246, 0.3)',
        hovertemplate='<b>%{theta}</b><br>Readiness: %{r:.1f}%<br>' +
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

def create_classification_levels_chart(responses: Dict[str, int]) -> List[Dict[str, Any]]:
    """
    Create classification levels visualization data.
    
    Args:
        responses: Dictionary of question responses
        
    Returns:
        List of dictionaries with category data for visualization
    """
    categories = ["Fairness", "Privacy", "Security", "Transparency", "Accountability"]
    
    # Calculate readiness levels for each category
    category_data = []
    for i, category in enumerate(categories):
        category_responses = [responses.get(f"{i}_{j}", 0) for j in range(2)]
        avg_score = sum(category_responses) / len(category_responses) if category_responses else 0
        
        # Get hover description from ASSESSMENT_DATA
        full_category_name = list(ASSESSMENT_DATA.keys())[i]
        hover_desc = ASSESSMENT_DATA[full_category_name]['hover_description']
        
        # Calculate readiness level (inverted from risk scoring)
        readiness_score = (2 - avg_score) / 2 * 100
        
        if readiness_score >= 75:
            level = "Advanced"
            position = 75
            color = "#10B981"  # Green
        elif readiness_score >= 50:
            level = "Developing"
            position = 50
            color = "#F59E0B"  # Orange
        else:
            level = "Basic"
            position = 25
            color = "#EF4444"  # Red
            
        category_data.append({
            "category": category,
            "level": level,
            "position": position,
            "color": color,
            "hover_description": hover_desc,
            "readiness_score": readiness_score
        })
    
    return category_data

# =============================================================================
# UI COMPONENTS
# =============================================================================

def display_header() -> None:
    """Display the header with HCL Tech branding."""
    st.markdown("""
    <div class="header-container">
        <div class="hcl-title">HCLTech | Engineering Progress</div>
        <div class="hcl-subtitle">AI Development Readiness Assessment</div>
        <p style="color: rgba(255, 255, 255, 0.7); margin-top: 1rem;">
            Assess and visualize your AI development readiness across software development lifecycle
        </p>
    </div>
    """, unsafe_allow_html=True)

def display_assessment_form() -> None:
    """Display the assessment form with hybrid tenet-controls approach."""
    categories = list(ASSESSMENT_DATA.keys())
    current_cat = categories[st.session_state.current_category]
    
    st.markdown(f"""
    <div class="assessment-card">
        <h2 style="color: #1f2937; margin-bottom: 1rem;">{current_cat}</h2>
        <p style="color: #6b7280; margin-bottom: 1rem;">{ASSESSMENT_DATA[current_cat]['description']}</p>
        <div style="background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px; margin-bottom: 1.5rem;">
            <strong style="color: #3b82f6;">Underlying Control Categories:</strong> 
            <span style="color: #6b7280;">{', '.join(ASSESSMENT_DATA[current_cat]['control_categories'])}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Display questions for current category
    for q_idx, question in enumerate(ASSESSMENT_DATA[current_cat]['questions']):
        st.markdown(f"""
        <div class="question-container">
            <h4 style="color: #374151; margin-bottom: 0.5rem;">Question {q_idx + 1}:</h4>
            <p style="color: #4b5563; margin-bottom: 1rem;">{question['text']}</p>
            <div style="background: rgba(107, 70, 193, 0.1); padding: 0.5rem; border-radius: 6px; margin-bottom: 1rem;">
                <small style="color: #6B46C1;"><strong>Control Focus:</strong> {question['control_focus']}</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        question_key = f"{st.session_state.current_category}_{q_idx}"
        
        # Radio button options
        selected_option = st.radio(
            "Select the option that best describes your current practices:",
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

def display_results() -> None:
    """Display the assessment results with visualizations."""
    readiness_result = calculate_readiness_level(st.session_state.responses)
    
    if not readiness_result:
        st.error("No assessment data available")
        return
    
    # Display readiness level
    readiness_class = f"risk-{readiness_result['level'].lower()}"
    if readiness_result['level'] == 'ADVANCED':
        readiness_class = "risk-low"
    elif readiness_result['level'] == 'DEVELOPING':
        readiness_class = "risk-medium"
    else:
        readiness_class = "risk-high"
        
    st.markdown(f"""
    <div class="{readiness_class}">
        🎯 AI Development Readiness Level: {readiness_result['level']} 
        ({readiness_result['percentage']:.1f}% Readiness Score)
    </div>
    """, unsafe_allow_html=True)
    
    # Summary Statistics Section
    category_data = create_classification_levels_chart(st.session_state.responses)
    
    advanced_count = sum(1 for cat in category_data if cat['level'] == 'Advanced')
    developing_count = sum(1 for cat in category_data if cat['level'] == 'Developing')
    basic_count = sum(1 for cat in category_data if cat['level'] == 'Basic')
    
    st.markdown("""
    <div class="risk-card" style="margin-bottom: 2rem;">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 1.8rem;">Summary Statistics</h2>
        <div style="display: flex; justify-content: space-around; margin-bottom: 2rem;">
            <div style="text-align: center;">
                <div style="font-size: 3rem; font-weight: bold; color: #10b981; margin-bottom: 0.5rem;">{}</div>
                <div style="color: rgba(255, 255, 255, 0.8); font-size: 1.1rem;">Advanced</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 3rem; font-weight: bold; color: #f59e0b; margin-bottom: 0.5rem;">{}</div>
                <div style="color: rgba(255, 255, 255, 0.8); font-size: 1.1rem;">Developing</div>
            </div>
            <div style="text-align: center;">
                <div style="font-size: 3rem; font-weight: bold; color: #ef4444; margin-bottom: 0.5rem;">{}</div>
                <div style="color: rgba(255, 255, 255, 0.8); font-size: 1.1rem;">Basic</div>
            </div>
        </div>
        <div style="border-top: 1px solid rgba(255, 255, 255, 0.2); padding-top: 1.5rem;">
            <div style="color: rgba(255, 255, 255, 0.8); margin-bottom: 0.5rem;">Overall Score</div>
            <div style="font-size: 2.5rem; font-weight: bold; color: #3b82f6;">{:.0f}%</div>
        </div>
    </div>
    """.format(advanced_count, developing_count, basic_count, readiness_result['percentage']), unsafe_allow_html=True)
    
    # Create two columns for visualizations
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="risk-card">
            <h3 style="color: white; margin-bottom: 1rem;">📊 Responsible AI Tenets</h3>
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
        
        for cat_data in category_data:
            st.markdown(f"""
            <div style="margin-bottom: 1rem;" title="{cat_data['hover_description']}">
                <div style="color: white; margin-bottom: 0.5rem; display: flex; align-items: center;">
                    <div style="width: 12px; height: 12px; background: {cat_data['color']}; border-radius: 50%; margin-right: 8px;"></div>
                    <span style="cursor: help;" title="Readiness Score: {cat_data['readiness_score']:.0f}% - {cat_data['hover_description']}">{cat_data['category']}</span>
                    <span style="margin-left: auto; font-weight: bold;" title="{cat_data['level']} Readiness Level">{cat_data['level']}</span>
                </div>
                <div style="background: rgba(255, 255, 255, 0.2); height: 8px; border-radius: 4px; overflow: hidden;" title="Readiness Level: {cat_data['readiness_score']:.0f}%">
                    <div style="background: {cat_data['color']}; height: 100%; width: {cat_data['position']}%; border-radius: 4px;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Tenet Descriptions Section
    st.markdown("""
    <div class="risk-card" style="margin: 2rem 0;">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 1.8rem;">Tenet Descriptions</h2>
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem;">
            <div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 10px; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">⚖️</div>
                <h3 style="color: white; margin-bottom: 1rem;">Fairness</h3>
                <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem;">Ensuring AI development tools and generated code treat all individuals and groups equitably, without bias or discrimination.</p>
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 10px; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">🔒</div>
                <h3 style="color: white; margin-bottom: 1rem;">Privacy</h3>
                <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem;">Protecting personal data and ensuring privacy throughout the AI-assisted development lifecycle.</p>
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 10px; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">👁️</div>
                <h3 style="color: white; margin-bottom: 1rem;">Transparency</h3>
                <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem;">Making AI development processes explainable and their impact on software functionality understandable.</p>
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 10px; text-align: center;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">📋</div>
                <h3 style="color: white; margin-bottom: 1rem;">Accountability</h3>
                <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem;">Establishing clear responsibility for AI-assisted development outcomes and software quality.</p>
            </div>
            <div style="background: rgba(255, 255, 255, 0.1); padding: 1.5rem; border-radius: 10px; text-align: center; grid-column: span 1;">
                <div style="font-size: 2rem; margin-bottom: 1rem;">🛡️</div>
                <h3 style="color: white; margin-bottom: 1rem;">Security</h3>
                <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem;">Protecting AI development tools and generated code from threats, attacks, and unauthorized access.</p>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Enhanced Recommended Actions Section
    st.markdown("""
    <div class="risk-card" style="margin: 2rem 0;">
        <h2 style="color: white; margin-bottom: 2rem; font-size: 1.8rem;">Recommended Actions</h2>
    """, unsafe_allow_html=True)
    
    # Immediate Actions (for Basic level tenets)
    basic_tenets = [cat for cat in category_data if cat['level'] == 'Basic']
    if basic_tenets:
        st.markdown("""
        <div style="margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                <div style="width: 12px; height: 12px; background: #ef4444; border-radius: 50%; margin-right: 8px;"></div>
                <h3 style="color: #ef4444; margin: 0; font-size: 1.4rem;">Immediate Actions Required (Basic Level)</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Define immediate actions for basic level tenets with control-based implementation
        immediate_actions = {
            "Fairness": {
                "icon": "⚖️",
                "tenet_focus": "Bias Prevention in AI Development & Code Generation",
                "control_implementation": {
                    "Governance Controls": [
                        "Establish AI development ethics committee with fairness accountability",
                        "Create formal bias review processes for all AI-generated code"
                    ],
                    "Technical Controls": [
                        "Deploy automated bias detection tools in development CI/CD pipeline",
                        "Implement demographic parity testing frameworks for AI-generated features"
                    ],
                    "Operational Controls": [
                        "Create fairness incident response procedures for development workflow",
                        "Establish regular fairness auditing schedule for AI tool usage"
                    ]
                },
                "standards": "EU AI Act Article 10 (Bias Monitoring), NIST RMF GOVERN-1.4"
            },
            "Privacy": {
                "icon": "🔒",
                "tenet_focus": "Data Protection in AI Development Environments",
                "control_implementation": {
                    "Technical Controls": [
                        "Implement data minimization and automated sanitization for AI tool inputs",
                        "Deploy privacy-preserving techniques (encryption, anonymization) in development"
                    ],
                    "Operational Controls": [
                        "Create secure development environment procedures for AI tool usage",
                        "Establish privacy impact assessment process for AI development activities"
                    ],
                    "Transparency Controls": [
                        "Implement clear data usage notifications for AI development tools",
                        "Create privacy policy disclosure mechanisms for development workflows"
                    ]
                },
                "standards": "EU AI Act Article 10 (Data Governance), NIST RMF GOVERN-1.6, GDPR"
            },
            "Security": {
                "icon": "🛡️",
                "tenet_focus": "AI Development Environment & Code Security",
                "control_implementation": {
                    "Technical Controls": [
                        "Implement AI-specific security controls and monitoring for development tools",
                        "Deploy prompt injection detection systems for development environments"
                    ],
                    "Operational Controls": [
                        "Create AI development security incident response procedures",
                        "Establish regular AI tool security assessment schedule"
                    ]
                },
                "standards": "OWASP AI Top 10, NIST RMF MANAGE-2.9, EU AI Act Article 15"
            },
            "Transparency": {
                "icon": "👁️",
                "tenet_focus": "AI Development Process Transparency & Code Attribution",
                "control_implementation": {
                    "Technical Controls": [
                        "Implement AI contribution tracking tools and code attribution systems",
                        "Deploy development decision logging and audit trail systems"
                    ],
                    "Transparency Controls": [
                        "Create AI tool documentation and development impact assessments",
                        "Implement stakeholder communication protocols for AI development usage"
                    ],
                    "Operational Controls": [
                        "Establish AI development explanation request handling procedures",
                        "Create development impact assessment processes for AI tool usage"
                    ]
                },
                "standards": "EU AI Act Article 13 (Transparency), NIST RMF MAP-5.1"
            },
            "Accountability": {
                "icon": "📋",
                "tenet_focus": "AI Development Oversight & Quality Responsibility",
                "control_implementation": {
                    "Governance Controls": [
                        "Establish clear AI development decision authority and escalation paths",
                        "Create AI development oversight committee with intervention powers"
                    ],
                    "Operational Controls": [
                        "Implement human-in-the-loop code review processes for AI-generated code",
                        "Deploy AI development performance monitoring dashboards"
                    ]
                },
                "standards": "EU AI Act Article 14 (Human Oversight), NIST RMF MANAGE-1.1"
            }
        }
        
        # Show immediate actions for basic level tenets
        for tenet in basic_tenets:
            tenet_name = tenet['category']
            if tenet_name in immediate_actions:
                action = immediate_actions[tenet_name]
                st.markdown(f"""
                <div style="margin: 1.5rem 0; padding: 1.5rem; background: rgba(239, 68, 68, 0.1); border-radius: 10px; border-left: 4px solid #ef4444;">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 1.5rem; margin-right: 0.5rem;">{action['icon']}</span>
                        <div>
                            <h4 style="color: #ef4444; margin: 0; font-size: 1.2rem;">{tenet_name} Tenet</h4>
                            <p style="color: rgba(255, 255, 255, 0.8); margin: 0.2rem 0 0 0; font-size: 0.9rem;">{action['tenet_focus']}</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Display control-based implementation
                for control_type, items in action['control_implementation'].items():
                    st.markdown(f"""
                    <div style="margin: 1rem 0; padding: 1rem; background: rgba(239, 68, 68, 0.05); border-radius: 8px;">
                        <h5 style="color: #ef4444; margin: 0 0 0.5rem 0; font-size: 1rem;">{control_type}</h5>
                        <ul style="color: rgba(255, 255, 255, 0.9); margin: 0; padding-left: 1.2rem;">
                    """, unsafe_allow_html=True)
                    
                    for item in items:
                        st.markdown(f"<li style='margin-bottom: 0.3rem; font-size: 0.9rem;'>{item}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="margin-top: 1rem; padding: 0.8rem; background: rgba(239, 68, 68, 0.2); border-radius: 6px;">
                        <strong style="color: #ef4444; font-size: 0.9rem;">Regulatory Compliance:</strong>
                        <span style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem;"> {action['standards']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                <div style="width: 12px; height: 12px; background: #ef4444; border-radius: 50%; margin-right: 8px;"></div>
                <h3 style="color: #ef4444; margin: 0; font-size: 1.4rem;">Immediate Actions Required (Basic Level)</h3>
            </div>
            <p style="color: rgba(255, 255, 255, 0.7); font-style: italic; margin-left: 20px;">
                No immediate actions required. All tenets are at developing or advanced levels.
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    # Recommended Improvements (for Developing level tenets)
    developing_tenets = [cat for cat in category_data if cat['level'] == 'Developing']
    if developing_tenets or basic_tenets:
        st.markdown("""
        <div style="margin-bottom: 2rem;">
            <div style="display: flex; align-items: center; margin-bottom: 1.5rem;">
                <div style="width: 12px; height: 12px; background: #f59e0b; border-radius: 50%; margin-right: 8px;"></div>
                <h3 style="color: #f59e0b; margin: 0; font-size: 1.4rem;">Recommended Improvements</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Define tenet-specific recommendations with control-based implementation
        tenet_recommendations = {
            "Fairness": {
                "icon": "⚖️",
                "tenet_focus": "Advanced Bias Prevention & Equity Assurance in Development",
                "control_implementation": {
                    "Governance Controls": [
                        "Establish comprehensive fairness governance framework for AI development",
                        "Implement regular fairness policy reviews and updates for development processes"
                    ],
                    "Technical Controls": [
                        "Deploy advanced bias detection and mitigation algorithms for AI-generated code",
                        "Implement continuous fairness monitoring systems for development workflows"
                    ],
                    "Operational Controls": [
                        "Create systematic fairness testing procedures for AI development outputs",
                        "Establish fairness performance benchmarking for AI tool effectiveness"
                    ]
                },
                "standards": "EU AI Act Article 10 (Bias Monitoring), NIST RMF GOVERN-1.4"
            },
            "Privacy": {
                "icon": "🔒",
                "tenet_focus": "Enhanced Data Protection & Privacy Engineering in Development",
                "control_implementation": {
                    "Technical Controls": [
                        "Implement advanced privacy-preserving techniques (differential privacy, federated learning) in development",
                        "Deploy automated privacy compliance monitoring for AI development activities"
                    ],
                    "Operational Controls": [
                        "Establish comprehensive privacy audit processes for AI development workflows",
                        "Create privacy-by-design development workflows for AI tool integration"
                    ],
                    "Transparency Controls": [
                        "Enhance developer consent and data usage transparency for AI tools",
                        "Implement comprehensive privacy policy management for development environments"
                    ]
                },
                "standards": "EU AI Act Article 10 (Data Governance), NIST RMF GOVERN-1.6, GDPR"
            },
            "Transparency": {
                "icon": "👁️",
                "tenet_focus": "Advanced AI Development Process Transparency & Code Explainability",
                "control_implementation": {
                    "Technical Controls": [
                        "Deploy advanced AI contribution tracking tools and code interpretation methods",
                        "Implement real-time development decision explanation systems"
                    ],
                    "Transparency Controls": [
                        "Create comprehensive development impact assessments for AI tool usage",
                        "Establish detailed AI development documentation standards"
                    ],
                    "Operational Controls": [
                        "Implement systematic transparency auditing processes for AI development",
                        "Create stakeholder explanation request workflows for AI development decisions"
                    ]
                },
                "standards": "EU AI Act Article 13 (Transparency), NIST RMF MAP-5.1"
            },
            "Accountability": {
                "icon": "📋",
                "tenet_focus": "Enhanced AI Development Oversight & Quality Management",
                "control_implementation": {
                    "Governance Controls": [
                        "Establish comprehensive AI development accountability frameworks",
                        "Implement advanced AI development governance committee structures"
                    ],
                    "Operational Controls": [
                        "Create systematic AI development performance review processes",
                        "Implement comprehensive AI development impact monitoring"
                    ],
                    "Transparency Controls": [
                        "Establish advanced stakeholder communication protocols for AI development",
                        "Create comprehensive AI development decision audit trails"
                    ]
                },
                "standards": "EU AI Act Article 14 (Human Oversight), NIST RMF MANAGE-1.1"
            },
            "Security": {
                "icon": "🛡️",
                "tenet_focus": "Advanced Threat Protection & Security Assurance in Development",
                "control_implementation": {
                    "Technical Controls": [
                        "Implement advanced adversarial attack protection systems for AI development tools",
                        "Deploy comprehensive AI development security monitoring tools"
                    ],
                    "Operational Controls": [
                        "Establish systematic AI development security assessment processes",
                        "Create advanced AI development threat response procedures"
                    ]
                },
                "standards": "OWASP AI Top 10, NIST RMF MANAGE-2.9, EU AI Act Article 15"
            }
        }
        
        # Show recommendations for tenets that need improvement
        improvement_needed = [cat['category'] for cat in category_data if cat['level'] in ['Developing', 'Basic']]
        
        for tenet_name in improvement_needed:
            if tenet_name in tenet_recommendations:
                rec = tenet_recommendations[tenet_name]
                st.markdown(f"""
                <div style="margin: 1.5rem 0; padding: 1.5rem; background: rgba(255, 255, 255, 0.05); border-radius: 10px; border-left: 4px solid #f59e0b;">
                    <div style="display: flex; align-items: center; margin-bottom: 1rem;">
                        <span style="font-size: 1.5rem; margin-right: 0.5rem;">{rec['icon']}</span>
                        <div>
                            <h4 style="color: #f59e0b; margin: 0; font-size: 1.2rem;">{tenet_name} Tenet</h4>
                            <p style="color: rgba(255, 255, 255, 0.8); margin: 0.2rem 0 0 0; font-size: 0.9rem;">{rec['tenet_focus']}</p>
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # Display control-based implementation
                for control_type, items in rec['control_implementation'].items():
                    st.markdown(f"""
                    <div style="margin: 1rem 0; padding: 1rem; background: rgba(245, 158, 11, 0.1); border-radius: 8px;">
                        <h5 style="color: #f59e0b; margin: 0 0 0.5rem 0; font-size: 1rem;">{control_type}</h5>
                        <ul style="color: rgba(255, 255, 255, 0.9); margin: 0; padding-left: 1.2rem;">
                    """, unsafe_allow_html=True)
                    
                    for item in items:
                        st.markdown(f"<li style='margin-bottom: 0.3rem; font-size: 0.9rem;'>{item}</li>", unsafe_allow_html=True)
                    
                    st.markdown("</ul></div>", unsafe_allow_html=True)
                
                st.markdown(f"""
                    <div style="margin-top: 1rem; padding: 0.8rem; background: rgba(59, 130, 246, 0.2); border-radius: 6px;">
                        <strong style="color: #3b82f6; font-size: 0.9rem;">Regulatory Alignment:</strong>
                        <span style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem;"> {rec['standards']}</span>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)  # Close recommended actions section
    
    # Implementation Roadmap
    if readiness_result['level'] in ['DEVELOPING', 'BASIC']:
        priority_text = (
            "Basic Readiness: Prioritize immediate implementation of fundamental controls across all basic-level tenets. Focus on establishing governance frameworks, technical safeguards, and operational procedures as foundational elements for AI development."
            if readiness_result['level'] == 'BASIC' else
            "Developing Readiness: Strengthen existing tenet foundations through enhanced control implementation. Systematically address gaps in developing-level tenets while maintaining current strengths in AI development practices."
        )
        
        st.markdown(f"""
        <div style="background: rgba(59, 130, 246, 0.2); border: 1px solid rgba(59, 130, 246, 0.4); padding: 1.5rem; border-radius: 10px; margin: 2rem 0;">
            <h4 style="color: #3b82f6; margin-bottom: 0.5rem;">🎯 Implementation Roadmap</h4>
            <p style="color: rgba(59, 130, 246, 0.9); font-size: 0.95rem; margin-bottom: 1rem;">{priority_text}</p>
            <div style="background: rgba(59, 130, 246, 0.1); padding: 1rem; border-radius: 8px;">
                <h5 style="color: #3b82f6; margin: 0 0 0.5rem 0; font-size: 1rem;">Hybrid Approach: Tenets → Controls → Implementation</h5>
                <p style="color: rgba(255, 255, 255, 0.8); font-size: 0.9rem; margin: 0;">
                    This assessment uses <strong>Responsible AI Tenets</strong> as the strategic framework while providing 
                    <strong>Control-based implementation</strong> guidance specifically for AI development practices. Each tenet maps to specific governance, 
                    technical, operational, and transparency controls for practical deployment in software development lifecycles.
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    # Reset button
    if st.button("🔄 Take Assessment Again"):
        # Clear all session state
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

def display_sidebar_progress() -> None:
    """Display assessment progress in the sidebar."""
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

# =============================================================================
# MAIN APPLICATION
# =============================================================================

def main() -> None:
    """Main application entry point."""
    try:
        # Initialize application
        initialize_session_state()
        display_header()
        
        # Display sidebar progress
        display_sidebar_progress()
        
        # Main content area
        if not st.session_state.assessment_complete:
            display_assessment_form()
        else:
            display_results()
            
    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.info("Please refresh the page to restart the assessment.")

# =============================================================================
# APPLICATION ENTRY POINT
# =============================================================================

if __name__ == "__main__":
    main()
