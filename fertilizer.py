import streamlit as st
class FertilizerTab:
    def __init__(self, mycursor, mydb):
        self.mycursor = mycursor
        self.mydb = mydb
    def fertilizer_create(self):
        st.subheader("สร้างข้อมูลปุ๋ย")
        cultivated_areas_id = st.number_input("ไอดีพื้นที่ปลูก", min_value=1, key="cultivated_areas_id")
        fertilizer_name = st.text_input("ชื่อของเขต", key="fertilizer_name")
        fertilizer_weight_in_kilogram = st.number_input("น้ำหนักของปุ๋ย (กิโลกรัม)",
                                                        key="fertilizer_weight_in_kilogram")
        fertilizer_productiondate = st.date_input("วันที่ใส่ปุ๋ย", key="productiondate")
        # fertilizer_type_id = st.number_input("ไอดีของชนิดปุ๋ย", key="ไอดีของชนิดปุ๋ย", min_value=1)
        fertilizer_type_name = st.selectbox("ชนิดปุ๋ย", ('15-15-15', '10-15-20'))
        # self.mycursor.execute("SELECT * FROM fertilizer")
        # result = self.mycursor.fetchall()
        create_button = st.button("สร้าง", key="create_button_fertilzier")
        if create_button:
            self.mycursor.execute("SELECT COUNT(*) FROM fertilizer")
            count = self.mycursor.fetchone()[0]
            # Insert new row
            sql = "INSERT INTO fertilizer(fertilizer_id, cultivated_areas_id, fertilizer_name, fertilizer_weight_in_kilogram, fertilizer_productiondate, type_name) VALUES (%s, %s, %s, %s, %s, %s)"
            val = (count + 1, cultivated_areas_id, fertilizer_name, fertilizer_weight_in_kilogram, fertilizer_productiondate,fertilizer_type_name)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            # sql = "insert into fertilizer(fertilizer_id, cultivated_areas_id, fertilizer_name, fertilizer_weight_in_kilogram, fertilizer_productiondate,  fertilizer_type_id) values(:1,:2,:3,:4,:5,:6)"
            # val = (len(result)+1, cultivated_areas_id, fertilizer_name, fertilizer_weight_in_kilogram, fertilizer_productiondate,
            #        fertilizer_type_id)
            # self.mycursor.execute(sql, val)
            # self.mydb._instance.commit()
            st.success("สร้างบันทึกสำเร็จ!!!")
    def fertilizer_read(self):
        st.subheader("อ่านข้อมูลปุ๋ย")
        self.mycursor.execute("SELECT * FROM fertilizer")
        result = self.mycursor.fetchall()
        for row in result:
            st.write(row)
    def fertilizer_update(self):
        st.subheader("อัพเดทข้อมูลปุ๋ย")
        fertilizer_id = st.number_input("ไอดีของปุ๋ย", key="update_fer_fer", min_value=1)
        cultivated_areas_id = st.number_input("ไอดีของพื้นที่ปลูก", key="update_fer_cul", min_value=1)
        fertilizer_name = st.text_input("ชื่อปุ๋ย", key="update_fer_fername")
        fertilizer_weight_in_kilogram = st.number_input("น้ำหนักของปุ๋ย", key="update_fer_weight")
        fertilizer_production = st.date_input("วันที่ใส่ปุ๋ย", key="update_fer_pro")
        # fertilizer_type_id = st.number_input("ไอดีของชนิดปุ๋ย", key="update_fer_typeid", min_value=1)
        fertilizer_type_name = st.selectbox("ชนิดปุ๋ย", ('15-15-15', '10-15-20'))
        update_button = st.button("อัพเดท", key="update_but_fer")
        if update_button:
            sql = "UPDATE fertilizer set cultivated_areas_id=%s,fertilizer_name=%s,fertilizer_weight_in_kilogram=%s,fertilizer_productiondate=%s,type_name=%s WHERE fertilizer_id=%s"
            val = (cultivated_areas_id, fertilizer_name, fertilizer_weight_in_kilogram, fertilizer_production,
                   fertilizer_type_name, fertilizer_id)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("อัพเดทข้อมูลสำเร็จ!!!")
    def fertilizer_delete(self):
        st.subheader("ลบข้อมูลปุ๋ย")
        id = st.number_input("ไอดีปุ๋ย", min_value=1, key="fertilizer_id")
        delete_button = st.button("ลบ", key="Delete_button_fer")
        if delete_button:
            sql = "DELETE FROM fertilizer WHERE fertilizer_id=%s"
            val = (id,)
            self.mycursor.execute(sql, val)
            self.mydb.commit()
            st.success("ลบข้อมูลสำเร็จ!!!")
