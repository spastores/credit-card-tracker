import streamlit as st
import pandas as pd
from datetime import datetime
import calendar

# --- APP CONFIGURATION ---
st.set_page_config(page_title="2026 Credit Card Optimizer", page_icon="💳", layout="centered")

# --- CUSTOM CSS FOR STYLING ---
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    .stProgress > div > div > div > div {
        background-color: #4CAF50;
    }
    </style>
    """, unsafe_allow_html=True)

# --- HEADER ---
st.title("💳 2026 Credit Card Optimizer")
st.markdown("Track your **Amex Gold**, **Chase Sapphire Reserve**, and **Citi Strata Premier** benefits for 2026.")
st.markdown("---")

# --- INITIALIZE SESSION STATE (DATABASE) ---
# This simulates a database. In a real app, this would be SQL/Firebase.
if 'data' not in st.session_state:
    st.session_state.data = {
        'amex_dining': 0,        # $10/mo ($120 yr)
        'amex_uber': 0,          # $10/mo ($120 yr)
        'amex_dunkin': 0,        # $7/mo ($84 yr)
        'amex_resy': 0,          # $50 semi-annually ($100 yr)
        'amex_hotel': 0,         # $100 per stay (The Hotel Collection)
        'csr_travel': 0,         # $300 yr
        'csr_dining_tables': 0,  # $150 semi-annually (Exclusive Tables)
        'csr_doordash_nc': 0,    # $10 x 2 /mo (Non-Restaurant)
        'csr_edit_hotel': 0,     # $250 semi-annually (The Edit)
        'citi_hotel': 0          # $100 yr (off $500+ stay)
    }

# --- DATE LOGIC ---
today = datetime.now()
current_month_name = calendar.month_name[today.month]
days_in_month = calendar.monthrange(today.year, today.month)[1]
days_left = days_in_month - today.day
half_year = "First Half" if today.month <= 6 else "Second Half"

# --- SIDEBAR: MONTHLY CHECKLIST ---
st.sidebar.header(f"📅 {current_month_name} 2026 Checklist")
st.sidebar.caption(f"You have {days_left} days left in the month!")

st.sidebar.subheader("Monthly Use-it-or-Lose-it")
amex_din_check = st.sidebar.checkbox("Amex Gold: Dining Credit ($10)", value=st.session_state.data['amex_dining'] > 0)
amex_uber_check = st.sidebar.checkbox("Amex Gold: Uber Cash ($10)", value=st.session_state.data['amex_uber'] > 0)
amex_dunk_check = st.sidebar.checkbox("Amex Gold: Dunkin' Credit ($7)", value=st.session_state.data['amex_dunkin'] > 0)
csr_dd_check = st.sidebar.checkbox("CSR: DoorDash Non-Food ($20)", value=st.session_state.data['csr_doordash_nc'] > 0)

# Update state based on checklist
if amex_din_check: st.session_state.data['amex_dining'] = 10
else: st.session_state.data['amex_dining'] = 0

if amex_uber_check: st.session_state.data['amex_uber'] = 10
else: st.session_state.data['amex_uber'] = 0

if amex_dunk_check: st.session_state.data['amex_dunkin'] = 7
else: st.session_state.data['amex_dunkin'] = 0

if csr_dd_check: st.session_state.data['csr_doordash_nc'] = 20
else: st.session_state.data['csr_doordash_nc'] = 0

# --- TABS FOR CARDS ---
tab1, tab2, tab3 = st.tabs(["🇺🇸 Amex Gold", "💎 Sapphire Reserve", "🏙️ Citi Premier"])

with tab1:
    st.header("American Express Gold")
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Annual Fee", "$325")
    with col2:
        # Calculate total value utilized
        total_amex_val = (st.session_state.data['amex_dining'] + 
                          st.session_state.data['amex_uber'] + 
                          st.session_state.data['amex_dunkin'] + 
                          st.session_state.data['amex_resy'])
        st.metric("Value Extracted (This Month/Period)", f"${total_amex_val}")

    st.subheader("Monthly Credits")
    st.info("💡 **Tip:** Use Uber Cash for pickup orders to avoid fees.")
    
    st.write(f"**Dining Credit ($10):** {'✅ Used' if amex_din_check else '❌ Unused'}")
    st.write(f"**Uber Cash ($10):** {'✅ Used' if amex_uber_check else '❌ Unused'}")
    st.write(f"**Dunkin' Credit ($7):** {'✅ Used' if amex_dunk_check else '❌ Unused'}")
    
    st.divider()
    
    st.subheader("Semi-Annual Credits (Resy)")
    resy_val = st.slider("Resy Credit Used (Jan-Jun or Jul-Dec)", 0, 50, st.session_state.data['amex_resy'])
    st.session_state.data['amex_resy'] = resy_val
    st.progress(resy_val / 50)
    st.caption(f"used ${resy_val} of $50 available for {half_year}")

with tab2:
    st.header("Chase Sapphire Reserve")
    st.caption("Includes 'The Edit' and 'Exclusive Tables' benefits new for 2025/26.")
    
    # 1. Travel Credit
    st.subheader("✈️ $300 Annual Travel Credit")
    travel_val = st.number_input("Amount spent on travel so far (automatically credited):", 0, 300, st.session_state.data['csr_travel'])
    st.session_state.data['csr_travel'] = travel_val
    st.progress(travel_val / 300)
    st.caption(f"${300 - travel_val} remaining")
    
    st.divider()
    
    # 2. The Edit Hotel Credit
    st.subheader("🏨 'The Edit' Hotel Credit")
    st.markdown("**Benefit:** $250 credit for Jan-Jun, and another $250 for Jul-Dec.")
    edit_val = st.slider(f"Credit used in {half_year}:", 0, 250, st.session_state.data['csr_edit_hotel'])
    st.session_state.data['csr_edit_hotel'] = edit_val
    st.progress(edit_val / 250)
    
    # 3. Exclusive Tables Dining
    st.subheader("🍽️ Exclusive Tables Dining Credit")
    st.markdown("**Benefit:** $150 credit for Jan-Jun, $150 for Jul-Dec at specific restaurants.")
    table_val = st.slider(f"Dining credit used in {half_year}:", 0, 150, st.session_state.data['csr_dining_tables'])
    st.session_state.data['csr_dining_tables'] = table_val
    st.progress(table_val / 150)

with tab3:
    st.header("Citi Strata Premier")
    st.caption("Formerly Citi Premier")
    
    st.subheader("🏨 $100 Annual Hotel Benefit")
    st.markdown("Get **$100 off** a single hotel stay of $500+ (excluding taxes/fees) when booked via Citi Travel.")
    
    citi_used = st.checkbox("Have you booked your $500+ hotel stay this year?", value=st.session_state.data['citi_hotel'] == 100)
    
    if citi_used:
        st.session_state.data['citi_hotel'] = 100
        st.success("✅ Benefit Utilized! You saved $100.")
    else:
        st.session_state.data['citi_hotel'] = 0
        st.warning("⚠️ Not yet used. Plan a trip!")

    st.markdown("### ⚡ Earning Multipliers Reminder")
    st.markdown("""
    * **10x:** Hotels/Car Rentals/Attractions (via Citi Travel)
    * **3x:** Air Travel, Dining, Supermarkets, Gas/EV
    """)

# --- SUMMARY SECTION ---
st.markdown("---")
st.header("💰 Total 2026 Value Realized")

total_possible = (120+120+84+100) + (300+500+300+240) + 100 # Approx max value of tracked perks
current_total = (
    st.session_state.data['amex_dining'] * 12 + # Projection for demo
    st.session_state.data['amex_uber'] * 12 + 
    st.session_state.data['amex_dunkin'] * 12 + 
    st.session_state.data['amex_resy'] * 2 + 
    st.session_state.data['csr_travel'] + 
    st.session_state.data['csr_edit_hotel'] * 2 +
    st.session_state.data['csr_dining_tables'] * 2 +
    st.session_state.data['csr_doordash_nc'] * 12 +
    st.session_state.data['citi_hotel']
)

# Simple visualizer for current month/period inputs only
real_time_value = (
    st.session_state.data['amex_dining'] + 
    st.session_state.data['amex_uber'] + 
    st.session_state.data['amex_dunkin'] + 
    st.session_state.data['amex_resy'] + 
    st.session_state.data['csr_travel'] + 
    st.session_state.data['csr_edit_hotel'] +
    st.session_state.data['csr_dining_tables'] +
    st.session_state.data['csr_doordash_nc'] +
    st.session_state.data['citi_hotel']
)

st.metric("Total Value Marked as Used (Current Period)", f"${real_time_value}")
st.caption("Note: This simple tracker resets when you close the browser. For permanent storage, a database connection is required.")
