import mysql.connector
import streamlit as st
from farmer_tab import FarmerTab
from cultivated_tab import CultivatedTab
from fertilizer import FertilizerTab
from fertilizer_type import Fertilizer_Type_Tab
from fuel import Fuel_Tab
from carbon_offset import carbon_offset
from carbon_footprint import carbon_footprint

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="NuT0863771558#",
    database="Ecarbon"
)
mycursor=mydb.cursor()
print("Connection Established")

farmer_tab = FarmerTab(mycursor, mydb)
cultivated_areas_tab = CultivatedTab(mycursor, mydb)
fertilizer_tab = FertilizerTab(mycursor, mydb)
fer_type_tab = Fertilizer_Type_Tab(mycursor, mydb)
fuel_tab = Fuel_Tab(mycursor, mydb)
carbon_offset_tab = carbon_offset(mycursor, mydb)
carbon_footprint_tab = carbon_footprint(mycursor, mydb)
#Streamlit App
def main():
    st.title("ปรับแต่งDatabase")
    tab1, tab2, tab3, tab4, tab5, tab6, tab7= st.tabs(["Farmer", "Cultivated_areas", "Fertilizer", "Fertilizer_type", "Fuel", "carbon_offset", "carbon_footprint"])
    option = st.sidebar.selectbox("Select an Operations", ("สร้าง", "อ่าน", "อัพเดท", "ลบ"))
#farmer tab
    with tab1:
        if option == "สร้าง":
            farmer_tab.create_farmer()
        elif option=="อ่าน":
            farmer_tab.read_farmer()
        elif option=="อัพเดท":
            farmer_tab.update_farmer()
        else:
            farmer_tab.delete_farmer()
#Cultivated Areas tab
    with tab2:
        if option=="สร้าง":
            cultivated_areas_tab.create_farmer()
        elif option=="อ่าน":
            cultivated_areas_tab.read_farmer()
        elif option=="อัพเดท":
            cultivated_areas_tab.update_farmer()
        else:
            cultivated_areas_tab.delete_farmer()
#Fertilizer
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