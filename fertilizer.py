import streamlit as st
import datetime
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
        fertilizer_photos = {
            '15-15-15': 'https://ksny.in.th/wp-content/uploads/2022/07/%E0%B8%8B%E0%B8%AD%E0%B8%A2%E0%B8%A5%E0%B9%8C%E0%B9%80%E0%B8%A1%E0%B8%95-15-15-15-50kg.jpg',
            '10-15-20': 'https://soilmate.co.th/uploads/fertilizers/935e1-soilmate-50kg-.png',
            '16-16-16': 'https://www.soilmate.co.th/uploads/fertilizers/2c82c-soilmate_dec-2021_16-16-16-01.png',
            '16-16-8': 'https://www.soilmate.co.th/uploads/fertilizers/a3bc8-soilmate_dec-2020_16-16-8.png',
            '16-8-8': 'https://www.soilmate.co.th/uploads/fertilizers/852a0-soilmate_dec-2020_16-8-8.png',
            '21-7-18': 'https://soilmate.co.th/uploads/fertilizers/7d25e-soilmate_dec-2020_21-7-18.png',
            '15-7-18': 'https://www.soilmate.co.th/uploads/fertilizers/5a15b-soilmate_dec-2020_15-7-18.png',
            '20-8-20': 'https://www.soilmate.co.th/uploads/fertilizers/dbdeb-soilmate_dec-2020_20-8-20.png',
            '14-6-28': 'https://www.soilmate.co.th/uploads/fertilizers/d9a57-soilmate_dec-2020_14-6-28.png',
            '14-7-35': 'https://www.soilmate.co.th/uploads/fertilizers/71fc6-soilmate_dec-2020_14-7-35.png'
        }

        # Display select box with fertilizer type names
        fertilizer_type_name = st.selectbox("ชนิดปุ๋ย", list(fertilizer_photos.keys()))

        # Display the corresponding photo using HTML
        if fertilizer_type_name in fertilizer_photos:
            photo_url = fertilizer_photos[fertilizer_type_name]
            st.write(f"<img src='{photo_url}' width='300'>", unsafe_allow_html=True)
        else:
            st.write("No photo available for this fertilizer type.")
        # fertilizer_type_name = st.selectbox("ชนิดปุ๋ย", ('15-15-15', '10-15-20', '16-16-16', '16-16-8', '16-8-8', '21-7-18', '15-7-18', '20-8-20', '14-6-28', '14-7-35'))
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
        fertilizer_name = st.text_input("ชื่อของเขต", key="update_fer_fername")
        fertilizer_weight_in_kilogram = st.number_input("น้ำหนักของปุ๋ย", key="update_fer_weight")
        fertilizer_production = st.date_input("วันที่ใส่ปุ๋ย", key="update_fer_pro", min_value=datetime.date(year=1970, month=12, day=31))
        # fertilizer_type_id = st.number_input("ไอดีของชนิดปุ๋ย", key="update_fer_typeid", min_value=1)
        fertilizer_photos = {
            '15-15-15': 'https://ksny.in.th/wp-content/uploads/2022/07/%E0%B8%8B%E0%B8%AD%E0%B8%A2%E0%B8%A5%E0%B9%8C%E0%B9%80%E0%B8%A1%E0%B8%95-15-15-15-50kg.jpg',
            '10-15-20': 'https://soilmate.co.th/uploads/fertilizers/935e1-soilmate-50kg-.png',
            '16-16-16': 'https://www.soilmate.co.th/uploads/fertilizers/2c82c-soilmate_dec-2021_16-16-16-01.png',
            '16-16-8': 'https://www.soilmate.co.th/uploads/fertilizers/a3bc8-soilmate_dec-2020_16-16-8.png',
            '16-8-8': 'https://www.soilmate.co.th/uploads/fertilizers/852a0-soilmate_dec-2020_16-8-8.png',
            '21-7-18': 'https://soilmate.co.th/uploads/fertilizers/7d25e-soilmate_dec-2020_21-7-18.png',
            '15-7-18': 'https://www.soilmate.co.th/uploads/fertilizers/5a15b-soilmate_dec-2020_15-7-18.png',
            '20-8-20': 'https://www.soilmate.co.th/uploads/fertilizers/dbdeb-soilmate_dec-2020_20-8-20.png',
            '14-6-28': 'https://www.soilmate.co.th/uploads/fertilizers/d9a57-soilmate_dec-2020_14-6-28.png',
            '14-7-35': 'https://www.soilmate.co.th/uploads/fertilizers/71fc6-soilmate_dec-2020_14-7-35.png'
        }

        # Display select box with fertilizer type names
        fertilizer_type_name = st.selectbox("ชนิดปุ๋ย", list(fertilizer_photos.keys()))

        # Display the corresponding photo using HTML
        if fertilizer_type_name in fertilizer_photos:
            photo_url = fertilizer_photos[fertilizer_type_name]
            st.write(f"<img src='{photo_url}' width='300'>", unsafe_allow_html=True)
        else:
            st.write("No photo available for this fertilizer type.")
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
