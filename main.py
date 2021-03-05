from flask import Flask, request, abort
from PIL import Image
import os, sys
from io import BytesIO
import pyocr, pyocr.builders

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, ImageMessage, ImageSendMessage
)

app = Flask(__name__)

YOUR_CHANNEL_ACCESS_TOKEN = os.environ["YOUR_CHANNEL_ACCESS_TOKEN"]
YOUR_CHANNEL_SECRET = os.environ["YOUR_CHANNEL_SECRET"]

line_bot_api = LineBotApi(YOUR_CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(YOUR_CHANNEL_SECRET)



@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text)
    )

lang = 'eng'
tools = pyocr.get_available_tools()
if len(tools) == 0:
    sys.exit(1)
tool = tools[0]

@handler.add(MessageEvent, message=ImageMessage)
def handle_image_message(event):
    message_content = line_bot_api.get_message_content(event.message.id)
    with open(f"static/"+event.message.id+".jpg", "wb") as f:
        f.write(message_content.content)
        image_url = f"static/"+event.message.id+".jpg"
    
    img = Image.open(image_url)
    
    txt = tool.image_to_string(
        img,
        lang=lang,
        builder=pyocr.builders.TextBuilder()
    )
    print(txt)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=txt)
    )

if __name__ == "__main__":
    #app.run()
    port = int(os.getenv("PORT", 5000))
    app.run(host="0.0.0.0", port=port)