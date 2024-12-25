import streamlit as st
from pages import economic_indicators, stock_market, interest_rates, currency_markets, crypto_markets

# Set page config
st.set_page_config(
    page_title="Economic Data Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize session states
if 'current_view' not in st.session_state:
    st.session_state.current_view = 'Economic Indicators'
if 'theme' not in st.session_state:
    st.session_state.theme = 'dark'

# Load CSS with dynamic theme
with open('static/css/style.css') as f:
    css_content = f.read()
    
# Apply theme-specific styles
if st.session_state.theme == 'light':
    theme_styles = """
        <style>
        .stApp {background-color: #ffffff !important;}
        section[data-testid="stSidebar"] {background-color: #f0f2f6 !important;}
        .sidebar-title {color: #00857c !important;}
        h1, h2, h3 {color: #00857c !important;}
        
        /* Navigation button styles */
        div[class*="stButton"] button {
            background-color: #00857c !important;
            border: none !important;
        }
        div[class*="stButton"] button:hover {
            background-color: #006b63 !important;
            border: none !important;
        }
        div[class*="stButton"] button p,
        div[class*="stButton"] button div,
        div[class*="stButton"] button span,
        div[class*="stButton"] button {
            color: #ffffff !important;
            font-weight: 500 !important;
            text-shadow: none !important;
        }
        
        /* Text colors */
        .element-container div.stMarkdown, 
        .element-container div.stMarkdown p, 
        .element-container div.stMarkdown li,
        div[data-testid="stMarkdownContainer"],
        div[data-testid="stMarkdownContainer"] p,
        div[class*="stMarkdown"],
        div[class*="stMarkdown"] p,
        div[class*="st-emotion-cache-"] p,
        div[class*="st-emotion-cache-"] {
            color: #0e1117 !important;
        }
        
        /* Last value text fix */
        div[class*="st-emotion-cache-"] span {
            color: #0e1117 !important;
        }
        
        /* Graph styles */
        .js-plotly-plot .plotly .gtitle,
        .js-plotly-plot .plotly .xtitle, 
        .js-plotly-plot .plotly .ytitle {
            color: #0e1117 !important;
        }
        .js-plotly-plot .plotly .xtick text, 
        .js-plotly-plot .plotly .ytick text {
            fill: #0e1117 !important;
            color: #0e1117 !important;
            font-weight: 600 !important;
        }
        .js-plotly-plot .plotly .xgrid,
        .js-plotly-plot .plotly .ygrid {
            stroke: rgba(14, 17, 23, 0.1) !important;
        }
        .js-plotly-plot .plotly .xaxis .zerolinelayer,
        .js-plotly-plot .plotly .yaxis .zerolinelayer {
            stroke: rgba(14, 17, 23, 0.5) !important;
        }
        
        /* Other elements */
        .logo-link {color: #00857c !important;}
        .logo-link:hover {color: #006b63 !important;}
        div[data-baseweb="notification"] {color: #0e1117 !important;}
        span.st-emotion-cache-10trblm {color: #0e1117 !important;}
        
        /* Theme button styles */
        button[kind="secondary"][data-testid="baseButton-secondary"] {
            background-color: #f0f2f6 !important;
            border: 2px solid #00857c !important;
            color: #00857c !important;
        }
        button[kind="secondary"][data-testid="baseButton-secondary"]:hover {
            background-color: #00857c !important;
            color: #ffffff !important;
        }
        </style>
    """
else:
    theme_styles = """
        <style>
        .stApp {background-color: #0e1117 !important;}
        section[data-testid="stSidebar"] {background-color: #1a1c24 !important;}
        .sidebar-title {color: #00FFF0 !important;}
        h1, h2, h3 {color: #00FFF0 !important;}
        
        /* Navigation button styles */
        div[class*="stButton"] button {
            background-color: #00FFF0 !important;
            border: none !important;
        }
        div[class*="stButton"] button:hover {
            background-color: #00ccbe !important;
            border: none !important;
        }
        div[class*="stButton"] button p,
        div[class*="stButton"] button div,
        div[class*="stButton"] button span,
        div[class*="stButton"] button {
            color: #0e1117 !important;
            font-weight: 500 !important;
            text-shadow: none !important;
        }
        
        /* Text colors */
        .element-container div.stMarkdown,
        .element-container div.stMarkdown p,
        .element-container div.stMarkdown li,
        div[data-testid="stMarkdownContainer"],
        div[data-testid="stMarkdownContainer"] p,
        div[class*="stMarkdown"],
        div[class*="stMarkdown"] p,
        div[class*="st-emotion-cache-"] p,
        div[class*="st-emotion-cache-"] {
            color: #ffffff !important;
        }
        
        /* Last value text fix */
        div[class*="st-emotion-cache-"] span {
            color: #ffffff !important;
        }
        
        /* Graph styles */
        .js-plotly-plot .plotly .gtitle,
        .js-plotly-plot .plotly .xtitle, 
        .js-plotly-plot .plotly .ytitle {
            color: #ffffff !important;
        }
        .js-plotly-plot .plotly .xtick text, 
        .js-plotly-plot .plotly .ytick text {
            fill: #ffffff !important;
            color: #ffffff !important;
            font-weight: 600 !important;
        }
        .js-plotly-plot .plotly .xgrid,
        .js-plotly-plot .plotly .ygrid {
            stroke: rgba(255, 255, 255, 0.1) !important;
        }
        .js-plotly-plot .plotly .xaxis .zerolinelayer,
        .js-plotly-plot .plotly .yaxis .zerolinelayer {
            stroke: rgba(255, 255, 255, 0.5) !important;
        }
        
        /* Other elements */
        .logo-link {color: #00FFF0 !important;}
        .logo-link:hover {color: #ffffff !important;}
        div[data-baseweb="notification"] {color: #ffffff !important;}
        span.st-emotion-cache-10trblm {color: #ffffff !important;}
        
        /* Theme button styles */
        button[kind="secondary"][data-testid="baseButton-secondary"] {
            background-color: #1a1c24 !important;
            border: 2px solid #00FFF0 !important;
            color: #00FFF0 !important;
        }
        button[kind="secondary"][data-testid="baseButton-secondary"]:hover {
            background-color: #00FFF0 !important;
            color: #0e1117 !important;
        }
        </style>
    """

st.markdown(f'<style>{css_content}</style>', unsafe_allow_html=True)
st.markdown(theme_styles, unsafe_allow_html=True)

# Add clickable text link
st.markdown("""
    <a href="https://pythoninvest.com" target="_blank" class="logo-link">
        PythonInvest
    </a>
""", unsafe_allow_html=True)

# Sidebar navigation
with st.sidebar:
    st.markdown('<p class="sidebar-title">Navigation</p>', unsafe_allow_html=True)
    
    # Navigation buttons
    views = {
        'Economic Indicators': economic_indicators,
        'Stock Market Overview': stock_market,
        'Interest Rates': interest_rates,
        'Currency Markets': currency_markets,
        'Crypto Markets': crypto_markets
    }
    
    for view_name, view_module in views.items():
        if st.button(view_name, key=view_name, help=None, use_container_width=True):
            st.session_state.current_view = view_name

# Main content
st.title('Economic Data Dashboard')

# Display content based on selected view
current_view = st.session_state.current_view
if current_view in views:
    views[current_view].show()
    
    # Theme toggle buttons at the bottom
    st.sidebar.markdown("<br>" * 5, unsafe_allow_html=True)  # Add space
    cols = st.sidebar.columns(2)
    with cols[0]:
        if st.button("Light Theme 🌞", key="light_theme", help=None, use_container_width=True):
            st.session_state.theme = "light"
            st.rerun()
    with cols[1]:
        if st.button("Dark Theme 🌙", key="dark_theme", help=None, use_container_width=True):
            st.session_state.theme = "dark"
            st.rerun()
