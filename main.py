import os
import streamlit as st
import streamlit_authenticator as stauth
from DB_Authentication import sign_up
import mysql.connector
from cultivated_tab import CultivatedTab
from fertilizer import FertilizerTab
from fertilizer_type import Fertilizer_Type_Tab
from fuel import Fuel_Tab
from carbon_offset import carbon_offset
from carbon_footprint import carbon_footprint
import pandas as pd
from PolygonDraw import polygon
import snowflake.connector
from streamlit_elements import elements, mui, html, nivo, dashboard
from dotenv import load_dotenv

load_dotenv()
# Set page configuration
st.set_page_config(page_title='Streamlit', page_icon=":farmer:",initial_sidebar_state="collapsed", layout="wide",)

# Establish database connection
# mydb = mysql.connector.connect(
#     host=st.secrets.db_credentials.host,
#     user=st.secrets.db_credentials.user,
#     password=st.secrets.db_credentials.password,
#     database=st.secrets.db_credentials.database,
# )
# mydb = st.connection("snowflake")
account = os.getenv('account')
user = os.getenv('user_snow')
password = os.getenv('password')
role = os.getenv('role')
warehouse = os.getenv('warehouse')
database = os.getenv('database')
schema = os.getenv('schema')
# account="PIPWYPD-LO69630"
# user="suchanat"
# password="NuT0863771558-"
# role="ACCOUNTADMIN"
# warehouse="COMPUTE_WH"
# database="ECARBON"
# schema="ECARBON"

mydb = snowflake.connector.connect(
    user=user,
    password=password,
    account=account,
    warehouse=warehouse,
    database=database,
    schema=schema
)
mycursor = mydb.cursor()
print("Connection Established")
cultivated_areas_tab = CultivatedTab(mycursor, mydb)
fertilizer_tab = FertilizerTab(mycursor, mydb)
fer_type_tab = Fertilizer_Type_Tab(mycursor, mydb)
fuel_tab = Fuel_Tab(mycursor, mydb)
carbon_offset_tab = carbon_offset(mycursor, mydb)
carbon_footprint_tab = carbon_footprint(mycursor, mydb)


def convert_df(df):
    return df.to_csv(index=False).encode('utf-8')
@st.cache_data(show_spinner=False)
def split_frame(input_df, rows):
    df = [input_df.loc[i : i + rows - 1, :] for i in range(0, len(input_df), rows)]
    return df

try:
    mycursor.execute("SELECT * FROM farmer")
    result = mycursor.fetchall()
    emails = []
    usernames = []
    passwords = []
    email_1 = len(usernames)

    for user in result:
        emails.append(user[7])  # Assuming email is the first field in the tuple
        usernames.append(user[7])
        passwords.append(user[6])  # Assuming password is the second field in the tuple
    credentials = {'usernames': {}}  # Fix the key here

    for index in range(len(emails)):
        credentials['usernames'][usernames[index]] = {'name': emails[index], 'password': passwords[index]}
    st.sidebar.image("https://www.mitrphol.com/images/netzero/netzero.png")
    authenticator = stauth.Authenticate(credentials, cookie_name='Streamlit', key='abcdef', cookie_expiry_days=4)

    info, info1 = st.columns(2)
    if st.session_state.get('state') is None:
        st.session_state.state = 'home'

    if st.session_state.state != 'login':
        select = st.sidebar.selectbox(
            "ล็อคอิน/สมัครบัญชี",
            ("ล็อคอิน", "สมัครบัญชี"),
            key='unique_selection_bar_key',
        )
        if len(usernames) == 0:
            st.subheader("ไม่มีบัญชีในระบบ โปรดสมัครบัญชี")
            sign_up()
        else:
            if select == 'ล็อคอิน':
                email, authenticator_status, username = authenticator.login(
                    fields={'Form name': ':green[เข้าสู่ระบบ]', 'Username': ':blue[อีเมล]', 'Password': ':blue[รหัสผ่าน]',
                            'Login': 'ล็อคอิน'})
            elif select == 'สมัครบัญชี':
                sign_up()
    if username:
        if username in usernames:
            if st.session_state["authentication_status"]:
                # Set st.session_state.disabled to True after successful login

                # st.subheader('หน้าหลัก')
                DashOrCrud = st.sidebar.selectbox("หน้ารวมผล หรือ CRUD", ("หน้ารวมผล", "CRUD"))
                # Define custom CSS for the download button
                custom_css = """
                                <style>
                                    .stDownloadButton>button {
                                        background-color: #008CBA;
                                        color: white;
                                    }
                                    .stButton>button {
                                    background-color: #008CBA;
                                        color: white;
                                    }
                                </style>
                            """
                st.markdown(custom_css, unsafe_allow_html=True)
                if DashOrCrud == 'CRUD':
                    tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs(
                        ["พื้นที่ปลูก", "ปุ๋ย", "ชนิดปุ๋ย", "น้ำมัน", "การทดแทนคาร์บอน", "คาร์บอนฟุตพริ้นท์รวม", "ขอบเขตพื้นที่", "หน้ารวมข้อมูล"])
                    sidebar_container = st.sidebar.empty()
                    option = sidebar_container.selectbox("เลือกวิธีการดำเนินการ", ("สร้าง", "อ่าน", "อัพเดท", "ลบ"))
                    st.sidebar.write(f"ยินดีต้อนรับ {username}")
                    authenticator.logout("ล็อคเอ้าท์", "sidebar")
                    with tab2:
                        if option == "สร้าง":
                            cultivated_areas_tab.create_farmer()
                        elif option == "อ่าน":
                            cultivated_areas_tab.read_farmer()
                        elif option == "อัพเดท":
                            cultivated_areas_tab.update_farmer()
                        else:
                            cultivated_areas_tab.delete_farmer()
                    # Fertilizer
                    with tab3:
                        if option == "สร้าง":
                            fertilizer_tab.fertilizer_create()
                        elif option == "อ่าน":
                            fertilizer_tab.fertilizer_read()
                        elif option == "อัพเดท":
                            fertilizer_tab.fertilizer_update()
                        else:
                            fertilizer_tab.fertilizer_delete()
                    with tab4:
                        if option == "สร้าง":
                            fer_type_tab.fer_type_create()
                        elif option == "อ่าน":
                            fer_type_tab.fer_type_read()
                        elif option == "อัพเดท":
                            fer_type_tab.fer_type_update()
                        else:
                            fer_type_tab.fer_type_del()
                    with tab5:
                        if option == "สร้าง":
                            fuel_tab.fuel_create()
                        elif option == "อ่าน":
                            fuel_tab.fuel_read()
                        elif option == "อัพเดท":
                            fuel_tab.fuel_update()
                        else:
                            fuel_tab.fuel_delete()
                    with tab6:
                        if option == "สร้าง":
                            carbon_offset_tab.carbon_offset_create()
                        elif option == "อ่าน":
                            carbon_offset_tab.carbon_offset_read()
                        elif option == "อัพเดท":
                            carbon_offset_tab.carbon_offset_update()
                        else:
                            carbon_offset_tab.carbon_offset_delete()
                    with tab7:
                        if option == "สร้าง":
                            carbon_footprint_tab.carbon_footprint_create()
                        elif option == "อ่าน":
                            carbon_footprint_tab.carbon_footprint_read()
                        elif option == "อัพเดท":
                            carbon_footprint_tab.carbon_footprint_update()
                        else:
                            carbon_footprint_tab.carbon_footprint_delete()
                    with tab8:
                        polygon()
                    with tab9:
                        mycursor.execute("SELECT * FROM farmer")
                        farmer_result = mycursor.fetchall()

                        # Convert the 'farmer' result to a DataFrame
                        farmer_df = pd.DataFrame(farmer_result, columns=['farmer_id', 'farmer_firstname', 'farmer_lastname',
                                                                         'farmer_birthday', 'farmer_start_membership',
                                                                          'phone_number', 'password',
                                                                         'email', 'image'])

                        # Execute the SQL query to fetch data from the 'carbon_footprint' table
                        mycursor.execute("SELECT * FROM cultivated_areas")
                        cultivated_areas_result = mycursor.fetchall()

                        # Convert the 'carbon_footprint' result to a DataFrame
                        cultivated_areas_df = pd.DataFrame(cultivated_areas_result,
                                                           columns=['cultivated_areas_id', 'farmer_id',
                                                                    'cultivated_areas_in_rai', 'latitude', 'longitude', 'deed'])

                        # Merge the two DataFrames based on the common column
                        merged_df = pd.merge(farmer_df, cultivated_areas_df, on='farmer_id', how='outer')


                        mycursor.execute("SELECT * FROM carbon_offset")
                        carbon_offset = mycursor.fetchall()
                        carbon_offset_df = pd.DataFrame(carbon_offset, columns=["carbon_offset_id", "cultivated_areas_id", "total_carbon_offset", "filer_cake_in_rai", "beans_in_rai"])
                        merged_df = pd.merge(merged_df,carbon_offset_df, on='cultivated_areas_id', how='outer')

                        mycursor.execute("SELECT * FROM carbon_footprint")
                        carbon_footprint = mycursor.fetchall()
                        carbon_footprint_df = pd.DataFrame(carbon_footprint, columns=["carbon_footprint_id", "cultivated_areas_id", "total_carbon_footprint", "GHG1", "GHG2", "GHG3"])
                        merged_df = pd.merge(merged_df, carbon_footprint_df, on='cultivated_areas_id', how='outer')

                        mycursor.execute("SELECT * FROM fuel")
                        fuel_query = mycursor.fetchall()
                        fuel_df = pd.DataFrame(fuel_query, columns=["fuel_id", "cultivated_areas_id", "fuel_used_in_kilogram"])
                        merged_df = pd.merge(merged_df, fuel_df, on="cultivated_areas_id", how='outer')


                        # mycursor.execute("SELECT * FROM fertilizer")
                        # fertilizer_query = mycursor.fetchall()
                        # fertilizer_df = pd.DataFrame(fertilizer_query, columns=["fertilizer_id", "cultivated_areas_id", "fertilizer_name", "fertilizer_weight_in_kilogram", "fertilizer_productiondate", "type_name"])
                        # merged_df = pd.merge(merged_df,fertilizer_df, on='cultivated_areas_id', how='outer')
                        #
                        #
                        # mycursor.execute("SELECT * FROM fertilizer_type")
                        # fer_type_query = mycursor.fetchall()
                        # fer_type_df = pd.DataFrame(fer_type_query, columns=["type_name", "description"])
                        # merged_df = pd.merge(merged_df, fer_type_df, on='type_name', how='outer')
                        #
                        # merged_df.drop_duplicates(['farmer_id', 'cultivated_areas_id'], inplace=True)
                        mycursor.execute("SELECT * FROM fertilizer")
                        fertilizer_query = mycursor.fetchall()
                        fertilizer_df = pd.DataFrame(fertilizer_query,
                                                     columns=["fertilizer_id", "cultivated_areas_id", "fertilizer_name",
                                                              "fertilizer_weight_in_kilogram",
                                                              "fertilizer_productiondate", "type_name"])

                        # Execute the second query to fetch fertilizer type data
                        mycursor.execute("SELECT * FROM fertilizer_type")
                        fer_type_query = mycursor.fetchall()
                        fer_type_df = pd.DataFrame(fer_type_query, columns=["type_name", "description"])

                        # Merge fertilizer_type with fertilizer on type_name
                        merged_fertilizer_df = pd.merge(fertilizer_df, fer_type_df, on='type_name', how='outer')

                        # Merge merged_fertilizer_df with merged_df on cultivated_areas_id
                        merged_df = pd.merge(merged_df, merged_fertilizer_df, on='cultivated_areas_id', how='outer')

                        merged_df.dropna(subset=['farmer_id'],inplace=True)
                        # Drop duplicates
                        merged_df.drop_duplicates(['farmer_id', 'cultivated_areas_id'], inplace=True)

                        # Convert fertilizer_weight_in_kilogram to float
                        merged_df['fertilizer_weight_in_kilogram'] = merged_df['fertilizer_weight_in_kilogram'].astype(float)

                        # Use .loc to filter rows based on the condition and perform the multiplication
                        merged_df.loc[merged_df['type_name'] == '15-15-15', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.5
                        # merged_df.loc[merged_df['type_name'] == '10-15-20', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.2
                        merged_df.loc[merged_df['type_name'] == '20-15-10', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.6
                        merged_df.loc[merged_df['type_name'] == '12-12-26', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.1
                        merged_df.loc[merged_df['type_name'] == '16-16-16', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.1
                        merged_df.loc[merged_df['type_name'] == '16-16-8', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.1
                        merged_df.loc[merged_df['type_name'] == '16-8-8', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.1
                        merged_df.loc[merged_df['type_name'] == '21-7-18', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.1
                        merged_df.loc[merged_df['type_name'] == '15-7-18', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.1
                        merged_df.loc[merged_df['type_name'] == '20-8-20', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.1
                        merged_df.loc[merged_df['type_name'] == '14-6-28', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.1
                        merged_df.loc[merged_df['type_name'] == '14-7-35', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.1

                        merged_df['GHGCalculation'] = merged_df['GHG1'] + merged_df['GHG2'] + merged_df['GHG3']
                        merged_df.insert(11, 'แปลงEcarbon', 'ใช่')
                        merged_df[['cultivated_areas_in_rai', 'total_carbon_offset', 'fertilizer_weight_in_kilogram']] = merged_df[['cultivated_areas_in_rai', 'total_carbon_offset', 'fertilizer_weight_in_kilogram']].astype(float).round(2)
                        merged_df.drop(columns=['password'], inplace=True)

                        # Sort and Search Dataframe
                        dataset = merged_df
                        # st.table(merged_df)
                        top_menu = st.columns(3)
                        with top_menu[0]:
                            sort = st.radio("เรียงข้อมูล", options=["ใช่", "ไม่"], horizontal=1, index=0)
                        if sort == "ใช่":
                            with top_menu[1]:
                                sort_field = st.selectbox("เรียงข้อมูลโดย", options=merged_df.columns)
                            with top_menu[2]:
                                sort_direction = st.radio(
                                    "วิธีการเรียง", options=["⬆️", "⬇️"], horizontal=True
                                )
                            dataset = merged_df.sort_values(
                                by=sort_field, ascending=sort_direction == "⬆️", ignore_index=True
                            )
                        pagination = st.container()
                        bottom_menu = st.columns((4, 1, 1))
                        with bottom_menu[2]:
                            batch_size = st.selectbox("ขนาดหน้า", options=[25, 50, 100])
                        with bottom_menu[1]:
                            total_pages = (
                                int(len(dataset) / batch_size) if int(len(dataset) / batch_size) > 0 else 1
                            )
                            current_page = st.number_input(
                                "หน้า", min_value=1, max_value=total_pages, step=1
                            )
                        with bottom_menu[0]:
                            st.markdown(f"หน้า **{current_page}** จาก **{total_pages}** ")

                        pages = split_frame(dataset, batch_size)
                        pagination.dataframe(data=pages[current_page - 1], use_container_width=True)
                        download_df = merged_df.drop(columns=['image', 'phone_number', 'deed', 'carbon_offset_id', 'carbon_offset_id', 'fuel_id', 'fertilizer_id', 'description', 'email', 'farmer_start_membership', 'farmer_birthday', 'carbon_footprint_id'])
                        csv = convert_df(download_df)

                        col = st.columns(5)
                        # Render the custom CSS
                        with col[2]:

                            # Define your download button
                            st.download_button(
                                "ดาวน์โหลดไฟล์",
                                csv,
                                "file.csv",
                                "text/csv",
                                key='download-csv'
                            )
                    # authenticator.logout("ล็อคเอ้าท์", "sidebar")
                elif DashOrCrud == 'หน้ารวมผล':
                    import matplotlib.pyplot as plt
                    import numpy as np
                    import plotly.graph_objs as go
                    col1 = st.columns([0.05, 0.52, 0.52, 0.05])
                    mycursor.execute("SELECT SUM(TOTAL_CARBON_FOOTPRINT) FROM carbon_footprint")
                    TotalCarbonFootprint = mycursor.fetchone()[0]  # Fetch the first column value from the first row
                    mycursor.execute("SELECT SUM(TOTAL_CARBON_OFFSET) FROM carbon_offset")
                    TotalCarbonOffset = mycursor.fetchone()[0]  # Fetch the first column value from the first row
                    # Generate mock data
                    with col1[1]:
                        with st.container(border=True, height=450):
                            data = {
                                'ปี': [2019, 2020, 2021, 2022],
                                'น้ำมัน': [100, 150, 200, 180],
                                'ปุ๋ย': [500, 550, 600, 620],
                                'ดิน': [300, 350, 400, 380]
                            }

                            # Create DataFrame
                            df = pd.DataFrame(data)

                            # Set index to 'Year' column
                            df.set_index('ปี', inplace=True)

                            # Convert DataFrame to Plotly-compatible format
                            data = []
                            colors = ['#53cae9', '#0cd580', '#1e76bd']  # Define colors for each category
                            for i, col in enumerate(df.columns):
                                data.append(go.Bar(x=df.index, y=df[col], name=col, marker_color=colors[i]))

                            # Create stacked bar chart
                            fig = go.Figure(data=data)
                            fig.update_layout(
                                barmode='stack',
                                title='สัดส่วนการเกิดคาร์บอนฟุตพริ้นท์',
                                xaxis_title='ปี',
                                yaxis_title='ตัน/คาร์บอน'
                            )

                            # Display the chart in Streamlit
                            st.plotly_chart(fig)
                    with col1[2]:
                        with st.container(border=True, height=450):
                            labels = ['คาร์บอนฟุตพริ้นท์', 'การทดแทนคาร์บอน']
                            sizes = [TotalCarbonFootprint, TotalCarbonOffset]
                            colors = ['#8ce4b4', '#9fe8d2']

                            # Create Plotly Figure for the donut chart
                            fig = go.Figure(
                                data=[go.Pie(labels=labels, values=sizes, hole=0.4, marker=dict(colors=colors))])

                            # Customize layout
                            fig.update_layout(title="คาร์บอนฟุตพริ้นท์/การทดแทนคาร์บอน")

                            # Display the donut chart in Streamlit
                            st.plotly_chart(fig)
                    col3 = st.columns([0.05, 0.52, 0.52, 0.05])
                    with col3[2]:
                        with st.container(border=True, height=300):
                            st.subheader("Info")
                            col = st.columns([0.1, 0.4, 0.4, 0.4])
                            with col[1]:
                                st.image("https://media.istockphoto.com/id/1323550608/vector/co2-reduction-cloud-eco-vector-icon.jpg?s=612x612&w=0&k=20&c=jO3OZfYAg9gB8TWvzH8BR64Lq3pFrfHcOvxpSgB-cjA=", width=150)
                                st.markdown(f"<p style='font-size: 20px; color: #B3B3B3'>Carbon Reduction</p>",unsafe_allow_html=True)
                            with col[2]:
                                st.image("https://static.vecteezy.com/system/resources/previews/031/757/668/original/carbon-credit-icon-for-graphic-design-logo-website-social-media-mobile-app-ui-illustration-png.png", width=119)
                                st.markdown(f"<p style='font-size: 20px; color: #B3B3B3'>Carbon Credit</p>",unsafe_allow_html=True)
                            with col[3]:
                                st.image("https://cdn-icons-png.flaticon.com/512/2485/2485389.png", width=119)
                                st.markdown(f"<p style='font-size: 20px; color: #B3B3B3'>Value: 800000 บาท</p>",unsafe_allow_html=True)
                            # st.subheader("Rating")
                            # st.markdown(f"<p style='font-size: 20px; color: #B3B3B3'>Rating</p>",
                            #             unsafe_allow_html=True)

                        #     start_date = pd.Timestamp('2023-01-01')
                        #     end_date = pd.Timestamp.now()
                        #
                        #     # Create a date range from January 2023 until now
                        #     date_range = pd.date_range(start=start_date, end=end_date, freq='M')
                        #
                        #     # Generate mock data for carbon footprint and carbon offset for each month
                        #     num_months = len(date_range)
                        #     carbon_footprint = np.random.randint(5, 20, size=num_months)
                        #     carbon_offset = np.random.randint(2, 15, size=num_months)
                        #
                        #     # Create DataFrame
                        #     data = {
                        #         'Date': date_range,
                        #         'Carbon_Footprint': carbon_footprint,
                        #         'Carbon_Offset': carbon_offset
                        #     }
                        #     df = pd.DataFrame(data)
                        #     df.set_index('Date', inplace=True)
                        #
                        #     # Plot using Plotly
                        #     fig = go.Figure()
                        #
                        #     # Add traces
                        #     fig.add_trace(go.Scatter(x=df.index, y=df['Carbon_Footprint'], mode='markers+lines',
                        #                              name='Carbon Footprint'))
                        #     fig.add_trace(
                        #         go.Scatter(x=df.index, y=df['Carbon_Offset'], mode='markers+lines', name='Carbon Offset'))
                        #
                        #     # Customize layout
                        #     fig.update_layout(
                        #         title='Carbon Footprint vs Carbon Offset',
                        #         xaxis_title='Month',
                        #         yaxis_title='Ton Carbon',
                        #         xaxis=dict(showgrid=True),
                        #         yaxis=dict(showgrid=True)
                        #     )
                        #
                        #     # Display chart in Streamlit
                        #     st.plotly_chart(fig)
                    with col3[1]:
                        with st.container(border=True, height=450):
                        # Define data
                            years = [2016, 2017, 2018, 2019, 2020]
                            carbon_footprint = [50, 45, 52, 55, 38]  # Example carbon footprint data
                            baseline = [50] * len(years)  # Example baseline data (constant)

                            # Create Plotly Figure
                            fig = go.Figure()

                            # Add traces for carbon footprint and baseline
                            fig.add_trace(
                                go.Scatter(x=years, y=carbon_footprint, mode='markers+lines', name='คาร์บอนฟุตพริ้นท์',
                                           marker=dict(color='#03b9cf')))
                            fig.add_trace(go.Scatter(x=years, y=baseline, mode='lines', name='ค่าที่ยอมรับได้',
                                                     line=dict(color='red', dash='dash')))

                            # Customize layout
                            fig.update_layout(
                                title='คาร์บอนฟุตพริ้นท์ในแต่ละปี',
                                xaxis_title='ปี',
                                yaxis_title='คาร์บอนฟุตพริ้นท์ (ตัน)',
                                legend=dict(x=0, y=1, xanchor='left', yanchor='top'),
                                xaxis=dict(tickmode='linear', tickvals=years),
                                yaxis=dict(showgrid=True),
                                plot_bgcolor='rgba(0,0,0,0)'
                            )

                            # Display the chart in Streamlit
                            st.plotly_chart(fig)


                    st.sidebar.write(f"ยินดีต้อนรับ {username}")
                    authenticator.logout("ล็อคเอ้าท์", "sidebar")

            elif not authenticator_status:
                with info:
                    st.error('รหัสผ่านไม่ถูกต้อง')
                    # Reset st.session_state.disabled to False on unsuccessful login
                    st.session_state.disabled = False
            else:
                with info:
                    st.warning('โปรดกรอกข้อมูล')
        else:
            with info:
                st.warning("ชื่อบัญชีไม่มีในระบบ โปรดกรอกชื่อบัญชีใหม่")

except Exception as e:
    print(f"An error occurred: {e}")
