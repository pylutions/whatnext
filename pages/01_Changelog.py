import streamlit as st
import components.initializer as initializer
import components.data_handler as data_handler
import components.ui_elements as ui_elements
import components.product_manager as product_manager
from components.custom.pagebrowser import pagebrowser


if __name__ == "__main__":
    st.set_page_config(page_title="What next?", page_icon="icon.ico", layout="wide")
    initializer.stylize()
    ui_elements.hide_header()
    tcol1, tcol2 = st.columns(2)
    tcol1.title('Changelog')
    initializer.initialize()
    if st.session_state['has_products']:
        with tcol2:
            product_index = product_manager.get_product_index()
            st.session_state['selected_product'] = st.selectbox('Product', options=st.session_state['products'],
                                                                index=product_index)
        url = product_manager.get_product_url()
        tcol2.write("Current product is: **" + st.session_state.selected_product + "** (more: " + url + ")")

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


    def button1_function():
        st.write("Button 1 was clicked!")


    def button2_function():
        st.write("Button 2 was clicked!")

    bg = st.get_option('theme.backgroundColor')
    tx = st.get_option('theme.textColor')
    st.write(bg)

    st.markdown(f"""
    <style>
        .xxx {{
            background-color: {bg};
            color: white;
            font-weight: bold;
            border-radius: 5px;
            padding: 10px;
            margin-right: 10px;
        }}
    </style>

    <div style="display:flex;">
        <button class="xxx" onclick="button1_function()">Button 1</button>
        <button class="xxx" onclick="button2_function()">Button 2</button>
    </div>
    """, unsafe_allow_html=True)

    value = pagebrowser(bgc=bg, txc=tx, pgn=1, dte=True)
    if value == 1:
        st.write('btn 1')
    st.button('Button 1')

    initializer.bmac()
