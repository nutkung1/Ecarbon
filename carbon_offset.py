import streamlit as st
class carbon_offset:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb
    def carbon_offset_create(self):
        st.subheader("สร้างข้อมูลการทดแทนคาร์บอน")
        cultivated_area_id = st.number_input("ไอดีพื้นที่ปลูก", min_value=1, key="cul_id_offset")
        total_carbon_offset = st.number_input("การทดแทนคาร์บอนรวม", key="total_carbon_offset")
        solar_cell = st.number_input("ใช้โซล่าเซลล์ทดแทนไปเท่าไหร่(MW)", key="solar_cell_offset")
        filter_cake = st.number_input("ใช้Filter Cakeทดแทนไปเท่าไหร่(Rai)", key="filter_cake")
        beans_rai = st.number_input("ปลูกถั่วเขียวไปกี่ไร่", key="beans_rai")
        create_button = st.button("บันทึก", key="carbon_offset_button")
        if create_button:
            self.mycursor.execute("SELECT COUNT(*) FROM carbon_offset")
            result = self.mycursor.fetchone()[0]
            sql = "insert into carbon_offset(carbon_offset_id, cultivated_areas_id, total_carbon_offset, solar_cell_in_MW, filer_cake_in_rai, beans_in_rai) values(%s,%s,%s,%s,%s,%s)"
            val = (result+1,cultivated_area_id,total_carbon_offset,solar_cell,filter_cake,beans_rai)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("สร้างบันทึกสำเร็จ!!!")
    def carbon_offset_read(self):
        st.subheader("อ่านข้อมูลการทดแทนคาร์บอน")
        self.mycursor.execute("SELECT * FROM carbon_offset")
        result = self.mycursor.fetchall()
        for row in result:
            st.write(row)
    def carbon_offset_update(self):
        st.subheader("อัพเดทข้อมูลการทดแทนคาร์บอน")
        id = st.number_input("ไอดีการทดแทนคาร์บอน", min_value=1, key="carbon_offset_id")
        cultivated_area_id = st.number_input("ไอดีพื้นที่ปลูก", min_value=1, key="cul_id_offset_up")
        total_carbon_offset = st.number_input("การทดแทนคาร์บอนรวม", key="total_carbon_offset_up")
        solar_cell = st.number_input("ใช้โซล่าเซลล์ทดแทนไปเท่าไหร่(MW)", key="solar_cell_offset_up")
        filter_cake = st.number_input("ใช้ฟิลเตอร์เค้กทดแทนไปเท่าไหร่(Rai)", key="filter_cake_up")
        beans_rai = st.number_input("ปลูกถั่วเขียวไปกี่ไร่", key="beans_rai_up")
        update_button = st.button("อัพเดท", key="carbon_offset_button")
        if update_button:
            sql = "UPDATE carbon_offset set cultivated_areas_id=%s, total_carbon_offset=%s, solar_cell_in_MW=%s, filer_cake_in_rai=%s, beans_in_rai=%s WHERE carbon_offset_id=%s"
            val = (cultivated_area_id, total_carbon_offset, solar_cell, filter_cake, beans_rai, id)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("อัพเดทข้อมูลสำเร็จ!!!")
    def carbon_offset_delete(self):
        st.subheader("ลบข้อมูล")
        id = st.number_input("ไอดีการทดแทนคาร์บอน", min_value=1, key="carbon_offset_del")
        delete_button = st.button("ลบ", key="Delete_button_carbon_offset")
        if delete_button:
            sql = "DELETE FROM carbon_offset WHERE carbon_offset_id=%s"
            val = (id,)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("ลบข้อมูลสำเร็จ!!!")
