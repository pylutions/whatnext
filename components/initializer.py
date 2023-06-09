import streamlit as st
from streamlit.components.v1 import html
import components.data_handler as data_handler


def initialize():
    if 'init' not in st.session_state:
        st.session_state['version'] = 1
        st.session_state['version_note'] = 'Initial version'

        if 'tenant' in st.secrets:
            if 'name' in st.secrets['tenant']:
                st.session_state['tenant'] = st.secrets['tenant']['name']
            else:
                st.error("Please add tenant name in the configuration.")
                return False
            if 'admin' in st.secrets['tenant']:
                st.session_state['admin'] = st.secrets['tenant']['admin']
            else:
                st.error("Please add a tenant admin in the configuration.")
                return False
            if 'password' not in st.secrets['tenant']:
                st.error("Please add a tenant admin password in the configuration.")
                return False
        else:
            st.error("Please add tenant information in the configuration.")
            return False

        if 'feature_db' in st.secrets:
            control = data_handler.version_control(st.session_state['version'], st.session_state['version_note'])

            if control:
                if 'has_products' not in st.session_state:
                    st.session_state['has_products'] = data_handler.get_products(False)

                if 'buymeacoffee' in st.secrets:
                    if 'enabled' in st.secrets['buymeacoffee']:
                        if st.secrets['buymeacoffee']['enabled'] and 'button' in st.secrets['buymeacoffee']:
                            st.session_state['bmcbutton'] = st.secrets['buymeacoffee']['button']


                # query params
                st.session_state.query_params = st.experimental_get_query_params()
                if 'product' in st.session_state.query_params:
                    st.session_state['query_product'] = st.session_state.query_params['product'][0]
                if 'feature' in st.session_state.query_params:
                    st.session_state['query_feature'] = st.session_state.query_params['feature'][0]
                if 'user_mail' in st.session_state.query_params:
                    st.session_state['user_mail'] = st.session_state.query_params['user_mail'][0]
                else:
                    st.session_state['user_mail'] = ''
                st.session_state['tenant'] = st.secrets['tenant']

                # Theme
                st.session_state['primaryColor'] = st.get_option('theme.primaryColor')
                st.session_state['backgroundColor'] = st.get_option('theme.backgroundColor')
                st.session_state['secondaryBackgroundColor'] = st.get_option('theme.secondaryBackgroundColor')
                st.session_state['textColor'] = st.get_option('theme.textColor')

                st.session_state['feature_states'] = ['new', 'active', 'rejected', 'done']
                #st.session_state['feature_page'] = 0
                #st.session_state['next_page'] = False
                #st.session_state['admin_page'] = 0
                st.session_state['step_size'] = 10

                st.session_state['show_feature'] = False
                st.session_state['user_id'] = 0

                st.session_state['registered'] = False
                st.session_state['user_essential'] = True
                st.session_state['user_agreement'] = True
                st.session_state['init'] = True
                return True
        else:
            st.error('Database information missing.')
            return False
    else:
        return True


def style_a_button():
    m = st.markdown("""
    <style>
    div.stButton > button:first-child {
        background-color: #ce1126;
        color: white;
        height: 3em;
        width: 12em;
        border-radius:10px;
        border:3px solid #000000;
        font-size:20px;
        font-weight: bold;
        margin: auto;
        display: block;
    }

    div.stButton > button:hover {
    	background:linear-gradient(to bottom, #ce1126 5%, #ff5a5a 100%);
    	background-color:#ce1126;
    }

    div.stButton > button:active {
    	position:relative;
    	top:3px;
    }

    </style>""", unsafe_allow_html=True)


def stylize():
    primaryColor = st.session_state['primaryColor']
    st.markdown(f"""
            <style>
            a, a: visited
            {{
                color: {primaryColor};
            }}
            </style>""", unsafe_allow_html=True)


    backgroundColor = st.session_state['backgroundColor']
    secondaryBackgroundColor = st.session_state['secondaryBackgroundColor']
    textColor = st.session_state['textColor']

    style = False
    script = False

    r = """
            const allElements = document.getElementsByTagName('*');
            console.log('test');

            // ✅ Loop through all elements (including html, head, meta, scripts)
            for (const element of allElements) {
                console.log(element);
            }        
            """

    if script:
        return_value = ("""
            // Define the color you want to replace
            const oldColor = 'red';
            const newColor = 'blue';
            
            // Get all the elements on the page
            const elements = document.getElementsByTagName('*');
            
            // Loop over each element
            for (let i = 0; i < elements.length; i++) {
              // Get the computed style of the element
              const style = window.getComputedStyle(elements[i]);
            
              // Get the value of the color property
              const color = style.getPropertyValue('color');
              // Print the previous color to the console
              alert('Previous color: ${color}');
              // Check if the color matches the old color you want to replace
              if (color === oldColor) {
                
            
                // Replace the color with the new color
                elements[i].style.color = newColor;
              }
            }
            return elements.length;
        """)
        #scr = f"<script>{sc}</script>"
        #st.markdown(f"Return value was: {return_value}")

        #st.markdown(scr, unsafe_allow_html=True)

    if style:
        st.markdown(f"""
            <style>
            # sidebar
            
            .css-vk3wp9 {{
                background-color: {secondaryBackgroundColor};
            }}
            
            
            [data-testid="stSidebar"] {{
                background-color: {secondaryBackgroundColor};
            }}
            
            # main area
            
            [data-testid="stSidebar"] {{
                background-color: {backgroundColor};
                #color: {textColor};
            }}
            
            .main {{
                background-color: {backgroundColor};
                #color: {textColor};
            }}
            
            
            p, h1, h2, h3, span, .stMarkdown {{
                color: {textColor} !important;
                
            }}
            
            span {{
                #background-color: {primaryColor};
            }}
            
            
            .st-dk {{
                background-color: {backgroundColor};
                border-color: {secondaryBackgroundColor};
                color: {textColor};
            }}
            
            .st-dk:active, .st-dk:focus-within, .st-dk:focus, .st-dk:visited{{
                border-color: {primaryColor};
                background-color: {backgroundColor};
            }}
            
            *:active, *:focus, *:focus-within, *:focus-visible , *:visited{{
                border-color: {primaryColor};
                background-color: {backgroundColor};
            }}
            
            
            # checkbox
            .st-f7, .st-ei, .st-e0, [type="checkbox"] {{
                background-color: {backgroundColor};
            }}
            .st-g1, .st-g2, .st-g3, .st-g4 {{
                border-color: {primaryColor};
                background-color: {backgroundColor};
            }}
            
            
            
            .st-bu {{
                background-color: {backgroundColor};
                border-color: {secondaryBackgroundColor};
                color: {textColor};
            }}
            
            .st-bu:active, .st-bu:focus-within, .st-bu:focus, .st-bu:visited{{
                border-color: {primaryColor};
                background-color: {backgroundColor};
            }}
            
            #[role="tab"] {{
            #    background-color: {primaryColor};
            #}}
            
            .st-e8:active {{
                background-color: {primaryColor};
            }}
            
            [type="checkbox"] {{
                background-color: {primaryColor};
            }}
            
            
            [data-baseweb="tab-highlight"] {{
                background-color: {primaryColor};
            }}
            
            .st-c7 {{
                color: {textColor};
                background-color: {backgroundColor};
                border-color: {primaryColor};
            }}
            .st-c7:hover, .st-c7:active, .st-c7:focus , st-c7:visited{{
                color: {primaryColor};
            }}
            .st-c8:hover, .st-c8:active{{
                border-color: {secondaryBackgroundColor};
                color: {primaryColor};
            }}
            
            
            
            a, a:visited {{
                color: {primaryColor};
            }}
            
            
            
            div.stButton > button:first-child {{
                background: {backgroundColor};       
                border-color: {secondaryBackgroundColor};            
            }}
            div.stButton > button:hover {{
                border-color: {primaryColor};
                color: {primaryColor};
            }}
            
            div.stButton > button:active {{
                border-color: {primaryColor};
                color: {textColor};
                outline-color: {primaryColor};
                box-shadow: 0px 0px 5px 5px {primaryColor};
                background-color: {backgroundColor};
            }}
            
            div.stButton > button:focus:not(:active) {{
            border-color: {primaryColor};
            box-shadow: none;
            color: #ffffff;
            background-color: {backgroundColor};
            }}
            
                        
        
            </style>""", unsafe_allow_html=True)



def bmac():

    if 'bmcbutton' in st.session_state:
        html(st.session_state.bmcbutton, width=74, height=80)

        st.markdown(
            """
            <style>
                iframe[width="74"] {
                    position: fixed;
                    top: 5%;
                    right: 0%;
                }
            </style>
            """,
            unsafe_allow_html=True,
        )
