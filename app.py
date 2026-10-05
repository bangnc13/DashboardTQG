import streamlit as st
import streamlit.components.v1 as components
import requests
import json

# Cấu hình trang rộng tràn màn hình (Wide mode)
st.set_page_config(
    page_title="TQG-Dashboard Kiểm Soát Ca Tồn & Checklist (CLL)",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Thêm CSS ẩn header/footer mặc định của Streamlit
st.markdown('''
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
    </style>
''', unsafe_allow_html=True)

# --- CẤU HÌNH BOT (ZALO & TELEGRAM) ---
ZALO_BOT_TOKEN = "3613571325008693860:BsVltrcHugOoOMZsOvVZywwbfdjueukaFtofsLetSAYUUevPgFQaQsUDOprWWesx"
ZALO_GROUP_ID = "zgr-9207abe0d78f3ed1679e"

TELEGRAM_BOT_TOKEN = "8800368290:AAFwOejPNccmO5HyXy5FVMH5symEgkqPNak"
TELEGRAM_GROUP_ID = "-1004469807641"

def send_zalo_group_message(message):
    """Hàm gửi tin nhắn vào Group Zalo qua Zalo Bot Platform API"""
    url = "https://bot.zaloplatforms.com/api/v1/message"
    headers = {
        "Authorization": f"Bearer {ZALO_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": {
            "group_id": ZALO_GROUP_ID
        },
        "message": {
            "text": message
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        res_data = response.json()
        if response.status_code == 200 and res_data.get("error") == 0:
            return True, res_data
        else:
            return False, res_data
    except Exception as e:
        return False, str(e)

def send_telegram_group_message(message):
    """Hàm gửi tin nhắn vào Group Telegram qua Telegram Bot API"""
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_GROUP_ID,
        "text": message,
        "parse_mode": "Markdown"
    }
    
    try:
        response = requests.post(url, json=payload)
        res_data = response.json()
        if response.status_code == 200 and res_data.get("ok"):
            return True, res_data
        else:
            return False, res_data
    except Exception as e:
        return False, str(e)

# Xử lý sự kiện gửi Zalo hoặc Telegram (nếu có param trong URL từ HTML Backend)
query_params = st.query_params
if "action" in query_params:
    action = query_params["action"]
    msg_content = query_params.get("msg", "📊 Báo cáo Kiểm soát Ca tồn (CLL)")
    
    if action == "send_zalo":
        success, res = send_zalo_group_message(msg_content)
        if success:
            st.success("✅ Đã gửi báo cáo thành công vào Group Zalo!")
        else:
            st.error(f"❌ Lỗi gửi tin nhắn Zalo: {res}")
            
    elif action == "send_telegram":
        success, res = send_telegram_group_message(msg_content)
        if success:
            st.success("✅ Đã gửi báo cáo thành công vào Group Telegram!")
        else:
            st.error(f"❌ Lỗi gửi tin nhắn Telegram: {res}")
            
    # Xoá param để tránh gửi lại khi refresh
    st.query_params.clear()

html_content = '''<!DOCTYPE html>
<html lang="vi" class="h-full bg-slate-50">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Kiểm Soát Ca Tồn & Checklist (CLL)</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Chart.js -->
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <!-- SheetJS (xlsx) for processing Excel files -->
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    <!-- FontAwesome icons -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <!-- Google Fonts -->
    <link href="
