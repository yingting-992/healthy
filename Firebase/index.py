# 更新 firebase_data.csv 的資料  
#讀取 Firebase 資料 ✔
import firebase_admin
from firebase_admin import credentials, db
import pandas as pd

# 初始化 Firebase Admin SDK
cred = credentials.Certificate(r"Firebase\healthy-food-938d3-firebase-adminsdk-6sfoq-443af85c21.json")
firebase_admin.initialize_app(cred, {
    "databaseURL": "https://healthy-food-938d3-default-rtdb.firebaseio.com"
})

# 讀取 Firebase 中的資料
ref = db.reference("/Users")  # 路徑：用戶資料
data = ref.get()

# 將資料轉換為 DataFrame
data_list = []
for key, value in data.items():
    data_list.append(value)

df = pd.DataFrame(data_list)
print(df)

# 將資料匯出成 CSV 檔案
df.to_csv(r"Firebase\firebase_data.csv", index=False)
