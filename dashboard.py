"""
Middlesex County Livability Dashboard - Interactive Zip Code Analysis
Professional design with interpretations and insights
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
from streamlit_folium import st_folium
import numpy as np

# Page configuration
st.set_page_config(
    page_title="Middlesex County Livability Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🏘️"
)

# Custom CSS for beautiful design - DARK MODE COMPATIBLE
st.markdown("""
<style>
    /* Force light background for entire app */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    }
    
    .main {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%) !important;
    }
    
    /* Force light sidebar */
    [data-testid="stSidebar"] {
        background-color: #ffffff !important;
    }
    
    [data-testid="stSidebar"] > div:first-child {
        background-color: #ffffff !important;
    }
    
    /* Headers - Always dark text */
    h1 {
        color: #1e3a8a !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 700;
        text-align: center;
        padding: 20px 0;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
    }
    
    h2 {
        color: #1e40af !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 600;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 10px;
        margin-top: 30px;
    }
    
    h3 {
        color: #2563eb !important;
        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
        font-weight: 500;
    }
    
    /* Regular text - dark on light */
    p, div, span, label {
        color: #1f2937 !important;
    }
    
    /* Colored boxes keep white text */
    .success-box h4, .success-box p, .success-box strong, .success-box * {
        color: #ffffff !important;
    }
    
    .warning-box h4, .warning-box p, .warning-box strong, .warning-box * {
        color: #ffffff !important;
    }
    
    .neutral-box h4, .neutral-box p, .neutral-box strong, .neutral-box * {
        color: #ffffff !important;
    }
    
    .county-box * {
        color: #ffffff !important;
    }
    
    /* Info boxes */
    .success-box {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%) !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        margin: 20px 0;
    }
    
    .warning-box {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        margin: 20px 0;
    }
    
    .neutral-box {
        background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%) !important;
        padding: 20px;
        border-radius: 15px;
        box-shadow: 0 8px 16px rgba(0,0,0,0.2);
        margin: 20px 0;
    }
    
    /* County info box */
    .county-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 20px;
        text-align: center;
        font-size: 18px;
        font-weight: 600;
    }
    
    /* Metric styling - force light backgrounds */
    [data-testid="stMetric"] {
        background-color: #ffffff !important;
        padding: 15px !important;
        border-radius: 10px !important;
        border: 1px solid #e5e7eb !important;
    }
    
    [data-testid="stMetricValue"] {
        color: #1e40af !important;
        font-size: 24px !important;
        font-weight: 700 !important;
    }
    
    [data-testid="stMetricLabel"] {
        color: #4b5563 !important;
    }
    
    /* Tabs - Force light theme */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255,255,255,0.9) !important;
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        height: 50px;
        background-color: #ffffff !important;
        border-radius: 8px;
        color: #1e40af !important;
        font-weight: 600;
        border: 2px solid #e5e7eb !important;
    }
    
    .stTabs [aria-selected="true"] {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
        border: 2px solid #764ba2 !important;
    }
    
    .stTabs [aria-selected="true"] * {
        color: #ffffff !important;
    }
    
    /* Data tables - white background, dark text */
    .dataframe {
        background-color: #ffffff !important;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    
    .dataframe thead tr th {
        background-color: #f3f4f6 !important;
        color: #1f2937 !important;
        font-weight: 600 !important;
    }
    
    .dataframe tbody tr td {
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    /* Select boxes - force white background */
    .stSelectbox label {
        color: #1f2937 !important;
        font-weight: 500 !important;
    }
    
    .stSelectbox > div > div {
        background-color: #ffffff !important;
        border-radius: 8px;
        border: 2px solid #3b82f6 !important;
    }
    
    .stSelectbox [data-baseweb="select"] {
        background-color: #ffffff !important;
    }
    
    .stSelectbox [data-baseweb="select"] div {
        color: #1f2937 !important;
    }
    
    /* CRITICAL FIX: Dropdown menu popover - force white background and dark text */
    [data-baseweb="popover"] {
        background-color: #ffffff !important;
    }
    
    [data-baseweb="menu"] {
        background-color: #ffffff !important;
        border: 1px solid #e5e7eb !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15) !important;
    }
    
    [role="option"] {
        background-color: #ffffff !important;
        color: #1f2937 !important;
        padding: 10px 16px !important;
    }
    
    [role="option"]:hover {
        background-color: #f3f4f6 !important;
        color: #1f2937 !important;
    }
    
    [aria-selected="true"][role="option"] {
        background-color: #dbeafe !important;
        color: #1e40af !important;
        font-weight: 600 !important;
    }
    
    /* Dropdown list container */
    [data-baseweb="select"] [role="listbox"] {
        background-color: #ffffff !important;
        max-height: 300px !important;
    }
    
    [data-baseweb="select"] ul {
        background-color: #ffffff !important;
    }
    
    [data-baseweb="select"] li {
        background-color: #ffffff !important;
        color: #1f2937 !important;
        padding: 10px 16px !important;
    }
    
    [data-baseweb="select"] li:hover {
        background-color: #f3f4f6 !important;
        color: #1f2937 !important;
    }
    
    /* Multi-select */
    .stMultiSelect label {
        color: #1f2937 !important;
        font-weight: 500 !important;
    }
    
    .stMultiSelect > div {
        background-color: #ffffff !important;
        border: 2px solid #3b82f6 !important;
        border-radius: 8px;
    }
    
    .stMultiSelect [data-baseweb="tag"] {
        background-color: #3b82f6 !important;
    }
    
    .stMultiSelect [data-baseweb="tag"] * {
        color: #ffffff !important;
    }
    
    /* Multi-select dropdown */
    .stMultiSelect [data-baseweb="popover"] {
        background-color: #ffffff !important;
    }
    
    .stMultiSelect [role="option"] {
        background-color: #ffffff !important;
        color: #1f2937 !important;
    }
    
    .stMultiSelect [role="option"]:hover {
        background-color: #f3f4f6 !important;
    }
    
    /* Markdown in main area */
    .stMarkdown {
        color: #1f2937 !important;
    }
    
    /* Info/success/warning/error messages */
    .stAlert {
        background-color: #ffffff !important;
        border-radius: 8px !important;
    }
    
    /* Buttons */
    .stButton > button {
        background-color: #3b82f6 !important;
        color: #ffffff !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
    }
    
    .stButton > button:hover {
        background-color: #2563eb !important;
    }
    
    .stDownloadButton > button {
        background-color: #10b981 !important;
        color: #ffffff !important;
    }
    
    .stDownloadButton > button:hover {
        background-color: #059669 !important;
    }
    
    /* Plotly charts - white background */
    .js-plotly-plot {
        background-color: #ffffff !important;
        border-radius: 10px;
    }
    
    .plotly {
        background-color: #ffffff !important;
    }
    
    /* Custom metric cards in HTML */
    div[style*="background: white"] {
        background-color: #ffffff !important;
    }
    
    /* Footer styling */
    div[style*="text-align: center"][style*="background: white"] {
        background-color: #ffffff !important;
    }
    
    /* Sidebar markdown text */
    [data-testid="stSidebar"] .stMarkdown {
        color: #1f2937 !important;
    }
    
    [data-testid="stSidebar"] p {
        color: #1f2937 !important;
    }
    
    /* Widget labels in sidebar */
    [data-testid="stSidebar"] label {
        color: #1f2937 !important;
    }
</style>
""", unsafe_allow_html=True)

# Load data


@st.cache_data
def load_data():
    try:
        df = pd.read_csv('middlesex_data_real.csv')
        df['zip_code'] = df['zip_code'].astype(str)
        return df
    except FileNotFoundError:
        st.error("⚠️ Data file not found! Please run 'create_real_data.py' first.")
        st.stop()

# Calculate scores


def calculate_scores(df):
    df = df.copy()

    df['crime_score'] = 100 - ((df['crime_rate'] - df['crime_rate'].min()) /
                               (df['crime_rate'].max() - df['crime_rate'].min()) * 100)
    df['education_score'] = ((df['education_index'] - df['education_index'].min()) /
                             (df['education_index'].max() - df['education_index'].min()) * 100)
    df['jobs_score'] = 100 - ((df['unemployment_rate'] - df['unemployment_rate'].min()) /
                              (df['unemployment_rate'].max() - df['unemployment_rate'].min()) * 100)
    df['housing_score'] = 100 - ((df['housing_burden'] - df['housing_burden'].min()) /
                                 (df['housing_burden'].max() - df['housing_burden'].min()) * 100)
    df['transportation_score'] = 100 - ((df['transportation_index'] - df['transportation_index'].min()) /
                                        (df['transportation_index'].max() - df['transportation_index'].min()) * 100)

    weights = {'crime_score': 0.25, 'education_score': 0.25, 'jobs_score': 0.20,
               'housing_score': 0.20, 'transportation_score': 0.10}

    df['livability_score'] = (
        df['crime_score'] * weights['crime_score'] +
        df['education_score'] * weights['education_score'] +
        df['jobs_score'] * weights['jobs_score'] +
        df['housing_score'] * weights['housing_score'] +
        df['transportation_score'] * weights['transportation_score']
    )

    return df

# Interpretation functions


def interpret_score(score):
    if score >= 80:
        return "Excellent", "#10b981", "🌟"
    elif score >= 65:
        return "Good", "#3b82f6", "✅"
    elif score >= 50:
        return "Average", "#f59e0b", "⚠️"
    else:
        return "Needs Improvement", "#ef4444", "❌"


def get_percentile(value, series):
    return int((series < value).sum() / len(series) * 100)


def interpret_income(income):
    if income >= 150000:
        return "Very High Income - Top tier economic status"
    elif income >= 100000:
        return "High Income - Above average prosperity"
    elif income >= 75000:
        return "Upper Middle Income - Comfortable living"
    elif income >= 50000:
        return "Middle Income - Moderate economic status"
    else:
        return "Lower Income - Economic challenges present"


def interpret_education(pct):
    if pct >= 75:
        return "Highly Educated - Strong intellectual capital"
    elif pct >= 60:
        return "Well Educated - Above average educational attainment"
    elif pct >= 45:
        return "Moderately Educated - Average education levels"
    elif pct >= 30:
        return "Lower Education - Below average attainment"
    else:
        return "Low Education - Significant educational gaps"


def interpret_unemployment(rate):
    if rate <= 2.5:
        return "Excellent Job Market - Very low unemployment"
    elif rate <= 4.0:
        return "Strong Job Market - Healthy employment"
    elif rate <= 6.0:
        return "Moderate Job Market - Average unemployment"
    else:
        return "Weak Job Market - High unemployment challenges"


def interpret_housing(burden):
    if burden <= 28:
        return "Very Affordable - Low housing cost burden"
    elif burden <= 32:
        return "Affordable - Manageable housing costs"
    elif burden <= 38:
        return "Moderately Expensive - Above average costs"
    else:
        return "Expensive - High housing cost burden"


def interpret_commute(time):
    if time <= 23:
        return "Excellent - Very short commute"
    elif time <= 27:
        return "Good - Reasonable commute time"
    elif time <= 32:
        return "Average - Typical commute duration"
    else:
        return "Long - Extended commute time"


def interpret_crime(rate):
    if rate <= 7:
        return "Very Safe - Low crime area"
    elif rate <= 12:
        return "Safe - Below average crime"
    elif rate <= 18:
        return "Moderately Safe - Average crime levels"
    else:
        return "Higher Crime - Above average crime rates"


# Load data
df = load_data()
df = calculate_scores(df)

# Title
st.markdown("<h1>🏘️ Middlesex County, MA - Livability Dashboard</h1>",
            unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size: 18px; color: #1e40af;'><i>Comprehensive Analysis of Quality of Life Across 57 Zip Codes</i></p>", unsafe_allow_html=True)

# Sidebar - Zip Code Selector
with st.sidebar:
    st.markdown("## 🔍 Zip Code Selector")

    # County info box
    st.markdown(f"""
    <div class='county-box'>
        📍 Middlesex County, MA<br>
        <span style='font-size: 14px;'>{len(df)} zip codes available</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    # STEP 1: Select City (optional filter)
    st.markdown("**Filter by City (Optional):**")
    available_cities = ['All Cities'] + sorted(df['city'].unique().tolist())
    selected_city = st.selectbox(
        "Choose a city within Middlesex County:",
        available_cities,
        index=0,
        key='city_selector'
    )

    # Filter by city if selected
    if selected_city != 'All Cities':
        display_df = df[df['city'] == selected_city].copy()
        st.markdown(
            f"*Showing {len(display_df)} zip codes in {selected_city}*")
    else:
        display_df = df.copy()
        st.markdown(
            f"*Showing all {len(display_df)} zip codes in Middlesex County*")

    st.markdown("---")

    # STEP 2: Select Zip Code (WITHOUT SCORES)
    st.markdown("**Select Zip Code:**")

    # Sort by livability score for better UX
    display_df_sorted = display_df.sort_values(
        'livability_score', ascending=False)

    # Create zip options WITHOUT scores shown
    zip_options = [f"{row['zip_code']} - {row['city']}"
                   for _, row in display_df_sorted.iterrows()]

    selected_option = st.selectbox(
        "Choose a zip code to analyze:",
        zip_options,
        index=0,
        key='zip_selector'
    )

    # Extract zip code
    selected_zip = str(selected_option.split(" - ")[0])

    st.markdown("---")

    # Safety check
    if df[df['zip_code'] == selected_zip].empty:
        st.error(f"⚠️ Zip code {selected_zip} not found in data!")
        st.stop()

    # Show quick stats for selected zip
    selected_data = df[df['zip_code'] == selected_zip].iloc[0]

    st.markdown("### 📊 Quick Overview")
    st.metric("Livability Score",
              f"{selected_data['livability_score']:.1f}/100")
    st.metric("City", selected_data['city'])
    st.metric("Population", f"{int(selected_data['population']):,}")

    st.markdown("---")
    st.markdown("### 🎯 Methodology")
    st.markdown("""
    **Composite Score Weights:**
    - 🛡️ Safety: 25%
    - 🎓 Education: 25%
    - 💼 Jobs: 20%
    - 🏠 Housing: 20%
    - 🚗 Transport: 10%
    """)

    st.markdown("---")

    # Show county statistics
    st.markdown("### 📈 County Statistics")
    st.metric("Avg Livability", f"{df['livability_score'].mean():.1f}")
    best_zip = df.loc[df['livability_score'].idxmax()]
    st.metric("Best Zip Code", f"{best_zip['zip_code']} ({best_zip['city']})")
    st.metric("Total Population", f"{int(df['population'].sum()):,}")

# Get selected zip code data
selected_data = df[df['zip_code'] == selected_zip].iloc[0]
overall_rating, overall_color, overall_emoji = interpret_score(
    selected_data['livability_score'])

# Main Content - Overall Score
st.markdown(f"""
<div style='background: linear-gradient(135deg, {overall_color} 0%, {overall_color}dd 100%); 
            color: white; padding: 30px; border-radius: 20px; text-align: center; 
            box-shadow: 0 10px 25px rgba(0,0,0,0.3); margin: 20px 0;'>
    <h1 style='color: white !important; margin: 0; font-size: 48px;'>{overall_emoji} {selected_zip} - {selected_data['city']}</h1>
    <h2 style='color: white !important; margin: 10px 0; font-size: 64px; font-weight: 700;'>{selected_data['livability_score']:.1f}/100</h2>
    <p style='font-size: 28px; margin: 0; color: white !important;'>{overall_rating} Livability Score</p>
    <p style='font-size: 18px; margin-top: 10px; opacity: 0.9; color: white !important;'>Ranked #{(df['livability_score'] > selected_data['livability_score']).sum() + 1} out of {len(df)} zip codes in Middlesex County</p>
</div>
""", unsafe_allow_html=True)

# Show county context
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("County Average", f"{df['livability_score'].mean():.1f}")
with col2:
    rank = (df['livability_score'] >
            selected_data['livability_score']).sum() + 1
    st.metric("Your Rank", f"#{rank} of {len(df)}")
with col3:
    better_than_pct = ((len(df) - rank) / len(df) * 100)
    st.metric("Better Than", f"{better_than_pct:.0f}%")
with col4:
    st.metric("City", selected_data['city'])

# Tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Detailed Analysis",
    "🗺️ Map View",
    "📈 Comparisons",
    "📉 Rankings",
    "📚 Interpretations"
])

# TAB 1: Detailed Analysis
with tab1:
    st.markdown("## 🔍 Comprehensive Score Breakdown")

    # Five variable cards in a row
    cols = st.columns(5)

    variables = [
        ("Safety", selected_data['crime_score'], "🛡️",
         selected_data['crime_rate'], "crimes/1000"),
        ("Education", selected_data['education_score'], "🎓",
         selected_data['pct_bachelors_plus'], "% Bachelor's+"),
        ("Jobs", selected_data['jobs_score'], "💼",
         selected_data['unemployment_rate'], "% unemployed"),
        ("Housing", selected_data['housing_score'], "🏠",
         selected_data['housing_burden'], "% income"),
        ("Transport", selected_data['transportation_score'],
         "🚗", selected_data['mean_commute_time'], "minutes")
    ]

    for i, (name, score, emoji, raw_value, unit) in enumerate(variables):
        rating, color, rating_emoji = interpret_score(score)
        with cols[i]:
            st.markdown(f"""
            <div style='background: white; padding: 20px; border-radius: 12px; 
                        box-shadow: 0 4px 8px rgba(0,0,0,0.1); text-align: center;
                        border-top: 5px solid {color};'>
                <div style='font-size: 40px; margin-bottom: 10px;'>{emoji}</div>
                <div style='font-size: 18px; font-weight: 600; color: #1e40af !important; margin-bottom: 5px;'>{name}</div>
                <div style='font-size: 36px; font-weight: 700; color: {color} !important; margin: 10px 0;'>{score:.1f}</div>
                <div style='font-size: 14px; color: #6b7280 !important; margin-bottom: 5px;'>{rating}</div>
                <div style='font-size: 12px; color: #9ca3af !important; background: #f3f4f6; padding: 5px; border-radius: 5px;'>
                    Raw: {raw_value:.1f} {unit}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Detailed Interpretations
    st.markdown("## 📖 What These Scores Mean")

    col1, col2 = st.columns(2)

    with col1:
        # Safety Analysis
        st.markdown("### 🛡️ Safety & Crime")
        crime_rating, crime_color, crime_emoji = interpret_score(
            selected_data['crime_score'])
        crime_interp = interpret_crime(selected_data['crime_rate'])
        percentile = get_percentile(
            selected_data['crime_rate'], df['crime_rate'])

        st.markdown(f"""
        <div class='{"success-box" if selected_data["crime_score"] >= 65 else "warning-box"}'>
            <h4>{crime_emoji} Score: {selected_data['crime_score']:.1f}/100 - {crime_rating}</h4>
            <p><strong>Crime Rate:</strong> {selected_data['crime_rate']:.1f} crimes per 1,000 residents</p>
            <p><strong>Interpretation:</strong> {crime_interp}</p>
            <p><strong>County Ranking:</strong> Safer than {100-percentile}% of Middlesex County zip codes</p>
            <p><strong>What this means:</strong> {"This is a very safe area with low crime rates. Residents can feel secure in their daily activities." if selected_data['crime_score'] >= 70 else "Crime rates are moderate to high. Extra precautions may be advisable." if selected_data['crime_score'] >= 50 else "Higher crime rates present. Consider safety measures and community involvement."}</p>
        </div>
        """, unsafe_allow_html=True)

        # Education Analysis
        st.markdown("### 🎓 Education Quality")
        edu_rating, edu_color, edu_emoji = interpret_score(
            selected_data['education_score'])
        edu_interp = interpret_education(selected_data['pct_bachelors_plus'])
        percentile = get_percentile(
            selected_data['pct_bachelors_plus'], df['pct_bachelors_plus'])

        st.markdown(f"""
        <div class='{"success-box" if selected_data["education_score"] >= 65 else "neutral-box"}'>
            <h4>{edu_emoji} Score: {selected_data['education_score']:.1f}/100 - {edu_rating}</h4>
            <p><strong>Educational Attainment:</strong> {selected_data['pct_bachelors_plus']:.1f}% have Bachelor's degree or higher</p>
            <p><strong>Interpretation:</strong> {edu_interp}</p>
            <p><strong>County Ranking:</strong> Better educated than {percentile}% of zip codes</p>
            <p><strong>What this means:</strong> {"This area has exceptional educational attainment, indicating strong schools, intellectual capital, and higher earning potential." if selected_data['education_score'] >= 70 else "Education levels are moderate. Good schools exist but educational attainment varies." if selected_data['education_score'] >= 50 else "Educational attainment is below average. Focus on educational improvement may be needed."}</p>
        </div>
        """, unsafe_allow_html=True)

        # Housing Analysis
        st.markdown("### 🏠 Housing Affordability")
        housing_rating, housing_color, housing_emoji = interpret_score(
            selected_data['housing_score'])
        housing_interp = interpret_housing(selected_data['housing_burden'])
        percentile = 100 - \
            get_percentile(
                selected_data['housing_burden'], df['housing_burden'])

        st.markdown(f"""
        <div class='{"success-box" if selected_data["housing_score"] >= 65 else "warning-box"}'>
            <h4>{housing_emoji} Score: {selected_data['housing_score']:.1f}/100 - {housing_rating}</h4>
            <p><strong>Housing Cost Burden:</strong> {selected_data['housing_burden']:.1f}% of income spent on housing</p>
            <p><strong>Median Home Value:</strong> ${int(selected_data['median_home_value']):,}</p>
            <p><strong>Interpretation:</strong> {housing_interp}</p>
            <p><strong>County Ranking:</strong> More affordable than {percentile}% of zip codes</p>
            <p><strong>What this means:</strong> {"Housing is affordable relative to incomes. Residents have financial flexibility after housing costs." if selected_data['housing_score'] >= 65 else "Housing costs are moderate. Careful budgeting required." if selected_data['housing_score'] >= 50 else "Housing is expensive relative to incomes. Cost burden may limit other spending."}</p>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        # Jobs Analysis
        st.markdown("### 💼 Job Opportunities")
        jobs_rating, jobs_color, jobs_emoji = interpret_score(
            selected_data['jobs_score'])
        jobs_interp = interpret_unemployment(
            selected_data['unemployment_rate'])
        percentile = 100 - \
            get_percentile(
                selected_data['unemployment_rate'], df['unemployment_rate'])

        st.markdown(f"""
        <div class='{"success-box" if selected_data["jobs_score"] >= 65 else "warning-box"}'>
            <h4>{jobs_emoji} Score: {selected_data['jobs_score']:.1f}/100 - {jobs_rating}</h4>
            <p><strong>Unemployment Rate:</strong> {selected_data['unemployment_rate']:.1f}%</p>
            <p><strong>Median Income:</strong> ${int(selected_data['median_income']):,}</p>
            <p><strong>Interpretation:</strong> {jobs_interp}</p>
            <p><strong>County Ranking:</strong> Better job market than {percentile}% of zip codes</p>
            <p><strong>What this means:</strong> {"Excellent job market with abundant opportunities. Very low unemployment indicates strong economic health." if selected_data['jobs_score'] >= 70 else "Job market is stable with moderate opportunities available." if selected_data['jobs_score'] >= 50 else "Job market challenges exist. Higher unemployment may indicate economic stress."}</p>
        </div>
        """, unsafe_allow_html=True)

        # Transportation Analysis
        st.markdown("### 🚗 Transportation & Commute")
        trans_rating, trans_color, trans_emoji = interpret_score(
            selected_data['transportation_score'])
        trans_interp = interpret_commute(selected_data['mean_commute_time'])
        percentile = 100 - \
            get_percentile(
                selected_data['mean_commute_time'], df['mean_commute_time'])

        st.markdown(f"""
        <div class='{"success-box" if selected_data["transportation_score"] >= 65 else "neutral-box"}'>
            <h4>{trans_emoji} Score: {selected_data['transportation_score']:.1f}/100 - {trans_rating}</h4>
            <p><strong>Mean Commute Time:</strong> {selected_data['mean_commute_time']:.1f} minutes</p>
            <p><strong>Interpretation:</strong> {trans_interp}</p>
            <p><strong>County Ranking:</strong> Shorter commute than {percentile}% of zip codes</p>
            <p><strong>What this means:</strong> {"Excellent location with short commutes. Saves time and reduces stress for daily travel." if selected_data['transportation_score'] >= 65 else "Commute times are average. Plan for typical travel durations." if selected_data['transportation_score'] >= 50 else "Longer commute times. Consider transit options or flexible work arrangements."}</p>
        </div>
        """, unsafe_allow_html=True)

        # Income Analysis
        st.markdown("### 💰 Economic Prosperity")
        income_interp = interpret_income(selected_data['median_income'])
        percentile = get_percentile(
            selected_data['median_income'], df['median_income'])

        st.markdown(f"""
        <div class='{"success-box" if selected_data["median_income"] >= 100000 else "neutral-box"}'>
            <h4>💰 Median Household Income: ${int(selected_data['median_income']):,}</h4>
            <p><strong>Interpretation:</strong> {income_interp}</p>
            <p><strong>County Ranking:</strong> Higher income than {percentile}% of zip codes</p>
            <p><strong>What this means:</strong> {"This is a highly prosperous area with strong earning power and economic opportunities." if selected_data['median_income'] >= 120000 else "Income levels support a comfortable middle-class lifestyle." if selected_data['median_income'] >= 70000 else "Incomes are below county average. Economic challenges may be present."}</p>
        </div>
        """, unsafe_allow_html=True)

    # Radar Chart
    st.markdown("---")
    st.markdown("## 📊 Visual Score Profile")

    categories = ['Safety', 'Education', 'Jobs', 'Housing', 'Transportation']
    values = [
        selected_data['crime_score'],
        selected_data['education_score'],
        selected_data['jobs_score'],
        selected_data['housing_score'],
        selected_data['transportation_score']
    ]

    fig_radar = go.Figure()

    # Add selected zip
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        name=f'{selected_zip} - {selected_data["city"]}',
        line=dict(color='rgb(99, 102, 241)', width=3),
        fillcolor='rgba(99, 102, 241, 0.3)'
    ))

    # Add county average
    avg_values = [
        df['crime_score'].mean(),
        df['education_score'].mean(),
        df['jobs_score'].mean(),
        df['housing_score'].mean(),
        df['transportation_score'].mean()
    ]

    fig_radar.add_trace(go.Scatterpolar(
        r=avg_values,
        theta=categories,
        fill='toself',
        name='County Average',
        line=dict(color='rgb(156, 163, 175)', width=2, dash='dash'),
        fillcolor='rgba(156, 163, 175, 0.1)'
    ))

    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100],
                tickfont=dict(size=12, color='#1f2937'),
                gridcolor='rgba(0,0,0,0.1)'
            ),
            angularaxis=dict(
                tickfont=dict(size=14, color='#1e40af')
            ),
            bgcolor='rgba(255,255,255,0.9)'
        ),
        showlegend=True,
        legend=dict(
            x=0.5,
            y=-0.1,
            xanchor='center',
            orientation='h',
            font=dict(size=12, color='#1f2937')
        ),
        height=500,
        paper_bgcolor='#ffffff',
        plot_bgcolor='#ffffff'
    )

    st.plotly_chart(fig_radar, use_container_width=True)

# TAB 2: Map View
with tab2:
    st.markdown("## 🗺️ Middlesex County - Geographic View")

    # Create map centered on selected zip
    m = folium.Map(
        location=[selected_data['latitude'], selected_data['longitude']],
        zoom_start=11,
        tiles='CartoDB positron'
    )

    # Add markers for all zips
    for idx, row in df.iterrows():
        score = row['livability_score']
        is_selected = (str(row['zip_code']) == str(selected_zip))

        if score >= 75:
            color = '#10b981'
        elif score >= 60:
            color = '#3b82f6'
        elif score >= 45:
            color = '#f59e0b'
        else:
            color = '#ef4444'

        popup_html = f"""
        <div style="font-family: Arial; font-size: 13px; width: 220px;">
            <h4 style="margin: 5px 0; color: {color};">{row['city']}, MA {row['zip_code']}</h4>
            <b style="font-size: 16px;">Livability: {score:.1f}/100</b>
            <hr style="margin: 8px 0;">
            <table style="width: 100%; font-size: 12px;">
                <tr><td>🛡️ Safety:</td><td><b>{row['crime_score']:.1f}</b></td></tr>
                <tr><td>🎓 Education:</td><td><b>{row['education_score']:.1f}</b></td></tr>
                <tr><td>💼 Jobs:</td><td><b>{row['jobs_score']:.1f}</b></td></tr>
                <tr><td>🏠 Housing:</td><td><b>{row['housing_score']:.1f}</b></td></tr>
                <tr><td>🚗 Transport:</td><td><b>{row['transportation_score']:.1f}</b></td></tr>
            </table>
        </div>
        """

        folium.CircleMarker(
            location=[row['latitude'], row['longitude']],
            radius=15 if is_selected else 8,
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=f"{row['city']} ({row['zip_code']}): {score:.1f}",
            color='#fbbf24' if is_selected else color,
            fill=True,
            fillColor='#fbbf24' if is_selected else color,
            fillOpacity=0.9 if is_selected else 0.7,
            weight=4 if is_selected else 2
        ).add_to(m)

    # Add legend
    legend_html = """
    <div style="position: fixed; bottom: 50px; left: 50px; z-index: 1000; 
                background-color: white; padding: 15px; border-radius: 10px;
                border: 2px solid #ccc; font-size: 14px; box-shadow: 0 4px 8px rgba(0,0,0,0.2);">
        <h4 style="margin: 0 0 10px 0; color: #1e40af;">Livability Score</h4>
        <div><span style="color: #10b981; font-size: 20px;">●</span> Excellent (75-100)</div>
        <div><span style="color: #3b82f6; font-size: 20px;">●</span> Good (60-74)</div>
        <div><span style="color: #f59e0b; font-size: 20px;">●</span> Average (45-59)</div>
        <div><span style="color: #ef4444; font-size: 20px;">●</span> Below Average (&lt;45)</div>
        <hr style="margin: 10px 0;">
        <div><span style="color: #fbbf24; font-size: 20px;">⭐</span> <b>Selected Zip Code</b></div>
    </div>
    """
    m.get_root().html.add_child(folium.Element(legend_html))

    st_folium(m, width=1200, height=600, returned_objects=[])

    # Nearby zip codes
    st.markdown("---")
    st.markdown("### 📍 Nearby Zip Codes Comparison")

    # Calculate distances
    df_temp = df.copy()
    df_temp['distance'] = ((df_temp['latitude'] - selected_data['latitude'])**2 +
                           (df_temp['longitude'] - selected_data['longitude'])**2)**0.5

    nearby = df_temp[df_temp['zip_code'] !=
                     selected_zip].nsmallest(6, 'distance')

    if len(nearby) > 0:
        cols = st.columns(3)
        for i, (idx, row) in enumerate(nearby.iterrows()):
            with cols[i % 3]:
                rating, color, emoji = interpret_score(row['livability_score'])
                st.markdown(f"""
                <div style='background: white; padding: 15px; border-radius: 10px; 
                            border-left: 5px solid {color}; box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                            margin-bottom: 15px;'>
                    <h4 style='margin: 0 0 10px 0; color: #1e40af !important;'>{row['zip_code']} - {row['city']}</h4>
                    <div style='font-size: 28px; font-weight: 700; color: {color} !important;'>{row['livability_score']:.1f}</div>
                    <div style='font-size: 14px; color: #6b7280 !important;'>{rating}</div>
                </div>
                """, unsafe_allow_html=True)

# TAB 3: Comparisons
with tab3:
    st.markdown("## 📊 Compare Zip Codes in Middlesex County")

    # Multi-select for comparison
    comparison_zips = st.multiselect(
        "Select zip codes to compare (up to 5):",
        [f"{row['zip_code']} - {row['city']}" for _,
            row in df.iterrows() if str(row['zip_code']) != str(selected_zip)],
        default=[],
        max_selections=5
    )

    if comparison_zips:
        comparison_zip_codes = [str(z.split(" - ")[0])
                                for z in comparison_zips]
        comparison_df = df[df['zip_code'].isin(
            [selected_zip] + comparison_zip_codes)]

        # Bar charts for each variable
        col1, col2 = st.columns(2)

        variables_to_plot = [
            ('crime_score', 'Safety Score', '🛡️'),
            ('education_score', 'Education Score', '🎓'),
            ('jobs_score', 'Jobs Score', '💼'),
            ('housing_score', 'Housing Score', '🏠'),
            ('transportation_score', 'Transportation Score', '🚗'),
            ('livability_score', 'Overall Livability', '⭐')
        ]

        for i, (col_name, title, emoji) in enumerate(variables_to_plot):
            with col1 if i % 2 == 0 else col2:
                fig = px.bar(
                    comparison_df,
                    x='zip_code',
                    y=col_name,
                    color=col_name,
                    title=f"{emoji} {title}",
                    labels={'zip_code': 'Zip Code', col_name: 'Score'},
                    color_continuous_scale='RdYlGn',
                    range_color=[0, 100]
                )
                fig.update_layout(
                    height=300,
                    showlegend=False,
                    paper_bgcolor='#ffffff',
                    plot_bgcolor='#ffffff',
                    font=dict(color='#1f2937')
                )
                fig.update_traces(
                    marker_line_color='rgb(8,48,107)',
                    marker_line_width=1.5
                )
                st.plotly_chart(fig, use_container_width=True)

        # Comparison table
        st.markdown("### 📋 Detailed Comparison Table")
        comp_table = comparison_df[[
            'zip_code', 'city', 'livability_score', 'crime_score',
            'education_score', 'jobs_score', 'housing_score', 'transportation_score',
            'median_income', 'median_home_value', 'population'
        ]].copy()

        comp_table.columns = ['Zip', 'City', 'Overall', 'Safety', 'Education',
                              'Jobs', 'Housing', 'Transport', 'Med. Income',
                              'Med. Home Value', 'Population']

        # Format numbers
        comp_table['Med. Income'] = comp_table['Med. Income'].apply(
            lambda x: f"${int(x):,}")
        comp_table['Med. Home Value'] = comp_table['Med. Home Value'].apply(
            lambda x: f"${int(x):,}")
        comp_table['Population'] = comp_table['Population'].apply(
            lambda x: f"{int(x):,}")

        # Round scores
        for col in ['Overall', 'Safety', 'Education', 'Jobs', 'Housing', 'Transport']:
            comp_table[col] = comp_table[col].round(1)

        st.dataframe(comp_table, use_container_width=True, hide_index=True)
    else:
        st.info("👆 Select zip codes above to see detailed comparisons")

# TAB 4: Rankings
with tab4:
    st.markdown("## 🏆 Middlesex County Rankings")

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🌟 Top 10 Zip Codes")
        top10 = df.nlargest(10, 'livability_score')[
            ['zip_code', 'city', 'livability_score']
        ].copy()
        top10['Rank'] = range(1, len(top10) + 1)
        top10.columns = ['Zip', 'City', 'Score', 'Rank']
        top10 = top10[['Rank', 'Zip', 'City', 'Score']]
        top10['Score'] = top10['Score'].round(1)

        # Highlight if selected zip is in top 10
        def highlight_selected(row):
            if str(row['Zip']) == str(selected_zip):
                return ['background-color: #fef3c7'] * len(row)
            return [''] * len(row)

        st.dataframe(
            top10.style.apply(highlight_selected, axis=1),
            use_container_width=True,
            hide_index=True
        )

    with col2:
        st.markdown("### ⚠️ Bottom 10 Zip Codes")
        bottom10 = df.nsmallest(10, 'livability_score')[
            ['zip_code', 'city', 'livability_score']
        ].copy()
        bottom10['Rank'] = range(len(df), len(df) - len(bottom10), -1)
        bottom10.columns = ['Zip', 'City', 'Score', 'Rank']
        bottom10 = bottom10[['Rank', 'Zip', 'City', 'Score']]
        bottom10['Score'] = bottom10['Score'].round(1)

        st.dataframe(
            bottom10.style.apply(highlight_selected, axis=1),
            use_container_width=True,
            hide_index=True
        )

    # Category rankings
    st.markdown("---")
    st.markdown("### 📊 Category-Specific Rankings")

    col1, col2, col3 = st.columns(3)

    categories = [
        ('crime_score', 'Safety', '🛡️', col1),
        ('education_score', 'Education', '🎓', col2),
        ('jobs_score', 'Job Market', '💼', col3),
        ('housing_score', 'Housing', '🏠', col1),
        ('transportation_score', 'Transportation', '🚗', col2)
    ]

    for score_col, name, emoji, col in categories:
        rank = (df[score_col] > selected_data[score_col]).sum() + 1
        with col:
            st.markdown(f"""
            <div style='background: white; padding: 15px; border-radius: 10px; 
                        text-align: center; box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                        margin-bottom: 15px; border: 1px solid #e5e7eb;'>
                <div style='font-size: 32px;'>{emoji}</div>
                <div style='font-size: 16px; font-weight: 600; color: #1e40af !important;'>{name}</div>
                <div style='font-size: 28px; font-weight: 700; color: #6366f1 !important; margin: 10px 0;'>#{rank}</div>
                <div style='font-size: 14px; color: #6b7280 !important;'>out of {len(df)} zips</div>
            </div>
            """, unsafe_allow_html=True)

# TAB 5: Interpretations Guide
with tab5:
    st.markdown("## 📚 Understanding the Scores")

    st.markdown("""
    ### 🎯 What Do These Scores Actually Mean?
    
    This guide helps you understand what each score tells you about quality of life in Middlesex County.
    """)

    st.markdown("---")

    # Overall Livability
    st.markdown("### ⭐ Overall Livability Score")
    st.markdown("""
    The **Overall Livability Score** is a weighted composite of all five factors:
    
    - **80-100**: 🌟 **Excellent** - Top-tier quality of life. These are highly desirable areas with strong performance across all metrics.
    - **65-79**: ✅ **Good** - Above-average quality of life. Minor weaknesses but overall very livable.
    - **50-64**: ⚠️ **Average** - Typical quality of life. Mix of strengths and weaknesses.
    - **Below 50**: ❌ **Needs Improvement** - Below-average quality of life. Significant challenges in multiple areas.
    
    **Your score of {:.1f}** means this zip code ranks **#{} out of {}** in Middlesex County.
    """.format(selected_data['livability_score'],
               (df['livability_score'] >
                selected_data['livability_score']).sum() + 1,
               len(df)))

    st.markdown("---")

    # Detailed factor explanations
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🛡️ Safety Score")
        st.markdown("""
        **What it measures:** Crime rates per 1,000 residents (violent + property crimes)
        
        **Interpretation:**
        - **Low crime (< 10/1000)**: Very safe, walk-friendly neighborhoods
        - **Moderate (10-18/1000)**: Average safety, normal precautions advised
        - **High crime (> 18/1000)**: Higher vigilance needed
        
        **Why it matters:** Safety affects property values, insurance rates, and daily comfort.
        """)

        st.markdown("### 🎓 Education Score")
        st.markdown("""
        **What it measures:** % adults with Bachelor's degree+, school quality, college access
        
        **Interpretation:**
        - **High (> 70%)**: Elite educational environment
        - **Good (50-70%)**: Well-educated community
        - **Low (< 50%)**: Educational challenges present
        
        **Why it matters:** Indicates school quality, intellectual capital, and future earning potential.
        """)

        st.markdown("### 🏠 Housing Affordability Score")
        st.markdown("""
        **What it measures:** % of income spent on housing costs
        
        **Interpretation:**
        - **Affordable (< 30%)**: Manageable housing costs
        - **Moderate (30-35%)**: Tight but workable
        - **Expensive (> 35%)**: Financial strain likely
        
        **Why it matters:** High housing costs limit savings and quality of life spending.
        """)

    with col2:
        st.markdown("### 💼 Job Opportunity Score")
        st.markdown("""
        **What it measures:** Local unemployment rate
        
        **Interpretation:**
        - **Excellent (< 3%)**: Very strong job market
        - **Good (3-5%)**: Healthy employment
        - **Weak (> 5%)**: Job market challenges
        
        **Why it matters:** Job availability affects income stability and economic mobility.
        """)

        st.markdown("### 🚗 Transportation Score")
        st.markdown("""
        **What it measures:** Average commute time to work
        
        **Interpretation:**
        - **Short (< 25 min)**: Excellent location, less stress
        - **Average (25-30 min)**: Typical commute
        - **Long (> 30 min)**: Significant time investment
        
        **Why it matters:** Long commutes reduce free time and increase transportation costs.
        """)

        st.markdown("### 💰 Median Income")
        st.markdown("""
        **What it measures:** Typical household earnings
        
        **Interpretation:**
        - **High (> $120K)**: Affluent community
        - **Upper-middle ($80-120K)**: Comfortable living
        - **Middle ($50-80K)**: Moderate means
        - **Lower (< $50K)**: Economic challenges
        
        **Why it matters:** Income levels indicate economic vitality and purchasing power.
        """)

    st.markdown("---")

    st.markdown("### 🎲 How to Use These Scores")
    st.markdown("""
    1. **For Home Buyers:** Look for high overall scores with strong performance in your priorities (e.g., if you have kids, prioritize Education and Safety)
    
    2. **For Renters:** Focus on Housing Affordability and Transportation if budget-conscious
    
    3. **For Investors:** High Education + Low Unemployment often indicates stable property values
    
    4. **For Families:** Prioritize Safety and Education scores
    
    5. **For Young Professionals:** Transportation score matters most if commuting to Boston
    
    **Remember:** No single score tells the whole story. Consider your personal priorities and visit areas in person!
    """)

# Footer
st.markdown("---")
st.markdown(f"""
<div style='text-align: center; padding: 20px; font-size: 14px; background: white; border-radius: 10px; border: 1px solid #e5e7eb;'>
    <p style='color: #1f2937 !important; font-weight: 600; margin: 0;'><b>Middlesex County Livability Analysis Dashboard</b></p>
    <p style='color: #4b5563 !important; margin: 10px 0;'>Currently viewing: Zip Code <b>{selected_zip}</b> ({selected_data['city']})</p>
    <p style='color: #6b7280 !important; margin: 10px 0;'>Data Sources: U.S. Census Bureau ACS 2022 (5-year estimates) | FBI UCR | Mass DOE | BLS</p>
    <p style='color: #6b7280 !important; margin: 10px 0;'>Created by Sushmitha | Northeastern University | Data Visualization Project | December 2024</p>
    <p style='margin-top: 15px; font-size: 12px; color: #9ca3af !important;'>
        <i>Disclaimer: Scores represent analytical perspectives based on available data. 
        Visit areas personally and consult multiple sources when making residential decisions.</i>
    </p>
</div>
""", unsafe_allow_html=True)
