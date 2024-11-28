import streamlit as st
from pages import economic_indicators, stock_market, interest_rates, currency_markets, crypto_markets

# Set page config
st.set_page_config(
    page_title="Economic Data Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session state for navigation if it doesn't exist
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'Economic Indicators'

# Load CSS
with open('static/css/style.css') as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Add clickable text link
st.markdown("""
    <a href="https://pythoninvest.com" target="_blank" class="logo-link">
        PythonInvest
    </a>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown('<p class="sidebar-title">Navigation</p>', unsafe_allow_html=True)
    views = {
        'Economic Indicators': economic_indicators,
        'Stock Market Overview': stock_market,
        'Interest Rates': interest_rates,
        'Currency Markets': currency_markets,
        'Crypto Markets': crypto_markets
    }
    
    for view_name, view_module in views.items():
        if st.button(view_name, key=view_name, help=f"View {view_name}", use_container_width=True):
            st.session_state.current_view = view_name

# Main content
st.title('Economic Data Dashboard')

# Display content based on selected view
current_view = st.session_state.current_view
if current_view in views:
    views[current_view].show()
