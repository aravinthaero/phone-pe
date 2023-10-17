import mysql.connector
import pandas as pd
import streamlit as st
import plotly.express as px

# Establish a connection to the database
conn = mysql.connector.connect(user='root', password='123456', host='localhost', database='project')
cursor = conn.cursor()

# Create a Streamlit app
st.title('PhonePe Pulse Data Visualization')

# Sidebar menu
with st.sidebar:
    selected = st.selectbox("Menu", ["Home", "Top Charts", "Explore Data", "District","About"], index=0)

# Define the "Home" section
if selected == "Home":
    st.markdown("# :violet[Data Visualization and Exploration]")
    st.markdown("## :violet[A User-Friendly Tool Using Streamlit and Plotly]")
    col1, col2 = st.columns([3, 2], gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[Technologies used:] Github Cloning, Python, Pandas, MySQL, mysql-connector-python, Streamlit, and Plotly.")
        st.markdown("### :violet[Overview:] In this Streamlit web app, you can visualize the PhonePe Pulse data and gain insights on transactions, users, top states, districts, pincodes, and more using bar charts, pie charts, and geo map visualizations.")

# Define the "Top Charts" section
if selected == "Top Charts":
    st.markdown("## :violet[Top Charts]")
    
    Type = st.sidebar.selectbox("**Type**", ("Transactions", "Users"))
    
    col1, col2 = st.columns([1, 1.5], gap="large")
    
    with col1:
        Year = st.slider("**Year**", min_value=2018, max_value=2022)
        Quarter = st.slider("Quarter", min_value=1, max_value=4)
    
    with col2:
        st.info(
            """
            #### From this menu, we can get insights like:
            - Overall ranking on a particular Year and Quarter.
            - Top 10 State, District, Pincode based on Total number of transactions and Total amount spent on PhonePe.
            - Top 10 State, District, Pincode based on Total PhonePe users and their app opening frequency.
            - Top 10 mobile brands and their percentage based on how many people use PhonePe.
            """, icon="🔍"
        )
        

    # User input for the table name
    table_name = st.selectbox('Select a table from the database', ['agg_user', 'agg_trans', 'map_tran', 'map_user', 'top_tran', 'top_users'])

    # Check if a table name is provided
    if table_name:
        # Execute a SELECT query to retrieve data from the specified table
        query = f"SELECT * FROM {table_name} WHERE Transaction_Year = {Year} AND Quarters = {Quarter}"
        cursor.execute(query)

        # Fetch the data into a DataFrame
        data = cursor.fetchall()
        df = pd.DataFrame(data, columns=[column[0] for column in cursor.description])

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Data Table
        st.subheader('Data Table')
        st.write(df)

        # Data Visualization
        st.subheader('Data Visualization')
        x_column = st.selectbox('Select X-Axis Column', df.columns)
        y_column = st.selectbox('Select Y-Axis Column', df.columns)
        title = st.text_input('Chart Title', f'{table_name} Data Visualization')
        fig = px.bar(df, x=x_column, y=y_column, title=title)
        st.plotly_chart(fig)

        # Add a pie chart
        st.subheader('Pie Chart')

        # Let the user select the column for the pie chart
        pie_column = st.selectbox('Select Data Column for Pie Chart', df.columns)

        # Create a pie chart using Plotly Express
        pie_fig = px.pie(df, names=pie_column, title=f'{table_name} Pie Chart')

        st.plotly_chart(pie_fig)

    # You can add more interactive elements and customization as needed.

if selected == "Explore Data":
        conn = mysql.connector.connect(user='root', password='123456', host='localhost', database='project')
        cursor = conn.cursor()

    # Create a Streamlit app
        st.title('Data Visualization for PhonePe Pulse Tables')

    # Sidebar menu
        with st.sidebar:
            table_name = st.selectbox('Select a table from the database', ['agg_user', 'agg_trans', 'map_tran', 'top_tran'])
            selected = st.selectbox("Menu", ["Bar Chart", "Pie Chart"], index=0)

        # Define the "Bar Chart" section
        if selected == "Bar Chart":
            st.markdown("## :violet[Bar Chart]")

            # User input for the year
            year = st.slider("Select Year", min_value=2018, max_value=2022)

            # Execute a query to retrieve data for the specified year
            cursor.execute(f"SELECT States, SUM(Transaction_Count) AS Total_Transactions FROM {table_name} WHERE Transaction_Year = {year} GROUP BY States ORDER BY States")
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=['State', 'Total_Transactions'])

            # Create a bar chart using Plotly Express
            fig = px.bar(df, x='State', y='Total_Transactions', title=f'Transactions by State for {year}')
            st.plotly_chart(fig)

        # Define the "Pie Chart" section
        if selected == "Pie Chart":
            st.markdown("## :violet[Pie Chart]")

            # User input for the year
            year = st.slider("Select Year", min_value=2018, max_value=2022)

            # Execute a query to retrieve data for the specified year
            cursor.execute(f"SELECT States, SUM(Transaction_Count) AS Total_Transactions FROM {table_name} WHERE Transaction_Year = {year} GROUP BY States ORDER BY States")
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=['State', 'Total_Transactions'])

            # Create a pie chart using Plotly Express
            fig = px.pie(df, names='State', values='Total_Transactions', title=f'Transactions by State for {year}')
            st.plotly_chart(fig)

        # Close the cursor and connection
        cursor.close()
        conn.close()

if selected== "District":

        

        conn = mysql.connector.connect(user='root', password='123456', host='localhost', database='project')
        cursor = conn.cursor()

        # Create a Streamlit app
        st.title('Total Transaction Amount for PhonePe Pulse Tables')

        # Sidebar menu
        with st.sidebar:
            table_name = st.selectbox('Select a table from the database', ['agg_user', 'agg_trans', 'map_tran', 'top_tran'])

            # Dynamically populate the state and district select boxes based on the table columns
            cursor.execute(f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}'")
            columns = [column[0] for column in cursor.fetchall()]

            selected_state = 'All'
            selected_district = 'All'

            if 'States' in columns:
                states_query = f"SELECT DISTINCT States FROM {table_name}"
                cursor.execute(states_query)
                state_results = cursor.fetchall()
                state_values = ['All'] + [result[0] for result in state_results]
                selected_state = st.selectbox('Select State', state_values)

            if 'District' in columns:
                if selected_state == 'All':
                    district_values = ['All']
                else:
                    districts_query = f"SELECT DISTINCT District FROM {table_name} WHERE States = '{selected_state}'"
                    cursor.execute(districts_query)
                    district_results = cursor.fetchall()
                    district_values = ['All'] + [result[0] for result in district_results]
                selected_district = st.selectbox('Select District', district_values)

        # User input for the year
        year = st.slider("Select Year", min_value=2018, max_value=2022)

        # Build the SQL query based on state and district filters
        query = f"SELECT SUM(Transaction_Count) AS Total_Transactions FROM {table_name} WHERE Transaction_Year = {year}"

        if selected_state != 'All':
            query += f" AND States = '{selected_state}'"

        if selected_district != 'All':
            query += f" AND District = '{selected_district}'"

        cursor.execute(query)
        total_transaction_amount = cursor.fetchone()[0]

        # Display the total transaction amount in a larger font size using HTML
        st.markdown(f'<p style="font-size:36px">{total_transaction_amount}</p>', unsafe_allow_html=True)

        # Close the cursor and connection
        cursor.close()
        conn.close()

if selected == "About":
    col1,col2 = st.columns([3,3],gap="medium")
    with col1:
        st.write(" ")
        st.write(" ")
        st.markdown("### :violet[About PhonePe Pulse:] ")
        st.write("##### BENGALURU, India, On Sept. 3, 2021 PhonePe, India's leading fintech platform, announced the launch of PhonePe Pulse, India's first interactive website with data, insights and trends on digital payments in the country. The PhonePe Pulse website showcases more than 2000+ Crore transactions by consumers on an interactive map of India. With  over 45% market share, PhonePe's data is representative of the country's digital payment habits.")
        
        st.write("##### The insights on the website and in the report have been drawn from two key sources - the entirety of PhonePe's transaction data combined with merchant and customer interviews. The report is available as a free download on the PhonePe Pulse website and GitHub.")
        
        st.markdown("### :violet[About PhonePe:] ")
        st.write("##### PhonePe is India's leading fintech platform with over 300 million registered users. Using PhonePe, users can send and receive money, recharge mobile, DTH, pay at stores, make utility payments, buy gold and make investments. PhonePe forayed into financial services in 2017 with the launch of Gold providing users with a safe and convenient option to buy 24-karat gold securely on its platform. PhonePe has since launched several Mutual Funds and Insurance products like tax-saving funds, liquid funds, international travel insurance and Corona Care, a dedicated insurance product for the COVID-19 pandemic among others. PhonePe also launched its Switch platform in 2018, and today its customers can place orders on over 600 apps directly from within the PhonePe mobile app. PhonePe is accepted at 20+ million merchant outlets across Bharat")
        
       
    with col2:
        st.write(" ")
        st.write(" ")
        st.write(" ")
        st.write(" ")