import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
import requests
from datetime import datetime
import numpy as np

# Set page configuration with custom theme
st.set_page_config(
    page_title="Arogyakosh Accident Analytics",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🚨"
)

# Apply custom CSS for modern look
st.markdown("""
<style>
 /* Main container styling - dark background */
.main {
  background-color: #2d2d2d;
  color: #e0e0e0;
}

/* Header styling */
.main-header {
  background-color: #0e53a7;
  padding: 1.5rem;
  border-radius: 10px;
  color: white;
  margin-bottom: 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.3);
}

/* Dashboard title */
.dashboard-title {
  font-size: 2.2rem !important;
  font-weight: 700 !important;
  margin-bottom: 0 !important;
}

/* Cards styling */
.metric-card {
  background-color: #333333;
  border-radius: 10px;
  padding: 1.2rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  text-align: center;
}

.metric-value {
  font-size: 1.8rem;
  font-weight: 700;
  color: #4a86e8;
}

.metric-label {
  font-size: 0.9rem;
  color: #c0c0c0;
  margin-top: 0.3rem;
}

/* Chart containers */
.chart-container {
  background-color: #333333;
  border-radius: 10px;
  padding: 1rem;
  box-shadow: 0 4px 12px rgba(0,0,0,0.2);
  margin-bottom: 20px;
}

.chart-title {
  font-size: 1.2rem;
  font-weight: 600;
  color: #e0e0e0;
  margin-bottom: 1rem;
  padding-bottom: 0.5rem;
  border-bottom: 1px solid #444444;
}

/* Custom tab styles */
.stTabs [data-baseweb="tab-list"] {
  gap: 15px;
}

.stTabs [data-baseweb="tab"] {
  height: 50px;
  white-space: pre-wrap;
  background-color: #3a3a3a;
  border-radius: 5px 5px 0px 0px;
  gap: 1em;
  padding-top: 10px;
  padding-bottom: 10px;
  color: #e0e0e0;
}

.stTabs [aria-selected="true"] {
  background-color: #0e53a7 !important;
  color: white !important;
}

/* Other UI elements */
.stButton button {
  background-color: #0e53a7;
  color: white;
  border-radius: 5px;
  border: none;
  padding: 0.3rem 1rem;
  font-weight: 500;
}

.stButton button:hover {
  background-color: #0a4184;
}

/* AI Insight styling - Grok response with blackish background */
.ai-insight {
  background-color: #222222;
  border-left: 4px solid #0e53a7;
  padding: 1rem;
  margin-top: 1rem;
  color: #e0e0e0;
}

/* Sidebar styling */
.css-1lcbmhc.e1fqkh3o3 {
  background-color: #2a2a2a;
  padding: 2rem 1rem;
}

/* Filter section */
.filter-section {
  background-color: #333333;
  padding: 1rem;
  border-radius: 10px;
  margin-bottom: 15px;
}

.filter-header {
  font-weight: 600;
  margin-bottom: 10px;
  color: #e0e0e0;
}

/* Footer */
.footer {
  text-align: center;
  margin-top: 30px;
  padding: 10px;
  font-size: 0.8rem;
  color: #b0b0b0;
}
</style>
""", unsafe_allow_html=True)

# Load dataset
@st.cache_data
def load_data():
    df = pd.read_csv("indian_accident_dataset_1000.csv", parse_dates=["Date"])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month_name()
    df['Month_num'] = df['Date'].dt.month
    df['Day'] = df['Date'].dt.day_name()
    df['Hour'] = pd.to_datetime(df['Time'], format='%H:%M:%S').dt.hour
    return df

df = load_data()

# Sidebar with improved styling
with st.sidebar:
    st.markdown("<h3 style='text-align: center; color: #0e53a7;'>🚧 Arogyakosh</h3>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; margin-bottom: 20px;'>Accident Analytics Platform</p>", unsafe_allow_html=True)
    
    st.markdown("<div class='filter-section'>", unsafe_allow_html=True)
    st.markdown("<p class='filter-header'>🔍 Data Filters</p>", unsafe_allow_html=True)
    
    # Date range filter
    current_year = datetime.now().year
    
    max_year = df['Year'].max()
    selected_year_range = st.slider(
        "Year Range", 
        min_value=2024, 
        max_value=max_year,
        value=(2024, max_year)
    )
    
    # Multi-selects for other filters
    states_list = sorted(df['State'].unique())
    selected_state = st.multiselect(
        "Select States", 
        options=states_list,
        default=states_list[:3] if len(states_list) >= 3 else states_list
    )
    
    selected_weather = st.multiselect(
        "Weather Conditions", 
        options=sorted(df['Weather Condition'].unique()),
        default=[]
    )
    
    selected_severity = st.multiselect(
        "Accident Severity", 
        options=sorted(df['Severity'].unique()),
        default=[]
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<div class='filter-section'>", unsafe_allow_html=True)
    st.markdown("<p class='filter-header'>🔧 Display Settings</p>", unsafe_allow_html=True)
    chart_theme = st.selectbox(
        "Chart Color Theme",
        options=["Blues", "viridis", "plasma", "inferno", "magma", "cividis"]
    )
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Export options
    st.markdown("<div class='filter-section'>", unsafe_allow_html=True)
    st.markdown("<p class='filter-header'>📊 Export Options</p>", unsafe_allow_html=True)
    if st.button("📥 Export Dashboard PDF"):
        st.info("Export functionality would be implemented here")
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Last updated timestamp
    st.markdown("<div class='footer'>Last updated: May 9, 2025</div>", unsafe_allow_html=True)

# Filter the data based on selections
filtered_df = df[(df['Year'] >= selected_year_range[0]) & (df['Year'] <= selected_year_range[1])]
if selected_state:
    filtered_df = filtered_df[filtered_df['State'].isin(selected_state)]
if selected_weather:
    filtered_df = filtered_df[filtered_df['Weather Condition'].isin(selected_weather)]
if selected_severity:
    filtered_df = filtered_df[filtered_df['Severity'].isin(selected_severity)]

# Function to request Groq summary with improved prompt
def get_groq_summary(prompt):
    try:
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer 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"},
            json={
                "model": "llama3-8b-8192",
                "messages": [{"role": "user", "content": prompt}]
            }
        )
        return response.json()['choices'][0]['message']['content']
    except Exception as e:
        return f"⚠️ Could not retrieve AI analysis. Error: {str(e)}"

# Dashboard Header
st.markdown("<div class='main-header'>", unsafe_allow_html=True)
st.markdown("<h1 class='dashboard-title'>🚨 Arogyakosh Accident Analytics</h1>", unsafe_allow_html=True)
st.markdown("<p>Smart insights for accident prevention and emergency response optimization</p>", unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Key Metrics Row
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{len(filtered_df)}</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-label'>Total Accidents</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col2:
    severe_count = len(filtered_df[filtered_df['Severity'] == 'Fatal'])
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{severe_count}</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-label'>Fatal Accidents</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col3:
    avg_response = round(filtered_df['Emergency Services Response Time (min)'].mean(), 1)
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{avg_response}</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-label'>Avg. Response Time (min)</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

with col4:
    top_cause = filtered_df['Cause of Accident'].value_counts().index[0] if not filtered_df.empty else "N/A"
    st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
    st.markdown(f"<div class='metric-value'>{top_cause.split()[0]}</div>", unsafe_allow_html=True)
    st.markdown("<div class='metric-label'>Top Accident Cause</div>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

# Dashboard tabs
tab1, tab2, tab3 = st.tabs(["📊 Trends & Analysis", "🗺️ Geographic Insights", "⚡ AI Insights"])

with tab1:
    # First row of charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 class='chart-title'>📅 Monthly Accident Distribution</h3>", unsafe_allow_html=True)
        
        if not filtered_df.empty:
            # Sort by month number for chronological order
            monthly_data = filtered_df.groupby(['Month_num', 'Month']).size().reset_index(name='Count')
            monthly_data = monthly_data.sort_values('Month_num')
            
            fig = px.bar(
                monthly_data, 
                x='Month', 
                y='Count',
                color_discrete_sequence=[px.colors.sequential.Blues[3]],
                labels={'Count': 'Number of Accidents'},
                height=250
            )
            fig.update_layout(
                margin=dict(l=20, r=20, t=30, b=10),
                xaxis_title=None,
                yaxis_title=None,
                plot_bgcolor='black',
                paper_bgcolor='black'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 class='chart-title'>🔄 Accidents by Time of Day</h3>", unsafe_allow_html=True)
        
        if not filtered_df.empty:
            hour_data = filtered_df.groupby('Hour').size().reset_index(name='Count')
            
            # Fill in missing hours with zero counts
            all_hours = pd.DataFrame({'Hour': range(0, 24)})
            hour_data = pd.merge(all_hours, hour_data, on='Hour', how='left').fillna(0)
            
            fig = px.line(
                hour_data, 
                x='Hour', 
                y='Count', 
                markers=True,
                color_discrete_sequence=[px.colors.sequential.Plasma[3]],
                height=250
            )
            fig.update_layout(
                margin=dict(l=20, r=20, t=30, b=10),
                xaxis_title=None,
                yaxis_title=None,
                plot_bgcolor='black',
                paper_bgcolor='black',
                xaxis=dict(tickmode='linear', tick0=0, dtick=3)
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Second row of charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 class='chart-title'>🌦️ Weather Impact Analysis</h3>", unsafe_allow_html=True)
        
        if not filtered_df.empty:
            weather_data = filtered_df['Weather Condition'].value_counts().reset_index()
            weather_data.columns = ['Weather Condition', 'Count']
            
            fig = px.pie(
                weather_data, 
                values='Count', 
                names='Weather Condition',
                hole=0.4,
                color_discrete_sequence=px.colors.sequential.Viridis,
                height=250
            )
            fig.update_layout(
                margin=dict(l=0, r=0, t=10, b=10),
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5),
                plot_bgcolor='black',
                paper_bgcolor='black'
            )
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 class='chart-title'>⚖️ Severity by Accident Cause</h3>", unsafe_allow_html=True)
        
        if not filtered_df.empty:
            # Get top 5 causes for better visibility
            top_causes = filtered_df['Cause of Accident'].value_counts().nlargest(5).index.tolist()
            cause_severity = filtered_df[filtered_df['Cause of Accident'].isin(top_causes)]
            
            fig = px.histogram(
                cause_severity, 
                x='Cause of Accident', 
                color='Severity',
                color_discrete_sequence=px.colors.sequential.RdBu,
                height=250,
                barmode='group'
            )
            fig.update_layout(
                margin=dict(l=20, r=20, t=30, b=60),
                xaxis_title=None,
                yaxis_title="Count",
                legend_title="Severity",
                plot_bgcolor='black',
                paper_bgcolor='black',
                xaxis={'categoryorder':'total descending'}
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Third row - yearly trend and response time
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 class='chart-title'>📈 Yearly Accident Trend</h3>", unsafe_allow_html=True)
        
        if not filtered_df.empty:
            yearly_data = filtered_df.groupby('Year').size().reset_index(name='Count')
            
            fig = px.line(
                yearly_data,
                x='Year',
                y='Count',
                markers=True,
                color_discrete_sequence=[px.colors.sequential.Greens[5]],
                height=250
            )
            fig.update_layout(
                margin=dict(l=20, r=20, t=30, b=10),
                xaxis_title=None,
                yaxis_title="Number of Accidents",
                plot_bgcolor='black',
                paper_bgcolor='black',
                xaxis=dict(tickmode='linear')
            )
            # Add trend line
            fig.add_traces(
                px.scatter(
                    yearly_data, 
                    x='Year', 
                    y='Count', 
                    trendline="ols", 
                    color_discrete_sequence=[px.colors.sequential.Greens[7]]
                ).data[1]
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 class='chart-title'>⏱️ Response Time vs Severity</h3>", unsafe_allow_html=True)
        
        if not filtered_df.empty:
            fig = px.box(
                filtered_df,
                x='Severity',
                y='Emergency Services Response Time (min)',
                color='Severity',
                color_discrete_sequence=px.colors.sequential.Oranges,
                height=250
            )
            fig.update_layout(
                margin=dict(l=20, r=20, t=30, b=10),
                xaxis_title=None,
                yaxis_title="Minutes",
                plot_bgcolor='black',
                paper_bgcolor='black',
                showlegend=False
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
        st.markdown("</div>", unsafe_allow_html=True)

with tab2:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<h3 class='chart-title'>🗺️ Accident Hotspots by City & State</h3>", unsafe_allow_html=True)
    
    if not filtered_df.empty:
        # City analysis
        city_data = filtered_df.groupby('City').size().reset_index(name='Count')
        city_data = city_data.sort_values('Count', ascending=False).head(10)
        
        fig = px.bar(
            city_data,
            x='Count',
            y='City',
            orientation='h',
            color='Count',
            color_continuous_scale=px.colors.sequential.Blues,
            height=350
        )
        fig.update_layout(
            margin=dict(l=20, r=20, t=30, b=10),
            xaxis_title="Number of Accidents",
            yaxis_title=None,
            plot_bgcolor='black',
            paper_bgcolor='black',
            yaxis={'categoryorder':'total ascending'}
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data available for the selected filters.")
    st.markdown("</div>", unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 class='chart-title'>🛣️ Road Condition Analysis</h3>", unsafe_allow_html=True)
        
        if not filtered_df.empty:
            road_data = filtered_df.groupby('Road Condition').size().reset_index(name='Count')
            
            fig = px.pie(
                road_data,
                values='Count',
                names='Road Condition',
                color_discrete_sequence=px.colors.sequential.Viridis,
                height=300
            )
            fig.update_layout(
                margin=dict(l=20, r=20, t=30, b=10),
                plot_bgcolor='black',
                paper_bgcolor='black'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col2:
        st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
        st.markdown("<h3 class='chart-title'>🔍 City-Severity Heatmap</h3>", unsafe_allow_html=True)
        
        if not filtered_df.empty:
            # Get top 10 cities for better visibility
            top_cities = filtered_df['City'].value_counts().nlargest(8).index.tolist()
            city_df = filtered_df[filtered_df['City'].isin(top_cities)]
            
            # Create crosstab
            heatmap_data = pd.crosstab(city_df['City'], city_df['Severity'])
            
            fig = px.imshow(
                heatmap_data,
                color_continuous_scale=px.colors.sequential.Blues,
                height=300,
                aspect="auto"
            )
            fig.update_layout(
                margin=dict(l=20, r=20, t=30, b=10),
                xaxis_title="Severity",
                yaxis_title="City",
                plot_bgcolor='black',
                paper_bgcolor='black'
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("No data available for the selected filters.")
        st.markdown("</div>", unsafe_allow_html=True)

with tab3:
    st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
    st.markdown("<h3 class='chart-title'>🧠 AI-Powered Accident Insights</h3>", unsafe_allow_html=True)
    
    # Create AI insight tabs
    insight_tab1, insight_tab2, insight_tab3 = st.tabs(["🔍 Overview", "⚠️ Risk Factors", "🏥 Response Analysis"])
    
    with insight_tab1:
        if st.button("Generate Overall Accident Insights", key="gen_overall"):
            if not filtered_df.empty:
                with st.spinner("Analyzing accident data..."):
                    sample = filtered_df.sample(min(5, len(filtered_df)))[['Year', 'Month', 'City', 'Cause of Accident', 'Severity', 'Weather Condition']]
                    prompt = f"""Analyze this accident dataset and provide 3-4 key insights about patterns, trends and notable observations:
                    
                    Dataset summary:
                    - Total records: {len(filtered_df)}
                    - Time period: {filtered_df['Year'].min()} to {filtered_df['Year'].max()}
                    - Top causes: {', '.join(filtered_df['Cause of Accident'].value_counts().nlargest(3).index.tolist())}
                    - Severity breakdown: {dict(filtered_df['Severity'].value_counts())}
                    
                    Sample records:
                    {sample.to_string(index=False)}
                    
                    Format your response with bullet points for key findings and make it concise but insightful.
                    """
                    ai_response = get_groq_summary(prompt)
                    st.markdown(f"<div class='ai-insight'>{ai_response}</div>", unsafe_allow_html=True)
            else:
                st.warning("No data available with current filters to generate insights.")
    
    with insight_tab2:
        if st.button("Analyze Risk Factors", key="gen_risk"):
            if not filtered_df.empty:
                with st.spinner("Analyzing risk factors..."):
                    sample = filtered_df.sample(min(5, len(filtered_df)))[['Weather Condition', 'Road Condition', 'Time', 'Day', 'Cause of Accident', 'Severity']]
                    prompt = f"""Analyze this accident dataset and identify key risk factors and patterns that contribute to accidents:
                    
                    Risk factor summary:
                    - Weather conditions: {dict(filtered_df['Weather Condition'].value_counts())}
                    - Road conditions: {dict(filtered_df['Road Condition'].value_counts())}
                    - Time of day distribution: Morning ({len(filtered_df[filtered_df['Hour'].between(6, 12)])}), 
                      Afternoon ({len(filtered_df[filtered_df['Hour'].between(12, 18)])}), 
                      Evening ({len(filtered_df[filtered_df['Hour'].between(18, 22)])}), 
                      Night ({len(filtered_df[filtered_df['Hour'].between(22, 6)])})
                    
                    Sample records:
                    {sample.to_string(index=False)}
                    
                    Based on this data, provide 3-4 key risk factors and when accidents are most likely to occur.
                    Format with bullet points and be concise but actionable.
                    """
                    ai_response = get_groq_summary(prompt)
                    st.markdown(f"<div class='ai-insight'>{ai_response}</div>", unsafe_allow_html=True)
            else:
                st.warning("No data available with current filters to analyze risk factors.")
    
    with insight_tab3:
        if st.button("Emergency Response Analysis", key="gen_response"):
            if not filtered_df.empty:
                with st.spinner("Analyzing emergency response data..."):
                    response_by_severity = filtered_df.groupby('Severity')['Emergency Services Response Time (min)'].agg(['mean', 'min', 'max']).reset_index()
                    response_by_city = filtered_df.groupby('City')['Emergency Services Response Time (min)'].mean().nlargest(5).reset_index()
                    
                    prompt = f"""Analyze emergency response times in this accident dataset:
                    
                    Response time by severity:
                    {response_by_severity.to_string(index=False)}
                    
                    Cities with longest average response times:
                    {response_by_city.to_string(index=False)}
                    
                    Overall average response time: {filtered_df['Emergency Services Response Time (min)'].mean():.2f} minutes
                    
                    Provide 2-3 key observations about emergency response patterns and recommendations for improvement.
                    Format with bullet points and be concise but actionable.
                    """
                    ai_response = get_groq_summary(prompt)
                    st.markdown(f"<div class='ai-insight'>{ai_response}</div>", unsafe_allow_html=True)
            else:
                st.warning("No data available with current filters to analyze emergency response.")
    
    st.markdown("</div>", unsafe_allow_html=True)

# Footer
st.markdown("""
<div class='footer'>
    <p>Arogyakosh Accident Analytics Dashboard | Powered by AI & Data Science</p>
    <p>© 2025 Arogyakosh - Making roads safer through data-driven insights</p>
</div>
""", unsafe_allow_html=True)