import streamlit as st
import streamlit.components.v1 as components
import requests
import pandas as pd
import threading
from flask import Flask, request, jsonify

# --- CẤU HÌNH ZALO BOT & GOOGLE SHEETS ---
ZALO_BOT_TOKEN = "3613571325008693860:BsVltrcHugOoOMZsOvVZywwbfdjueukaFtofsLetSAYUUevPgFQaQsUDOprWWesx"
ZALO_GROUP_ID = "zgr-9207abe0d78f3cd1679c"
GOOGLE_SHEET_ID = '1qKW7OcGegD1IXcgV5WYXuzcUzYvpjZw-CqgzpYDLKoM'

# --- HÀM TỰ ĐỘNG ĐỌC DỮ LIỆU TỪ GOOGLE SHEETS ĐỂ TRẢ VỀ CHO BOT ---
def fetch_kpi_summary_for_bot():
    """Đọc dữ liệu trực tiếp từ Google Sheets để tính toán nhanh các chỉ số gửi qua Zalo"""
    csv_url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/gviz/tq?tqx=out:csv"
    try:
        df = pd.read_csv(csv_url)
        total_cases = len(df)
        
        # Thống kê nhanh các chỉ số cơ bản
        # Tìm cột Tồn giờ (Cột I tương ứng index 8 hoặc tên cột chứa 'tồn giờ')
        overdue_cases = 0
        urgent_cases = 0
        repeat_cases = 0
        
        for col in df.columns:
            col_lower = str(col).lower()
            if 'tồn giờ' in col_lower or 'ton gio' in col_lower:
                overdue_cases = len(df[pd.to_numeric(df[col], errors='coerce') >= 24])
            if 'giục' in col_lower:
                urgent_cases = df[col].dropna().astype(str).str.strip().ne('').sum()
            if 'lặp' in col_lower or 'lap' in col_lower:
                repeat_cases = len(df[pd.to_numeric(df[col], errors='coerce') > 0])

        report_msg = (
            f"📊 **BẢO CÁO NHANH CA TỒN (CLL)**\n"
            f"- Tổng tồn: {total_cases} ca\n"
            f"- KH Giục: {urgent_cases} ca\n"
            f"- Tồn quá 24h: {overdue_cases} ca\n"
            f"- Checklist lặp > 0: {repeat_cases} ca\n\n"
            f"⚡ Hệ thống cập nhật realtime từ Google Sheets!"
        )
        return report_msg
    except Exception as e:
        return f"⚠️ Không thể đọc dữ liệu báo cáo lúc này: {str(e)}"

def send_zalo_group_message(message):
    """Hàm gửi tin nhắn chủ động vào Group Zalo qua Zalo Bot Platform API"""
    url = "https://bot.zaloplatforms.com/api/v1/message"
    headers = {
        "Authorization": f"Bearer {ZALO_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "recipient": {"group_id": ZALO_GROUP_ID},
        "message": {"text": message}
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

# --- KHỞI TẠO FLASK SERVER NHẬN WEBHOOK TỪ ZALO BOT ---
flask_app = Flask(__name__)

@flask_app.route('/zalo-webhook', methods=['POST'])
def zalo_webhook():
    """Endpoint lắng nghe sự kiện khi người dùng nhắn tin hoặc @bot trên Zalo"""
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    # Phân tích cấu trúc payload từ Zalo Bot (tuỳ thuộc vào chuẩn event của Zalo Bot Platform)
    # Khi có người @bot hoặc gửi tin nhắn, hệ thống sẽ trigger vào đây
    message_text = ""
    try:
        # Cấu trúc thông điệp Zalo Bot gửi tới webhook
        event_name = data.get("event_name", "")
        if "message" in data or event_name == "user_send_text":
            # Trích xuất nội dung tin nhắn hoặc kiểm tra nếu có từ khóa kích hoạt
            message_text = data.get("message", {}).get("text", "").lower()
            
            # Phản hồi khi có người @bot hoặc gọi lệnh báo cáo
            if "@bot" in message_text or "bao cao" in message_text or "kpi" in message_text:
                summary_text = fetch_kpi_summary_for_bot()
                send_zalo_group_message(summary_text)
    except Exception as e:
        print(f"Webhook processing error: {e}")

    return jsonify({"status": "success", "error": 0}), 200

def run_flask():
    """Chạy Flask server ngầm ở cổng 5000 để làm webhook nhận tin nhắn từ Zalo"""
    flask_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

# Khởi chạy Flask webhook ngầm trong luồng riêng biệt (Thread) ngay khi app khởi động
if 'flask_started' not in st.session_state:
    st.session_state['flask_started'] = True
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()


# --- CẤU HÌNH GIAO DIỆN STREAMLIT ---
st.set_page_config(
    page_title="TQG-Dashboard Kiểm Soát Ca Tồn & Checklist (CLL)",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown('''
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
    </style>
''', unsafe_allow_html=True)

# Xử lý sự kiện gửi Zalo thủ công từ nút bấm trên giao diện
query_params = st.query_params
if "action" in query_params and query_params["action"] == "send_zalo":
    msg_content = query_params.get("msg", "📊 Báo cáo Kiểm soát Ca tồn (CLL)")
    success, res = send_zalo_group_message(msg_content)
    if success:
        st.success("✅ Đã gửi báo cáo thành công vào Group Zalo!")
    else:
        st.error(f"❌ Lỗi gửi tin nhắn: {res}")
    st.query_params.clear()

# --- MÃ HTML/JS GIAO DIỆN DASHBOARD HOÀN CHỈNH ---
html_content = '''<!DOCTYPE html>
<html lang="vi" class="h-full bg-slate-50">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Kiểm Soát Ca Tồn & Checklist (CLL)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        .col-highlight { background-color: #f7f9f2 !important; border-left: 1px solid #d4e1bd; border-right: 1px solid #d4e1bd; }
    </style>
</head>
<body class="h-full text-slate-800 font-sans antialiased flex flex-col p-6">
    <div class="max-w-7xl w-full mx-auto space-y-6">
        <div class="flex items-center justify-between bg-white p-4 rounded-xl shadow-sm border">
            <h1 class="text-lg font-bold text-slate-900">🚀 Dashboard TQG - Sẵn sàng kết nối Bot Zalo</h1>
            <button onclick="triggerSendZalo()" class="px-4 py-2 bg-blue-500 text-white text-xs font-bold rounded-lg shadow hover:bg-blue-600 transition">
                <i class="fa-solid fa-paper-plane mr-1"></i> Gửi Báo Cáo Nhanh Zalo
            </button>
        </div>
    </div>
    <script>
        function triggerSendZalo() {
            const defaultMsg = "📊 Báo cáo Kiểm soát Ca tồn (CLL) từ Web Dashboard trực tuyến!";
            window.parent.location.search = `?action=send_zalo&msg=${encodeURIComponent(defaultMsg)}`;
        }
    </script>
</body>
</html>'''

components.html(html_content, height=300, scrolling=True)
