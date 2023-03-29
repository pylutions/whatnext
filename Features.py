import streamlit as st
import components.data_handler as data_handler
import components.initializer as initializer
import components.product_manager as product_manager
import components.ui_elements as ui_elements


def show_sidebar():
    with st.sidebar:
        st.header("Welcome to the public backlog!")
        st.write("Upvote the features you care about or submit new requests.")

        #product_index = product_manager.get_product_index()
        #st.session_state['selected_product'] = st.selectbox('Product', options=st.session_state['products'], index=product_index)
        #st.write('---')
        st.write("For participating, please enter a valid e-mail address.")
        if 'user_mail' in st.session_state:
            mail = st.session_state.user_mail
        else:
            mail = ''
        st.session_state.user_mail = st.text_input('E-Mail', placeholder='me@email.com', label_visibility='collapsed', value=mail)
        st.checkbox('Updates about your feature requests and upvotes.', key='user_essential')
        st.checkbox('Other product updates. No spam, just updates.', key='user_agreement')
        if 'display_user_error' in st.session_state:
            if st.session_state.display_user_error[0] == 'error':
                st.error(st.session_state.display_user_error[1])
            elif st.session_state.display_user_error[0] == 'info':
                st.info(st.session_state.display_user_error[1])
            del st.session_state.display_user_error





if __name__ == "__main__":
    st.set_page_config(page_title="What next?", page_icon="icon.ico", layout="wide")
    initializer.stylize()
    ui_elements.hide_header()
    tcol1, tcol2 = st.columns(2)
    tcol1.title('What next?')

    initializer.initialize()


    if st.session_state['has_products']:
        show_sidebar()
        feedback = st.sidebar.empty()
        #
        with tcol2:
            product_index = product_manager.get_product_index()
            st.session_state['selected_product'] = st.selectbox('Product', options=st.session_state['products'],
                                                                index=product_index)
        url = product_manager.get_product_url()
        tcol2.write("Current product is: **" + st.session_state.selected_product + "** (more: " + url + ")")
        tab1, tab2, tab3 = st.tabs(['Feature backlog', 'Submit feature', 'Account'])
        with tab1:
            col1, col2, col3 = st.columns([3, 2, 1])
            col1.header('Feature backlog')
            col2.text_input('Search features')
            col3.button('Refresh')

            ui_elements.list_view('feature_backlog')


        with tab2:
            st.header('Submit a request')
            ui_elements.submit_feature_form(False)
        with tab3:
            st.write("Welcome to the future, when there is proper authentication and everything.")
    else:
        st.write(f'The admin of **{st.session_state.tenant}** has not added any products yet.')

    initializer.bmac()
