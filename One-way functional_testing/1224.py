#firebase 連接 linebot 單向測試  (還沒試過)
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage
)
import requests

app = Flask(__name__)

# LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = ""
LINE_CHANNEL_SECRET = ""
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Azure ML API 設定
AZURE_ML_ENDPOINT = "https://<your-ml-endpoint>.azurewebsites.net/score"
AZURE_API_KEY = "YOUR_AZURE_ML_API_KEY"

# 發送資料到 Azure ML API
def get_predictions(input_data):
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {AZURE_API_KEY}"
    }
    payload = {"data": input_data}
    response = requests.post(AZURE_ML_ENDPOINT, headers=headers, json=payload)
    
    if response.status_code == 200:
        return response.json()
    else:
        return {"error": response.text}

# LINE Bot 訊息處理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text.strip()

    # 檢查用戶是否輸入了預測指令
    if user_message.startswith("預測體重"):
        try:
            # 假設用戶輸入格式為：預測體重 175,70,25,male
            _, data_str = user_message.split(" ", 1)
            height, weight, age, gender = data_str.split(",")

            # 構建 input_data
            input_data = [{
                "Height": int(height),
                "Weight": int(weight),
                "Age": int(age),
                "Gender": gender.lower()
            }]

            # 調用 Azure ML API 取得預測結果
            prediction_result = get_predictions(input_data)

            # 處理 Azure ML API 回應
            if "error" in prediction_result:
                reply_text = f"預測發生錯誤：{prediction_result['error']}"
            else:
                predictions = prediction_result.get("predictions", [])
                if predictions:
                    predicted_weight = predictions[0].get("predicted_weight", "未知")
                    advice = predictions[0].get("advice", "沒有建議。")
                    reply_text = (
                        f"預測結果：一個月後的體重為 {predicted_weight} 公斤\n"
                        f"建議：{advice}"
                    )
                else:
                    reply_text = "無法獲取預測結果，請稍後再試。"
        except Exception as e:
            reply_text = f"處理您的輸入時發生錯誤：{str(e)}"
    else:
        # 默認回覆訊息
        reply_text = "請輸入『預測體重 身高,體重,年齡,性別』來查看一個月後的體重預測結果！"

    # 回傳結果給用戶
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_text)
    )
    

# Webhook Callback
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

if __name__ == "__main__":
    app.run(port=5000)
