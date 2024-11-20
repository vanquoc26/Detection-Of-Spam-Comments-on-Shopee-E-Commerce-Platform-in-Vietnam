from pymongo import MongoClient

# Kết nối tới MongoDB server
client = MongoClient("mongodb://127.0.0.1:27017/")

# Tạo database tên là Shopee
mydb = client["Shopee"]

# Tạo Collection (bảng) tên là reviews
collection = mydb.reviews