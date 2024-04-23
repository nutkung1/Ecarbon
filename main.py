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
import matplotlib.pyplot as plt
import numpy as np
from dotenv import load_dotenv

load_dotenv()
# Set page configuration
st.set_page_config(page_title='Streamlit', initial_sidebar_state="collapsed")

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

                st.subheader('หน้าหลัก')
                DashOrCrud = st.sidebar.selectbox("หน้ารวมผล หรือ CRUD", ("หน้ารวมผล", "CRUD"))
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
                        carbon_offset_df = pd.DataFrame(carbon_offset, columns=["carbon_offset_id", "cultivated_areas_id", "total_carbon_offset", "solar_cell_in_MW", "filer_cake_in_rai", "beans_in_rai"])
                        merged_df = pd.merge(merged_df,carbon_offset_df, on='cultivated_areas_id', how='outer')

                        mycursor.execute("SELECT * FROM carbon_footprint")
                        carbon_footprint = mycursor.fetchall()
                        carbon_footprint_df = pd.DataFrame(carbon_footprint, columns=["carbon_footprint_id", "cultivated_areas_id", "total_carbon_footprint", "GHG1", "GHG2", "GHG3"])
                        merged_df = pd.merge(merged_df, carbon_footprint_df, on='cultivated_areas_id', how='outer')

                        mycursor.execute("SELECT * FROM fuel")
                        fuel_query = mycursor.fetchall()
                        fuel_df = pd.DataFrame(fuel_query, columns=["fuel_id", "cultivated_areas_id", "fuel_used_in_kilogram"])
                        merged_df = pd.merge(merged_df, fuel_df, on="cultivated_areas_id", how='outer')

                        mycursor.execute("SELECT * FROM fertilizer")
                        fertilizer_query = mycursor.fetchall()
                        fertilizer_df = pd.DataFrame(fertilizer_query, columns=["fertilizer_id", "cultivated_areas_id", "fertilizer_name", "fertilizer_weight_in_kilogram", "fertilizer_productiondate", "type_name"])
                        merged_df = pd.merge(merged_df,fertilizer_df, on='cultivated_areas_id', how='outer')


                        mycursor.execute("SELECT * FROM fertilizer_type")
                        fer_type_query = mycursor.fetchall()
                        fer_type_df = pd.DataFrame(fer_type_query, columns=["type_name", "description"])
                        merged_df = pd.merge(merged_df, fer_type_df, on='type_name', how='outer')

                        merged_df.drop_duplicates(['farmer_id', 'cultivated_areas_id'], inplace=True)

                        # Convert fertilizer_weight_in_kilogram to float
                        merged_df['fertilizer_weight_in_kilogram'] = merged_df['fertilizer_weight_in_kilogram'].astype(float)

                        # Use .loc to filter rows based on the condition and perform the multiplication
                        merged_df.loc[merged_df['type_name'] == '15-15-15', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.5
                        merged_df.loc[merged_df['type_name'] == '10-15-20', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.2
                        merged_df.loc[merged_df['type_name'] == '20-15-10', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.6
                        merged_df.loc[merged_df['type_name'] == '12-12-26', 'FertilizerCalculation'] = merged_df['fertilizer_weight_in_kilogram'] * 3.1


                        merged_df['GHGCalculation'] = merged_df['GHG1'] + merged_df['GHG2'] + merged_df['GHG3']
                        merged_df.drop(columns=['password'], inplace=True)

                        # Sort and Search Dataframe
                        dataset = merged_df
                        # st.table(merged_df)
                        top_menu = st.columns(3)
                        with top_menu[0]:
                            sort = st.radio("เรียงข้อมูล", options=["ใช่", "ไม่"], horizontal=1, index=1)
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
                        download_df = merged_df.drop(columns=['image', 'phone_number', 'cultivated_areas_id', 'deed', 'carbon_offset_id', 'carbon_offset_id', 'fuel_id', 'fertilizer_id', 'description', 'email', 'farmer_start_membership', 'farmer_birthday', 'carbon_footprint_id'])

                        csv = convert_df(download_df)

                        st.download_button(
                            "ดาวน์โหลดไฟล์",
                            csv,
                            "file.csv",
                            "text/csv",
                            key='download-csv'
                        )
                    # authenticator.logout("ล็อคเอ้าท์", "sidebar")
                elif DashOrCrud == 'หน้ารวมผล':
                    col1, col2 = st.columns(2)
                    mycursor.execute("SELECT SUM(TOTAL_CARBON_FOOTPRINT) FROM carbon_footprint")
                    TotalCarbonFootprint = mycursor.fetchone()[0]  # Fetch the first column value from the first row
                    mycursor.execute("SELECT SUM(TOTAL_CARBON_OFFSET) FROM carbon_offset")
                    TotalCarbonOffset = mycursor.fetchone()[0]  # Fetch the first column value from the first row
                    # with col1:
                        # Generate mock data
                    start_date = pd.Timestamp('2023-01-01')
                    end_date = pd.Timestamp.now()

                    # Create a date range from January 2023 until now
                    date_range = pd.date_range(start=start_date, end=end_date, freq='M')

                    # Generate mock data for carbon footprint and carbon offset for each month
                    num_months = len(date_range)
                    carbon_footprint = np.random.randint(5, 20,
                                                         size=num_months)  # Generating random values for carbon footprint
                    carbon_offset = np.random.randint(2, 15,
                                                      size=num_months)  # Generating random values for carbon offset

                    # Create DataFrame
                    data = {
                        'Date': date_range,
                        'Carbon_Footprint': carbon_footprint,
                        'Carbon_Offset': carbon_offset
                    }
                    df = pd.DataFrame(data)
                    df.set_index('Date', inplace=True)

                    # Plot
                    fig, ax = plt.subplots()
                    df.plot(ax=ax, marker='o')

                        # Customize plot
                    ax.set_ylabel('Ton Carbon')
                    ax.set_xlabel('Month')
                    ax.set_title('Carbon Footprint vs Carbon Offset')
                    plt.grid()
                    # Highlight each month
                    # for month in df.index.month.unique():
                    #     ax.axvline(df[df.index.month == month].index[0], color='gray', linestyle='--')

                    # Display chart in Streamlit
                    st.pyplot(fig)

                    # with col2:
                    labels = ['Carbon Footprint', 'Carbon Offset']
                    sizes = [TotalCarbonFootprint, TotalCarbonOffset]
                    colors = ['#ff9999', '#66b3ff']

                    # Plot
                    fig1, ax1 = plt.subplots()
                    ax1.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90)
                    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
                    plt.title("The proportion between Carbon Credit and CarbonFootprint in 2024")
                    # Display chart in Streamlit
                    st.pyplot(fig1)
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
