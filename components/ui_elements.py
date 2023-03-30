import streamlit as st
from streamlit_tags import st_tags, st_tags_sidebar
import components.product_manager as product_manager
import components.data_handler as data_handler
from components.custom.pagebrowser import pagebrowser


def hide_header():
    hide_decoration_bar_style = '<style>header {visibility: hidden;}</style>'
    st.markdown(hide_decoration_bar_style, unsafe_allow_html=True)



def submit_feature_form(admin):

    with st.form("submit_feature", clear_on_submit=True):
        index = product_manager.get_product_index()
        st.write('Product:')
        new_product = st.selectbox('Product', options=st.session_state['products'], index=index,
                                        label_visibility='collapsed')
        st.write('Category:')
        new_category = st.selectbox('Category', options=product_manager.categories, label_visibility='collapsed')
        st.write('Title:')
        new_feature_name = st.text_input('Feature name', label_visibility='collapsed')
        st.write('Description:')
        new_feature_description = st.text_area('Feature description', label_visibility='collapsed')
        new_tags = st_tags(
            label='Enter tags:',
            text='Press enter to add more',
            value=[],
            suggestions=['five', 'six', 'seven', 'eight', 'nine', 'three', 'eleven', 'ten', 'four'],
            maxtags=20)
        if admin:
            st.write('Status')
            status = st.selectbox('Status', options=st.session_state['feature_states'], index=1,
                                            label_visibility='collapsed')
            button = 'Add'
        else:
            button = 'Submit'

        submitted_feature = st.form_submit_button(button)
        if submitted_feature:
            if admin:
                user = 1
                can_submit = True
            else:
                if product_manager.check_user():
                    user = st.session_state.user_id
                    status = 'new'
                    can_submit = True
                else:
                    can_submit = False
            if can_submit:
                if new_feature_name and new_feature_description:

                    result = data_handler.submit_feature(product_manager.get_product_table_id(),
                                                         new_feature_name,
                                                         new_feature_description,
                                                         new_tags,
                                                         new_category,
                                                         user,
                                                         status)
                    if result == 'Feature added successfully':
                        st.info(result)
                    else:
                        st.warning(result)
                else:
                    st.warning('Enter a valid feature name and description.')


def del_data():
    if 'data' in st.session_state:
        del st.session_state['data']


def approve(feature):
    data_handler.update_feature_status(feature, 'active')


def reject(feature):
    data_handler.update_feature_status(feature, 'rejected')


def delete(feature):
    data_handler.update_feature_status(feature, 'deleted')


def update(feature):
    st.write('Update: '+str(feature))


def show(feature):
    st.session_state['show_feature'] = True
    st.session_state['active_feature'] = feature


def show_feature(feature):
    feat = data_handler.fetch_feature_by_id(feature)
    st.write(feat)

def upvote(feature_id):
    if product_manager.check_user():
        data_handler.register_upvote(feature_id, st.session_state.user_id)


def list_view(type):
    if type == 'feature_backlog':
        if 'feature_backlog_page' not in st.session_state:
            st.session_state['feature_backlog_page'] = 0
            st.session_state['feature_backlog_next'] = False

        df = data_handler.fetch_features_by_product_status(product_manager.get_product_table_id(),
                                                           'active',
                                                           st.session_state['feature_backlog_page'],
                                                           "vote_count DESC")
        if not df.empty or st.session_state.feature_backlog_next:
            st.write('---')
            for ind, feature in df.iterrows():
                feature_id = feature.feature_id
                clbt, col1, col2, col3, col4 = st.columns([1, 2, 3, 1, 1])
                clbt.button('Show', key='show' + str(ind), on_click=show, args=[feature_id])
                col1.write(feature.feature_name)
                col2.write(feature.feature_description)
                col3.write(str(feature.vote_count))
                col4.button('Upvote', key='upvote' + str(ind), on_click=upvote, args=[feature_id])
                st.write('---')
            st.session_state['feature_backlog_page'], st.session_state['feature_backlog_next'], reload = page_browser(df, st.session_state['feature_backlog_page'], 'feature_backlog')

            if reload:
                st.experimental_rerun()
        else:
            st.write('No open feature requests. Submit one?')
    if type == 'approve':
        if 'approve_page' not in st.session_state:
            st.session_state['approve_page'] = 0
            st.session_state['approve_next'] = False

        df = data_handler.fetch_features_by_status_with_mail('new', st.session_state['approve_page'])
        if not df.empty or st.session_state.approve_next:
            st.header('Approve feature requests')
            st.write('---')
            for ind, feature in df.iterrows():
                feature_id = feature.feature_id
                col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 4, 2, 1, 1])
                col1.write(feature['product_id'])
                col2.write(feature.feature_name)
                col3.write(feature.feature_description)
                col4.write(feature.user_mail)
                col5.button('Approve', key='approve' + str(ind), on_click=approve, args=[feature_id])
                col6.button('Reject', key='reject' + str(ind), on_click=reject, args=[feature_id])

                st.write('---')
            st.session_state['approve_page'], st.session_state['approve_next'], reload = page_browser(
                df, st.session_state['approve_page'], 'approve_page')

            if reload:
                st.experimental_rerun()

    if type == 'edit_features':
        if 'edit_features_page' not in st.session_state:
            st.session_state['edit_features_page'] = 0
            st.session_state['edit_features_next'] = False
        df = data_handler.fetch_features_by_status_with_mail('active', st.session_state['edit_features_page'])
        if not df.empty or st.session_state.edit_features_next:
            st.header('Edit or delete features')
            st.write('---')

            for ind, feature in df.iterrows():
                feature_id = feature.feature_id
                col1, col2, col3, col4, col5, col6 = st.columns([1, 2, 4, 2, 1, 1])
                col1.write(feature['product_id'])
                col2.write(feature.feature_name)
                col3.write(feature.feature_description)
                col4.write(feature.user_mail)
                col5.button('Update', key='update' + str(ind), on_click=update, args=[feature_id])
                col6.button('Delete', key='delete' + str(ind), on_click=delete, args=[feature_id])

                st.write('---')

            st.session_state['edit_features_page'], st.session_state['edit_features_next'], reload = page_browser(
                df, st.session_state['edit_features_page'], 'edit_features_page')

            if reload:
                st.experimental_rerun()




def page_browser(data, page, name):
    reload_data = False
    key = "pb"+name
    next = True
    value = pagebrowser(bgc=st.session_state['backgroundColor'],
                        txc=st.session_state['textColor'],
                        pgn=page, dte=data.empty,
                        key=key)
    if value == 1:
        page = 0
        reload_data = True
    elif value == 2:
        page = page - 1
        reload_data = True
    elif value == 3:
        page = page + 1
        reload_data = True

    if page == 0:
        next = False

    del st.session_state[key]

    return page, next, reload_data

