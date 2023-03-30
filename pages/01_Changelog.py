import streamlit as st
import components.initializer as initializer
import components.data_handler as data_handler
import components.ui_elements as ui_elements
import components.product_manager as product_manager


if __name__ == "__main__":
    st.set_page_config(page_title="What next?", page_icon="icon.ico", layout="wide")
    ui_elements.hide_header()
    tcol1, tcol2 = st.columns(2)
    tcol1.title('Changelog')
    if initializer.initialize():
        #initializer.stylize()
        if st.session_state['has_products']:
            with tcol2:
                product_index = product_manager.get_product_index()
                st.session_state['selected_product'] = st.selectbox('Product', options=st.session_state['products'],
                                                                    index=product_index)
            url = product_manager.get_product_url()
            tcol2.write("Current product is: **" + st.session_state.selected_product + "** (more: " + url + ")")

            ui_elements.list_view('changelog')



        else:
            st.write(f'The admin of **{st.session_state.tenant}** has not added any products yet.')

        initializer.bmac()
