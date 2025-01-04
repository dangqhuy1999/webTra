import mysql.connector
from mysql.connector import Error

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.cursor = None
        self.connect()  # Kiểm tra kết nối ngay khi khởi tạo

    def connect(self):
        try:
            # Kết nối đến cơ sở dữ liệu
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                self.cursor = self.connection.cursor()
                print("Kết nối thành công đến cơ sở dữ liệu.")
        except Error as e:
            print(f"Lỗi kết nối: {e}")

    def insert(self, table, columns, values):
        try:
            # Xây dựng câu lệnh INSERT động
            column_str = ', '.join(columns)
            placeholders = ', '.join(['%s'] * len(values))
            sql = f"INSERT INTO {table} ({column_str}) VALUES ({placeholders})"
            
            self.cursor.execute(sql, values)
            self.connection.commit()  # Lưu thay đổi vào cơ sở dữ liệu
            print("Dữ liệu đã được chèn thành công.")
        except Error as e:
            print(f"Lỗi khi chèn dữ liệu: {e}")
    def delete(self, table, id_value):
        try:
            sql = f"DELETE FROM {table} WHERE id = %s"
            self.cursor.execute(sql, (id_value,))
            self.connection.commit()
            print(f"Hàng có id = {id_value} đã được xóa.")
        except Error as e:
            print(f"Lỗi khi xóa dữ liệu: {e}")
    def fetch_one(self, table, condition):
      try:
        sql = f"SELECT * FROM {table} WHERE {condition}"
        self.cursor.execute(sql)
        return self.cursor.fetchone()
      except Error as e:
        print(f"Lỗi: {e}")
        return None
    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
            print("Kết nối đã được đóng.")

'''
# Ví dụ sử dụng
if __name__ == "__main__":
    db = Database('localhost', 'huyne', 'Aa@12345', 'web2')  # Thay thế thông tin kết nối
    columns = ['detail', 'description', 'yturn']
    values = ['Detail example', 'Description example', 10]
    
    db.insert('infop', columns, values)
    db.close()
'''
