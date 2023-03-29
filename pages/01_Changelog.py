import streamlit as st
import components.initializer as initializer
import components.data_handler as data_handler
import components.ui_elements as ui_elements
import components.product_manager as product_manager
from datetime import datetime


if __name__ == "__main__":
    st.set_page_config(page_title="What next?", page_icon="icon.ico", layout="wide")
    initializer.stylize()
    ui_elements.hide_header()
    st.title('Changelog')
    initializer.initialize()
    if st.session_state['has_products']:

        df = data_handler.fetch_features_by_product_status(product_manager.get_product_table_id(),
                                                           'done',
                                                            st.session_state.feature_page,
                                                           "done_date"
                                                           )
        if not df.empty or st.session_state['next_page']:
            st.write('---')
            for ind, feature in df.iterrows():
                feature_id = feature.feature_id
                col1, col2, col3, col4 = st.columns([2, 4, 1, 1])
                col1.write(feature.feature_name)
                col2.write(feature.feature_description)
                col3.write(str(feature.vote_count))
                st.write('---')
            ui_elements.page_browser(df)
        #st.set_option('theme.primaryColor', 'white')



    else:
        st.write(f'The admin of **{st.session_state.tenant}** has not added any products yet.')

    initializer.bmac()