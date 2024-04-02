import streamlit as st
class carbon_offset:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb
    def carbon_offset_create(self):
        st.subheader("สร้างข้อมูลcarbon offset")
        cultivated_area_id = st.number_input("ไอดีพื้นที่ปลูก", min_value=1, key="cul_id_offset")
        total_carbon_offset = st.number_input("carbon offsetรวม", key="total_carbon_offset")
        solar_cell = st.number_input("ใช้Solar Cellทดแทนไปเท่าไหร่(MW)", key="solar_cell_offset")
        filter_cake = st.number_input("ใช้Filter Cakeทดแทนไปเท่าไหร่(Rai)", key="filter_cake")
        beans_rai = st.number_input("ปลูกถั่วเขียวไปกี่ไร่", key="beans_rai")
        create_button = st.button("สร้าง", key="carbon_offset_button")
        self.mycursor.execute("SELECT * FROM carbon_offset")
        result = self.mycursor.fetchall()
        if create_button:
            sql = "insert into carbon_offset(carbon_offset_id, cultivated_areas_id, total_carbon_offset, solar_cell_in_MW, filer_cake_in_rai, beans_in_rai) values(:1,:2,:3,:4,:5,:6)"
            val = (len(result)+1,cultivated_area_id,total_carbon_offset,solar_cell,filter_cake,beans_rai)
            self.mycursor.execute(sql, val)
            self.mydb._instance.commit()
            st.success("สร้างบันทึกสำเร็จ!!!")
    def carbon_offset_read(self):
        st.subheader("อ่านข้อมูลCarbon Offset")
        self.mycursor.execute("SELECT * FROM carbon_offset")
        result = self.mycursor.fetchall()
        for row in result:
            st.write(row)
    def carbon_offset_update(self):
        st.subheader("อัพเดทข้อมูลCarbon Offset")
        id = st.number_input("ไอดีCarbon Offset", min_value=1, key="carbon_offset_id")
        cultivated_area_id = st.number_input("ไอดีพื้นที่ปลูก", min_value=1, key="cul_id_offset_up")
        total_carbon_offset = st.number_input("carbon offsetรวม", key="total_carbon_offset_up")
        solar_cell = st.number_input("ใช้Solar Cellทดแทนไปเท่าไหร่(MW)", key="solar_cell_offset_up")
        filter_cake = st.number_input("ใช้Filter Cakeทดแทนไปเท่าไหร่(Rai)", key="filter_cake_up")
        beans_rai = st.number_input("ปลูกถั่วเขียวไปกี่ไร่", key="beans_rai_up")
        update_button = st.button("อัพเดท", key="carbon_offset_button")
        if update_button:
            sql = "UPDATE carbon_offset set cultivated_areas_id=?, total_carbon_offset=?, solar_cell_in_MW=?, filer_cake_in_rai=?, beans_in_rai=? WHERE carbon_offset_id=?"
            val = (cultivated_area_id, total_carbon_offset, solar_cell, filter_cake, beans_rai, id)
            self.mycursor.execute(sql, val)
            self.mydb._instance.commit()
            st.success("อัพเดทข้อมูลสำเร็จ!!!")
    def carbon_offset_delete(self):
        st.subheader("ลบข้อมูล")
        id = st.number_input("ไอดีCarbon Offset", min_value=1, key="carbon_offset_del")
        delete_button = st.button("ลบ", key="Delete_button_carbon_offset")
        if delete_button:
            sql = "DELETE FROM carbon_offset WHERE carbon_offset_id=?"
            val = (id,)
            self.mycursor.execute(sql, val)
            self.mydb._instance.commit()
            st.success("Record Deleted Successfully!!!")
