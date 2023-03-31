import streamlit as st
import mysql.connector
import pandas as pd
from datetime import datetime


def checkdbc(dbc):
    return dbc.is_connected()


#@st.cache_resource(validate=checkdbc)
def get_database_connection():
    if 'dbc' not in st.session_state:
        st.session_state['dbc'] = mysql.connector.connect(**st.secrets["feature_db"])

    if not st.session_state['dbc'].is_connected():
        st.session_state['dbc'] = mysql.connector.connect(**st.secrets["feature_db"])

    return st.session_state['dbc']


def get_products(force):
    if 'products' not in st.session_state or force:
        query = "SELECT * FROM products"
        result = fetch_features(query)
        st.session_state['products_table'] = result #pd.DataFrame(result, columns=['product', 'url'])
    if st.session_state['products_table'].empty:
        return False
    else:
        st.session_state['products'] = st.session_state['products_table'][['product', 'url']]
        return True


def version_control(version, version_note):
    try:
        dbc = get_database_connection()
        cursor = dbc.cursor()
        query = "SELECT COUNT(*) FROM information_schema.tables WHERE table_name = 'version_history'"
        cursor.execute(query)
        if cursor.fetchone()[0] == 1:
            query = "SELECT version from version_history"
            cursor.execute(query)
            fetched = cursor.fetchall()
            cols = cursor.column_names
            df = pd.DataFrame(fetched, columns=cols)

            cursor.close()
            if df['version'].max() < version:
                st.write('upgrade required')
                return False
            else:
                return True
        else:
            tables = (
                ('version_history',
                 "(version INT PRIMARY KEY, version_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, version_note VARCHAR(1023))"),
                ('products',
                 "(product_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, product VARCHAR(255), url VARCHAR(255), state VARCHAR(255))"),
                ('users',
                 "(user_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, user_mail VARCHAR(255), essential BOOL, newsletter BOOL, join_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, auto_approve_comments BOOL DEFAULT 0), banned BOOL DEFAULT 0"),
                ('features',
                 "(feature_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, product_id int, feature_name VARCHAR(255), feature_description VARCHAR(1023), tags VARCHAR(1023), category VARCHAR(255), submitted TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, done_date TIMESTAMP, submitter int, vote_count int, status VARCHAR(255), FOREIGN KEY (product_id) REFERENCES products(product_id), FOREIGN KEY (submitter) REFERENCES users(user_id))"),
                ('upvotes',
                 "(vote_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, feature_id INT, user_id INT, FOREIGN KEY (feature_id) REFERENCES features(feature_id), FOREIGN KEY (user_id) REFERENCES users(user_id))"),
                ('comments',
                 "(comment_id INT NOT NULL AUTO_INCREMENT PRIMARY KEY, comment VARCHAR(1023), vote_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, feature_id INT, user_id INT, status VARCHAR(255), FOREIGN KEY (feature_id) REFERENCES features(feature_id), FOREIGN KEY (user_id) REFERENCES users(user_id))")
            )

            for table in tables:
                query = f"CREATE TABLE IF NOT EXISTS {table[0]} {table[1]}"
                cursor.execute(query)
            sql = "INSERT IGNORE INTO version_history (version, version_note) VALUES (%s, %s)"
            values = (version, version_note)
            cursor.execute(sql, values)
            dbc.commit()

            cursor.close()
            return True
    except Exception as e:
        st.error('Something went wrong with the database connection. If you are the admin, please check the configuration.')
        st.write(e)





def fetch_from_table(table_name):
    dbc = get_database_connection()
    cursor = dbc.cursor()
    cursor.execute(f"SELECT * FROM {table_name}")
    fetched = cursor.fetchall()
    cols = cursor.column_names
    df = pd.DataFrame(fetched, columns=cols)
    return df


def fetch_features_by_product_status(product, status, page, orderby):
    start = page * st.session_state.step_size
    limit = str(start) + "," + str(st.session_state.step_size)
    clause = f" WHERE product_id={product} AND status='{status}'"
    query = "SELECT * FROM features" + clause + " ORDER BY "+orderby+" LIMIT " + limit
    return fetch_features(query)


def fetch_features_by_status_with_mail(status, page):
    start = page * st.session_state.step_size
    limit = str(start) + "," + str(st.session_state.step_size)
    clause = f" WHERE features.status='{status}'"
    query = "SELECT features.*, users.user_mail FROM features JOIN users ON features.submitter = users.user_id" + clause +" LIMIT " + limit
    return fetch_features(query)

def fetch_feature_by_id(fid):
    query = f"SELECT * FROM features WHERE feature_id={fid}"
    return fetch_features(query)

def fetch_features(query):
    dbc = get_database_connection()
    cursor = dbc.cursor()
    cursor.execute(query)
    fetched = cursor.fetchall()
    cols = cursor.column_names
    df = pd.DataFrame(fetched, columns=cols)
    return df


def register_upvote(feature, user):
    dbc = get_database_connection()
    cursor = dbc.cursor()
    values = (feature, user)
    sql = f"SELECT * FROM upvotes WHERE feature_id={feature} AND user_id={user}"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result:
        st.session_state['display_user_error'] = ('info', 'You have already voted for this feature.')
    else:
        sql = "INSERT IGNORE INTO upvotes (feature_id, user_id) VALUES (%s, %s)"
        cursor.execute(sql, values)
        query = "UPDATE features SET vote_count = vote_count + 1 WHERE feature_id = %s"
        values = (feature,)
        cursor.execute(query, values)
        dbc.commit()
        st.session_state['display_user_error'] = ('info', 'Thanks for voting!')


def update_feature_status(feature, status):
    dbc = get_database_connection()
    cursor = dbc.cursor()
    done_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    if status == 'done':
        query = f"UPDATE features SET status='{status}' AND done_date='{done_date}' WHERE feature_id={feature}"
    else:
        query = f"UPDATE features SET status='{status}' WHERE feature_id={feature}"
    cursor.execute(query)
    dbc.commit()


def create_user(user_mail, newsletter):
    dbc = get_database_connection()
    cursor = dbc.cursor()
    sql = "INSERT IGNORE INTO users (user_mail, newsletter) VALUES (%s, %s)"
    values = (user_mail, newsletter)
    cursor.execute(sql, values)
    dbc.commit()
    return cursor.lastrowid

def update_user(user_id, user_mail, essential, newsletter):
    clause = f" WHERE user_id='{user_id}'"
    query = f"UPDATE users SET essential={essential}, newsletter={newsletter}, user_mail='{user_mail}'" + clause
    dbc = get_database_connection()
    cursor = dbc.cursor()
    cursor.execute(query)
    dbc.commit()


def get_user_id(user_mail, essential, newsletter):
    clause = f" WHERE user_mail='{user_mail}'"
    query = "SELECT user_id, essential, newsletter FROM users" + clause
    dbc = get_database_connection()
    cursor = dbc.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    if result:
        st.session_state['user_id'] = result[0]
        st.session_state['essential'] = result[1]
        st.session_state['newsletter'] = result[2]
    else:
        sql = "INSERT IGNORE INTO users (user_mail, essential, newsletter) VALUES (%s, %s, %s)"
        values = (user_mail, essential, newsletter)
        cursor.execute(sql, values)
        dbc.commit()
        st.session_state['user_id'] = cursor.lastrowid


def submit_feature(product, feature_name, feature_description, tags, category, submitter, status):
    tags = ';'.join(tags)
    dbc = get_database_connection()
    cursor = dbc.cursor()
    query = "INSERT INTO features (product_id, feature_name, feature_description, tags, category, submitter, vote_count, status) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    values = (product, feature_name, feature_description, tags, category, submitter, 0, status)
    cursor.execute(query, values)
    dbc.commit()
    return 'Feature added successfully'


def submit_product(product_name, product_url):
    # check if product already exists
    if st.session_state.has_products:
        if product_name in st.session_state['products']['product'].values:
            return 'Product already exists!'
    dbc = get_database_connection()
    cursor = dbc.cursor()
    query = "INSERT INTO products (product, url, state) VALUES (%s, %s, %s)"
    values = (product_name, product_url, 'active')
    cursor.execute(query, values)
    dbc.commit()
    st.session_state['has_products'] = get_products(True)
    return 'Product created successfully'



