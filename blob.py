import smtplib
from email.mime.text import MIMEText
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage, TextSendMessage,
    QuickReply, QuickReplyButton, MessageAction, FlexSendMessage
)
import requests
from bs4 import BeautifulSoup
import json
import os
from azure.storage.blob import BlobServiceClient
from dotenv import load_dotenv

# 加載 .env 文件中的環境變數
load_dotenv()

# LINE Bot 設定
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# Azure Custom Vision 設定
AZURE_CUSTOM_VISION_URL = ""
AZURE_CUSTOM_VISION_KEY = ""


# Azure Blob 儲存體設定
AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
BLOB_CONTAINER_NAME = os.getenv("BLOB_CONTAINER_NAME")


# SMTP 配置
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'zsj9413@gmail.com'
SENDER_PASSWORD = 'tjfm tcya zfab oejf'

# 用戶回饋狀態
feedback_dict = {}

# 載入外部 JSON 文件
def load_calorie_info(json_path=r"C:\Users\User\Downloads\calorie_info.json"):
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

# 爬取網頁內容並生成 Flex Message
def fetch_web_content(section_type):
    url = "https://yingting-992.github.io/healthy/reptile/grab.html"
    response = requests.get(url)

    app.logger.info(f"Fetched URL: {url} with status {response.status_code}")
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        if section_type == '增肌':
            section_id = 'muscle'
            link_class = 'gain-muscle'
        elif section_type == '減脂':
            section_id = 'fat_loss'
            link_class = 'lose-fat'
        else:
            return None

        # 爬取增肌或減脂的段落
        sections = soup.find_all('span', id=section_id)
        if sections:
            title = f"你真的了解{section_type}嗎?"
            paragraphs = []
            links = []
            for section in sections:
                section_paragraphs = section.find_all('p')
                for p in section_paragraphs:
                    paragraphs.append(p.text.strip())
                section_links = section.find_all('a', class_=link_class)
                for link in section_links:
                    links.append(f"\ud83d\udd17 {link.text.strip()}: {link['href']}")

            contents = [{"type": "text", "text": paragraph, "wrap": True, "margin": "md"} for paragraph in paragraphs]
            link_contents = [{"type": "text", "text": link, "wrap": True, "margin": "md"} for link in links]

            flex_message = {
                "type": "bubble",
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {"type": "text", "text": title, "weight": "bold", "size": "lg", "align": "center", "color": "#2ECC71"},
                        {"type": "separator", "margin": "md"},
                        *contents,
                        {"type": "separator", "margin": "md"},
                        {"type": "text", "text": "相關連結：", "weight": "bold", "margin": "md"},
                        *link_contents
                    ]
                }
            }
            return flex_message
        else:
            return None
    else:
        app.logger.error("無法獲取內容，請檢查網址或網頁結構")
        return None

# 處理用戶發送的訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    app.logger.info(f"Received message: {user_message}")

    try:
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
        elif user_message in ["增肌", "減脂"]:
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
    except Exception as e:
        app.logger.error(f"處理訊息時發生錯誤: {e}")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="處理錯誤，請稍後再試！")
        )
        
        
# 上傳圖片到 Azure Blob 儲存體
def upload_image_to_blob(image_path, blob_name):
    try:
        blob_client = container_client.get_blob_client(blob_name)
        with open(image_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=True)
        return blob_client.url
    except Exception as e:
        app.logger.error(f"上傳圖片失敗: {e}")
        return None


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


@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    image_path = os.path.join(os.getcwd(), "uploaded_image.jpg")
    try:
        # 下載圖片
        message_content = line_bot_api.get_message_content(event.message.id)
        with open(image_path, "wb") as f:
            for chunk in message_content.iter_content():
                f.write(chunk)

        # 圖片分析
        detected_object = analyze_image_with_custom_vision(image_path)

        # 上傳至 Blob
        blob_name = f"user_images/{event.message.id}.jpg"
        blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
        container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)
        with open(image_path, "rb") as data:
            container_client.upload_blob(name=blob_name, data=data, overwrite=True)
        
        # 刪除本地圖片
        os.remove(image_path)
        
        # 回應結果
        if detected_object in CALORIE_INFO:
            reply_message = f"檢測到的物件是：{detected_object}\n熱量：{CALORIE_INFO[detected_object]}"
        else:
            reply_message = "未能識別圖片中的物件，請再試一次！"

    except Exception as e:
        app.logger.error(f"處理圖片時發生錯誤: {e}")
        reply_message = "處理圖片時發生錯誤，請稍後再試！"

    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=reply_message)
    )



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

if __name__ == "__main__":
    app.run(port=5000)