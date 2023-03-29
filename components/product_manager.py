import streamlit as st
import components.data_handler as data_handler
import re
from streamlit.components.v1 import html


categories = ['Feature', 'Bug']


regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

def is_valid(email):
    if re.fullmatch(regex, email):
      return True
    else:
      return False


def get_product_index():
    index = 0
    if 'query_product' in st.session_state:
        if st.session_state.query_product in st.session_state.products['product'].values:
            index = st.session_state.products[st.session_state.products['product'] == st.session_state.query_product].index[0]
            index = int(index)
    return index


def get_product_url():
    url = st.session_state.products.loc[st.session_state.products['product'] == st.session_state.selected_product].values[0, 1]
    return url


def get_product_table_id():
    id = st.session_state.products_table.loc[st.session_state.products_table['product'] == st.session_state.selected_product].values[0, 0]
    return id


def check_user():
    # is called when the user first does something, e.g. upvote or submit
    if 'user_mail' in st.session_state:
        if 'checked_mail' in st.session_state:
            if st.session_state.checked_mail == st.session_state.user_mail:
                return True
        if is_valid(st.session_state.user_mail):
            data_handler.get_user_id(st.session_state.user_mail, st.session_state.user_essential, st.session_state.user_agreement)
            if 'user_id' in st.session_state:
                st.session_state['checked_mail'] = st.session_state.user_mail
                return True
            else:
                return False
        else:
            st.session_state['display_user_error'] = ('error', 'Invalid email address!')
            scr = """
                     <script type="text/javascript">alert("For voting and submitting please enter a valid email address in the sidebar.");</script>
                     """
            html(scr)
            return False
    else:
        return False
