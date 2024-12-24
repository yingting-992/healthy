import os
import json
import smtplib
import requests
from datetime import datetime  # 用於產生時間戳
from email.mime.text import MIMEText
from flask import Flask, request, abort
from bs4 import BeautifulSoup
from dotenv import load_dotenv

from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, ImageMessage,
    TextSendMessage, QuickReply, QuickReplyButton,
    MessageAction, FlexSendMessage
)

# Azure Blob 套件
from azure.storage.blob import BlobServiceClient
from urllib.parse import urljoin  # 用於處理可能的相對路徑

# 1. 載入 .env 中的環境變數
load_dotenv()

# 2. Flask 應用初始化
app = Flask(__name__)

# 3. LINE Bot 設定
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")

line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(LINE_CHANNEL_SECRET)

# 4. Azure Custom Vision 設定
AZURE_CUSTOM_VISION_URL = "https://food70-prediction.cognitiveservices.azure.com/customvision/v3.0/Prediction/1a75e191-f35b-4657-879c-ef0b8d0a68d9/classify/iterations/Iteration2/image"
AZURE_CUSTOM_VISION_KEY = "8pMOLkNndA3qrDFy6Yjn0ZkgWBjoErhz3ruqhiVhT3zRFOXbXh71JQQJ99ALACYeBjFXJ3w3AAAIACOG5bXr"

# 5. SMTP（郵件）配置
SMTP_SERVER = 'smtp.gmail.com'
SMTP_PORT = 587
SENDER_EMAIL = 'zsj9413@gmail.com'
SENDER_PASSWORD = 'tjfm tcya zfab oejf'

# 6. Azure Blob 儲存體設定
AZURE_STORAGE_CONNECTION_STRING = "DefaultEndpointsProtocol=https;AccountName=healthy;AccountKey=/KaT8yQ461o3B4TWUDNhRingFu28EO70b53PWHzMeiQ5js9MFgDTBNW+7xER5vm3sQDe+R9j5hyR+AStS50GLQ==;EndpointSuffix=core.windows.net"
BLOB_CONTAINER_NAME = "hhh"

# 建立 BlobServiceClient 與 ContainerClient
blob_service_client = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
container_client = blob_service_client.get_container_client(BLOB_CONTAINER_NAME)

# ---------------- 全域紀錄無法辨識的圖片 ---------------
unrecognized_images = []  # 用於記錄無法辨識的圖片編號(或其他資訊)
# ------------------------------------------------------

# 7. 用戶回饋狀態（簡單紀錄用戶的回饋流程）
feedback_dict = {}

# 8. 載入外部 JSON：calorie_info.json
def load_calorie_info(json_path="./linebot/calorie_info.json"):
    with open(json_path, "r", encoding="utf-8") as f:
        return json.load(f)

CALORIE_INFO = load_calorie_info()

# 9. 發送郵件函數
def send_email(feedback):
    """
    將回饋內容透過 Gmail SMTP 發送給自己。
    """
    subject = "用戶反饋"
    body = f"用戶反饋: {feedback}"
    msg = MIMEText(body, _charset="utf-8")
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = SENDER_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        app.logger.error(f"發送郵件失敗: {e}")

# ---------------- 寄送無法辨識圖片清單 ----------------
def send_unrecognized_images_email(images_list):
    """
    將收集到的無法辨識圖片清單 (images_list) 寄送給自己。
    """
    subject = "累積 3 張無法辨識的圖片通知"
    body_lines = ["以下為 3 張無法辨識的圖片編號："]
    body_lines.extend(images_list)  # 將清單內容加入
    body = "\n".join(body_lines)

    msg = MIMEText(body, _charset="utf-8")
    msg['Subject'] = subject
    msg['From'] = SENDER_EMAIL
    msg['To'] = SENDER_EMAIL

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SENDER_EMAIL, SENDER_PASSWORD)
            server.send_message(msg)
    except Exception as e:
        app.logger.error(f"發送無法辨識圖片清單失敗: {e}")
# ------------------------------------------------------

# 10. 上傳圖片到 Azure Blob 儲存體（不回傳 URL）
def upload_image_to_blob(image_path, blob_name):
    """
    將本機上的 image_path 檔案上傳到 Azure Blob 容器中，檔名為 blob_name。
    成功上傳後，不回傳任何 URL。
    """
    try:
        blob_client = container_client.get_blob_client(blob_name)
        with open(image_path, "rb") as data:
            blob_client.upload_blob(data, overwrite=False)
    except Exception as e:
        app.logger.error(f"上傳圖片失敗: {e}")

# ---------------- 文章爬取 (新版) ----------------
def fetch_web_content(section_type):
    """
    依照使用者選擇的 section_type (增肌 or 減脂)，
    抓取網頁對應 <span> 區塊下的 <p> 和 <a>，
    先顯示所有文章段落，再顯示對應連結。
    """
    base_url = "https://yingting-992.github.io/healthy/reptile/grab.html"
    response = requests.get(base_url)
    if response.status_code != 200:
        return None

    soup = BeautifulSoup(response.text, "html.parser")
    # 根據使用者選擇「增肌」或「減脂」決定哪個區塊
    section_id = 'muscle' if section_type == '增肌' else 'fat_loss'
    sections = soup.find_all('span', id=section_id)
    if not sections:
        return None

    # Flex Message 大標題
    title_text = f"你真的了解{section_type}嗎？"

    # 文章段落 (p) & 連結 (a)
    paragraph_contents = []
    link_list = []

    for section in sections:
        # 先抓 <p> 文字（文章內容）
        for p_tag in section.find_all('p'):
            paragraph_contents.append(p_tag.get_text(strip=True))

        # 再抓 <a> 連結
        for a_tag in section.find_all('a', href=True):
            link_url = urljoin(base_url, a_tag['href'])
            # 若 <a> 裡沒文字，可用「增肌連結 / 減脂連結」或「查看連結」作為替代
            link_text = a_tag.get_text(strip=True) or f"{section_type}連結"
            link_list.append((link_text, link_url))

    # ---- 組裝 Flex Message ----
    body_contents = []

    # (1) 先放段落文字
    for idx, paragraph in enumerate(paragraph_contents, start=1):
        body_contents.append({
            "type": "text",
            "text": paragraph,
            "wrap": True,
            "margin": "md",
            "color": "#666666",
            "size": "sm"
        })
        # 段落間加分隔線
        if idx < len(paragraph_contents):
            body_contents.append({
                "type": "separator",
                "margin": "md",
                "color": "#EEEEEE"
            })

    # (2) 段落後再顯示「連結列表」
    if link_list:
        body_contents.append({
            "type": "separator",
            "margin": "lg",
            "color": "#AAAAAA"
        })
        body_contents.append({
            "type": "text",
            "text": "以下為本區塊中的相關連結",
            "weight": "bold",
            "margin": "md",
            "color": "#555555"
        })
        for i, (link_text, link_url) in enumerate(link_list, start=1):
            body_contents.append({
                "type": "separator",
                "margin": "md",
                "color": "#EEEEEE"
            })
            body_contents.append({
                "type": "text",
                "text": f"{link_text}\n({link_url})",
                "wrap": True,
                "color": "#3498DB",
                "margin": "sm",
                "action": {
                    "type": "uri",
                    "label": "查看連結",
                    "uri": link_url
                }
            })

    # 組合成 bubble
    flex_message = {
        "type": "bubble",
        "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "text",
                    "text": title_text,
                    "weight": "bold",
                    "size": "lg",
                    "align": "center",
                    "color": "#2ECC71"
                },
                {
                    "type": "separator",
                    "margin": "md",
                    "color": "#AAAAAA"
                },
                *body_contents
            ]
        }
    }
    return flex_message

# 12. 文字訊息事件處理
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text
    user_id = event.source.user_id

    # (A) 使用者輸入 "文章"
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

    # (B) 增肌 or 減脂 -> 爬取文章
    if user_message in ["增肌", "減脂"]:
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

    # (C) 意見回饋
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

    # (D) 接收用戶選的回饋類型
    if user_message in ["功能建議", "內容建議", "其他"]:
        feedback_dict[user_id] = user_message
        reply_text = TextSendMessage(
            text=f"請輸入您的{user_message}，我們非常重視您的意見！"
        )
        line_bot_api.reply_message(event.reply_token, reply_text)
        return

    # (E) 回饋內容 -> 用 smtp 寄送
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

    # (F) 飲食小知識功能
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

    if user_message == "減脂小知識":
        reply_text = TextSendMessage(text="減脂無負擔，輕鬆塑健康！💪")
        line_bot_api.reply_message(event.reply_token, reply_text)
        return

    if user_message == "增肌小知識":
        reply_text = TextSendMessage(text="增肌有策略，力量更有型！🏋️")
        line_bot_api.reply_message(event.reply_token, reply_text)
        return

    # (G) 未識別的訊息
    reply_text = TextSendMessage(text="抱歉，我無法識別您的訊息，請選擇功能選單再試一次！")
    line_bot_api.reply_message(event.reply_token, reply_text)

# 13. 圖片訊息事件處理
@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    """
    1) 先將使用者上傳的圖片下載到本機 (uploaded_image.jpg)。
    2) 呼叫 Azure Custom Vision 做圖像辨識。
    3) 上傳該圖片到 Azure Blob（不回傳 URL）。
    4) 結合辨識結果回覆使用者。
    5) 若辨識不出來 → 回覆「圖片無法辨識」，並記錄到 unrecognized_images。
       當累積 3 筆時，自動寄信給自己。
    """
    image_path = os.path.join(os.getcwd(), "uploaded_image.jpg")
    try:
        # 1) 下載圖片
        message_content = line_bot_api.get_message_content(event.message.id)
        with open(image_path, "wb") as f:
            for chunk in message_content.iter_content():
                f.write(chunk)

        # 2) 使用 Azure Custom Vision 做辨識
        detected_object = analyze_image_with_custom_vision(image_path)

        # 3) 生成不重覆的檔名並上傳到 Azure Blob
        timestamp_str = datetime.now().strftime("%Y%m%d%H%M%S")
        blob_name = f"{event.source.user_id}_{timestamp_str}.jpg"
        upload_image_to_blob(image_path, blob_name)

        # 移除本機暫存檔
        os.remove(image_path)

        # 4) 判斷是否辨識得出結果
        if not detected_object:
            reply_message = "圖片無法辨識，請再試一次！"

            # 記錄無法辨識
            unrecognized_images.append(blob_name)

            # 改成累積 3 筆就寄送 email
            if len(unrecognized_images) >= 3:
                send_unrecognized_images_email(unrecognized_images)
                unrecognized_images.clear()
        else:
            if detected_object in CALORIE_INFO:
                reply_message = (
                    f"檢測到的物件是：{detected_object}\n"
                    f"熱量：{CALORIE_INFO[detected_object]}"
                )
            else:
                reply_message = "未能識別圖片中的物件，請再試一次！"

    except Exception as e:
        app.logger.error(f"處理圖片時發生錯誤: {e}")
        reply_message = "處理圖片時發生錯誤，請稍後再試！"

    line_bot_api.reply_message(event.reply_token, TextSendMessage(text=reply_message))

# 14. 圖像分析：Azure Custom Vision
def analyze_image_with_custom_vision(image_path):
    headers = {
        "Prediction-Key": AZURE_CUSTOM_VISION_KEY,
        "Content-Type": "application/octet-stream"
    }
    try:
        with open(image_path, "rb") as image_data:
            response = requests.post(AZURE_CUSTOM_VISION_URL, headers=headers, data=image_data)
        if response.status_code != 200:
            app.logger.error(f"Azure Custom Vision API 錯誤：{response.status_code}, {response.text}")
            return None

        result = response.json()
        predictions = result.get("predictions", [])
        if not predictions:
            return None

        top_prediction = max(predictions, key=lambda x: x["probability"])
        if top_prediction["probability"] > 0.3:
            return top_prediction["tagName"].lower()
        return None

    except Exception as e:
        app.logger.error(f"分析圖片失敗: {e}")
        return None

# 15. 建立 Webhook 路由
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers.get('X-Line-Signature')
    body = request.get_data(as_text=True)
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

# 16. 主程式入口
if __name__ == "__main__":
    app.run(port=5000)
