import os
import streamlit as st
from datetime import datetime
from langchain_core.messages import HumanMessage
from main import app


st.set_page_config(
    page_title="AI Travel Booking System",
    page_icon="✈️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

html, body, .stApp {
font-family: 'Inter', sans-serif;
background-color: #080d14;
}

.hero-wrapper {
position: reletive;
border-radius: 20px;
overflow:hidden;
margin-bottom: 2rem;
height: 280px;
}

.hero-bg
{
width:100%;
height:100%,
object-fit:cover;
display:block;
filter:brightness(0.35);
position: absolute;
top:0;
left:0;
}
.hero-content {
position: relative;
z-index:2;
height:100%;
display:flex;
flex-direction: column;
align-items:center;
padding: 2rem;
}

.hero-badge {
background: rgba(58,123, 213, 0.25);
border: 1px solid rgba(58,123,213,0.5);
color: #7ab8f5 !important;
font-size:0.75rem;
font-weight: 600;
letter-spacing:0.12em;
text_transform:uppercase;
padding:0.3rem 0.9rem;
border-radium:20px;
margin-bottom:0.9rem;
display:inline-block;
 }
 
 .hero.title {
 font-size: 2.6rem;
 font-weight: 700;
 color: #ffffff;
 margin: 0 0 0.6rem;
 line-height: 1.2;
 }
 
 .hero.sub
 {
 color: #94adc8;
 font-size: 1rem;
 max_width: 560px;
 }
 
 .input-card {
 background: #0e1623;
 border: 1px solid #1e2e44;
 border-radius: 16px;
 padding: 1.6rem 1.8rem;
 margin-bottom: 1.5rem;
 }
 
 .input-label{
 color: #7ab8f5;
 font-size:0.8rem;
 font-weight:600;
 letter-spacing: 0.1em;
 text-transform: uppercase;
 margin-bottom: 0.5rem;
 }
 
 /* ── Quick destinations ── */
.dest-row {
    display: flex;
    gap: 0.5rem;
    flex-wrap: wrap;
    margin: 0.8rem 0 1.2rem;
}
.dest-chip {
    background: #111b2b;
    border: 1px solid #1e3050;
    color: #f7fdf4;
    padding: 0.35rem 0.85rem;
    border-radius: 20px;
    font-size: 0.82rem;
    cursor: pointer;
    transition: all 0.2s;
}
.dest-chip:hover { background: #1a2e47; border-color: #3a7bd5; color: #fff; }

/* ── Generate button ── */
div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #1a6bbf 0%, #0d4a8a 50%, #0a3d75 100%) !important;
    color: #ffffff !important;
    border: none !important;
    border-radius: 12px !important;
    padding: 0.85rem 2.5rem !important;
    font-size: 1.05rem !important;
    font-weight: 700 !important;
    letter-spacing: 0.03em !important;
    width: 100% !important;
    box-shadow: 0 0 24px rgba(26,107,191,0.35), 0 4px 15px rgba(0,0,0,0.4) !important;
    transition: all 0.3s ease !important;
}
div[data-testid="stButton"] > button:hover {
    box-shadow: 0 0 40px rgba(26,107,191,0.6), 0 6px 20px rgba(0,0,0,0.5) !important;
    transform: translateY(-2px) !important;
    background: linear-gradient(135deg, #2278d4 0%, #1057a0 50%, #0d4a8a 100%) !important;
}
div[data-testid="stButton"] > button:active {
    transform: translateY(0px) !important;
}

/* ── Agent status cards ── */
[data-testid="stStatusWidget"] {
    background: #0e1a2e !important;
    border: 1px solid #1e3050 !important;
    border-radius: 12px !important;
}
[data-testid="stStatusWidget"] > div:first-child {
    background: #0e1a2e !important;
    border-radius: 12px 12px 0 0 !important;
}
[data-testid="stStatusWidget"] details,
[data-testid="stStatusWidget"] details > div,
[data-testid="stStatusWidget"] [data-testid="stVerticalBlock"] {
    background: #0a1520 !important;
    color: #ffffff !important;
    padding: 0.25rem 0.5rem !important;
}
[data-testid="stStatusWidget"] * { color: #ffffff !important; }
[data-testid="stStatusWidget"] a { color: #4ea8f0 !important; }
[data-testid="stStatusWidget"] hr { border-color: #1e3050 !important; }

/* ── Section headers ── */
.sec-head {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    margin: 2rem 0 0.75rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e2e44;
}
.sec-head span { font-size: 1.15rem; font-weight: 600; color: #e0edf8; }

/* ── Metric bar ── */
.metric-row {
    display: flex;
    gap: 1rem;
    margin: 1.5rem 0;
}
.metric-box {
    flex: 1;
    background: #0e1623;
    border: 1px solid #1e2e44;
    border-radius: 12px;
    padding: 1rem 1.2rem;
    text-align: center;
}
.metric-val { font-size: 1.8rem; font-weight: 700; color: #4ea8f0; }
.metric-lbl { font-size: 0.78rem; color: #5a7a96; margin-top: 0.2rem; text-transform: uppercase; letter-spacing: 0.08em; }

/* ── Final plan ── */
.final-card {
    background: linear-gradient(160deg, #0c1a2e 0%, #0a1520 100%);
    border: 1px solid #1e3a5c;
    border-left: 4px solid #3a7bd5;
    border-radius: 14px;
    padding: 1.8rem;
    line-height: 1.8;
    color: #cce0f5;
    font-size: 0.95rem;
}

/* ── Save bar ── */
.save-bar {
    background: #0e1623;
    border: 1px solid #1e2e44;
    border-radius: 10px;
    padding: 0.85rem 1.2rem;
    color: #5a8ab0;
    font-size: 0.88rem;
    margin-top: 0.5rem;
}

</style>
""", unsafe_allow_html=True)


#Hero----------------------------------------------------------
st.markdown ("""
<div class="hero-wrapper">
     <img class="hero-bg"
           src="https://images.unsplash.com/photo-1436491865332-7a61a109cc05?w=1400&q=80"
           alt="airplane above clouds"/>
        <div class="hero-content">
             <div class="hero-badge"> Multi-agent AI System</div>
             <div class="hero-title"> AI Travel Booking System </div>
             <div class="hero-sub">Four Specialized Agents Work together - Searching Flights, Hotels, Building an itinerary, and delivering your perfect trip plan.</div>
        </div>

</div>  
           
           
           """, unsafe_allow_html=True)

# Destination Image Strip -------------------------------------

DESTINATIONS = [
    ("🇯🇵 Tokyo",     "https://images.unsplash.com/photo-1540959733332-eab4deabeeaf?w=300&q=70"),
    ("🇫🇷 Paris",     "https://images.unsplash.com/photo-1502602898657-3e91760cbb34?w=300&q=70"),
    ("🇹🇭 Bangkok",   "https://images.unsplash.com/photo-1508009603885-50cf7c579365?w=300&q=70"),
    ("🇮🇹 Rome",      "https://images.unsplash.com/photo-1552832230-c0197dd311b5?w=300&q=70"),
    ("🇦🇪 Dubai",     "https://images.unsplash.com/photo-1512453979798-5ea266f8880c?w=300&q=70"),
]

cols = st.columns(5)

for col, (name, img_url) in zip (cols, DESTINATIONS):
    with col:
        st.markdown (f"""
        <div style="border-radius:10px;overflow:hidden;position:relatove;hight:90px;cursor:pointer;">

<img src="{img_url}" style="width:100%,height:100%;object-fit:cover;filter:brightness(0.55);"/>
<div style="position:absolute;bottom:8px; left:0; right:0; text-align:center;
color:#fff; font-size:0.8rem; font-weight:600;">{name}</div>
</div>
""", unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)



#Input------------------------------------------------------
st.markdown("<div class='input-label'> Describe Your Trip </div>", unsafe_allow_html=True)
QUICK = st.columns(len(QUICK))
quick_fill= ""
for qc, label in zi(qcols, QUICK):
    with qc, label in zip(qcols,QUICK):
        with qc:
            if st.button(label, key=f"q_{label}"):
                quick_fill =label


                   user_query = st.text_area(
       "",
       value=quick_fill,
       placeholder="e.g Plan a complete 7 day japan trip including flights, hotels and sightseeing under 2lakhs",
       height = 100,
       label_visibility="collapsed",
   )    

generate =st.button("Generate My trvel plan", use_container_width=True)


#agent_Pipline-----------------------------------------

AGENT_META = {
    "filght_agent": ("✈️", "Flight Agent"),
    "hotel_agent": ("🏨", "Hotel Agent"),
    "itinerary-agent": ("🗓️", "Itinerary Agent"),
    "final_agent": ("🧠", "Final Agent"),
}


if generate:
    if not user_query.strip():
        st.warning("Please describe your trip first.")
    else:
        config = {"configurable": {"thread_id": thread_id}}
        collected = {"flight_results": "", "hotel_results": "",
                     "itinerary": "", "final_response":"", "llm_calls":0}

        st.markdown("---")
        st.markdown("<div class='sec-head'><span>🤖 Agent Pipeline - LIVE </span></div>",
                    unsafe_allow_html=True)

      for chunk in app.stream(
          {
              "message": [HumanMessage(content=user_query)],
              "user_query": user_query,
              "flight_results": "",
              "hotel_results": "",
              "itinerary": "",
              "llm_calls": 0,

          },
          config=config,
          stream_mode="updates",
      ):

      for node_name, state_update in chunk.items():
          icon, label = AGENT_META.get(node_name, ("🔧", node_name))

          with st.status(f"{icon} {label}", state="complete", expanded=True):
              if node_name == "flight_agent":
                  text = state_update.get ("fliht_results", "")
                  collected ["flight_results"] =text
                  st.markdown(text or "_No flight data returned._")

                elif node_name == "hotel_agent":
                      text = state_update.get("hotel_results", "")
                      collected["hotel_results"] = text 
                     st.markdown(text or "_No hostel data returned._")

elif node_name == "itinerary_agent":
      text = state_update.get("itinerary", "")
      collected ["itinerary_results"] = text
      st.markdown(text or "_No itinerary genrated._")

elif node_name == "final_agent":
      msgs = state_update.get("messages", [])
      text = msgs[-1].content if msgs else ""
      collected["final_response"]= text 
      st.markdown(text or "_No final response._")

      collected["llm_calls"] = state_update.get("llm_calls", collected["llm_calls"])


#Metrics--------------------------------------------------------

st.markdown(f"""
<div class="metric-row">
     <div class="metric-box"><div class="metric-val">4</div><div class="metric-lbl"> Agents Run</div></div>
     <div class="metric-box"><div class="metric-val">{collected['llm_calls']}</div><div class="metric-lbl">LLM Calls</div></div>

     <div class="metric-box"><div class="metric-val>✅ </div> <div class="metric-lbl">Status</div></div>
     </div>
     """, unsafe_allow_html=True)


#final plan card

if collected["final_response"]:
    st.markdown("<div class='sec-head'><span> Final Travel Plan </span></div>",
                unsafe_allow_html=True)
    st.markdown(f"<div class='final-card'>{collected['final_response']}</div>",
                unsafe_allow_html=True)

    #Save
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"travel_plan_{timestamp}.md"
    save_dir = os.path.join(os.path.dirname(__file__), "travel_plans")
    os.makedirs(save_dir,exist_ok=True)


    file_content = f"""# Travel Plan
    **Query:** {user_query}
**Generated:** {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
**User ID:** {thread_id}

{collected['flight_results'] or 'N/A'}
{collected['hotel_results'] or 'N/A'}
{collected['itinerary'] or 'N/A'}
{collected['final_response'] or 'N/A'}

*LLM Calls: {collected['llm_calls']}*
"""


    with open(os.path.join(save_dir, filename), "w", encoding="uft-8") as f:
        f.wreite(file_content)
        dl_col, info_col = st.columns([1, 3])
        with dl_col:
            st.download_button("Download Plan", data=file_content,
                               file_name=filename, mime="text/markdown",
                               use_container_width=True)
        with info_col:
            st.markdown(f"<div class='save-bar'> Auto_saved -> <code> travel_plans/{filename}</code></div>",
                       unsafe_allow_html=True)    