#圖正常   文章是舊的
import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, TextSendMessage,
    QuickReply, QuickReplyButton, MessageAction
)
import requests
from bs4 import BeautifulSoup
import json
import os

# LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = "/FGgyGN3HRkCPIUyrj694l3wgO02htU+cmIfnhhBHawC6550rDajjaYbeX0Y0LY4CP/ALmASpGIclGoQXw2/ZMGG6WhEvm+CKoGSKaTKaO8hJT3CMZytUluskj0gcobEJoj/f7jFKsO/0rM7wHeruwdB04t89/1O/w1cDnyilFU="
LINE_CHANNEL_SECRET = "969aed1d7a639c88b209d81bfd47db0f"
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
def load_calorie_info(json_path=r"C:\Users\at930\OneDrive\桌面\筆記夾\azure證照107\新增資料夾\healthy\calorie_info.json"):
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

# 获取网页内容的函数
def fetch_web_content(section_type):
    url = "https://yingting-992.github.io/data/dd.html"
    response = requests.get(url)

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # 根據 section_type 決定篩選條件
        if section_type == '增肌':
            section_id = 'muscle'
            link_class = 'gain-muscle'
        elif section_type == '減脂':
            section_id = 'fat_loss'
            link_class = 'lose-fat'
        else:
            return "無效的選擇。"

        # 查找相應的文章內容
        sections = soup.find_all('span', id=section_id)
        if sections:
            message = ""
            for section in sections:
                title = section.find('h1').text if section.find('h1') else None
                content = section.find_all('p')

                if title:
                    message += f"=== {title.upper()} ===\n"
                for p in content:
                    message += f"{p.text}\n\n"

            # 获取对应该类的 <a> 标签
            links = soup.find_all('a', class_=link_class)
            if links:
                message += "\n相關連結：\n"
                for link in links:
                    link_text = link.text.strip()
                    link_href = link['href'].strip()
                    message += f"{link_href}\n"
            
            return message
        else:
            return "沒有找到相關內容。"
    else:
        return "請求失敗，無法獲取網頁內容。"

# 處理用戶訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_id = event.source.user_id
    user_message = event.message.text

    # 顯示快速選單，選擇增肌或減脂
    if user_message == "文章":
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

    elif user_message in ["增肌", "減脂"]:
        # 爬取相應的文章並回傳給用戶
        content = fetch_web_content(user_message)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content)
        )
        return

# 圖片分析功能
def analyze_image_with_custom_vision(image_path):
    headers = {
        "Prediction-Key": AZURE_CUSTOM_VISION_KEY,
        "Content-Type": "application/octet-stream"
    }
    with open(image_path, "rb") as image_data:
        response = requests.post(AZURE_CUSTOM_VISION_URL, headers=headers, data=image_data)
    if response.status_code != 200:
        print(f"Azure Custom Vision API 錯誤：{response.status_code}, {response.text}")
        return None
    result = response.json()
    predictions = result.get("predictions", [])
    if predictions:
        top_prediction = max(predictions, key=lambda x: x["probability"])
        if top_prediction["probability"] > 0.3:
            return top_prediction["tagName"].lower()
    return None

# Flask 應用初始化
app = Flask(__name__)

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_text_message(event):
    user_id = event.source.user_id
    user_message = event.message.text

    if user_message == "文章":
        quick_reply = QuickReply(items=[
            QuickReplyButton(action=MessageAction(label="增肌", text="增肌")),
            QuickReplyButton(action=MessageAction(label="減脂", text="減脂"))
        ])
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請選擇增肌或減脂", quick_reply=quick_reply)
        )
        return

    elif user_message in ["增肌", "減脂"]:
        content = fetch_web_content(user_message)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content)
        )
        return

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

    if user_message in ["功能建議", "內容建議", "其他"]:
        feedback_dict[user_id] = user_message
        reply_text = TextSendMessage(text=f"請輸入您的{user_message}，我們非常重視您的意見！")
        line_bot_api.reply_message(event.reply_token, reply_text)
        return

    if feedback_dict.get(user_id) in ["功能建議", "內容建議", "其他"]:
        feedback_type = feedback_dict[user_id]
        try:
            send_email(f"{feedback_type}: {user_message.strip()}")
            reply_text = TextSendMessage(text=f"您的{feedback_type}已發送！感謝您的回饋！")
            feedback_dict[user_id] = None
        except Exception as e:
            reply_text = TextSendMessage(text=f"發送郵件失敗: {e}")
        line_bot_api.reply_message(event.reply_token, reply_text)
        return

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    image_path = os.path.join(os.getcwd(), "uploaded_image.jpg")
    try:
        message_content = line_bot_api.get_message_content(event.message.id)
        with open(image_path, "wb") as f:
            for chunk in message_content.iter_content():
                f.write(chunk)

        # 日誌檢查
        print(f"圖片已成功保存至 {image_path}")

        # 分析圖片
        detected_object = analyze_image_with_custom_vision(image_path)

        # 刪除圖片
        os.remove(image_path)

        if detected_object in CALORIE_INFO:
            reply_message = f"檢測到的物件是：{detected_object}\n熱量：{CALORIE_INFO[detected_object]}"
        else:
            reply_message = "未能識別圖片中的物件，請再試一次！"

    except Exception as e:
        print(f"處理圖片時發生錯誤: {e}")
        reply_message = "處理圖片時發生錯誤，請稍後再試！"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )

if __name__ == "__main__":
    app.run(port=5000)
