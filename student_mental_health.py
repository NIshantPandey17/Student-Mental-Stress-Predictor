import streamlit as st
import pickle
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# Load model
@st.cache_data
def load_model():
    try:
        with open("student_stress_model.pkl", "rb") as f:
            model = pickle.load(f)
        return model
    except FileNotFoundError:
        st.error("Model file not found. Please ensure 'student_stress_model.pkl' is in the same directory.")
        return None

# Recreate the label encoder manually
from sklearn.preprocessing import LabelEncoder
@st.cache_data
def create_label_encoder():
    le = LabelEncoder()
    le.fit(["High", "Medium", "Low"])
    return le

model = load_model()
le = create_label_encoder()

# Page configuration
st.set_page_config(
    page_title="Student Mental Health Detector", 
    page_icon="🧠", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Enhanced CSS for better visibility and UX
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
    
    /* Main app styling with softer background */
        .stApp {
        background: linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%);
        font-family: 'Inter', sans-serif;
        min-height: 100vh;
    }
    
    /* Main container with better contrast */
    .main .block-container {
        background-color: rgba(255, 255, 255, 0.95);
        backdrop-filter: blur(20px);
        border-radius: 20px;
        padding: 2.5rem;
        margin-top: 1rem;
        box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(255, 255, 255, 0.2);
    }
    
    /* Header styling with better contrast */
        .main-header {
        text-align: center;
        padding: 3rem 2rem;
        background: linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%);
        border: 5px solid #e2e8f0;
        margin-bottom: 2rem;
        color: #f0f0f0;  /* light gray/near white text */
        box-shadow: 0 8px 20px rgba(44, 62, 80, 0.6);  /* softer shadow */
    }
    
    .main-header h1 {
        margin-bottom: 0.5rem;
        font-weight: 700;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .main-header p {
        margin: 0;
        opacity: 0.9;
        font-weight: 800;
        
    }
    
    /* Section headers with dark text for contrast */
    .section-header {
        color: #2d3748 !important;
        font-weight: 600;
        margin-bottom: 1.5rem;
        padding-bottom: 0.5rem;
        border-bottom: 3px solid #667eea;
    }
    
    /* Enhanced metric cards */
    .metric-card {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        color: #2d3748;
        padding: 1.5rem;
        border-radius: 15px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
    }
    
    /* Recommendation boxes with better readability */
    .recommendation-box {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        color: #2d3748;
        padding: 2rem;
        border-radius: 20px;
        border: 1px solid #e2e8f0;
        margin: 1.5rem 0;
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.08);
        position: relative;
        overflow: hidden;
    }
    
    .recommendation-box::before {
        content: '';
        position: absolute;
        left: 0;
        top: 0;
        width: 5px;
        height: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    }
    
    .recommendation-box h4 {
        color: #1a202c !important;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .recommendation-box ul li {
        color: #4a5568 !important;
        margin-bottom: 0.5rem;
        line-height: 1.6;
    }
    
    .recommendation-box p {
        color: #2d3748 !important;
        line-height: 1.6;
    }
    
    /* Sidebar improvements */
    .sidebar-info {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        color: #2d3748;
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
    }
    
    .sidebar-info h4 {
        color: #1a202c !important;
        font-weight: 600;
        margin-bottom: 1rem;
    }
    
    .sidebar-info ol li {
        color: #4a5568 !important;
        margin-bottom: 0.5rem;
        line-height: 1.6;
    }
    
    /* Enhanced wellness tip */
        .wellness-tip {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        color: #2d3748;  /* dark text for readability */
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.05);
        border: 1px solid #e2e8f0;
    }

    
    .wellness-tip strong {
        color: #2d3748;
    }
    
    /* Sidebar styling */
        section[data-testid="stSidebar"] {
        background: linear-gradient(135deg, #f0f4f8 0%, #d9e2ec 100%);
        backdrop-filter: blur(20px);
        border-right: 1px solid rgba(255, 255, 255, 0.2);
    }

    
    /* Enhanced button styling */
    .stButton > button {
        width: 100%;
        height: 3.5rem;
        font-size: 18px;
        font-weight: 600;
        border-radius: 15px;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border: none;
        color: white;
        transition: all 0.3s ease;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
        letter-spacing: 0.5px;
    }
    
    .stButton > button:hover {
        transform: translateY(-3px);
        box-shadow: 0 15px 40px rgba(102, 126, 234, 0.4);
        background: linear-gradient(135deg, #5a67d8 0%, #6b46c1 100%);
    }
    
    /* Input field improvements */
    .stSelectbox > div > div {
        background-color: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        color: #2d3748;
        transition: border-color 0.2s ease;
    }
    
    .stSelectbox > div > div:focus-within {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stNumberInput > div > div > input {
        background-color: #ffffff;
        border: 2px solid #e2e8f0;
        border-radius: 10px;
        color: #2d3748;
        font-weight: 500;
    }
    
    .stNumberInput > div > div > input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stRadio > div {
        background: linear-gradient(135deg, #2c3e50 0%, #4ca1af 100%);
        border: 2px solid #e2e8f0;
        border-radius: 15px;
        padding: 0.5rem;
    }
    
    .stSlider > div > div > div {
        background-color: #f7fafc;
        border-radius: 10px;
        padding: 0.4rem;
        border: 1px solid #e2e8f0;
    }
    
    /* Text styling with better contrast */
    .stMarkdown h1, .stMarkdown h2 {
        color: #1a202c !important;
        font-weight: 700;
        text-shadow: none;
    }
    
    .stMarkdown h3, .stMarkdown h4 {
        color: #2d3748 !important;
        font-weight: 600;
        text-shadow: none;
    }
    
    .stMarkdown p {
        color: #4a5568 !important;
        text-shadow: none;
        line-height: 1.6;
    }
    
    /* Enhanced metric styling */
    [data-testid="metric-container"] {
        background: linear-gradient(135deg, #ffffff 0%, #f8fafc 100%);
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 10px 30px rgba(0, 0, 0, 0.08);
        border: 1px solid #e2e8f0;
        transition: transform 0.2s ease;
    }
    
    [data-testid="metric-container"]:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px rgba(0, 0, 0, 0.12);
    }
    
    [data-testid="metric-container"] > div {
        color: #2d3748 !important;
    }
    
    [data-testid="metric-container"] [data-testid="metric-value"] {
        color: #667eea !important;
        font-weight: 700;
    }
    
   
    
    /* Loading spinner */
    .stSpinner {
        text-align: center;
    }
    
    /* Divider styling */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(90deg, transparent, #e2e8f0, transparent);
        margin: 2rem 0;
    }
    
    /* Footer styling */
    .footer-text {
        text-align: center;
        color: #718096 !important;
        padding: 2rem;
        background: #f7fafc;
        border-radius: 15px;
        margin-top: 2rem;
    }
    
    .footer-text p {
        color: #718096 !important;
        margin-bottom: 0.5rem;
    }
    
    .footer-text small {
        color: #a0aec0 !important;
    }
    
    /* Responsive adjustments */
    @media (max-width: 768px) {
        .main .block-container {
            padding: 1.5rem;
        }
        
        .main-header {
            padding: 2rem 1rem;
        }
        
        .recommendation-box {
            padding: 1.5rem;
        }
        
    }
</style>
""", unsafe_allow_html=True)

# Header
st.markdown("""
<div class="main-header">
    <h1>🧠 Student Mental Health Detector</h1>
    <p style="font-size: 18px; margin: 0;">Understand your stress levels and get personalized recommendations</p>
</div>
""", unsafe_allow_html=True)

# Sidebar with information

st.sidebar.markdown('<h2 class="section-header">📋 Quick Guide</h2>', unsafe_allow_html=True)
st.sidebar.markdown("""
<div class="sidebar-info">
<h4>How it works:</h4>
<ol>
<li><strong>Input your data:</strong> Fill in your daily habits and lifestyle information</li>
<li><strong>Get prediction:</strong> Our AI model analyzes your inputs</li>
<li><strong>Receive recommendations:</strong> Get personalized tips to improve your mental health</li>
</ol>
</div>
""", unsafe_allow_html=True)

# Add some wellness tips in sidebar
st.sidebar.markdown('<h2 class="section-header">💡 Daily Wellness Tips</h2>', unsafe_allow_html=True)
wellness_tips = [
    "💤 Aim for 7-9 hours of sleep daily",
    "🏃‍♂️ Exercise for at least 30 minutes, 3 times per week",
    "📚 Take breaks every 50 minutes while studying",
    "👥 Stay connected with friends and family",
    "🧘‍♂️ Practice mindfulness or meditation",
    "📱 Limit screen time before bedtime"
]
tip_of_day = wellness_tips[datetime.now().day % len(wellness_tips)]
st.sidebar.markdown(f"""
<div class="wellness-tip">
<strong>💫 Tip of the Day:</strong><br>
{tip_of_day}
</div>
""", unsafe_allow_html=True)

# Main content area
col1, col2 = st.columns([2, 1])
with col1:
    st.markdown('<h2 class="section-header">📊 Personal Information</h2>', unsafe_allow_html=True)
    
    # --- Combine all inputs in a single column ---
    age = st.number_input(
        "What's your age?", 
        min_value=17, 
        max_value=25, 
        value=20,
        help="Your current age (between 17-25 years)"
    )

    social_support = st.radio(
        "Do you have reliable social support? (family, friends, counselors)",
        ["Yes", "No"],
        help="Social support includes having people you can talk to about your problems"
    )

    sleep = st.slider(
        "💤 Sleep Hours (per day)", 
        1, 10, 7,
        help="Average hours of sleep you get per night"
    )

    study = st.slider(
        "📚 Study Hours (per day)", 
        1, 10, 4,
        help="Hours spent studying or doing academic work daily"
    )

    screen = st.slider(
        "📱 Screen Time (hours per day)", 
        1, 12, 6,
        help="Total time spent on phones, computers, TV, etc."
    )

    exercise = st.slider(
        "🏃‍♂️ Exercise (times per week)", 
        0, 7, 2,
        help="Number of times you engage in physical exercise per week"
    )


with col2:
    st.markdown('<h2 class="section-header">📈 Your Health Metrics</h2>', unsafe_allow_html=True)
    
    # Display current inputs as metrics
    st.metric("Age", f"{age} years")
    st.metric("Social Support", "Yes ❤️" if social_support == "Yes" else "Limited 💙")
    st.metric("Sleep Quality", "Good ✅" if sleep >= 7 else "Needs Improvement ⚠️")
    st.metric("Study-Life Balance", "Balanced ⚖️" if study <= 6 else "High Study Load 📚")
    st.metric("Screen Time", "Moderate 📱" if screen <= 8 else "High ⚠️")
    st.metric("Exercise Level", "Active 💪" if exercise >= 3 else "Low Activity 🚶‍♂️")
    

# Prediction section
st.markdown("---")
st.markdown('<h2 class="section-header">🔮 Stress Level Prediction</h2>', unsafe_allow_html=True)

if model is not None:
    # Convert social support to numeric
    social_support_val = 1 if social_support == "Yes" else 0
    
    if st.button("🔍 Analyze My Mental Health"):
        with st.spinner("Analyzing your data..."):
            # Add a small delay for better UX
            import time
            time.sleep(1)
            
            features = np.array([[age, sleep, study, screen, exercise, social_support_val]])
            prediction = model.predict(features)[0]
            stress_label = le.inverse_transform([prediction])[0]
            
            # Create visualization
            col1, col2, col3 = st.columns([1, 2, 1])
            
            with col2:
                # Stress level gauge
                if stress_label == "High":
                    color = "#ff4757"
                    emoji = "🔴"
                    score = 85
                elif stress_label == "Medium":
                    color = "#ffa502"
                    emoji = "🟡"
                    score = 50
                else:
                    color = "#2ed573"
                    emoji = "🟢"
                    score = 15
                
                fig = go.Figure(go.Indicator(
                    mode = "gauge+number+delta",
                    value = score,
                    domain = {'x': [0, 1], 'y': [0, 1]},
                    title = {'text': "Stress Level", 'font': {'size': 20, 'color': '#2d3748'}},
                    gauge = {
                        'axis': {'range': [None, 100], 'tickcolor': '#4a5568'},
                        'bar': {'color': color, 'thickness': 0.8},
                        'steps': [
                            {'range': [0, 30], 'color': "#e6ffed"},
                            {'range': [30, 70], 'color': "#fff3cd"},
                            {'range': [70, 100], 'color': "#ffe6e6"}
                        ],
                        'threshold': {
                            'line': {'color': color, 'width': 4},
                            'thickness': 0.75,
                            'value': score
                        }
                    }
                ))
                fig.update_layout(
                    height=300,
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    font={'color': '#2d3748'}
                )
                st.plotly_chart(fig, use_container_width=True)
            
            st.markdown(f'<h3 style="text-align: center; color: #2d3748;">{emoji} Predicted Stress Level: <span style="color: {color}; font-weight: 700;">{stress_label}</span></h3>', unsafe_allow_html=True)
            
            # Recommendations based on prediction
            st.markdown('<h2 class="section-header">💡 Personalized Recommendations</h2>', unsafe_allow_html=True)
            
            if stress_label == "High":
                st.markdown("""
                <div class="recommendation-box">
                <h4>🚨 High Stress Level Detected</h4>
                <p><strong>Immediate Actions Needed:</strong></p>
                <ul>
                    <li>🛌 <strong>Prioritize Sleep:</strong> Aim for 7-9 hours of quality sleep each night</li>
                    <li>📱 <strong>Reduce Screen Time:</strong> Limit recreational screen time, especially 2 hours before bed</li>
                    <li>🧘‍♂️ <strong>Practice Relaxation:</strong> Try deep breathing exercises, meditation, or yoga daily</li>
                    <li>👥 <strong>Seek Support:</strong> Talk to friends, family, or consider speaking with a counselor</li>
                    <li>📚 <strong>Study Smart:</strong> Take 15-minute breaks every hour while studying</li>
                    <li>🏃‍♂️ <strong>Move Your Body:</strong> Even a 10-minute walk can help reduce stress</li>
                </ul>
                <p><strong>⚠️ Important:</strong> Consider speaking with a mental health professional if stress persists or interferes with daily activities.</p>
                </div>
                """, unsafe_allow_html=True)
                
            elif stress_label == "Medium":
                st.markdown("""
                <div class="recommendation-box">
                <h4>⚖️ Moderate Stress Level</h4>
                <p><strong>Areas for Improvement:</strong></p>
                <ul>
                    <li>💤 <strong>Sleep Optimization:</strong> Maintain a consistent sleep schedule and create a relaxing bedtime routine</li>
                    <li>🏃‍♂️ <strong>Increase Physical Activity:</strong> Add 2-3 more exercise sessions per week</li>
                    <li>⏱️ <strong>Time Management:</strong> Use techniques like the Pomodoro method for better study-life balance</li>
                    <li>📱 <strong>Digital Wellness:</strong> Set specific hours for screen time and stick to them</li>
                    <li>🤝 <strong>Social Connection:</strong> Schedule regular time with supportive friends and family</li>
                    <li>🎯 <strong>Set Priorities:</strong> Focus on what's most important and let go of perfectionism</li>
                </ul>
                <p><strong>💡 Tip:</strong> You're on the right track! Small, consistent changes can make a big difference.</p>
                </div>
                """, unsafe_allow_html=True)
                
            else:
                st.markdown("""
                <div class="recommendation-box">
                <h4>✅ Low Stress Level - Excellent Work!</h4>
                <p><strong>Keep up the great habits:</strong></p>
                <ul>
                    <li>🎯 <strong>Maintain Balance:</strong> Continue your healthy lifestyle patterns</li>
                    <li>💪 <strong>Build Resilience:</strong> Develop additional coping strategies for future challenges</li>
                    <li>📈 <strong>Monitor Changes:</strong> Stay aware of your stress levels as circumstances change</li>
                    <li>🤝 <strong>Support Others:</strong> Share your healthy habits and strategies with friends</li>
                    <li>🎉 <strong>Celebrate Success:</strong> Acknowledge and reward yourself for maintaining good mental health</li>
                    <li>🧠 <strong>Keep Learning:</strong> Continue exploring stress management and wellness techniques</li>
                </ul>
                <p><strong>🌟 Great job!</strong> You're a role model for healthy student life balance.</p>
                </div>
                """, unsafe_allow_html=True)
            
            # Lifestyle Analysis Chart
            st.markdown('<h3 class="section-header">📊 Your Lifestyle Analysis</h3>', unsafe_allow_html=True)
            
            categories = ['Sleep Quality', 'Study Balance', 'Screen Time', 'Exercise', 'Social Support']
            scores = [
                min(sleep / 8 * 100, 100),  # Sleep score
                max(0, 100 - (study - 4) * 15),  # Study balance (optimal around 4-5 hours)
                max(0, 100 - (screen - 4) * 10),  # Screen time (lower is better)
                min(exercise / 4 * 100, 100),  # Exercise score
                social_support_val * 100  # Social support
            ]
            
            fig_radar = go.Figure()
            fig_radar.add_trace(go.Scatterpolar(
                r=scores,
                theta=categories,
                fill='toself',
                name='Your Profile',
                line_color='#667eea',
                fillcolor='rgba(102, 126, 234, 0.2)'
            ))
            
            fig_radar.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100],
                        tickfont={'color': '#4a5568'},
                        gridcolor='#e2e8f0'
                    ),
                    angularaxis=dict(
                        tickfont={'color': '#2d3748'}
                    )
                ),
                showlegend=True,
                title={
                    'text': "Personal Wellness Profile",
                    'x': 0.5,
                    'font': {'size': 20, 'color': '#2d3748'}
                },
                height=500,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font={'color': '#2d3748'}
            )
            
            st.plotly_chart(fig_radar, use_container_width=True)

# Footer
st.markdown("---")
st.markdown("""
<div class="footer-text">
    <p><strong>💝 Take care of your mental health - it's just as important as your physical health!</strong></p>
    <p><small>This tool provides general guidance and should not replace professional medical advice. If you're experiencing persistent stress or mental health concerns, please consult with a qualified healthcare professional.</small></p>
</div>
""", unsafe_allow_html=True)