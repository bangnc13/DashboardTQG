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

def send_zalo_group_message(message):
    """Hàm gửi tin nhắn vào Group Zalo qua Zalo Bot Platform API (Đã xử lý an toàn phản hồi)"""
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
        
        # Kiểm tra nếu nội dung trả về rỗng
        if not response.text.strip():
            return False, f"API trả về phản hồi rỗng (Mã lỗi HTTP: {response.status_code})"
            
        # Thử parse JSON an toàn
        try:
            res_data = response.json()
        except Exception:
            return False, f"Phản hồi không hợp lệ (HTTP {response.status_code}): {response.text}"
            
        if response.status_code == 200 and res_data.get("error") == 0:
            return True, res_data
        else:
            return False, res_data
    except Exception as e:
        return False, str(e)

def fetch_kpi_summary_for_bot():
    """Hàm độc lập giúp bot Zalo tự động đọc dữ liệu từ Google Sheets để trả về khi bị @mention"""
    csv_url = f"https://docs.google.com/spreadsheets/d/{GOOGLE_SHEET_ID}/gviz/tq?tqx=out:csv"
    try:
        df = pd.read_csv(csv_url)
        total_cases = len(df)
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
            f"📊 **BÁO CÁO NHANH CA TỒN (CLL)**\n"
            f"- Tổng tồn: {total_cases} ca\n"
            f"- KH Giục: {urgent_cases} ca\n"
            f"- Tồn quá 24h: {overdue_cases} ca\n"
            f"- Checklist lặp > 0: {repeat_cases} ca\n\n"
            f"⚡ Hệ thống cập nhật realtime từ Google Sheets!"
        )
        return report_msg
    except Exception as e:
        return f"⚠ Không thể đọc dữ liệu báo cáo lúc này: {str(e)}"

# --- KHỞI TẠO FLASK SERVER NHẬN WEBHOOK TỪ ZALO ---
flask_app = Flask(__name__)

@flask_app.route('/zalo-webhook', methods=['POST'])
def zalo_webhook():
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400
    try:
        event_name = data.get("event_name", "")
        if "message" in data or event_name == "user_send_text":
            message_text = data.get("message", {}).get("text", "").lower()
            if "@bot" in message_text or "bao cao" in message_text or "kpi" in message_text:
                summary_text = fetch_kpi_summary_for_bot()
                send_zalo_group_message(summary_text)
    except Exception as e:
        print(f"Webhook processing error: {e}")
    return jsonify({"status": "success", "error": 0}), 200

def run_flask():
    flask_app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)

if 'flask_started' not in st.session_state:
    st.session_state['flask_started'] = True
    t = threading.Thread(target=run_flask, daemon=True)
    t.start()


# --- CẤU HÌNH TRANG STREAMLIT ---
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
            padding-top: 0rem !important;
            padding-bottom: 0rem !important;
            padding-left: 0rem !important;
            padding-right: 0rem !important;
            max-width: 100% !important;
        }
    </style>
''', unsafe_allow_html=True)

# Thanh công cụ Streamlit chứa nút bấm gửi Zalo trực tiếp
col_zalo_1, col_zalo_2 = st.columns([6, 1])
with col_zalo_2:
    if st.button("📤 Gửi ngay qua Zalo", use_container_width=True, type="primary"):
        default_msg = f"📊 Báo cáo Kiểm soát Ca tồn (CLL) từ Web Dashboard trực tuyến!"
        success, res = send_zalo_group_message(default_msg)
        if success:
            st.success("✅ Đã gửi báo cáo thành công vào Group Zalo!")
        else:
            st.error(f"❌ Lỗi gửi tin nhắn: {res}")

# --- GIAO DIỆN HTML/CSS/JS DASHBOARD HOÀN CHỈNH ---
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
    
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        paleOlive: {
                            50: '#f7f9f2', 100: '#e9efdc', 200: '#d4e1bd', 300: '#b7ce96',
                            400: '#94b36c', 500: '#759948', 600: '#5c7b35', 700: '#465e28',
                            800: '#3a4e23', 900: '#30411d', 950: '#1c2810'
                        }
                    },
                    fontFamily: { sans: ['Inter', 'sans-serif'] }
                }
            }
        }
    </script>
    <style>
        ::-webkit-scrollbar { width: 6px; height: 6px; }
        ::-webkit-scrollbar-track { background: #f1f5f9; }
        ::-webkit-scrollbar-thumb { background: #cbd5e1; border-radius: 4px; }
        .col-highlight { background-color: #f7f9f2 !important; border-left: 1px solid #d4e1bd; border-right: 1px solid #d4e1bd; }
        .dark .col-highlight { background-color: rgba(117, 153, 72, 0.12) !important; border-left: 1px solid rgba(117, 153, 72, 0.3); border-right: 1px solid rgba(117, 153, 72, 0.3); }
        @keyframes slideIn { from { transform: translateY(-100%); opacity: 0; } to { transform: translateY(0); opacity: 1; } }
        .animate-toast { animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
    </style>
</head>
<body class="h-full text-slate-800 dark:text-slate-100 dark:bg-slate-900 font-sans antialiased flex flex-col">

    <div id="toastContainer" class="fixed top-4 right-4 z-50 space-y-2 pointer-events-none"></div>

    <!-- MODAL NHẬP PASSWORD -->
    <div id="passwordModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center hidden">
        <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-700 p-6 w-full max-w-sm mx-4">
            <div class="flex items-center space-x-3 mb-4">
                <div class="w-10 h-10 rounded-xl bg-amber-100 text-amber-600 flex items-center justify-center font-bold">
                    <i class="fa-solid fa-lock text-lg"></i>
                </div>
                <div>
                    <h3 id="modalTitle" class="text-base font-bold text-slate-900 dark:text-white">Xác thực quyền thao tác</h3>
                    <p id="modalDesc" class="text-xs text-slate-500">Vui lòng nhập mật khẩu để tiếp tục</p>
                </div>
            </div>
            <div class="space-y-4">
                <input type="password" id="importPasswordInput" placeholder="Nhập mật khẩu..." onkeyup="if(event.key==='Enter') verifyPassword()" class="w-full px-3 py-2 text-sm bg-slate-50 dark:bg-slate-900 border rounded-lg focus:outline-none dark:text-white">
                <p id="passwordError" class="text-xs text-rose-500 mt-1 hidden"><i class="fa-solid fa-circle-exclamation mr-1"></i>Mật khẩu không đúng!</p>
                <div class="flex items-center justify-end space-x-2">
                    <button onclick="closePasswordModal()" class="px-4 py-2 text-xs font-medium text-slate-600 dark:text-slate-300">Hủy</button>
                    <button onclick="verifyPassword()" class="px-4 py-2 text-xs font-semibold text-white bg-emerald-600 rounded-lg">Xác nhận</button>
                </div>
            </div>
        </div>
    </div>

    <header class="bg-white dark:bg-slate-800 border-b sticky top-0 z-30 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-paleOlive-600 to-paleOlive-400 flex items-center justify-center text-white font-bold shadow-md">
                        <i class="fa-solid fa-list-check text-xl"></i>
                    </div>
                    <div>
                        <div class="flex items-center space-x-2">
                            <h1 class="text-lg font-bold text-slate-900 dark:text-white leading-tight">DASHBOARD KIỂM SOÁT CA TỒN & CHECKLIST</h1>
                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-paleOlive-100 text-paleOlive-900">Báo Cáo Kiểm Soát</span>
                        </div>
                        <p class="text-xs text-slate-500">Make by BangNC13</p>
                    </div>
                </div>

                <div class="flex items-center space-x-3">
                    <button id="syncBtn" onclick="fetchGoogleSheetData(true)" class="inline-flex items-center px-3 py-2 text-xs font-semibold rounded-lg text-white bg-emerald-600 hover:bg-emerald-700 transition shadow-sm">
                        <i id="syncIcon" class="fa-solid fa-arrows-rotate mr-2"></i><span>Đồng bộ</span>
                    </button>
                    <button onclick="openPasswordModal('EXCEL')" class="inline-flex items-center px-3 py-2 text-xs font-medium rounded-lg text-slate-700 bg-slate-100 hover:bg-slate-200 dark:text-slate-200 dark:bg-slate-700">
                        <i class="fa-solid fa-file-excel text-emerald-600 mr-2"></i><span>File Excel</span>
                    </button>
                    <input type="file" id="excelFileInput" accept=".xlsx, .xls, .csv" class="hidden" onchange="handleFileUpload(event)">
                    <button onclick="exportDataCSV()" class="inline-flex items-center px-3 py-2 text-xs font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700">
                        <i class="fa-solid fa-download mr-1.5"></i> Export Excel
                    </button>
                    <button onclick="toggleDarkMode()" class="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-700">
                        <i class="fa-solid fa-moon dark:hidden text-lg"></i>
                        <i class="fa-solid fa-sun hidden dark:inline text-lg text-amber-400"></i>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        <!-- BỘ LỌC -->
        <div class="bg-gradient-to-r from-paleOlive-100/90 via-paleOlive-50 to-white dark:from-paleOlive-950/60 dark:via-slate-800 p-4 rounded-xl border-2 border-paleOlive-400 shadow-md flex flex-col md:flex-row items-center justify-between gap-4">
            <div class="flex items-center space-x-3">
                <div class="w-11 h-11 rounded-xl bg-paleOlive-600 text-white flex items-center justify-center shadow-md shrink-0">
                    <i class="fa-solid fa-user-shield text-xl"></i>
                </div>
                <div>
                    <div class="flex items-center space-x-2">
                        <label for="filterColAN" class="text-sm font-bold text-paleOlive-950 dark:text-paleOlive-100 uppercase">Lọc Theo Quản Lý Phụ Trách</label>
                        <span id="activeManagerBadge" class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-paleOlive-200 text-paleOlive-900">Tất cả</span>
                    </div>
                    <p class="text-xs text-slate-600 dark:text-slate-400">Chọn Quản lý để cập nhật lại toàn bộ KPI, biểu đồ và bảng dữ liệu</p>
                </div>
            </div>
            <div class="w-full md:w-80 shrink-0">
                <select id="filterColAN" onchange="onColANChange()" class="w-full py-2.5 px-3 text-xs font-bold bg-white dark:bg-slate-900 border-2 border-paleOlive-500 rounded-xl dark:text-white">
                    <option value="">-- Tất cả Quản lý --</option>
                </select>
            </div>
        </div>

        <!-- KPI CARDS -->
        <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-slate-500 uppercase">Tổng Ca Tồn</div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiTotal" class="text-2xl font-bold dark:text-white">0</span>
                    <span id="kpiTotalSub" class="text-xs text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full">Tất cả</span>
                </div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-blue-500"></div>
            </div>
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-rose-600 uppercase flex justify-between"><span>KH Giục Tiến Độ</span><i class="fa-solid fa-bullhorn"></i></div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiUrgent" class="text-2xl font-bold text-rose-600">0</span>
                    <span id="kpiUrgentPct" class="text-xs text-rose-700 bg-rose-50 px-2 py-0.5 rounded-full">0%</span>
                </div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-rose-500"></div>
            </div>
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-amber-600 uppercase flex justify-between"><span>CLL Đang Tồn</span><i class="fa-solid fa-rotate-right"></i></div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiRepeat" class="text-2xl font-bold text-amber-600">0</span>
                    <span id="kpiRepeatCases" class="text-xs text-amber-700 bg-amber-50 px-2 py-0.5 rounded-full">0 ca</span>
                </div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-amber-500"></div>
            </div>
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-purple-600 uppercase flex justify-between"><span>Tồn Giờ ≥ 24H</span><i class="fa-solid fa-clock"></i></div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiOverdue" class="text-2xl font-bold text-purple-600">0</span>
                    <span id="kpiOverduePct" class="text-xs text-purple-700 bg-purple-50 px-2 py-0.5 rounded-full">0%</span>
                </div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-purple-500"></div>
            </div>
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-indigo-600 uppercase flex justify-between"><span>Đang Xử Lý</span><i class="fa-solid fa-gears"></i></div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiProcessing" class="text-2xl font-bold text-indigo-600">0</span>
                    <span id="kpiProcessingPct" class="text-xs text-indigo-700 bg-indigo-50 px-2 py-0.5 rounded-full">0%</span>
                </div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-indigo-500"></div>
            </div>
        </div>

        <!-- CHARTS -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white dark:bg-slate-800 p-5 rounded-xl border shadow-sm flex flex-col">
                <h2 class="text-sm font-bold dark:text-white mb-2"><i class="fa-solid fa-chart-pie text-amber-500 mr-2"></i>1. Thống Kê Checklist Lặp</h2>
                <div class="relative flex-1 min-h-[260px]"><canvas id="chartRepeatPriority"></canvas></div>
            </div>
            <div class="bg-white dark:bg-slate-800 p-5 rounded-xl border shadow-sm flex flex-col">
                <h2 class="text-sm font-bold dark:text-white mb-2"><i class="fa-solid fa-chart-bar text-blue-500 mr-2"></i>2. Top Block Tồn Ca Nhiều Nhất</h2>
                <div class="relative flex-1 min-h-[260px]"><canvas id="chartTopBlock"></canvas></div>
            </div>
            <div class="bg-white dark:bg-slate-800 p-5 rounded-xl border shadow-sm flex flex-col">
                <h2 class="text-sm font-bold dark:text-white mb-2"><i class="fa-solid fa-network-wired text-emerald-500 mr-2"></i>3. Tồn theo POP</h2>
                <div class="relative flex-1 min-h-[260px]"><canvas id="chartTopPop"></canvas></div>
            </div>
            <div class="bg-white dark:bg-slate-800 p-5 rounded-xl border shadow-sm flex flex-col">
                <h2 class="text-sm font-bold dark:text-white mb-2"><i class="fa-solid fa-user-gear text-purple-500 mr-2"></i>4. Top KTV Tồn Ca nhiều nhất</h2>
                <div class="relative flex-1 min-h-[260px]"><canvas id="chartTopTech"></canvas></div>
            </div>
        </div>

        <!-- TABLE SECTION -->
        <div class="bg-white dark:bg-slate-800 rounded-xl border shadow-sm overflow-hidden">
            <div class="p-5 border-b space-y-4 bg-paleOlive-50/60 dark:bg-paleOlive-950/20">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <h2 class="text-base font-bold dark:text-white"><i class="fa-solid fa-table-cells text-paleOlive-600 mr-2"></i>BẢNG KIỂM SOÁT DỮ LIỆU TỒN CA</h2>
                    <div class="flex items-center space-x-2">
                        <label class="inline-flex items-center space-x-2 text-xs font-semibold text-paleOlive-900 dark:text-paleOlive-200 bg-paleOlive-100 dark:bg-paleOlive-900/50 px-3 py-1.5 rounded-lg cursor-pointer border">
                            <input type="checkbox" id="chkNonZero" onchange="applyFilters()" class="w-4 h-4 text-paleOlive-600 rounded">
                            <span><i class="fa-solid fa-filter mr-1"></i> Chỉ lấy CL Lặp khác 0</span>
                        </label>
                        <button onclick="resetFilters()" class="px-3 py-1.5 text-xs font-medium text-slate-600 bg-slate-100 dark:text-slate-300 dark:bg-slate-700 rounded-lg">Xóa Lọc</button>
                    </div>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
                    <input type="text" id="searchInput" oninput="applyFilters()" placeholder="Tìm Số HĐ, KH..." class="w-full pl-3 py-1.5 text-xs bg-white dark:bg-slate-900 border rounded-lg dark:text-white sm:col-span-2 lg:col-span-1">
                    <select id="filterTech" onchange="applyFilters()" class="w-full py-1.5 px-3 text-xs bg-white dark:bg-slate-900 border rounded-lg dark:text-white"><option value="">Tất cả Nhân sự</option></select>
                    <select id="filterUrgent" onchange="applyFilters()" class="w-full py-1.5 px-3 text-xs bg-white dark:bg-slate-900 border rounded-lg dark:text-white">
                        <option value="">Tất cả KH Giục</option><option value="YES">Có giục tiến độ</option><option value="NO">Không giục tiến độ</option>
                    </select>
                    <select id="filterRepeat" onchange="applyFilters()" class="w-full py-1.5 px-3 text-xs bg-white dark:bg-slate-900 border rounded-lg dark:text-white">
                        <option value="">Tất cả CL Lặp</option><option value="1">Lặp 1 lần</option><option value="2">Lặp 2 lần</option><option value="3">Lặp ≥ 3 lần</option>
                    </select>
                    <select id="filterBlock" onchange="applyFilters()" class="w-full py-1.5 px-3 text-xs bg-white dark:bg-slate-900 border rounded-lg dark:text-white"><option value="">Tất cả Block</option></select>
                </div>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse text-xs">
                    <thead>
                        <tr class="bg-paleOlive-100 dark:bg-paleOlive-900/60 text-paleOlive-900 dark:text-paleOlive-200 font-bold border-b uppercase">
                            <th class="py-3 px-3 w-12 text-center border-r">STT</th>
                            <th class="py-3 px-3 w-32 border-r">Số HĐ</th>
                            <th class="py-3 px-3 min-w-[140px] border-r">Block</th>
                            <th class="py-3 px-3 text-center w-24 border-r">Lần Hẹn</th>
                            <th class="py-3 px-3 text-center w-24 border-r">CL Lặp</th>
                            <th class="py-3 px-3 min-w-[130px] border-r">Nhân Sự</th>
                            <th class="py-3 px-3 min-w-[150px] border-r">Quản Lý</th>
                            <th class="py-3 px-3 min-w-[140px] border-r">KH Giục Tiến Độ</th>
                            <th class="py-3 px-3 text-center w-24">Tồn Giờ</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody" class="divide-y dark:divide-paleOlive-800/40"></tbody>
                </table>
            </div>

            <div class="px-5 py-3 bg-paleOlive-100/50 dark:bg-paleOlive-950/40 border-t flex flex-col sm:flex-row items-center justify-between gap-3 text-xs">
                <div>Hiển thị từ <span id="startIndex" class="font-bold">0</span> đến <span id="endIndex" class="font-bold">0</span> trong tổng số <span id="totalCount" class="font-bold">0</span> ca tồn</div>
                <div id="paginationControls" class="flex items-center space-x-1"></div>
                <div class="italic">BangNC13-TQG.</div>
            </div>
        </div>
    </main>

    <script>
        const DEFAULT_PASSWORD = "1900";
        const LOCAL_STORAGE_KEY = "TQG_DASHBOARD_DATASET";
        const PAGE_SIZE = 10;
        let currentPage = 1;
        let pendingAction = null;

        const managerMapping = {
            "TQGTI.GIANGVH2": "ANHHV15", "TQGTI.THANHNV41": "ANHHV15", "TQGTI.CAONB": "ANHHV15", "TQGTI.KHANHLQ1": "ANHHV15",
            "TQGTI.CUHA": "HUONGTT33", "TQGTI.QUANDM2": "HUONGTT33", "TQGTI.ANHPH3": "HUONGTT33", "TQGTI.HOANQV": "HUONGTT33", "TQGTI.CHIENMM": "HUONGTT33", "TQGTI.HUNGDQ5": "HUONGTT33",
            "TQGTI.CUONGLM8": "LYHK7", "TQGTI.NGHIANV6": "LYHK7", "TQGTI.CONGND4": "LYHK7",
            "TQGTI.QUYETNT1": "TAMVTT5", "TQGTI.BINHLV6": "TAMVTT5", "TQGTI.DUNGNT26": "TAMVTT5", "TQGTI.QUANHV1": "TAMVTT5",
            "TQGTI.HIEUNV38": "HANGVTT12", "TQGTI.HUYNHNX": "HANGVTT12", "TQGTI.HANHPB": "HANGVTT12", "TQGTI.GIANGLV2": "HANGVTT12",
            "TQGTI.NAMVD2": "TRANGDTH35", "TQGTI.THANHNV8": "TRANGDTH35", "TQGTI.TUANQD": "TRANGDTH35", "TQGTI.CUORGDD9": "TRANGDTH35",
            "TQGTI.DANGNV": "TRANGHT28", "TQGTI.BINHTH1": "TRANGHT28", "TQGTI.TRUNGNX3": "TRANGHT28", "TQGTI.TUNGDT4": "TRANGHT28",
            "TQGTI.TIENVT3": "UYENHT15", "TQGTI.LUCMDC": "UYENHT15", "TQGTI.CAOTT": "UYENHT15", "TQGTI.TUANLQ2": "UYENHT15", "TQGTI.HUNGCV4": "UYENHT15"
        };

        const GOOGLE_SHEET_ID = '1qKW7OcGegD1IXcgV5WYXuzcUzYvpjZw-CqgzpYDLKoM';
        let currentDataset = [];
        let chartRepeatPriority = null, chartTopBlock = null, chartTopPop = null, chartTopTech = null;

        function openPasswordModal(actionType = 'EXCEL') {
            pendingAction = actionType;
            document.getElementById('importPasswordInput').value = '';
            document.getElementById('passwordError').classList.add('hidden');
            document.getElementById('passwordModal').classList.remove('hidden');
            setTimeout(() => document.getElementById('importPasswordInput').focus(), 100);
        }
        function closePasswordModal() { document.getElementById('passwordModal').classList.add('hidden'); pendingAction = null; }
        function verifyPassword() {
            if (document.getElementById('importPasswordInput').value === DEFAULT_PASSWORD) {
                closePasswordModal();
                if (pendingAction === 'EXCEL') document.getElementById('excelFileInput').click();
            } else {
                document.getElementById('passwordError').classList.remove('hidden');
            }
        }

        function calculateTonGioFromColumnI(dateStr) {
            if (!dateStr && dateStr !== 0) return 0;
            if (typeof dateStr === 'number' && dateStr < 10000) return Math.max(0, Math.floor(dateStr));
            let parsedDate = null;
            if (typeof dateStr === 'number') {
                parsedDate = new Date(Math.round((dateStr - 25569) * 86400 * 1000));
            } else {
                const str = String(dateStr).trim();
                if (!str) return 0;
                if (!isNaN(str) && Number(str) < 10000) return Math.max(0, Math.floor(Number(str)));
                const parts = str.split(/[ T]+/);
                const datePart = parts[0];
                const timePart = parts[1] || "00:00:00";
                if (datePart.includes('/') || datePart.includes('-')) {
                    const sep = datePart.includes('/') ? '/' : '-';
                    const comps = datePart.split(sep);
                    if (comps.length === 3) {
                        let d, m, y;
                        if (comps[0].length === 4) { y = parseInt(comps[0]); m = parseInt(comps[1])-1; d = parseInt(comps[2]); }
                        else { d = parseInt(comps[0]); m = parseInt(comps[1])-1; y = parseInt(comps[2]); }
                        const tComps = timePart.split(':');
                        parsedDate = new Date(y, m, d, parseInt(tComps[0])||0, parseInt(tComps[1])||0, parseInt(tComps[2])||0);
                    }
                }
                if (!parsedDate || isNaN(parsedDate.getTime())) parsedDate = new Date(str);
            }
            if (!parsedDate || isNaN(parsedDate.getTime())) return 0;
            const diffHours = Math.floor((new Date() - parsedDate) / (1000 * 60 * 60));
            return diffHours > 0 ? diffHours : 0;
        }

        function showToast(message, type = 'info') {
            const container = document.getElementById('toastContainer');
            if (!container) return;
            const toast = document.createElement('div');
            const bg = { success: 'bg-emerald-600', error: 'bg-rose-600', info: 'bg-slate-800' };
            toast.className = `flex items-center space-x-2 px-4 py-3 rounded-xl shadow-lg text-xs font-medium text-white animate-toast ${bg[type]||bg.info}`;
            toast.innerHTML = `<span>${message}</span>`;
            container.appendChild(toast);
            setTimeout(() => toast.remove(), 3000);
        }

        function populateFilterOptions() {
            const anSel = document.getElementById('filterColAN'), techSel = document.getElementById('filterTech'), blockSel = document.getElementById('filterBlock');
            if (!anSel) return;
            const curAN = anSel.value, curTech = techSel.value, curBlock = blockSel.value;
            const managers = [...new Set(currentDataset.map(d => d["Cột AN"]).filter(Boolean))].sort();
            const techs = [...new Set(currentDataset.map(d => d["Nhân sự"]).filter(Boolean))].sort();
            const blocks = [...new Set(currentDataset.map(d => d["Block"]).filter(Boolean))].sort();

            anSel.innerHTML = '<option value="">-- Tất cả Quản lý --</option>' + managers.map(m => `<option value="${m}">${m}</option>`).join('');
            anSel.value = curAN;
            techSel.innerHTML = '<option value="">Tất cả Nhân sự</option>' + techs.map(t => `<option value="${t}">${t}</option>`).join('');
            techSel.value = curTech;
            blockSel.innerHTML = '<option value="">Tất cả Block</option>' + blocks.map(b => `<option value="${b}">${b}</option>`).join('');
            blockSel.value = curBlock;
        }

        function onColANChange() {
            document.getElementById('activeManagerBadge').textContent = document.getElementById('filterColAN').value || 'Tất cả';
            applyFilters();
        }

        function resetFilters() {
            ['filterColAN', 'searchInput', 'filterTech', 'filterUrgent', 'filterRepeat', 'filterBlock'].forEach(id => document.getElementById(id).value = '');
            document.getElementById('chkNonZero').checked = false;
            document.getElementById('activeManagerBadge').textContent = 'Tất cả';
            applyFilters();
        }

        function getFilteredData() {
            const an = document.getElementById('filterColAN')?.value || '';
            const search = document.getElementById('searchInput')?.value?.toLowerCase().trim() || '';
            const tech = document.getElementById('filterTech')?.value || '';
            const urgent = document.getElementById('filterUrgent')?.value || '';
            const repeat = document.getElementById('filterRepeat')?.value || '';
            const block = document.getElementById('filterBlock')?.value || '';
            const nonZero = document.getElementById('chkNonZero')?.checked || false;

            return currentDataset.filter(item => {
                if (an && item["Cột AN"] !== an) return false;
                if (tech && item["Nhân sự"] !== tech) return false;
                if (block && item["Block"] !== block) return false;
                if (nonZero && item["CL Lặp"] === 0) return false;
                if (urgent) {
                    const hasUrg = Boolean(item["KH Giục Tiến Độ"] && item["KH Giục Tiến Độ"].toString().trim() !== '');
                    if (urgent === 'YES' && !hasUrg) return false;
                    if (urgent === 'NO' && hasUrg) return false;
                }
                if (repeat) {
                    if (repeat === '1' && item["CL Lặp"] !== 1) return false;
                    if (repeat === '2' && item["CL Lặp"] !== 2) return false;
                    if (repeat === '3' && item["CL Lặp"] < 3) return false;
                }
                if (search && !item["Số HĐ"]?.toLowerCase().includes(search) && !item["Tên đầy đủ"]?.toLowerCase().includes(search)) return false;
                return true;
            });
        }

        function applyFilters() { currentPage = 1; const f = getFilteredData(); updateKPIs(f); renderCharts(f); renderTable(f); }

        function updateKPIs(data) {
            const total = data.length;
            const repeatCases = data.filter(d => (d["CL Lặp"] || 0) > 0).length;
            const overdue = data.filter(d => (d["Tồn giờ"] || 0) >= 24).length;
            const processing = data.filter(d => d["TTCL"] === 'Đang XL').length;
            const urgent = data.filter(d => d["KH Giục Tiến Độ"] && d["KH Giục Tiến Độ"].toString().trim() !== '').length;

            document.getElementById('kpiTotal').textContent = total;
            document.getElementById('kpiUrgent').textContent = urgent;
            document.getElementById('kpiUrgentPct').textContent = total ? Math.round((urgent / total) * 100) + '%' : '0%';
            document.getElementById('kpiRepeat').textContent = repeatCases;
            document.getElementById('kpiRepeatCases').textContent = repeatCases + ' ca';
            document.getElementById('kpiOverdue').textContent = overdue;
            document.getElementById('kpiOverduePct').textContent = total ? Math.round((overdue / total) * 100) + '%' : '0%';
            document.getElementById('kpiProcessing').textContent = processing;
            document.getElementById('kpiProcessingPct').textContent = total ? Math.round((processing / total) * 100) + '%' : '0%';
        }

        function goToPage(p) { currentPage = p; renderTable(getFilteredData()); }

        function renderTable(data) {
            const tbody = document.getElementById('tableBody');
            const total = data.length, totalPages = Math.ceil(total / PAGE_SIZE) || 1;
            if (currentPage > totalPages) currentPage = totalPages;
            if (currentPage < 1) currentPage = 1;
            const start = (currentPage - 1) * PAGE_SIZE, end = Math.min(start + PAGE_SIZE, total);

            document.getElementById('startIndex').textContent = total ? start + 1 : 0;
            document.getElementById('endIndex').textContent = end;
            document.getElementById('totalCount').textContent = total;
            renderPagination(totalPages);

            if (!tbody) return;
            if (!total) { tbody.innerHTML = `<tr><td colspan="9" class="py-8 text-center text-slate-400 italic">Không tìm thấy ca tồn nào</td></tr>`; return; }

            tbody.innerHTML = data.slice(start, end).map((item, idx) => {
                const isRep = (item["CL Lặp"] || 0) > 0, isOv = (item["Tồn giờ"] || 0) >= 24;
                const urg = item["KH Giục Tiến Độ"] ? item["KH Giục Tiến Độ"].toString().trim() : '';
                return `
                    <tr class="hover:bg-paleOlive-100/50 dark:hover:bg-paleOlive-900/35 transition border-b">
                        <td class="py-2.5 px-3 text-center text-slate-500">${start + idx + 1}</td>
                        <td class="py-2.5 px-3 font-semibold text-blue-600">${item["Số HĐ"] || '-'}</td>
                        <td class="py-2.5 px-3 font-medium">${item["Block"] || '-'}</td>
                        <td class="py-2.5 px-3 text-center">${item["Số lần hẹn"] || 0}</td>
                        <td class="py-2.5 px-3 text-center col-highlight font-semibold">${isRep ? `<span class="px-2 py-0.5 rounded-full bg-amber-100 text-amber-900">${item["CL Lặp"]}</span>` : '0'}</td>
                        <td class="py-2.5 px-3 font-medium">${item["Nhân sự"] || '-'}</td>
                        <td class="py-2.5 px-3 font-medium text-paleOlive-900 dark:text-paleOlive-200 col-highlight">${item["Cột AN"] || '-'}</td>
                        <td class="py-2.5 px-3 font-medium text-rose-600">${urg ? `<span class="px-2 py-0.5 rounded bg-rose-100 text-rose-800">${urg}</span>` : '-'}</td>
                        <td class="py-2.5 px-3 text-center ${isOv ? 'text-purple-600 font-bold' : ''}">${item["Tồn giờ"] ?? 0}h</td>
                    </tr>
                `;
            }).join('');
        }

        function renderPagination(totalPages) {
            const container = document.getElementById('paginationControls');
            if (!container || totalPages <= 1) { container.innerHTML = ''; return; }
            let html = `<button onclick="goToPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''} class="px-2 py-1 border rounded bg-white dark:bg-slate-800 disabled:opacity-40"><i class="fa-solid fa-chevron-left"></i></button>`;
            for (let p = 1; p <= totalPages; p++) {
                html += `<button onclick="goToPage(${p})" class="px-2.5 py-1 border rounded ${p === currentPage ? 'bg-paleOlive-600 text-white font-bold' : 'bg-white dark:bg-slate-800'}">${p}</button>`;
            }
            html += `<button onclick="goToPage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''} class="px-2 py-1 border rounded bg-white dark:bg-slate-800 disabled:opacity-40"><i class="fa-solid fa-chevron-right"></i></button>`;
            container.innerHTML = html;
        }

        function renderCharts(data) {
            const isDark = document.documentElement.classList.contains('dark');
            const color = isDark ? '#94a3b8' : '#475569';
            const hasRep = data.filter(d => (d["CL Lặp"] || 0) > 0).length, noRep = data.filter(d => (d["CL Lặp"] || 0) === 0).length;

            if (chartRepeatPriority) chartRepeatPriority.destroy();
            const ctx1 = document.getElementById('chartRepeatPriority')?.getContext('2d');
            if (ctx1) chartRepeatPriority = new Chart(ctx1, { type: 'doughnut', data: { labels: ['Có CL Lặp (>0)', 'Không Lặp (=0)'], datasets: [{ data: [hasRep, noRep], backgroundColor: ['#f59e0b', '#3b82f6'] }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color } } } } });

            const blockMap = {}; data.forEach(d => { if (d["Block"]) blockMap[d["Block"]] = (blockMap[d["Block"]] || 0) + 1; });
            const sBlocks = Object.entries(blockMap).sort((a, b) => b[1] - a[1]).slice(0, 8);
            if (chartTopBlock) chartTopBlock.destroy();
            const ctx2 = document.getElementById('chartTopBlock')?.getContext('2d');
            if (ctx2) chartTopBlock = new Chart(ctx2, { type: 'bar', data: { labels: sBlocks.map(b => b[0]), datasets: [{ data: sBlocks.map(b => b[1]), backgroundColor: '#0284c7', borderRadius: 6 }] }, options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color }, beginAtZero: true }, y: { ticks: { color }, grid: { display: false } } } } });

            const popMap = {}; data.forEach(d => { if (d["POP"]) popMap[d["POP"]] = (popMap[d["POP"]] || 0) + 1; });
            const sPops = Object.entries(popMap).sort((a, b) => b[1] - a[1]).slice(0, 8);
            if (chartTopPop) chartTopPop.destroy();
            const ctx3 = document.getElementById('chartTopPop')?.getContext('2d');
            if (ctx3) chartTopPop = new Chart(ctx3, { type: 'bar', data: { labels: sPops.map(p => p[0]), datasets: [{ data: sPops.map(p => p[1]), backgroundColor: '#10b981', borderRadius: 6 }] }, options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color }, grid: { display: false } }, y: { ticks: { color }, beginAtZero: true } } } });

            const techMap = {}; data.forEach(d => { if (d["Nhân sự"]) techMap[d["Nhân sự"]] = (techMap[d["Nhân sự"]] || 0) + 1; });
            const sTechs = Object.entries(techMap).sort((a, b) => b[1] - a[1]).slice(0, 8);
            if (chartTopTech) chartTopTech.destroy();
            const ctx4 = document.getElementById('chartTopTech')?.getContext('2d');
            if (ctx4) chartTopTech = new Chart(ctx4, { type: 'bar', data: { labels: sTechs.map(t => t[0]), datasets: [{ data: sTechs.map(t => t[1]), backgroundColor: '#8b5cf6', borderRadius: 6 }] }, options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color }, beginAtZero: true }, y: { ticks: { color }, grid: { display: false } } } } });
        }

        async function fetchGoogleSheetData(showNotif = true) {
            const url = `https://docs.google.com/spreadsheets/d/${GOOGLE_SHEET_ID}/gviz/tq?tqx=out:csv&_nc=${Date.now()}`;
            const icon = document.getElementById('syncIcon');
            if (icon) icon.classList.add('fa-spin');
            try {
                if (showNotif) showToast('Đang đồng bộ Google Sheets...', 'info');
                const res = await fetch(url);
                const text = await res.text();
                const wb = XLSX.read(text, { type: 'string' });
                const rows = XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]], { header: 1, defval: '' });
                if (processRows(rows) && showNotif) showToast(`Đồng bộ thành công ${currentDataset.length} ca tồn!`, 'success');
            } catch (err) {
                if (showNotif) showToast('Lỗi đồng bộ: ' + err.message, 'error');
            } finally {
                if (icon) icon.classList.remove('fa-spin');
            }
        }

        function processRows(rows) {
            if (!rows || rows.length <= 1) return false;
            let hIdx = 0;
            for (let r = 0; r < Math.min(10, rows.length); r++) {
                if (rows[r].map(c => String(c).toUpperCase()).join(' ').includes('SỐ HĐ')) { hIdx = r; break; }
            }
            const headers = rows[hIdx].map(h => String(h).trim());
            const getCol = (names, fb) => {
                const idx = headers.findIndex(h => names.some(n => h.toLowerCase().includes(n.toLowerCase())));
                return idx !== -1 ? idx : fb;
            };

            const records = [];
            for (let r = hIdx + 1; r < rows.length; r++) {
                const row = rows[r];
                if (!row || !row.length) continue;
                const soHD = String(row[getCol(['Số HĐ'], 5)] || '').trim();
                const block = String(row[getCol(['Block'], 4)] || '').trim();
                if (!soHD && !block) continue;
                const tech = String(row[getCol(['Nhân sự'], 18)] || '').trim();
                records.push({
                    "Block": block, "Số HĐ": soHD, "Tên đầy đủ": String(row[getCol(['Tên đầy đủ'], 6)] || '').trim(),
                    "Tồn giờ": calculateTonGioFromColumnI(row[8]), "Số lần hẹn": parseInt(row[getCol(['Lần hẹn'], 14)], 10) || 0,
                    "CL Lặp": parseInt(row[getCol(['CL Lặp'], 15)], 10) || 0, "Nhân sự": tech,
                    "KH Giục Tiến Độ": String(row[getCol(['Giục'], 21)] || '').trim(),
                    "TTCL": String(row[getCol(['TTCL'], 19)] || 'Đang XL').trim(),
                    "POP": String(row[20] || '').trim().substring(0, 7),
                    "Cột AN": managerMapping[tech] || String(row[getCol(['cột an'], 39)] || '').trim()
                });
            }
            if (records.length) { currentDataset = records; populateFilterOptions(); applyFilters(); return true; }
            return false;
        }

        function handleFileUpload(e) {
            const file = e.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(evt) {
                const wb = XLSX.read(new Uint8Array(evt.target.result), { type: 'array' });
                if (processRows(XLSX.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]], { header: 1, defval: '' }))) {
                    showToast(`Import thành công ${currentDataset.length} ca!`, 'success');
                }
            };
            reader.readAsArrayBuffer(file);
            e.target.value = '';
        }

        function exportDataCSV() {
            const data = getFilteredData();
            if (!data.length) { showToast('Không có dữ liệu!', 'error'); return; }
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(data), "Kiểm Soát Ca Tồn");
            XLSX.writeFile(wb, "Bao_Cao_Kiem_Soat_Ca_Ton.xlsx");
            showToast('Đã xuất file Excel!', 'success');
        }

        function toggleDarkMode() {
            document.documentElement.classList.toggle('dark');
            renderCharts(getFilteredData());
        }

        window.onload = function() {
            fetchGoogleSheetData(true);
            setInterval(() => fetchGoogleSheetData(false), 30000);
        };
    </script>
</body>
</html>'''

components.html(html_content, height=1350, scrolling=True)
