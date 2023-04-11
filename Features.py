import streamlit as st
import components.data_handler as data_handler
import components.initializer as initializer
import components.product_manager as product_manager
import components.ui_elements as ui_elements



def register(container):
    with st.form(key='reg'+str(container)):
        if 'user_mail' in st.session_state:
            mail = st.session_state.user_mail
        else:
            mail = ''
        st.session_state.user_mail = st.text_input('E-Mail', placeholder='me@email.com',
                                                   label_visibility='collapsed', value=mail)

        if st.session_state['registered']:
            st.session_state['user_essential'] = st.checkbox('Updates about your feature requests and upvotes.',
                                                             value=st.session_state['user_essential'])
            st.session_state['user_agreement'] = st.checkbox('Other product updates. No spam, just updates.',
                                                             value=st.session_state['user_agreement'])
            btn_text = 'Update'
        else:
            btn_text = "Register/Sign in"
        register = st.form_submit_button(btn_text)
        if register:
            if product_manager.check_user():
                st.session_state['registered'] = True
                data_handler.update_user(st.session_state['user_id'],
                                         st.session_state['user_mail'],
                                         st.session_state['user_essential'],
                                         st.session_state['user_agreement'])

                st.experimental_rerun()


def show_sidebar():
    with st.sidebar:
        st.header("Welcome to the public backlog!")
        st.write("Upvote the features you care about or submit new requests.")

        #product_index = product_manager.get_product_index()
        #st.session_state['selected_product'] = st.selectbox('Product', options=st.session_state['products'], index=product_index)
        #st.write('---')
        st.write("For participating, please enter a valid e-mail address.")
        #if 'user_mail' in st.session_state:
        #    mail = st.session_state.user_mail
        #else:
        #    mail = ''

        register(0)
                #else:
                #    st.write('ooops')


        if 'display_user_error' in st.session_state:
            if st.session_state.display_user_error[0] == 'error':
                st.error(st.session_state.display_user_error[1])
            elif st.session_state.display_user_error[0] == 'info':
                st.info(st.session_state.display_user_error[1])
            del st.session_state.display_user_error





if __name__ == "__main__":
    st.set_page_config(page_title="What next?", page_icon="icon.ico", layout="wide")

    ui_elements.hide_header()
    tcol1, tcol2 = st.columns(2)
    tcol1.title('What next?')
    if initializer.initialize():
        #initializer.stylize()

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
                col1, col2, col3 = st.columns([4, 3, 1])
                col1.header('Feature backlog')
                col2.text_input('Search features')
                col3.write('')
                col3.write('')
                col3.button('Refresh')

                if st.session_state['show_feature']:

                    ui_elements.show_feature(st.session_state['active_feature'])

                    if st.button('Back'):
                        st.session_state['show_feature'] = False
                        st.experimental_rerun()
                else:
                    ui_elements.list_view('feature_backlog')


            with tab2:
                st.header('Submit a request')
                if st.session_state['registered']:
                    ui_elements.submit_feature_form(False)
                else:
                    register(2)
            with tab3:
                st.header('My account')
                if st.session_state['registered']:
                    st.write("Change preferences:")
                    with st.form("preferences"):
                        st.session_state['user_essential'] = st.checkbox('Updates about your feature requests and upvotes.',
                                                                             value=st.session_state['user_essential'])
                        st.session_state['user_agreement'] = st.checkbox('Other product updates. No spam, just updates.',
                                                                             value=st.session_state['user_agreement'])
                        change_pref = st.form_submit_button('Save')
                        if change_pref:
                            data_handler.update_user(st.session_state['user_id'],
                                                     st.session_state['user_mail'],
                                                     st.session_state['user_essential'],
                                                     st.session_state['user_agreement'])
                            st.experimental_rerun()
                    st.error("Danger zone")
                    if st.button('Delete all my data'):
                        data_handler.update_user(st.session_state['user_id'],
                                                 'deleted',
                                                 0,
                                                 0)
                        st.session_state.user_mail = ''
                        st.session_state['registered'] = False
                        st.experimental_rerun()
                else:
                    register(1)
        else:
            st.write(f'The admin of **{st.session_state.tenant}** has not added any products yet.')


        #if st.button('send mail'):
        #    data_handler.send_mail()
        initializer.bmac()
