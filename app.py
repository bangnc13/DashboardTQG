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
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: {
                            50: '#eff6ff',
                            100: '#dbeafe',
                            500: '#3b82f6',
                            600: '#2563eb',
                            700: '#1d4ed8',
                        },
                        paleOlive: {
                            50: '#f7f9f2',
                            100: '#e9efdc',
                            200: '#d4e1bd',
                            300: '#b7ce96',
                            400: '#94b36c',
                            500: '#759948',
                            600: '#5c7b35',
                            700: '#465e28',
                            800: '#3a4e23',
                            900: '#30411d',
                            950: '#1c2810'
                        },
                        amberYellow: '#fef08a',
                        amberBorder: '#eab308'
                    },
                    fontFamily: {
                        sans: ['Inter', 'sans-serif'],
                    }
                }
            }
        }
    </script>
    <style>
        ::-webkit-scrollbar {
            width: 6px;
            height: 6px;
        }
        ::-webkit-scrollbar-track {
            background: #f1f5f9;
        }
        ::-webkit-scrollbar-thumb {
            background: #cbd5e1;
            border-radius: 4px;
        }
        ::-webkit-scrollbar-thumb:hover {
            background: #94a3b8;
        }
        
        .col-highlight {
            background-color: #f7f9f2 !important;
            border-left: 1px solid #d4e1bd;
            border-right: 1px solid #d4e1bd;
        }
        .dark .col-highlight {
            background-color: rgba(117, 153, 72, 0.12) !important;
            border-left: 1px solid rgba(117, 153, 72, 0.3);
            border-right: 1px solid rgba(117, 153, 72, 0.3);
        }
        
        @keyframes slideIn {
            from { transform: translateY(-100%); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
        .animate-toast {
            animation: slideIn 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        }
    </style>
</head>
<body class="h-full text-slate-800 dark:text-slate-100 dark:bg-slate-900 font-sans antialiased flex flex-col">

    <div id="toastContainer" class="fixed top-4 right-4 z-50 space-y-2 pointer-events-none"></div>

    <!-- MODAL NHẬP PASSWORD BẢO MẬT -->
    <div id="passwordModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center hidden">
        <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-700 p-6 w-full max-w-sm mx-4 transform transition-all">
            <div class="flex items-center space-x-3 mb-4">
                <div class="w-10 h-10 rounded-xl bg-amber-100 dark:bg-amber-900/40 text-amber-600 dark:text-amber-400 flex items-center justify-center font-bold">
                    <i class="fa-solid fa-lock text-lg"></i>
                </div>
                <div>
                    <h3 id="modalTitle" class="text-base font-bold text-slate-900 dark:text-white">Xác thực quyền thao tác</h3>
                    <p id="modalDesc" class="text-xs text-slate-500 dark:text-slate-400">Vui lòng nhập mật khẩu để tiếp tục</p>
                </div>
            </div>

            <div class="space-y-4">
                <div>
                    <input type="password" id="importPasswordInput" placeholder="Nhập mật khẩu..." onkeyup="if(event.key==='Enter') verifyPassword()" class="w-full px-3 py-2 text-sm bg-slate-50 dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-emerald-500 dark:text-white">
                    <p id="passwordError" class="text-xs text-rose-500 mt-1 hidden"><i class="fa-solid fa-circle-exclamation mr-1"></i>Mật khẩu không đúng!</p>
                </div>

                <div class="flex items-center justify-end space-x-2">
                    <button onclick="closePasswordModal()" class="px-4 py-2 text-xs font-medium text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-700 rounded-lg transition">Hủy</button>
                    <button onclick="verifyPassword()" class="px-4 py-2 text-xs font-semibold text-white bg-emerald-600 hover:bg-emerald-700 rounded-lg transition shadow-sm">Xác nhận</button>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL CONFIRM ZALO -->
    <div id="zaloModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center hidden">
        <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-700 p-6 w-full max-w-md mx-4 transform transition-all">
            <div class="flex items-center space-x-3 mb-4">
                <div class="w-10 h-10 rounded-xl bg-blue-100 dark:bg-blue-900/40 text-blue-600 dark:text-blue-400 flex items-center justify-center font-bold">
                    <i class="fa-solid fa-paper-plane text-lg"></i>
                </div>
                <div>
                    <h3 class="text-base font-bold text-slate-900 dark:text-white">Gửi báo cáo qua Zalo</h3>
                    <p class="text-xs text-slate-500 dark:text-slate-400">Bot Thư Ký TQG sẽ gửi nội dung này vào nhóm</p>
                </div>
            </div>

            <div class="space-y-4">
                <div>
                    <textarea id="zaloMessageContent" rows="7" class="w-full px-3 py-2 text-sm bg-slate-50 dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 dark:text-white resize-none"></textarea>
                </div>

                <div class="flex items-center justify-end space-x-2">
                    <button onclick="closeZaloModal()" class="px-4 py-2 text-xs font-medium text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-700 rounded-lg transition">Hủy</button>
                    <button onclick="triggerSendZalo()" class="px-4 py-2 text-xs font-semibold text-white bg-blue-600 hover:bg-blue-700 rounded-lg transition shadow-sm">
                        <i class="fa-brands fa-diaspora mr-1"></i> Gửi ngay
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- MODAL CONFIRM TELEGRAM -->
    <div id="telegramModal" class="fixed inset-0 bg-slate-900/60 backdrop-blur-sm z-50 flex items-center justify-center hidden">
        <div class="bg-white dark:bg-slate-800 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-700 p-6 w-full max-w-md mx-4 transform transition-all">
            <div class="flex items-center space-x-3 mb-4">
                <div class="w-10 h-10 rounded-xl bg-sky-100 dark:bg-sky-900/40 text-sky-600 dark:text-sky-400 flex items-center justify-center font-bold">
                    <i class="fa-brands fa-telegram text-lg"></i>
                </div>
                <div>
                    <h3 class="text-base font-bold text-slate-900 dark:text-white">Gửi báo cáo qua Telegram</h3>
                    <p class="text-xs text-slate-500 dark:text-slate-400">Bot sẽ gửi nội dung này vào nhóm Telegram</p>
                </div>
            </div>

            <div class="space-y-4">
                <div>
                    <textarea id="telegramMessageContent" rows="7" class="w-full px-3 py-2 text-sm bg-slate-50 dark:bg-slate-900 border border-slate-300 dark:border-slate-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-sky-500 dark:text-white resize-none"></textarea>
                </div>

                <div class="flex items-center justify-end space-x-2">
                    <button onclick="closeTelegramModal()" class="px-4 py-2 text-xs font-medium text-slate-600 hover:bg-slate-100 dark:text-slate-300 dark:hover:bg-slate-700 rounded-lg transition">Hủy</button>
                    <button onclick="triggerSendTelegram()" class="px-4 py-2 text-xs font-semibold text-white bg-sky-600 hover:bg-sky-700 rounded-lg transition shadow-sm">
                        <i class="fa-brands fa-telegram mr-1"></i> Gửi ngay
                    </button>
                </div>
            </div>
        </div>
    </div>

    <header class="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 sticky top-0 z-30 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-paleOlive-600 to-paleOlive-400 flex items-center justify-center text-white font-bold shadow-md shadow-paleOlive-200 dark:shadow-none">
                        <i class="fa-solid fa-list-check text-xl"></i>
                    </div>
                    <div>
                        <div class="flex items-center space-x-2">
                            <h1 class="text-lg font-bold text-slate-900 dark:text-white leading-tight">DASHBOARD KIỂM SOÁT CA TỒN & CHECKLIST</h1>
                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-paleOlive-100 text-paleOlive-900 border border-paleOlive-300 dark:bg-paleOlive-900/40 dark:text-paleOlive-200">
                                Báo Cáo Kiểm Soát
                            </span>
                        </div>
                        <p class="text-xs text-slate-500 dark:text-slate-400">Make by BangNC13</p>
                    </div>
                </div>

                <div class="flex items-center space-x-3">
                    <!-- NÚT GỬI ZALO -->
                    <button onclick="openZaloModal()" class="inline-flex items-center px-3 py-2 text-xs font-bold rounded-lg text-white bg-blue-500 hover:bg-blue-600 transition shadow-sm" title="Gửi thông báo vào Group Zalo">
                        <i class="fa-solid fa-paper-plane mr-2 text-sm"></i>
                        <span>Gửi Zalo</span>
                    </button>

                    <!-- NÚT GỬI TELEGRAM -->
                    <button onclick="openTelegramModal()" class="inline-flex items-center px-3 py-2 text-xs font-bold rounded-lg text-white bg-sky-500 hover:bg-sky-600 transition shadow-sm" title="Gửi thông báo vào Group Telegram">
                        <i class="fa-brands fa-telegram mr-2 text-sm"></i>
                        <span>Gửi Telegram</span>
                    </button>
                    
                    <div class="w-px h-6 bg-slate-200 dark:bg-slate-700 mx-1"></div>

                    <div class="flex items-center space-x-2">
                        <span class="flex h-2.5 w-2.5 relative" title="Chế độ tự động đồng bộ Realtime đang bật">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                        </span>
                        <button id="syncBtn" onclick="fetchGoogleSheetData(true)" class="inline-flex items-center px-3 py-2 text-xs font-semibold rounded-lg text-white bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 transition shadow-sm">
                            <i id="syncIcon" class="fa-solid fa-arrows-rotate mr-2 text-sm"></i>
                            <span>Đồng bộ</span>
                        </button>
                    </div>

                    <button onclick="openPasswordModal('EXCEL')" class="inline-flex items-center px-3 py-2 text-xs font-medium rounded-lg text-slate-700 bg-slate-100 hover:bg-slate-200 dark:text-slate-200 dark:bg-slate-700 dark:hover:bg-slate-600 transition shadow-sm" title="Upload file offline nếu cần">
                        <i class="fa-solid fa-file-excel text-emerald-600 dark:text-emerald-400 mr-2 text-sm"></i>
                        <span>File Excel</span>
                    </button>
                    <input type="file" id="excelFileInput" accept=".xlsx, .xls, .csv" class="hidden" onchange="handleFileUpload(event)">

                    <button onclick="exportDataCSV()" class="inline-flex items-center px-3 py-2 text-xs font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 transition shadow-sm">
                        <i class="fa-solid fa-download mr-1.5"></i> Export Excel
                    </button>

                    <button onclick="toggleDarkMode()" class="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-700 transition" title="Đổi giao diện">
                        <i class="fa-solid fa-moon dark:hidden text-lg"></i>
                        <i class="fa-solid fa-sun hidden dark:inline text-lg text-amber-400"></i>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">

        <!-- BỘ LỌC QUẢN LÝ TẬP TRUNG -->
        <div class="bg-gradient-to-r from-paleOlive-100/90 via-paleOlive-50 to-white dark:from-paleOlive-950/60 dark:via-slate-800 dark:to-slate-800 p-4 rounded-xl border-2 border-paleOlive-400 dark:border-paleOlive-600 shadow-md flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
            <div class="flex items-center space-x-3">
                <div class="w-11 h-11 rounded-xl bg-paleOlive-600 text-white flex items-center justify-center shadow-md shrink-0">
                    <i class="fa-solid fa-user-shield text-xl"></i>
                </div>
                <div>
                    <div class="flex items-center space-x-2">
                        <label for="filterColAN" class="text-sm font-bold text-paleOlive-950 dark:text-paleOlive-100 uppercase tracking-wide">
                            Lọc Theo Quản Lý Phụ Trách
                        </label>
                        <span id="activeManagerBadge" class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-paleOlive-200 text-paleOlive-900 dark:bg-paleOlive-800 dark:text-paleOlive-100">
                            Tất cả
                        </span>
                    </div>
                    <p class="text-xs text-slate-600 dark:text-slate-400">Chọn Quản lý để cập nhật lại toàn bộ các ô chỉ số KPI, Biểu đồ phân tích và Bảng dữ liệu phía dưới</p>
                </div>
            </div>

            <div class="w-full md:w-80 shrink-0">
                <div class="relative">
                    <select id="filterColAN" onchange="onColANChange()" class="w-full py-2.5 pl-3 pr-8 text-xs font-bold bg-white dark:bg-slate-900 border-2 border-paleOlive-500 dark:border-paleOlive-500 text-paleOlive-950 dark:text-paleOlive-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-paleOlive-600 shadow-sm cursor-pointer transition">
                        <option value="">-- Tất cả Quản lý --</option>
                    </select>
                </div>
            </div>
        </div>

        <!-- KPI Cards Area -->
        <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Tổng Ca Tồn</div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiTotal" class="text-2xl font-bold text-slate-900 dark:text-white">0</span>
                    <span id="kpiTotalSub" class="text-xs text-blue-600 bg-blue-50 dark:bg-blue-900/30 dark:text-blue-300 px-2 py-0.5 rounded-full">Tất cả</span>
                </div>
                <div class="mt-2 text-xs text-slate-500 dark:text-slate-400 truncate">Tổng hợp hợp đồng tồn</div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-blue-500"></div>
            </div>

            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-rose-600 dark:text-rose-400 uppercase tracking-wider flex items-center justify-between">
                    <span>KH Giục Tiến Độ</span>
                    <i class="fa-solid fa-bullhorn"></i>
                </div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiUrgent" class="text-2xl font-bold text-rose-600 dark:text-rose-400">0</span>
                    <span id="kpiUrgentPct" class="text-xs text-rose-700 bg-rose-50 dark:bg-rose-900/30 dark:text-rose-300 px-2 py-0.5 rounded-full">0%</span>
                </div>
                <div class="mt-2 text-xs text-slate-500 dark:text-slate-400 truncate">Có ghi nhận giục tiến độ</div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-rose-500"></div>
            </div>

            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-amber-600 dark:text-amber-400 uppercase tracking-wider flex items-center justify-between">
                    <span>CLL Đang Tồn</span>
                    <i class="fa-solid fa-rotate-right"></i>
                </div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiRepeat" class="text-2xl font-bold text-amber-600 dark:text-amber-400">0</span>
                    <span id="kpiRepeatCases" class="text-xs text-amber-700 bg-amber-50 dark:bg-amber-900/30 dark:text-amber-300 px-2 py-0.5 rounded-full">0 ca</span>
                </div>
                <div class="mt-2 text-xs text-slate-500 dark:text-slate-400">Tổng số ca vụ lặp (Lặp > 0)</div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-amber-500"></div>
            </div>

            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-purple-600 dark:text-purple-400 uppercase tracking-wider flex items-center justify-between">
                    <span>Tồn Giờ ≥ 24H</span>
                    <i class="fa-solid fa-clock"></i>
                </div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiOverdue" class="text-2xl font-bold text-purple-600 dark:text-purple-400">0</span>
                    <span id="kpiOverduePct" class="text-xs text-purple-700 bg-purple-50 dark:bg-purple-900/30 dark:text-purple-300 px-2 py-0.5 rounded-full">0%</span>
                </div>
                <div class="mt-2 text-xs text-slate-500 dark:text-slate-400">Ca quá hạn 1 ngày</div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-purple-500"></div>
            </div>

            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-indigo-600 dark:text-indigo-400 uppercase tracking-wider flex items-center justify-between">
                    <span>Đang Xử Lý</span>
                    <i class="fa-solid fa-gears"></i>
                </div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiProcessing" class="text-2xl font-bold text-indigo-600 dark:text-indigo-400">0</span>
                    <span id="kpiProcessingPct" class="text-xs text-indigo-700 bg-indigo-50 dark:bg-indigo-900/30 dark:text-indigo-300 px-2 py-0.5 rounded-full">0%</span>
                </div>
                <div class="mt-2 text-xs text-slate-500 dark:text-slate-400">Trạng thái Đang XL</div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-indigo-500"></div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white dark:bg-slate-800 p-5 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm flex flex-col">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h2 class="text-sm font-bold text-slate-900 dark:text-white flex items-center">
                            <i class="fa-solid fa-chart-pie text-amber-500 mr-2"></i>
                            1. Thống Kê Checklist Lặp
                        </h2>
                        <p class="text-xs text-slate-500 dark:text-slate-400">Tỷ lệ ca tồn có Checklist lặp so với không lặp</p>
                    </div>
                </div>
                <div class="relative flex-1 min-h-[260px]">
                    <canvas id="chartRepeatPriority"></canvas>
                </div>
            </div>

            <div class="bg-white dark:bg-slate-800 p-5 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm flex flex-col">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h2 class="text-sm font-bold text-slate-900 dark:text-white flex items-center">
                            <i class="fa-solid fa-chart-bar text-blue-500 mr-2"></i>
                            2. Top Block Tồn Ca Nhiều Nhất
                        </h2>
                        <p class="text-xs text-slate-500 dark:text-slate-400">Đơn vị địa bàn phát sinh sự cố</p>
                    </div>
                </div>
                <div class="relative flex-1 min-h-[260px]">
                    <canvas id="chartTopBlock"></canvas>
                </div>
            </div>

            <div class="bg-white dark:bg-slate-800 p-5 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm flex flex-col">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h2 class="text-sm font-bold text-slate-900 dark:text-white flex items-center">
                            <i class="fa-solid fa-network-wired text-emerald-500 mr-2"></i>
                            3. Tồn theo POP
                        </h2>
                        <p class="text-xs text-slate-500 dark:text-slate-400"> </p>
                    </div>
                </div>
                <div class="relative flex-1 min-h-[260px]">
                    <canvas id="chartTopPop"></canvas>
                </div>
            </div>

            <div class="bg-white dark:bg-slate-800 p-5 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm flex flex-col">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h2 class="text-sm font-bold text-slate-900 dark:text-white flex items-center">
                            <i class="fa-solid fa-user-gear text-purple-500 mr-2"></i>
                            4. Top KTV Tồn Ca nhiều nhất
                        </h2>
                        <p class="text-xs text-slate-500 dark:text-slate-400">Xếp hạng nhân sự có số tồn case vụ cao nhất</p>
                    </div>
                </div>
                <div class="relative flex-1 min-h-[260px]">
                    <canvas id="chartTopTech"></canvas>
                </div>
            </div>
        </div>

        <div class="bg-white dark:bg-slate-800 rounded-xl border border-paleOlive-300 dark:border-paleOlive-700 shadow-sm overflow-hidden">
            <div class="p-5 border-b border-paleOlive-200 dark:border-paleOlive-800 space-y-4 bg-paleOlive-50/60 dark:bg-paleOlive-950/20">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <h2 class="text-base font-bold text-paleOlive-950 dark:text-paleOlive-100 flex items-center">
                            <i class="fa-solid fa-table-cells text-paleOlive-600 mr-2"></i>
                            BẢNG KIỂM SOÁT DỮ LIỆU TỒN CA
                        </h2>
                        <p class="text-xs text-paleOlive-800/80 dark:text-paleOlive-300/80">Xem, tìm kiếm và lọc bổ sung dữ liệu tồn ca theo nhu cầu</p>
                    </div>

                    <div class="flex items-center space-x-2">
                        <label class="inline-flex items-center space-x-2 text-xs font-semibold text-paleOlive-900 dark:text-paleOlive-200 bg-paleOlive-100 dark:bg-paleOlive-900/50 px-3 py-1.5 rounded-lg cursor-pointer border border-paleOlive-300 dark:border-paleOlive-700 hover:bg-paleOlive-200 dark:hover:bg-paleOlive-800/60 transition shadow-sm">
                            <input type="checkbox" id="chkNonZero" onchange="applyFilters()" class="w-4 h-4 text-paleOlive-600 rounded border-paleOlive-300 focus:ring-paleOlive-500 dark:bg-slate-800">
                            <span><i class="fa-solid fa-filter mr-1 text-paleOlive-700 dark:text-paleOlive-300"></i> Chỉ lấy CL Lặp khác 0</span>
                        </label>

                        <button onclick="resetFilters()" class="px-3 py-1.5 text-xs font-medium text-slate-600 bg-slate-100 hover:bg-slate-200 dark:text-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 rounded-lg transition">
                            <i class="fa-solid fa-arrows-rotate mr-1"></i> Xóa Tất Cả Lọc
                        </button>
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 pt-2">
                    <div class="relative sm:col-span-2 lg:col-span-1">
                        <i class="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-slate-400 text-xs"></i>
                        <input type="text" id="searchInput" oninput="applyFilters()" placeholder="Tìm Số HĐ, KH..." class="w-full pl-8 pr-3 py-1.5 text-xs bg-white dark:bg-slate-900 border border-paleOlive-300 dark:border-paleOlive-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-paleOlive-500 dark:text-white">
                    </div>

                    <div>
                        <select id="filterTech" onchange="applyFilters()" class="w-full py-1.5 px-3 text-xs bg-white dark:bg-slate-900 border border-paleOlive-300 dark:border-paleOlive-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-paleOlive-500 dark:text-white">
                            <option value="">Tất cả Nhân sự</option>
                        </select>
                    </div>

                    <div>
                        <select id="filterUrgent" onchange="applyFilters()" class="w-full py-1.5 px-3 text-xs bg-white dark:bg-slate-900 border border-paleOlive-300 dark:border-paleOlive-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-paleOlive-500 dark:text-white">
                            <option value="">T
