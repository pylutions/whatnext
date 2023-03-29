import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
import components.initializer as initializer
import components.data_handler as data_handler
import components.ui_elements as ui_elements


if __name__ == "__main__":
    st.set_page_config(page_title="What next?", page_icon="icon.ico", layout="wide")
    initializer.stylize()
    ui_elements.hide_header()
    st.title('Admin page')
    initializer.initialize()
    if 'admin_logged_in' not in st.session_state:
        with st.form("admin_signin"):
            st.write("Please provide admin credentials:")
            user_name = st.text_input('Admin')
            password = st.text_input('Password', type="password")
            login = st.form_submit_button("Login")
            if login:
                if user_name == st.secrets.admin and password == st.secrets.password:
                    st.session_state['admin_logged_in'] = True
                    st.session_state['admin'] = user_name
                    data_handler.create_user('Admin', 0)
                    st.experimental_rerun()
                else:
                    st.warning('Wrong credentials!')
    elif st.session_state.admin_logged_in:
        st.sidebar.header('Welcome, ' + st.session_state['admin'] + '!')
        tab1, tab2 = st.tabs(['Feature management', 'Data & analytics'])
        with tab1:
            ui_elements.list_view('approve')

            col1, col2 = st.columns(2)
            with col1:
                st.header('Add a product')
                with st.form("submit_product", clear_on_submit=True):
                    new_product_name = st.text_input('Product name')
                    new_product_url = st.text_input('Product url')
                    submitted_product = st.form_submit_button("Add")
                    if submitted_product:
                        if new_product_name and new_product_url:
                            result = data_handler.submit_product(new_product_name, new_product_url)
                            if result == 'Product created successfully':
                                st.info(result)
                            else:
                                st.warning(result)
                        else:
                            st.warning('Enter a valid product name and URL.')
                if st.session_state.has_products:
                    st.header('Edit products')
                    with st.form("edit_products"):
                        for ind, product in st.session_state.products_table.iterrows():
                            c1, c2, c3 = st.columns(3)
                            product_id = str(product['product_id'])
                            c1.text_input('Product', value=product['product'], label_visibility='collapsed', key="prod"+product_id)
                            c2.text_input('URL', value=product['url'], label_visibility='collapsed', key="url"+product_id)
                            if product['state'] == 'active':
                                check = True
                            else:
                                check = False
                            c3.checkbox('Active', value=check, key="active"+product_id)

                        edit_product = st.form_submit_button("Save")
                        if edit_product:
                            st.write('edit')

            with col2:
                st.header('Add a feature')
                if st.session_state.has_products:
                    ui_elements.submit_feature_form(True)
                else:
                    st.write('No products yet, add one first.')

            ui_elements.list_view('edit_features')




        with tab2:
            st.header('Analytics')
    initializer.bmac()
