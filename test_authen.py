import yaml
from yaml.loader import SafeLoader
import streamlit_authenticator as stauth
import streamlit as st
import mysql.connector
from farmer_tab import FarmerTab
from cultivated_tab import CultivatedTab
from fertilizer import FertilizerTab
from fertilizer_type import Fertilizer_Type_Tab
from fuel import Fuel_Tab
from carbon_offset import carbon_offset
from carbon_footprint import carbon_footprint

with open('/Users/suchanatratanarueangrong/Mitrphol_ecarbon/Streamlit/CRUD_REAL/q.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days'],
    config['preauthorized']
)

register = st.sidebar.button("สมัครสมาชิก", key="register")

if register:
    try:
        email_of_registered_user, username_of_registered_user, name_of_registered_user = authenticator.register_user(preauthorization=False, fields={'Form name':'สมัครบัญชี', 'Email':'อีเมล', 'Username':'ชื่อบัญชี', 'Password':'รหัสผ่าน', 'Repeat password':'กรอกรหัสผ่านอีกครั้ง', 'Register':'สมัคร'})
        if email_of_registered_user:
            st.success('สมัครสมาชิกสำเร็จ')
            with open('/Users/suchanatratanarueangrong/Mitrphol_ecarbon/Streamlit/CRUD_REAL/q.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
        login = st.sidebar.button("ล็อคอิน", key="login")
    except Exception as e:
        st.error(e)
else:
    forget_password = st.sidebar.button("ลืมรหัส", key="forget_password")
    forget_username = st.sidebar.button("ลืมชื่อบัญชี", key="forget_username")
    if forget_password:
        try:
            login1 = st.sidebar.button("ล็อคอิน", key="login1")
            username_of_forgotten_password, email_of_forgotten_password, new_random_password = authenticator.forgot_password(fields={'Form name':'ลืมรหัสผ่าน', 'Username':'ชื่อบัญชี', 'Submit':'ส่ง'})
            if username_of_forgotten_password:
                st.success('New password to be sent securely')
                with open('/Users/suchanatratanarueangrong/Mitrphol_ecarbon/Streamlit/CRUD_REAL/q.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                # The developer should securely transfer the new password to the user.
            elif username_of_forgotten_password == False:
                st.error('Username not found')
        except Exception as e:
            st.error(e)
    elif forget_username:
        try:
            login2 = st.sidebar.button("ล็อคอิน", key="login2")
            username_of_forgotten_username, email_of_forgotten_username = authenticator.forgot_username(fields={'Form name':'ลืมชื่อบัญชี', 'Email':'อีเมลล์', 'Submit':'ส่ง'})
            if username_of_forgotten_username:
                st.success('Username to be sent securely')
                with open('/Users/suchanatratanarueangrong/Mitrphol_ecarbon/Streamlit/CRUD_REAL/q.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
                # The developer should securely transfer the username to the user.
            elif username_of_forgotten_username == False:
                st.error('Email not found')
        except Exception as e:
            st.error(e)
    else:
        authenticator.login(fields={'Form name':'เข้าสู่ระบบ', 'Username':'ชื่อบัญชี', 'Name':'ชื่อ', 'Password':'รหัสผ่าน', 'Login':'ล็อคอิน', 'Name':'ชื่อ'})
if st.session_state["authentication_status"]:
    reset_password = st.sidebar.button("ตั้งรหัสผ่านใหม่", key="reset_password")
    if reset_password:
        try:
            if authenticator.reset_password(st.session_state["username"]):
                st.success('Password modified successfully')
                with open('/Users/suchanatratanarueangrong/Mitrphol_ecarbon/Streamlit/CRUD_REAL/q.yaml', 'w') as file:
                    yaml.dump(config, file, default_flow_style=False)
        except Exception as e:
            st.error(e)
    authenticator.logout("ล็อคเอ้าท์", "sidebar")
    st.sidebar.write(f'ยินดีต้อนรับ *{st.session_state["name"]}*')
    mydb = mysql.connector.connect(
        host=st.secrets.db_credentials.host,
        user=st.secrets.db_credentials.user,
        password=st.secrets.db_credentials.password,
        database=st.secrets.db_credentials.database,
    )
    mycursor = mydb.cursor()
    print("Connection Established")

    farmer_tab = FarmerTab(mycursor, mydb)
    cultivated_areas_tab = CultivatedTab(mycursor, mydb)
    fertilizer_tab = FertilizerTab(mycursor, mydb)
    fer_type_tab = Fertilizer_Type_Tab(mycursor, mydb)
    fuel_tab = Fuel_Tab(mycursor, mydb)
    carbon_offset_tab = carbon_offset(mycursor, mydb)
    carbon_footprint_tab = carbon_footprint(mycursor, mydb)

    # Streamlit App
    def main():
        st.title("ปรับแต่งDatabase")
        tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs(
            ["Farmer", "Cultivated_areas", "Fertilizer", "Fertilizer_type", "Fuel", "carbon_offset",
             "carbon_footprint"])
        option = st.sidebar.selectbox("Select an Operations", ("สร้าง", "อ่าน", "อัพเดท", "ลบ"))
        # farmer tab
        with tab1:
            if option == "สร้าง":
                farmer_tab.create_farmer()
            elif option == "อ่าน":
                farmer_tab.read_farmer()
            elif option == "อัพเดท":
                farmer_tab.update_farmer()
            else:
                farmer_tab.delete_farmer()
        # Cultivated Areas tab
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


    if __name__ == "__main__":
        main()
elif st.session_state["authentication_status"] is False:
    st.error('Username/password is incorrect')
    try:
        if authenticator.reset_password(st.session_state["username"]):
            st.success('Password modified successfully')
            with open('/Users/suchanatratanarueangrong/Mitrphol_ecarbon/Streamlit/CRUD_REAL/q.yaml', 'w') as file:
                yaml.dump(config, file, default_flow_style=False)
    except Exception as e:
        st.error(e)
