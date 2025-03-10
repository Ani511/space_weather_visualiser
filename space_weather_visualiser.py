import streamlit as st  
import requests  
import pandas as pd  
from datetime import datetime, timedelta 
import plotly.express as px  

event_descriptions = {  
    "CME": "Coronal Mass Ejection (CME): A massive burst of solar wind and magnetic fields rising above the solar corona.",  
    "GST": "Geomagnetic Storm (GST): Disturbances in Earth's magnetosphere caused by solar wind shocks.", 
    "FLR": "Solar Flare (FLR): A sudden flash of increased brightness on the Sun, usually observed near its surface.",  
    "SEP": "Solar Energetic Particle (SEP): High-energy particles emitted by the Sun, often associated with solar flares and CMEs.",  
    "IPS": "Interplanetary Shock (IPS): Shock waves traveling through space, often caused by CMEs or solar wind variations.",  
    "RBE": "Radiation Belt Enhancement (RBE): An increase in the density of charged particles in Earth's radiation belts.",  
    "MPC": "Magnetopause Crossing (MPC): When solar wind plasma crosses Earth's magnetopause, the boundary of the magnetosphere.",  
    "HSS": "High Speed Stream (HSS): Streams of fast-moving solar wind emanating from coronal holes on the Sun.",  
    "notifications": "Notifications: General alerts and updates related to various space weather events."  
}

space_theme_css = """
<style>
/* Background and text colors */  
body {  # Styling the body of the app 
    background-color: #0e1117;  # Set background color 
    color: #FAFAFA;  # Set text color 
    font-family: 'Arial', sans-serif;  # Set font family 
}
.sidebar .sidebar-content {  # Styling the sidebar content 
    background-color: #262730;  # Set sidebar background color 
    color: #FAFAFA;  # Set sidebar text color 
}
/* Remove the default Streamlit header */  
.css-1d391kg {  # Targeting specific CSS class 
    background-color: #0e1117;  # Set background color for header 
}
.css-1v3fvcr {  # Targeting another CSS class 
    color: #FAFAFA;  # Set text color 
}
.css-1adrfps.edgvbvh3 {  # Targeting nested CSS classes 
    background-color: #262730;  # Set background color 
}
/* Style for expander headers */  
.streamlit-expanderHeader {  # Styling expander headers 
    color: #1f77b4;  # Set color for expander headers 
}
</style>
"""  

st.markdown(space_theme_css, unsafe_allow_html=True)  

st.title("🌌  Space Weather Visualizer")  
st.markdown("""
This application visualizes space weather trends using NASA's DONKI API. 
Explore events like Coronal Mass Ejections (CME), Geomagnetic Storms (GST), Solar Flares (FLR), and more.
""")  

st.sidebar.header("Configuration")  


api_key = st.sidebar.text_input("Enter your NASA API Key:", value="DEMO_KEY")  

event_types = {  
    "CME (Coronal Mass Ejection)": "CME",  
    "GST (Geomagnetic Storm)": "GST",  
    "FLR (Solar Flare)": "FLR",  
    "SEP (Solar Energetic Particle)": "SEP", 
    "IPS (Interplanetary Shock)": "IPS",  
    "RBE (Radiation Belt Enhancement)": "RBE",  
    "MPC (Magnetopause Crossing)": "MPC",  
    "HSS (High Speed Stream)": "HSS",  
    "Notifications": "notifications"  
}

selected_event_display = st.sidebar.selectbox(  
    "Select Space Weather Event Type:",  
    list(event_types.keys()),  
    format_func=lambda x: x  
)

api_endpoint = event_types[selected_event_display]  
st.sidebar.markdown("### Date Range")  
default_end_date = datetime.utcnow().date()  
default_start_date = default_end_date - timedelta(days=30)  

start_date = st.sidebar.date_input("Start Date:", default_start_date)  
end_date = st.sidebar.date_input("End Date:", default_end_date)  

if start_date > end_date:  
    st.sidebar.error("Error: End date must fall after start date.")  
fetch_button = st.sidebar.button("Fetch Data")  


st.sidebar.markdown("### Event Information")  
with st.sidebar.expander("ℹ️ What is this event?"):  
    st.write(event_descriptions.get(api_endpoint, "No description available.")) 

st.sidebar.markdown("### Glossary")  
with st.sidebar.expander("📖 View Glossary"):  
    for term, description in event_descriptions.items():  
        st.markdown(f"**{term}**: {description}")  


st.sidebar.markdown("### Help")  
with st.sidebar.expander("❓ How to Use This App"):
    st.write("""
    1. **Enter API Key**: Provide your NASA API Key.
    2. **Select Event Type**: Choose the space weather event you're interested in.
    3. **Set Date Range**: Specify the start and end dates for the data visualization.
    4. **Fetch Data**: Click the "Fetch Data" button to retrieve and visualize the data.
    5. **View Details**: Expand the raw JSON data or raw data sections to inspect the data.
    6. **Explore**: Interact with the plots to learn more about specific events.
    """)  

@st.cache_data(ttl=3600)  
def fetch_space_weather(event, start, end, key):  
    base_url = f"https://api.nasa.gov/DONKI/{event}"  
    parms = {  
        "startDate": start.strftime("%Y-%m-%d"),  
        "endDate": end.strftime("%Y-%m-%d"),  
        "api_key": key  
    }
    
    
    if event == "CME": 
        parms.update({ 
            "mostAccurateOnly": "true",  
            "completeEntryOnly": "true",  
            "speed": 500,  
            "halfAngle": 30,  
            "catalog": "ALL"  
        })
    elif event == "notifications": 
        parms.update({  
            "type": "all"  
        })
    
    response = requests.get(base_url, params=parms)  
    
    if response.status_code == 200:  
        return response.json()  
    else:  
        st.error(f"Error fetching data: {response.status_code} - {response.text}")  
        return None  

if fetch_button: 
    if not api_key:  
        st.error("Please enter your NASA API Key to proceed.")  
    else:  
        with st.spinner("Fetching data..."):  
            data = fetch_space_weather(api_endpoint, start_date, end_date, api_key) 
        
        if data:  
            st.success("Data fetched successfully!")  
            
            
            with st.expander("Show Raw JSON Data for Debugging"): 
                st.json(data)  
            
        
            if isinstance(data, list): 
                df = pd.json_normalize(data)  
                
                
                date_field_mapping = {  
                    "CME": "startTime",  
                    "GST": "startTime",  
                    "FLR": "beginTime",  
                    "SEP": "eventTime",  
                    "IPS": "eventTime",  
                    "RBE": "eventTime",  
                    "MPC": "eventTime",  
                    "HSS": "eventTime", 
                    "notifications": "messageIssueTime" 
                }
                
    
                y_label_mapping = {  
                    "CME": "Number of CMEs", 
                    "GST": "Average Kp Index", 
                    "FLR": "Number of Solar Flares",
                    "SEP": "Number of Solar Energetic Particles", 
                    "IPS": "Number of Interplanetary Shocks", 
                    "RBE": "Number of Radiation Belt Enhancements",  
                    "MPC": "Number of Magnetopause Crossings",  
                    "HSS": "Number of High Speed Streams",  
                    "notifications": "Number of Notifications"  
                }
                
                
                y_label = y_label_mapping.get(api_endpoint, "Count")  
            
                date_field = date_field_mapping.get(api_endpoint, None)  
                
                if date_field and date_field in df.columns: 
                    df['date'] = pd.to_datetime(df[date_field], errors='coerce').dt.date  
                else:  
                    
                    possible_keys = [col for col in df.columns if 'date' in col.lower() or 'time' in col.lower()]  
                    if possible_keys:  
                        date_field = possible_keys[0] 
                        st.warning(f"Using '{date_field}' as the date field.")  
                        df['date'] = pd.to_datetime(df[date_field], errors='coerce').dt.date  
                    else:  
                        st.error("No suitable date field found in the data.")  
                        df['date'] = pd.NaT  
                
                
                if api_endpoint == "CME":  
                    df_grouped = df.groupby('date').size().reset_index(name='count')  
                    st.markdown("### Selected Event Information")  
                    st.write(event_descriptions.get(api_endpoint, "No description available."))  
                    st.subheader(f"{selected_event_display} from {start_date} to {end_date}")  
                    fig = px.line(df_grouped, x='date', y='count', title=f"Trend of {selected_event_display} Over Time",  
                                        labels={"date": "Date", "count": y_label},  
                                        markers=True, template="plotly_dark")  
                    st.plotly_chart(fig, use_container_width=True)  
                
                elif api_endpoint == "GST": 
                    if 'allKpIndex' in df.columns:  
                        kp_df = df.explode('allKpIndex') 
                        kp_df = pd.json_normalize(kp_df['allKpIndex'])  
                        kp_df['date'] = pd.to_datetime(kp_df['observedTime'], errors='coerce').dt.date  
                        df_grouped = kp_df.groupby('date').agg({'kpIndex': 'mean'}).reset_index()  
                        
                        st.markdown("### Selected Event Information")
                        st.write(event_descriptions.get(api_endpoint, "No description available."))
                        
                        st.subheader(f"{selected_event_display} Kp Index from {start_date} to {end_date}") 
                        fig = px.line(df_grouped, x='date', y='kpIndex', title=f"Average Kp Index of {selected_event_display} Over Time",  
                                          labels={"date": "Date", "kpIndex": y_label},  
                                          markers=True, template="plotly_dark")  
                        st.plotly_chart(fig, use_container_width=True)
                    else:  
                        st.error("No 'allKpIndex' data available to plot.")
                elif api_endpoint == "notifications":  
                    
                    df_grouped = df.groupby('date').size().reset_index(name='count') 
                    
                    st.markdown("### Selected Event Information")  
                    st.write(event_descriptions.get(api_endpoint, "No description available."))  
                    st.subheader(f"{selected_event_display} from {start_date} to {end_date}")  
                    fig = px.bar(df_grouped, x='date', y='count', title=f"Number of {selected_event_display} Over Time",
                                     template="plotly_dark")  
                    st.plotly_chart(fig, use_container_width=True)  
                
                else:  
                    df_grouped = df.groupby('date').size().reset_index(name='count')
                    
                    
                    st.markdown("### Selected Event Information")
                    st.write(event_descriptions.get(api_endpoint, "No description available."))  
                    
                    st.subheader(f"{selected_event_display} from {start_date} to {end_date}")  
                    fig = px.bar(df_grouped, x='date', y='count', title=f"Number of {selected_event_display} Over Time",  
                                     labels={"date": "Date", "count": y_label},  
                                     template="plotly_dark")  
                    st.plotly_chart(fig, use_container_width=True)  
                    
            
                with st.expander("Show Raw Data"):  
                    st.write(df)  
            else:  
                st.write("No data available for the selected parameters.")  