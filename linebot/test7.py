import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    QuickReply, QuickReplyButton, MessageAction, FlexSendMessage
)
import requests
from bs4 import BeautifulSoup
import json
import os

# LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = "SyEZaXoxa5KTe1lJXRq7EaVG7ANeoTav0hVEYwGVMQU/OoohwFIIsvPwpj8hG4G3zsN4ZrLfspKVGmFQMOpOd0KvIyoQPQ2waJCYus/GEpWi6Btau6TLxt/an1UfeiuqDcAv4/HKTd7hIrOzbEjNLwdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "f080443160cd17dca0a74f5e649323ed"
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# Azure Custom Vision 設定
AZURE_CUSTOM_VISION_URL = "https://hhhtt-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/09df699c-0bac-4052-b505-e158b7e42092/classify/iterations/Iteration2/image"
AZURE_CUSTOM_VISION_KEY = "3lLEQUuqbJPCfvcXLQ8MOidnB5eN8mAVJ371kjIOry8gBIlXRekTJQQJ99ALACYeBjFXJ3w3AAAIACOGgCTU"

# SMTP 配置
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'zsj9413@gmail.com'
SENDER_PASSWORD = 'tjfm tcya zfab oejf'

# 用戶回饋狀態
feedback_dict = {}

# 載入外部 JSON 文件
def load_calorie_info(json_path=r"C:\Users\USER\Desktop\高科資料\程式設計報告\linebot\calorie_info.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

# 使用 JSON 數據
CALORIE_INFO = load_calorie_info()

# 發送郵件函數
def send_email(feedback):
    subject = "用戶反饋"
    body = f"用戶反饋: {feedback}"
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = SENDER_EMAIL
    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        print(f"發送郵件失敗: {e}")


# Flask 應用初始化
app = Flask(__name__)

# 爬取網頁內容並生成 Flex Message
# 爬取網頁內容並生成 Flex Message
def fetch_web_content(section_type):
    url = "https://yingting-992.github.io/healthy/grab.html"  # 網頁的目標連結
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        section_id = 'muscle' if section_type == '增肌' else 'fat_loss'
        sections = soup.find_all('span', id=section_id)
        if sections:
            title = f"你真的了解{section_type}嗎?"
            contents = [{"type": "text", "text": p.text.strip(), "wrap": True, "margin": "md"}
                        for section in sections for p in section.find_all('p')]

            # 加入文章連結
            article_link = {
                "type": "text",
                "text": f"了解更多請點擊：[查看完整文章]({url})",
                "wrap": True,
                "margin": "md",
                "color": "#3498DB",
                "action": {
                    "type": "uri",
                    "label": "查看完整文章",
                    "uri": url
                }
            }

            # 合併 Flex Message 的內容
            flex_message = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": title, "weight": "bold", "size": "lg", "align": "center", "color": "#2ECC71"},
                        {"type": "separator", "margin": "md"},
                        *contents,
                        article_link  # 新增文章連結到 Flex Message
                    ]
                }
            }
            return flex_message
    return None


# 處理用戶發送的訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id

    if user_message == "文章":
        # 提供選項讓用戶選擇增肌或減脂
        quick_reply = QuickReply(
            items=[
                QuickReplyButton(action=MessageAction(label="增肌", text="增肌")),
                QuickReplyButton(action=MessageAction(label="減脂", text="減脂"))
            ]
        )
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請選擇增肌或減脂", quick_reply=quick_reply)
        )
        return

    if user_message in ["增肌", "減脂"]:
        # 根據用戶選擇爬取相應的內容並返回 Flex Message
        content = fetch_web_content(user_message)
        if content:
            line_bot_api.reply_message(
                event.reply_token,
                FlexSendMessage(alt_text=f"{user_message}文章", contents=content)
            )
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="未能找到相關內容，請再試一次！")
            )
        return
       # 意見回饋選單
    if user_message == "意見回饋":
        reply_text = TextSendMessage(
            text="請選擇您想回饋的類型：",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="功能建議", text="功能建議")),
                    QuickReplyButton(action=MessageAction(label="內容建議", text="內容建議")),
                    QuickReplyButton(action=MessageAction(label="其他", text="其他"))
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, reply_text)
        return

    # 處理用戶選擇的回饋類型
    if user_message in ["功能建議", "內容建議", "其他"]:
        feedback_dict[user_id] = user_message
        reply_text = TextSendMessage(
            text=f"請輸入您的{user_message}，我們非常重視您的意見！"
        )
        line_bot_api.reply_message(event.reply_token, reply_text)
        return

    # 接收具體的回饋內容並發送郵件
    if feedback_dict.get(user_id) in ["功能建議", "內容建議", "其他"]:
        feedback_type = feedback_dict[user_id]
        try:
            send_email(f"{feedback_type}: {user_message.strip()}")
            reply_text = TextSendMessage(text=f"您的{feedback_type}已發送！感謝您的回饋！")
            feedback_dict[user_id] = None  # 清除狀態
        except Exception as e:
            reply_text = TextSendMessage(text=f"發送郵件失敗: {e}")
        line_bot_api.reply_message(event.reply_token, reply_text)
        return

    # 飲食小知識功能
    if user_message == "飲食小知識":
        reply_text = TextSendMessage(
            text="請選擇您想了解的主題：",
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label="減脂小知識", text="減脂小知識")),
                    QuickReplyButton(action=MessageAction(label="增肌小知識", text="增肌小知識"))
                ]
            )
        )
        line_bot_api.reply_message(event.reply_token, reply_text)
        return

    # 減脂小知識
    if user_message == "減脂小知識":
        reply_text = TextSendMessage(
            text=('減脂無負擔，輕鬆塑健康！💪'
            )
        )
        line_bot_api.reply_message(event.reply_token, reply_text)
        return

    # 增肌小知識
    if user_message == "增肌小知識":
        reply_text = TextSendMessage(
            text=('增肌有策略，力量更有型！🏋️'
            )
        )
        line_bot_api.reply_message(event.reply_token, reply_text)
        return


    # 回覆用戶未識別的訊息
    reply_text = TextSendMessage(text="抱歉，我無法識別您的訊息，請選擇功能選單再試一次！")
    line_bot_api.reply_message(event.reply_token, reply_text)

# # 圖片分析功能
# def analyze_image_with_custom_vision(image_path):
#     headers = {
#         "Prediction-Key": AZURE_CUSTOM_VISION_KEY,
#         "Content-Type": "application/octet-stream"
#     }
#     with open(image_path, "rb") as image_data:
#         response = requests.post(AZURE_CUSTOM_VISION_URL, headers=headers, data=image_data)
#     if response.status_code != 200:
#         print(f"Azure Custom Vision API 錯誤：{response.status_code}, {response.text}")
#         return None
#     result = response.json()
#     predictions = result.get("predictions", [])
#     if predictions:
#         top_prediction = max(predictions, key=lambda x: x["probability"])
#         if top_prediction["probability"] > 0.3:
#             return top_prediction["tagName"].lower()
#     return None



# Flask callback
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

if __name__ == "__main__":
    app.run(port=5000)






