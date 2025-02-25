import streamlit as st  
import requests  
import pandas as pd  
from datetime import datetime, timedelta 
import plotly.express as px  

Agnirvaevent_descriptions = {  
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

Agnirvaspace_theme_css = """
<style>
/* Background and text colors */  /* Commented by Agnirva.com */
body {  # Styling the body of the app (Commented by Agnirva.com)
    background-color: #0e1117;  # Set background color (Commented by Agnirva.com)
    color: #FAFAFA;  # Set text color (Commented by Agnirva.com)
    font-family: 'Arial', sans-serif;  # Set font family (Commented by Agnirva.com)
}
.sidebar .sidebar-content {  # Styling the sidebar content (Commented by Agnirva.com)
    background-color: #262730;  # Set sidebar background color (Commented by Agnirva.com)
    color: #FAFAFA;  # Set sidebar text color (Commented by Agnirva.com)
}
/* Remove the default Streamlit header */  /* Commented by Agnirva.com */
.css-1d391kg {  # Targeting specific CSS class (Commented by Agnirva.com)
    background-color: #0e1117;  # Set background color for header (Commented by Agnirva.com)
}
.css-1v3fvcr {  # Targeting another CSS class (Commented by Agnirva.com)
    color: #FAFAFA;  # Set text color (Commented by Agnirva.com)
}
.css-1adrfps.edgvbvh3 {  # Targeting nested CSS classes (Commented by Agnirva.com)
    background-color: #262730;  # Set background color (Commented by Agnirva.com)
}
/* Style for expander headers */  /* Commented by Agnirva.com */
.streamlit-expanderHeader {  # Styling expander headers (Commented by Agnirva.com)
    color: #1f77b4;  # Set color for expander headers (Commented by Agnirva.com)
}
</style>
"""  

st.markdown(Agnirvaspace_theme_css, unsafe_allow_html=True)  

st.title("🌌 Agnirva Space Weather Visualizer")  
st.markdown("""
This application visualizes space weather trends using NASA's DONKI API. 
Explore events like Coronal Mass Ejections (CME), Geomagnetic Storms (GST), Solar Flares (FLR), and more.
""")  

st.sidebar.header("Configuration")  


Agnirvaapi_key = st.sidebar.text_input("Enter your NASA API Key:", value="DEMO_KEY")  

Agnirvaevent_types = {  
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

Agnirvaselected_event_display = st.sidebar.selectbox(  
    "Select Space Weather Event Type:",  
    list(Agnirvaevent_types.keys()),  
    format_func=lambda x: x  
)

Agnirvaapi_endpoint = Agnirvaevent_types[Agnirvaselected_event_display]  
st.sidebar.markdown("### Date Range")  
Agnirvadefault_end_date = datetime.utcnow().date()  
Agnirvadefault_start_date = Agnirvadefault_end_date - timedelta(days=30)  

Agnirvastart_date = st.sidebar.date_input("Start Date:", Agnirvadefault_start_date)  
Agnirvaend_date = st.sidebar.date_input("End Date:", Agnirvadefault_end_date)  

if Agnirvastart_date > Agnirvaend_date:  
    st.sidebar.error("Error: End date must fall after start date.")  
Agnirvafetch_button = st.sidebar.button("Fetch Data")  


st.sidebar.markdown("### Event Information")  
with st.sidebar.expander("ℹ️ What is this event?"):  
    st.write(Agnirvaevent_descriptions.get(Agnirvaapi_endpoint, "No description available.")) 

st.sidebar.markdown("### Glossary")  
with st.sidebar.expander("📖 View Glossary"):  
    for term, description in Agnirvaevent_descriptions.items():  
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
def Agnirvafetch_space_weather(Agnirvaevent, Agnirvastart, Agnirvaend, Agnirvakey):  
    Agnirvabase_url = f"https://api.nasa.gov/DONKI/{Agnirvaevent}"  
    Agnirvaparms = {  
        "startDate": Agnirvastart.strftime("%Y-%m-%d"),  
        "endDate": Agnirvaend.strftime("%Y-%m-%d"),  
        "api_key": Agnirvakey  
    }
    
    
    if Agnirvaevent == "CME": 
        Agnirvaparms.update({ 
            "mostAccurateOnly": "true",  
            "completeEntryOnly": "true",  
            "speed": 500,  
            "halfAngle": 30,  
            "catalog": "ALL"  
        })
    elif Agnirvaevent == "notifications": 
        Agnirvaparms.update({  
            "type": "all"  
        })
    
    Agnirvaresponse = requests.get(Agnirvabase_url, params=Agnirvaparms)  
    
    if Agnirvaresponse.status_code == 200:  
        return Agnirvaresponse.json()  
    else:  
        st.error(f"Error fetching data: {Agnirvaresponse.status_code} - {Agnirvaresponse.text}")  
        return None  

if Agnirvafetch_button: 
    if not Agnirvaapi_key:  
        st.error("Please enter your NASA API Key to proceed.")  
    else:  
        with st.spinner("Fetching data..."):  
            Agnirvadata = Agnirvafetch_space_weather(Agnirvaapi_endpoint, Agnirvastart_date, Agnirvaend_date, Agnirvaapi_key) 
        
        if Agnirvadata:  
            st.success("Data fetched successfully!")  
            
            
            with st.expander("Show Raw JSON Data for Debugging"): 
                st.json(Agnirvadata)  
            
        
            if isinstance(Agnirvadata, list): 
                Agnirvadf = pd.json_normalize(Agnirvadata)  
                
                
                Agnirvadate_field_mapping = {  
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
                
    
                Agnirvay_label_mapping = {  
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
                
                
                Agnirvay_label = Agnirvay_label_mapping.get(Agnirvaapi_endpoint, "Count")  
            
                Agnirvadate_field = Agnirvadate_field_mapping.get(Agnirvaapi_endpoint, None)  
                
                if Agnirvadate_field and Agnirvadate_field in Agnirvadf.columns: 
                    Agnirvadf['date'] = pd.to_datetime(Agnirvadf[Agnirvadate_field], errors='coerce').dt.date  
                else:  
                    
                    Agnirvapossible_keys = [col for col in Agnirvadf.columns if 'date' in col.lower() or 'time' in col.lower()]  
                    if Agnirvapossible_keys:  
                        Agnirvadate_field = Agnirvapossible_keys[0] 
                        st.warning(f"Using '{Agnirvadate_field}' as the date field.")  
                        Agnirvadf['date'] = pd.to_datetime(Agnirvadf[Agnirvadate_field], errors='coerce').dt.date  
                    else:  
                        st.error("No suitable date field found in the data.")  
                        Agnirvadf['date'] = pd.NaT  
                
                
                if Agnirvaapi_endpoint == "CME":  
                    Agnirvadf_grouped = Agnirvadf.groupby('date').size().reset_index(name='count')  
                    st.markdown("### Selected Event Information")  
                    st.write(Agnirvaevent_descriptions.get(Agnirvaapi_endpoint, "No description available."))  
                    st.subheader(f"{Agnirvaselected_event_display} from {Agnirvastart_date} to {Agnirvaend_date}")  
                    Agnirvafig = px.line(Agnirvadf_grouped, x='date', y='count', title=f"Trend of {Agnirvaselected_event_display} Over Time",  
                                        labels={"date": "Date", "count": Agnirvay_label},  
                                        markers=True, template="plotly_dark")  
                    st.plotly_chart(Agnirvafig, use_container_width=True)  
                
                elif Agnirvaapi_endpoint == "GST": 
                    if 'allKpIndex' in Agnirvadf.columns:  
                        Agnirvakp_df = Agnirvadf.explode('allKpIndex') 
                        Agnirvakp_df = pd.json_normalize(Agnirvakp_df['allKpIndex'])  
                        Agnirvakp_df['date'] = pd.to_datetime(Agnirvakp_df['observedTime'], errors='coerce').dt.date  
                        Agnirvadf_grouped = Agnirvakp_df.groupby('date').agg({'kpIndex': 'mean'}).reset_index()  
                        
                        st.markdown("### Selected Event Information")
                        st.write(Agnirvaevent_descriptions.get(Agnirvaapi_endpoint, "No description available."))
                        
                        st.subheader(f"{Agnirvaselected_event_display} Kp Index from {Agnirvastart_date} to {Agnirvaend_date}") 
                        Agnirvafig = px.line(Agnirvadf_grouped, x='date', y='kpIndex', title=f"Average Kp Index of {Agnirvaselected_event_display} Over Time",  
                                          labels={"date": "Date", "kpIndex": Agnirvay_label},  
                                          markers=True, template="plotly_dark")  
                        st.plotly_chart(Agnirvafig, use_container_width=True)
                    else:  
                        st.error("No 'allKpIndex' data available to plot.")
                elif Agnirvaapi_endpoint == "notifications":  
                    
                    Agnirvadf_grouped = Agnirvadf.groupby('date').size().reset_index(name='count') 
                    
                    st.markdown("### Selected Event Information")  
                    st.write(Agnirvaevent_descriptions.get(Agnirvaapi_endpoint, "No description available."))  
                    st.subheader(f"{Agnirvaselected_event_display} from {Agnirvastart_date} to {Agnirvaend_date}")  
                    Agnirvafig = px.bar(Agnirvadf_grouped, x='date', y='count', title=f"Number of {Agnirvaselected_event_display} Over Time",
                                     template="plotly_dark")  
                    st.plotly_chart(Agnirvafig, use_container_width=True)  
                
                else:  
                    Agnirvadf_grouped = Agnirvadf.groupby('date').size().reset_index(name='count')
                    
                    
                    st.markdown("### Selected Event Information")
                    st.write(Agnirvaevent_descriptions.get(Agnirvaapi_endpoint, "No description available."))  
                    
                    st.subheader(f"{Agnirvaselected_event_display} from {Agnirvastart_date} to {Agnirvaend_date}")  
                    Agnirvafig = px.bar(Agnirvadf_grouped, x='date', y='count', title=f"Number of {Agnirvaselected_event_display} Over Time",  
                                     labels={"date": "Date", "count": Agnirvay_label},  
                                     template="plotly_dark")  
                    st.plotly_chart(Agnirvafig, use_container_width=True)  
                    
            
                with st.expander("Show Raw Data"):  
                    st.write(Agnirvadf)  
            else:  
                st.write("No data available for the selected parameters.")  