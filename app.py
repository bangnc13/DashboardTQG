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

# Lấy Group ID và Token Zalo Bot
ZALO_BOT_TOKEN = "3613571325008693860:BsVltrcHugOoOMZsOvVZywwbfdjueukaFtofsLetSAYUUevPgFQaQsUDOprWWesx"
ZALO_GROUP_ID = "d71241c2588cb1d2e89d"

def send_zalo_group_message(message):
    """Hàm gửi tin nhắn vào Group Zalo qua Zalo Bot Platform API"""
    url = "https://bot.zaloplatforms.com/api/v1/message"
    headers = {
        "Authorization": f"Bearer {ZALO_BOT_TOKEN}",
        "Content-Type": "application/json"
    }
    
    # Cấu trúc payload chuẩn cho tin nhắn nhóm qua Zalo Bot
    payload = {
        "recipient": {
            "chat_id": ZALO_GROUP_ID
        },
        "message": {
            "text": message
        }
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        # Kiểm tra phản hồi thô từ server
        if not response.text or not response.text.strip():
            return False, f"API trả về phản hồi rỗng (HTTP Status Code: {response.status_code})"
        
        try:
            res_data = response.json()
        except json.JSONDecodeError:
            return False, f"HTTP Status {response.status_code} - Phản hồi từ Zalo: {response.text}"
        
        if response.status_code == 200 and res_data.get("error") == 0:
            return True, res_data
        else:
            return False, f"Mã lỗi từ Zalo: {res_data}"
    except Exception as e:
        return False, str(e)

# --- KHU VỰC GỬI ZALO TRỰC QUAN TRÊN STREAMLIT ---
with st.container():
    st.markdown("""
        <div style="background: linear-gradient(to right, #eff6ff, #dbeafe); padding: 12px 20px; border-bottom: 2px solid #3b82f6; display: flex; align-items: center; justify-content: space-between;">
            <div style="display: flex; align-items: center; gap: 10px;">
                <i class="fa-brands fa-diaspora" style="color: #2563eb; font-size: 20px;"></i>
                <span style="font-weight: bold; color: #1e3a8a; font-size: 14px;">BẢNG ĐIỀU KHIỂN GỬI BÁO CÁO NHÓM ZALO BOT</span>
            </div>
            <span style="font-size: 12px; color: #64748b;">(Tích hợp bắt lỗi chi tiết HTTP 500)</span>
        </div>
    """, unsafe_allow_html=True)
    
    col_zalo_1, col_zalo_2 = st.columns([4, 1])
    with col_zalo_1:
        default_zalo_msg = "📊 Báo cáo Kiểm soát Ca tồn (CLL):\n- Đơn vị: TQG\n- Trạng thái: Đang theo dõi ca tồn hệ thống\n\nTruy cập Dashboard để xem chi tiết biểu đồ!"
        zalo_msg_input = st.text_area("Nội dung tin nhắn gửi Zalo:", value=default_zalo_msg, height=80, label_visibility="collapsed")
    with col_zalo_2:
        st.markdown("<div style='height: 5px;'></div>", unsafe_allow_html=True)
        if st.button("🚀 Gửi ngay vào Zalo", type="primary", use_container_width=True):
            if not zalo_msg_input.strip():
                st.warning("⚠️ Vui lòng nhập nội dung tin nhắn cần gửi!")
            else:
                with st.spinner("Đang kết nối Zalo Bot API..."):
                    success, res = send_zalo_group_message(zalo_msg_input)
                    if success:
                        st.success("✅ Đã gửi báo cáo thành công vào Group Zalo!")
                    else:
                        st.error(f"❌ Lỗi gửi tin nhắn: {res}")

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
                        paleOlive: {
                            50: '#f7f9f2', 100: '#e9efdc', 200: '#d4e1bd', 300: '#b7ce96', 400: '#94b36c',
                            500: '#759948', 600: '#5c7b35', 700: '#465e28', 800: '#3a4e23', 900: '#30411d', 950: '#1c2810'
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

    <!-- MODAL NHẬP PASSWORD BẢO MẬT -->
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
                    <button onclick="closePasswordModal()" class="px-4 py-2 text-xs font-medium text-slate-600">Hủy</button>
                    <button onclick="verifyPassword()" class="px-4 py-2 text-xs font-semibold text-white bg-emerald-600 rounded-lg">Xác nhận</button>
                </div>
            </div>
        </div>
    </div>

    <header class="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 sticky top-0 z-30 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-paleOlive-600 to-paleOlive-400 flex items-center justify-center text-white font-bold shadow-md">
                        <i class="fa-solid fa-list-check text-xl"></i>
                    </div>
                    <div>
                        <h1 class="text-lg font-bold text-slate-900 dark:text-white leading-tight">DASHBOARD KIỂM SOÁT CA TỒN & CHECKLIST</h1>
                        <p class="text-xs text-slate-500 dark:text-slate-400">Make by BangNC13</p>
                    </div>
                </div>

                <div class="flex items-center space-x-3">
                    <div class="flex items-center space-x-2">
                        <span class="flex h-2.5 w-2.5 relative">
                            <span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
                            <span class="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500"></span>
                        </span>
                        <button id="syncBtn" onclick="fetchGoogleSheetData(true)" class="inline-flex items-center px-3 py-2 text-xs font-semibold rounded-lg text-white bg-emerald-600 hover:bg-emerald-700 transition shadow-sm">
                            <i id="syncIcon" class="fa-solid fa-arrows-rotate mr-2 text-sm"></i>
                            <span>Đồng bộ</span>
                        </button>
                    </div>

                    <button onclick="openPasswordModal('EXCEL')" class="inline-flex items-center px-3 py-2 text-xs font-medium rounded-lg text-slate-700 bg-slate-100 hover:bg-slate-200 dark:text-slate-200 dark:bg-slate-700 transition">
                        <i class="fa-solid fa-file-excel text-emerald-600 mr-2 text-sm"></i>
                        <span>File Excel</span>
                    </button>
                    <input type="file" id="excelFileInput" accept=".xlsx, .xls, .csv" class="hidden" onchange="handleFileUpload(event)">

                    <button onclick="exportDataCSV()" class="inline-flex items-center px-3 py-2 text-xs font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 transition">
                        <i class="fa-solid fa-download mr-1.5"></i> Export Excel
                    </button>

                    <button onclick="toggleDarkMode()" class="p-2 rounded-lg text-slate-500 hover:bg-slate-100 dark:text-slate-400 dark:hover:bg-slate-700 transition">
                        <i class="fa-solid fa-moon dark:hidden text-lg"></i>
                        <i class="fa-solid fa-sun hidden dark:inline text-lg text-amber-400"></i>
                    </button>
                </div>
            </div>
        </div>
    </header>

    <main class="flex-1 max-w-7xl w-full mx-auto px-4 sm:px-6 lg:px-8 py-6 space-y-6">
        <!-- BỘ LỌC QUẢN LÝ -->
        <div class="bg-gradient-to-r from-paleOlive-100/90 via-paleOlive-50 to-white dark:from-paleOlive-950/60 dark:via-slate-800 p-4 rounded-xl border-2 border-paleOlive-400 flex flex-col md:flex-row items-stretch md:items-center justify-between gap-4">
            <div class="flex items-center space-x-3">
                <div class="w-11 h-11 rounded-xl bg-paleOlive-600 text-white flex items-center justify-center shadow-md shrink-0">
                    <i class="fa-solid fa-user-shield text-xl"></i>
                </div>
                <div>
                    <label class="text-sm font-bold text-paleOlive-950 dark:text-paleOlive-100 uppercase tracking-wide">
                        Lọc Theo Quản Lý Phụ Trách <span id="activeManagerBadge" class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-paleOlive-200 text-paleOlive-900">Tất cả</span>
                    </label>
                    <p class="text-xs text-slate-600 dark:text-slate-400">Chọn Quản lý để cập nhật lại KPI, Biểu đồ và Dữ liệu</p>
                </div>
            </div>
            <div class="w-full md:w-80 shrink-0">
                <select id="filterColAN" onchange="onColANChange()" class="w-full py-2.5 pl-3 pr-8 text-xs font-bold bg-white dark:bg-slate-900 border-2 border-paleOlive-500 rounded-xl focus:outline-none dark:text-white cursor-pointer">
                    <option value="">-- Tất cả Quản lý --</option>
                </select>
            </div>
        </div>

        <!-- KPI CARDS -->
        <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-slate-500 uppercase tracking-wider">Tổng Ca Tồn</div>
                <div class="mt-2 flex items-baseline justify-between"><span id="kpiTotal" class="text-2xl font-bold">0</span></div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-blue-500"></div>
            </div>
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-rose-600 uppercase tracking-wider">KH Giục Tiến Độ</div>
                <div class="mt-2 flex items-baseline justify-between"><span id="kpiUrgent" class="text-2xl font-bold text-rose-600">0</span><span id="kpiUrgentPct" class="text-xs px-2 py-0.5 rounded-full bg-rose-50 text-rose-700">0%</span></div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-rose-500"></div>
            </div>
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-amber-600 uppercase tracking-wider">CLL Đang Tồn</div>
                <div class="mt-2 flex items-baseline justify-between"><span id="kpiRepeat" class="text-2xl font-bold text-amber-600">0</span><span id="kpiRepeatCases" class="text-xs px-2 py-0.5 rounded-full bg-amber-50 text-amber-700">0 ca</span></div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-amber-500"></div>
            </div>
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-purple-600 uppercase tracking-wider">Tồn Giờ ≥ 24H</div>
                <div class="mt-2 flex items-baseline justify-between"><span id="kpiOverdue" class="text-2xl font-bold text-purple-600">0</span><span id="kpiOverduePct" class="text-xs px-2 py-0.5 rounded-full bg-purple-50 text-purple-700">0%</span></div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-purple-500"></div>
            </div>
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-indigo-600 uppercase tracking-wider">Đang Xử Lý</div>
                <div class="mt-2 flex items-baseline justify-between"><span id="kpiProcessing" class="text-2xl font-bold text-indigo-600">0</span><span id="kpiProcessingPct" class="text-xs px-2 py-0.5 rounded-full bg-indigo-50 text-indigo-700">0%</span></div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-indigo-500"></div>
            </div>
        </div>

        <!-- BIỂU ĐỒ -->
        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div class="bg-white dark:bg-slate-800 p-5 rounded-xl border border-slate-200 shadow-sm"><canvas id="chartRepeatPriority"></canvas></div>
            <div class="bg-white dark:bg-slate-800 p-5 rounded-xl border border-slate-200 shadow-sm"><canvas id="chartTopBlock"></canvas></div>
            <div class="bg-white dark:bg-slate-800 p-5 rounded-xl border border-slate-200 shadow-sm"><canvas id="chartTopPop"></canvas></div>
            <div class="bg-white dark:bg-slate-800 p-5 rounded-xl border border-slate-200 shadow-sm"><canvas id="chartTopTech"></canvas></div>
        </div>

        <!-- BẢNG DỮ LIỆU -->
        <div class="bg-white dark:bg-slate-800 rounded-xl border border-paleOlive-300 shadow-sm overflow-hidden">
            <div class="p-5 border-b space-y-4 bg-paleOlive-50/60 dark:bg-slate-900">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <h2 class="text-base font-bold text-paleOlive-950 dark:text-paleOlive-100 flex items-center">
                        <i class="fa-solid fa-table-cells text-paleOlive-600 mr-2"></i> BẢNG KIỂM SOÁT DỮ LIỆU TỒN CA
                    </h2>
                    <div class="flex items-center space-x-2">
                        <label class="inline-flex items-center space-x-2 text-xs font-semibold px-3 py-1.5 rounded-lg cursor-pointer bg-paleOlive-100 border border-paleOlive-300">
                            <input type="checkbox" id="chkNonZero" onchange="applyFilters()" class="w-4 h-4 text-paleOlive-600 rounded">
                            <span>Chỉ lấy CL Lặp khác 0</span>
                        </label>
                        <button onclick="resetFilters()" class="px-3 py-1.5 text-xs font-medium text-slate-600 bg-slate-100 rounded-lg">Xóa Lọc</button>
                    </div>
                </div>
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3">
                    <input type="text" id="searchInput" oninput="applyFilters()" placeholder="Tìm Số HĐ, KH..." class="w-full px-3 py-1.5 text-xs bg-white dark:bg-slate-900 border rounded-lg dark:text-white">
                    <select id="filterTech" onchange="applyFilters()" class="w-full py-1.5 px-3 text-xs bg-white dark:bg-slate-900 border rounded-lg dark:text-white"><option value="">Tất cả Nhân sự</option></select>
                    <select id="filterUrgent" onchange="applyFilters()" class="w-full py-1.5 px-3 text-xs bg-white dark:bg-slate-900 border rounded-lg dark:text-white"><option value="">Tất cả KH Giục</option><option value="YES">Có giục</option><option value="NO">Không giục</option></select>
                    <select id="filterRepeat" onchange="applyFilters()" class="w-full py-1.5 px-3 text-xs bg-white dark:bg-slate-900 border rounded-lg dark:text-white"><option value="">Tất cả CL Lặp</option><option value="1">Lặp 1</option><option value="2">Lặp 2</option><option value="3">Lặp ≥ 3</option></select>
                    <select id="filterBlock" onchange="applyFilters()" class="w-full py-1.5 px-3 text-xs bg-white dark:bg-slate-900 border rounded-lg dark:text-white"><option value="">Tất cả Block</option></select>
                </div>
            </div>
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse text-xs">
                    <thead>
                        <tr class="bg-paleOlive-100 dark:bg-slate-700 text-paleOlive-900 font-bold border-b">
                            <th class="py-3 px-3 text-center">STT</th>
                            <th class="py-3 px-3">Số HĐ</th>
                            <th class="py-3 px-3">Block</th>
                            <th class="py-3 px-3 text-center">Lần Hẹn</th>
                            <th class="py-3 px-3 text-center">CL Lặp</th>
                            <th class="py-3 px-3">Nhân Sự</th>
                            <th class="py-3 px-3">Quản Lý</th>
                            <th class="py-3 px-3">KH Giục</th>
                            <th class="py-3 px-3 text-center">Tồn Giờ</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody" class="divide-y"></tbody>
                </table>
            </div>
            <div class="px-5 py-3 bg-paleOlive-100/50 flex items-center justify-between text-xs">
                <div>Hiển thị <span id="startIndex">0</span> - <span id="endIndex">0</span> / <span id="totalCount">0</span> ca tồn</div>
                <div id="paginationControls" class="flex items-center space-x-1"></div>
            </div>
        </div>
    </main>

    <script>
        const DEFAULT_PASSWORD = "1900";
        const PAGE_SIZE = 10;
        let currentPage = 1;
        let pendingAction = null;

        const managerMapping = {
            "TQGTI.GIANGVH2": "ANHHV15", "TQGTI.THANHNV41": "ANHHV15", "TQGTI.CAONB": "ANHHV15", "TQGTI.KHANHLQ1": "ANHHV15",
            "TQGTI.CUHA": "HUONGTT33", "TQGTI.QUANDM2": "HUONGTT33", "TQGTI.ANHPH3": "HUONGTT33", "TQGTI.HOANQV": "HUONGTT33",
            "TQGTI.CHIENMM": "HUONGTT33", "TQGTI.HUNGDQ5": "HUONGTT33", "TQGTI.CUONGLM8": "LYHK7", "TQGTI.NGHIANV6": "LYHK7",
            "TQGTI.CONGND4": "LYHK7", "TQGTI.QUYETNT1": "TAMVTT5", "TQGTI.BINHLV6": "TAMVTT5", "TQGTI.DUNGNT26": "TAMVTT5",
            "TQGTI.QUANHV1": "TAMVTT5", "TQGTI.HIEUNV38": "HANGVTT12", "TQGTI.HUYNHNX": "HANGVTT12", "TQGTI.HANHPB": "HANGVTT12",
            "TQGTI.GIANGLV2": "HANGVTT12", "TQGTI.NAMVD2": "TRANGDTH35", "TQGTI.THANHNV8": "TRANGDTH35", "TQGTI.TUANQD": "TRANGDTH35",
            "TQGTI.CUORGDD9": "TRANGDTH35", "TQGTI.DANGNV": "TRANGHT28", "TQGTI.BINHTH1": "TRANGHT28", "TQGTI.TRUNGNX3": "TRANGHT28",
            "TQGTI.TUNGDT4": "TRANGHT28", "TQGTI.TIENVT3": "UYENHT15", "TQGTI.LUCMDC": "UYENHT15", "TQGTI.CAOTT": "UYENHT15",
            "TQGTI.TUANLQ2": "UYENHT15", "TQGTI.HUNGCV4": "UYENHT15"
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

        function closePasswordModal() {
            document.getElementById('passwordModal').classList.add('hidden');
            pendingAction = null;
        }

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
                    const separator = datePart.includes('/') ? '/' : '-';
                    const dc = datePart.split(separator);
                    if (dc.length === 3) {
                        let day, month, year;
                        if (dc[0].length === 4) {
                            year = parseInt(dc[0], 10); month = parseInt(dc[1], 10) - 1; day = parseInt(dc[2], 10);
                        } else {
                            day = parseInt(dc[0], 10); month = parseInt(dc[1], 10) - 1; year = parseInt(dc[2], 10);
                        }
                        const tc = timePart.split(':');
                        parsedDate = new Date(year, month, day, parseInt(tc[0], 10) || 0, parseInt(tc[1], 10) || 0, parseInt(tc[2], 10) || 0);
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
            const bgColors = { success: 'bg-emerald-600 text-white', error: 'bg-rose-600 text-white', info: 'bg-slate-800 text-white' };
            const icons = { success: 'fa-circle-check', error: 'fa-circle-exclamation', info: 'fa-circle-info' };
            toast.className = `flex items-center space-x-2 px-4 py-3 rounded-xl shadow-lg text-xs font-medium animate-toast ${bgColors[type]} pointer-events-auto`;
            toast.innerHTML = `<i class="fa-solid ${icons[type]} text-sm"></i><span>${message}</span>`;
            container.appendChild(toast);
            setTimeout(() => { toast.style.opacity = '0'; setTimeout(() => toast.remove(), 300); }, 3000);
        }

        function populateFilterOptions() {
            const colANSelect = document.getElementById('filterColAN');
            const techSelect = document.getElementById('filterTech');
            const blockSelect = document.getElementById('filterBlock');
            if (!colANSelect || !techSelect || !blockSelect) return;

            const currentAN = colANSelect.value, currentTech = techSelect.value, currentBlock = blockSelect.value;
            const managers = [...new Set(currentDataset.map(d => d["Cột AN"]).filter(Boolean))].sort();
            const techs = [...new Set(currentDataset.map(d => d["Nhân sự"]).filter(Boolean))].sort();
            const blocks = [...new Set(currentDataset.map(d => d["Block"]).filter(Boolean))].sort();

            colANSelect.innerHTML = '<option value="">-- Tất cả Quản lý --</option>' + managers.map(m => `<option value="${m}">${m}</option>`).join('');
            colANSelect.value = currentAN;
            techSelect.innerHTML = '<option value="">Tất cả Nhân sự</option>' + techs.map(t => `<option value="${t}">${t}</option>`).join('');
            techSelect.value = currentTech;
            blockSelect.innerHTML = '<option value="">Tất cả Block</option>' + blocks.map(b => `<option value="${b}">${b}</option>`).join('');
            blockSelect.value = currentBlock;
        }

        function onColANChange() {
            document.getElementById('activeManagerBadge').textContent = document.getElementById('filterColAN').value || 'Tất cả';
            applyFilters();
        }

        function resetFilters() {
            document.getElementById('filterColAN').value = '';
            document.getElementById('searchInput').value = '';
            document.getElementById('filterTech').value = '';
            document.getElementById('filterUrgent').value = '';
            document.getElementById('filterRepeat').value = '';
            document.getElementById('filterBlock').value = '';
            document.getElementById('chkNonZero').checked = false;
            document.getElementById('activeManagerBadge').textContent = 'Tất cả';
            applyFilters();
        }

        function getFilteredData() {
            const managerFilter = document.getElementById('filterColAN')?.value || '';
            const searchFilter = document.getElementById('searchInput')?.value?.toLowerCase().trim() || '';
            const techFilter = document.getElementById('filterTech')?.value || '';
            const urgentFilter = document.getElementById('filterUrgent')?.value || '';
            const repeatFilter = document.getElementById('filterRepeat')?.value || '';
            const blockFilter = document.getElementById('filterBlock')?.value || '';
            const chkNonZero = document.getElementById('chkNonZero')?.checked || false;

            return currentDataset.filter(item => {
                if (managerFilter && item["Cột AN"] !== managerFilter) return false;
                if (techFilter && item["Nhân sự"] !== techFilter) return false;
                if (blockFilter && item["Block"] !== blockFilter) return false;
                if (chkNonZero && item["CL Lặp"] === 0) return false;
                if (urgentFilter) {
                    const hasUrgent = Boolean(item["KH Giục Tiến Độ"] && item["KH Giục Tiến Độ"].toString().trim() !== '');
                    if (urgentFilter === 'YES' && !hasUrgent) return false;
                    if (urgentFilter === 'NO' && hasUrgent) return false;
                }
                if (repeatFilter) {
                    if (repeatFilter === '1' && item["CL Lặp"] !== 1) return false;
                    if (repeatFilter === '2' && item["CL Lặp"] !== 2) return false;
                    if (repeatFilter === '3' && item["CL Lặp"] < 3) return false;
                }
                if (searchFilter) {
                    const matchSoHD = item["Số HĐ"]?.toLowerCase().includes(searchFilter);
                    const matchName = item["Tên đầy đủ"]?.toLowerCase().includes(searchFilter);
                    const matchUrgent = item["KH Giục Tiến Độ"]?.toLowerCase().includes(searchFilter);
                    if (!matchSoHD && !matchName && !matchUrgent) return false;
                }
                return true;
            });
        }

        function applyFilters() {
            currentPage = 1;
            const filtered = getFilteredData();
            updateKPIs(filtered);
            renderCharts(filtered);
            renderTable(filtered);
        }

        function updateKPIs(data) {
            const total = data.length;
            const repeatCases = data.filter(d => (d["CL Lặp"] || 0) > 0).length;
            const overdueCases = data.filter(d => (d["Tồn giờ"] || 0) >= 24).length;
            const processingCases = data.filter(d => d["TTCL"] === 'Đang XL').length;
            const urgentCases = data.filter(d => d["KH Giục Tiến Độ"] && d["KH Giục Tiến Độ"].toString().trim() !== '').length;

            document.getElementById('kpiTotal').textContent = total;
            document.getElementById('kpiUrgent').textContent = urgentCases;
            document.getElementById('kpiUrgentPct').textContent = total ? Math.round((urgentCases / total) * 100) + '%' : '0%';
            document.getElementById('kpiRepeat').textContent = repeatCases;
            document.getElementById('kpiRepeatCases').textContent = repeatCases + ' ca';
            document.getElementById('kpiOverdue').textContent = overdueCases;
            document.getElementById('kpiOverduePct').textContent = total ? Math.round((overdueCases / total) * 100) + '%' : '0%';
            document.getElementById('kpiProcessing').textContent = processingCases;
            document.getElementById('kpiProcessingPct').textContent = total ? Math.round((processingCases / total) * 100) + '%' : '0%';
        }

        function goToPage(page) { currentPage = page; renderTable(getFilteredData()); }

        function renderTable(data) {
            const tbody = document.getElementById('tableBody');
            const total = data.length;
            const totalPages = Math.ceil(total / PAGE_SIZE) || 1;
            if (currentPage > totalPages) currentPage = totalPages;
            if (currentPage < 1) currentPage = 1;

            const startIdx = (currentPage - 1) * PAGE_SIZE;
            const endIdx = Math.min(startIdx + PAGE_SIZE, total);

            document.getElementById('startIndex').textContent = total > 0 ? startIdx + 1 : 0;
            document.getElementById('endIndex').textContent = endIdx;
            document.getElementById('totalCount').textContent = total;
            renderPagination(totalPages);

            if (!tbody) return;
            if (total === 0) {
                tbody.innerHTML = `<tr><td colspan="9" class="py-8 text-center text-slate-400 italic">Không tìm thấy ca tồn nào phù hợp</td></tr>`;
                return;
            }

            tbody.innerHTML = data.slice(startIdx, endIdx).map((item, idx) => {
                const isRepeat = (item["CL Lặp"] || 0) > 0;
                const isOverdue = (item["Tồn giờ"] || 0) >= 24;
                const urgentVal = item["KH Giục Tiến Độ"] ? item["KH Giục Tiến Độ"].toString().trim() : '';

                const repeatBadge = isRepeat ? `<span class="px-2 py-0.5 rounded-full text-xs font-bold bg-amber-100 text-amber-900">${item["CL Lặp"]}</span>` : `<span class="text-slate-400">0</span>`;
                const urgentBadge = urgentVal ? `<span class="px-2 py-0.5 rounded-md text-xs font-semibold bg-rose-100 text-rose-800 border border-rose-300"><i class="fa-solid fa-triangle-exclamation mr-1"></i>${urgentVal}</span>` : `<span class="text-slate-400">-</span>`;

                return `
                    <tr class="hover:bg-paleOlive-100/50 transition border-b">
                        <td class="py-2.5 px-3 text-center text-slate-500 font-medium">${startIdx + idx + 1}</td>
                        <td class="py-2.5 px-3 font-semibold text-blue-600">${item["Số HĐ"] || '-'}</td>
                        <td class="py-2.5 px-3 font-medium">${item["Block"] || '-'}</td>
                        <td class="py-2.5 px-3 text-center">${item["Số lần hẹn"] || 0}</td>
                        <td class="py-2.5 px-3 text-center col-highlight font-semibold">${repeatBadge}</td>
                        <td class="py-2.5 px-3 font-medium">${item["Nhân sự"] || '-'}</td>
                        <td class="py-2.5 px-3 font-medium col-highlight">${item["Cột AN"] || '-'}</td>
                        <td class="py-2.5 px-3 font-medium text-rose-600">${urgentBadge}</td>
                        <td class="py-2.5 px-3 text-center ${isOverdue ? 'text-purple-600 font-bold' : ''}">${item["Tồn giờ"] ?? 0}h</td>
                    </tr>
                `;
            }).join('');
        }

        function renderPagination(totalPages) {
            const container = document.getElementById('paginationControls');
            if (!container || totalPages <= 1) { container.innerHTML = ''; return; }
            let html = `<button onclick="goToPage(${currentPage - 1})" ${currentPage === 1 ? 'disabled' : ''} class="px-2 py-1 rounded border"><i class="fa-solid fa-chevron-left"></i></button>`;
            for (let p = 1; p <= totalPages; p++) {
                html += `<button onclick="goToPage(${p})" class="px-2.5 py-1 rounded border ${p === currentPage ? 'bg-paleOlive-600 text-white font-bold' : ''}">${p}</button>`;
            }
            html += `<button onclick="goToPage(${currentPage + 1})" ${currentPage === totalPages ? 'disabled' : ''} class="px-2 py-1 rounded border"><i class="fa-solid fa-chevron-right"></i></button>`;
            container.innerHTML = html;
        }

        function renderCharts(data) {
            const isDark = document.documentElement.classList.contains('dark');
            const textColor = isDark ? '#94a3b8' : '#475569';
            const gridColor = isDark ? 'rgba(148, 163, 184, 0.1)' : 'rgba(203, 213, 225, 0.4)';

            const hasRepeat = data.filter(d => (d["CL Lặp"] || 0) > 0).length;
            const noRepeat = data.filter(d => (d["CL Lặp"] || 0) === 0).length;

            if (chartRepeatPriority) chartRepeatPriority.destroy();
            const ctx1 = document.getElementById('chartRepeatPriority')?.getContext('2d');
            if (ctx1) {
                chartRepeatPriority = new Chart(ctx1, {
                    type: 'doughnut',
                    data: { labels: ['Có CL Lặp (>0)', 'Không Lặp (=0)'], datasets: [{ data: [hasRepeat, noRepeat], backgroundColor: ['#f59e0b', '#3b82f6'] }] },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { position: 'bottom', labels: { color: textColor } } } }
                });
            }

            const blockMap = {};
            data.forEach(d => { if (d["Block"]) blockMap[d["Block"]] = (blockMap[d["Block"]] || 0) + 1; });
            const sortedBlocks = Object.entries(blockMap).sort((a, b) => b[1] - a[1]).slice(0, 8);
            if (chartTopBlock) chartTopBlock.destroy();
            const ctx2 = document.getElementById('chartTopBlock')?.getContext('2d');
            if (ctx2) {
                chartTopBlock = new Chart(ctx2, {
                    type: 'bar',
                    data: { labels: sortedBlocks.map(b => b[0]), datasets: [{ data: sortedBlocks.map(b => b[1]), backgroundColor: '#0284c7', borderRadius: 6 }] },
                    options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: textColor }, grid: { color: gridColor } }, y: { ticks: { color: textColor }, grid: { display: false } } } }
                });
            }

            const popMap = {};
            data.forEach(d => { if (d["POP"]) popMap[d["POP"]] = (popMap[d["POP"]] || 0) + 1; });
            const sortedPops = Object.entries(popMap).sort((a, b) => b[1] - a[1]).slice(0, 8);
            if (chartTopPop) chartTopPop.destroy();
            const ctx3 = document.getElementById('chartTopPop')?.getContext('2d');
            if (ctx3) {
                chartTopPop = new Chart(ctx3, {
                    type: 'bar',
                    data: { labels: sortedPops.map(p => p[0]), datasets: [{ data: sortedPops.map(p => p[1]), backgroundColor: '#10b981', borderRadius: 6 }] },
                    options: { responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: textColor }, grid: { display: false } }, y: { ticks: { color: textColor }, grid: { color: gridColor } } } }
                });
            }

            const techMap = {};
            data.forEach(d => { if (d["Nhân sự"]) techMap[d["Nhân sự"]] = (techMap[d["Nhân sự"]] || 0) + 1; });
            const sortedTechs = Object.entries(techMap).sort((a, b) => b[1] - a[1]).slice(0, 8);
            if (chartTopTech) chartTopTech.destroy();
            const ctx4 = document.getElementById('chartTopTech')?.getContext('2d');
            if (ctx4) {
                chartTopTech = new Chart(ctx4, {
                    type: 'bar',
                    data: { labels: sortedTechs.map(t => t[0]), datasets: [{ data: sortedTechs.map(t => t[1]), backgroundColor: '#8b5cf6', borderRadius: 6 }] },
                    options: { indexAxis: 'y', responsive: true, maintainAspectRatio: false, plugins: { legend: { display: false } }, scales: { x: { ticks: { color: textColor }, grid: { color: gridColor } }, y: { ticks: { color: textColor }, grid: { display: false } } } }
                });
            }
        }

        async function fetchGoogleSheetData(showNotification = true) {
            const csvUrl = `https://docs.google.com/spreadsheets/d/${GOOGLE_SHEET_ID}/gviz/tq?tqx=out:csv&_nc=${Date.now()}`;
            const syncIcon = document.getElementById('syncIcon');
            if (syncIcon) syncIcon.classList.add('fa-spin');
            try {
                if (showNotification) showToast('Đang đồng bộ Google Sheets...', 'info');
                const response = await fetch(csvUrl);
                if (!response.ok) throw new Error('Không thể kết nối Google Sheets.');
                
                const csvText = await response.text();
                const workbook = XLSX.read(csvText, { type: 'string' });
                const firstSheetName = workbook.SheetNames[0];
                const worksheet = workbook.Sheets[firstSheetName];
                const rowsMatrix = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: '' });

                if (processRowsMatrix(rowsMatrix)) {
                    if (showNotification) showToast(`Đồng bộ thành công ${currentDataset.length} ca tồn!`, 'success');
                }
            } catch (err) {
                if (showNotification) showToast('Lỗi đồng bộ: ' + err.message, 'error');
            } finally {
                if (syncIcon) syncIcon.classList.remove('fa-spin');
            }
        }

        function processRowsMatrix(rowsMatrix) {
            if (!rowsMatrix || rowsMatrix.length <= 1) return false;
            let headerRowIdx = 0;
            for (let r = 0; r < Math.min(10, rowsMatrix.length); r++) {
                if (rowsMatrix[r].map(c => String(c).toUpperCase()).join(' ').includes('SỐ HĐ')) { headerRowIdx = r; break; }
            }
            const headers = rowsMatrix[headerRowIdx].map(h => String(h).trim());
            const getColIdx = (names, fb) => {
                const idx = headers.findIndex(h => names.some(n => h.toLowerCase().includes(n.toLowerCase())));
                return idx !== -1 ? idx : fb;
            };

            const parsedRecords = [];
            for (let r = headerRowIdx + 1; r < rowsMatrix.length; r++) {
                const row = rowsMatrix[r];
                if (!row || row.length === 0) continue;
                const soHD = String(row[getColIdx(['Số HĐ'], 5)] || '').trim();
                const block = String(row[getColIdx(['Block'], 4)] || '').trim();
                if (!soHD && !block) continue;

                const nhanSuKey = String(row[getColIdx(['Nhân sự'], 18)] || '').trim();
                parsedRecords.push({
                    "STT": parsedRecords.length + 1,
                    "Block": block,
                    "Số HĐ": soHD,
                    "Tên đầy đủ": String(row[getColIdx(['Tên đầy đủ'], 6)] || '').trim(),
                    "Tồn giờ": calculateTonGioFromColumnI(row[8]),
                    "Số lần hẹn": parseInt(row[getColIdx(['Số lần hẹn'], 14)], 10) || 0,
                    "CL Lặp": parseInt(row[getColIdx(['CL Lặp'], 15)], 10) || 0,
                    "Nhân sự": nhanSuKey,
                    "KH Giục Tiến Độ": String(row[getColIdx(['KH Giục Tiến Độ'], 21)] || '').trim(),
                    "TTCL": String(row[getColIdx(['TTCL'], 19)] || 'Đang XL').trim(),
                    "POP": String(row[20] || '').trim().substring(0, 7),
                    "Cột AN": managerMapping[nhanSuKey] || String(row[getColIdx(['cột an'], 39)] || '').trim()
                });
            }

            if (parsedRecords.length > 0) {
                currentDataset = parsedRecords;
                populateFilterOptions();
                applyFilters();
                return true;
            }
            return false;
        }

        function handleFileUpload(event) {
            const file = event.target.files[0];
            if (!file) return;
            const reader = new FileReader();
            reader.onload = function(e) {
                const workbook = XLSX.read(new Uint8Array(e.target.result), { type: 'array' });
                if (processRowsMatrix(XLSX.utils.sheet_to_json(workbook.Sheets[workbook.SheetNames[0]], { header: 1, defval: '' }))) {
                    showToast(`Nạp thành công từ File Excel!`, 'success');
                }
            };
            reader.readAsArrayBuffer(file);
            event.target.value = '';
        }

        function exportDataCSV() {
            const dataToExport = getFilteredData();
            if (!dataToExport.length) { showToast('Không có dữ liệu xuất!', 'error'); return; }
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, XLSX.utils.json_to_sheet(dataToExport), "Kiểm Soát Ca Tồn");
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

# Render Dashboard
components.html(html_content, height=1400, scrolling=True)
