

# Create a virtual environment
python3 -m venv streamlit_env

# Activate the virtual environment
source streamlit_env/bin/activate

# Install dependencies
pip install streamlit plotly pandas numpy

# Run the application
streamlit run ai_risk_assessment.py





Visual Dashboard Elements (Similar to Screenshot)

Radar Chart: Pentagon-shaped visualization showing all 4 control categories
Classification Levels: Horizontal progress bars for each category with color coding
Risk Level Cards: Color-coded risk assessment results
Interactive Progress Tracking: Sidebar with real-time progress indicators

Assessment Structure

4 main categories with 2 questions each (8 total questions)
Risk-weighted scoring system (0=Low, 1=Medium, 2=High)
Progressive assessment flow with category-by-category navigation
Smart validation ensuring all questions are answered

Results Dashboard

Overall Risk Score: Color-coded HIGH/MEDIUM/LOW with percentage
Pillars Overview: Interactive radar chart showing strengths/weaknesses
Classification Levels: Category-specific risk bars with icons
5 Tailored Recommendations: For medium/high risk results with priority guidance

🚀 Installation & Usage
bash# Install dependencies
pip install streamlit plotly pandas numpy

# Run the application
streamlit run ai_risk_assessment.py
📊 Visual Elements

Heat Map Colors: Green (Low), Orange (Medium), Red (High) risk levels
Interactive Charts: Plotly-powered radar and progress visualizations
Responsive Design: Works on desktop and mobile devices
Real-time Updates: Dynamic progress tracking and instant results

The app provides a professional, enterprise-ready assessment tool that maintains the HCL Tech visual identity while delivering comprehensive AI risk evaluation for development teams using foundation models and automated processes in their SDLC.RetryClaude can make mistakes. Please double-check responses.

Visual Elements

Heat Map Colors: Green (Low), Orange (Medium), Red (High) risk levels
Interactive Charts: Plotly-powered radar and progress visualizations
Responsive Design: Works on desktop and mobile devices
Real-time Updates: Dynamic progress tracking and instant results