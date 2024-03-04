import streamlit as st
import pandas as pd
import base64
from datetime import timedelta
from couchbase.exceptions import CouchbaseException, DocumentNotFoundException
from couchbase.auth import PasswordAuthenticator
from couchbase.cluster import Cluster, QueryOptions
from couchbase.options import ClusterOptions
import json
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

# User Input
endpoint = st.text_input("Couchbase Endpoint", "couchbases://cb.wepvz44n89bkywd0.cloud.couchbase.com")
username = st.text_input("Couchbase Username", "abhijeet")
password = st.text_input("Couchbase Password", "Password@P1", type="password")
bucket_name = st.text_input("Couchbase Bucket Name", "sales_data")
scope_name = "_default"

# Connect options - authentication
auth = PasswordAuthenticator(username, password)

# Get a reference to our cluster
options = ClusterOptions(auth)

# Use the pre-configured profile below to avoid latency issues with your connection.
options.apply_profile("wan_development")

# Cluster and bucket setup with error handling
try:
    cluster = Cluster(endpoint, options)
    cluster.wait_until_ready(timedelta(seconds=5))
    cb = cluster.bucket(bucket_name)
    collection = cb.default_collection()
except Exception as e:
    st.error(f"Error connecting to Couchbase: {e}")
    exit(1)

# Create a N1QL query to fetch all keys
query = f'SELECT META().id FROM `{bucket_name}`'

# Execute the query
result = cluster.query(query)

# Get all keys
keys = [row['id'] for row in result.rows()]

# Get the sales data for all keys
sales_data_dict = {}
for key in keys:
    try:
        result = collection.get(key)
        sales_data_dict[key] = result.content_as[dict]
    except DocumentNotFoundException:
        continue

# Now sales_data_dict is a dictionary where:
#   - the keys are the document keys
#   - the values are the corresponding documents

# Create an empty DataFrame to store all sales data
df = pd.DataFrame()

# Loop over sales_data_dict to process each sales data document
for key, sales_data in sales_data_dict.items():
    if isinstance(sales_data, dict):
        temp_df = pd.DataFrame(sales_data, index=[0])
    else:
        temp_df = pd.DataFrame(sales_data)
    df = pd.concat([df, temp_df], ignore_index=True)

# Pages
page = st.sidebar.selectbox("Choose a page", ["Data Exploration", "Data Visualization"])

if page == "Data Exploration":
    # Display the DataFrame
    st.write(df)

    # Data Download
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # some strings <-> bytes conversions necessary here
    href = f'<a href="data:file/csv;base64,{b64}">Download CSV File</a> (right-click and save as &lt;some_name&gt;.csv)'
    st.markdown(href, unsafe_allow_html=True)

elif page == "Data Visualization":
    if df is not None:  # Check if df is not None before using it
        # Display different types of charts
        st.plotly_chart(px.line(df, x='month', y='sales', color='product'))

        # For pie chart, we use matplotlib
        fig, ax = plt.subplots()
        ax.pie(df['sales'], labels=df['product'], autopct='%1.1f%%')
        st.pyplot(fig)

        # For plotly chart
        fig = px.bar(df, x='product', y='sales', color='month')
        st.plotly_chart(fig)

        # For altair chart
        chart = alt.Chart(df).mark_bar().encode(
            x='product',
            y='sales',
            color='month'
        )
        st.altair_chart(chart)

        # For Vega Lite chart
        st.vega_lite_chart(df, {
            'mark': 'bar',
            'encoding': {
                'x': {'field': 'product', 'type': 'nominal'},
                'y': {'field': 'sales', 'type': 'quantitative'},
                'color': {'field': 'month', 'type': 'nominal'}
            }
        })