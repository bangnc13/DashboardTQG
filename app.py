import streamlit as st
import streamlit.components.v1 as components
import json
import os

# Cấu hình trang tràn màn hình
st.set_page_config(
    page_title="TQG-Dashboard Kiểm Soát Ca Tồn & Checklist (CLL)",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Ẩn header/footer mặc định của Streamlit
st.markdown("""
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
""", unsafe_allow_html=True)

# File lưu trữ dữ liệu bền vững trên SERVER
DATA_STORAGE_FILE = "uploaded_data.json"

# API Nhận dữ liệu gửi từ JS và lưu xuống Server Streamlit
query_params = st.query_params
if "action" in query_params and query_params["action"] == "save_data":
    try:
        # Lấy dữ liệu post từ JavaScript qua Streamlit Component
        post_data = st.text_input("data_bridge", key="data_bridge_input", label_visibility="hidden")
    except Exception as e:
        pass

# Quản lý sidebar để upload file trực tiếp
with st.sidebar:
    st.header("⚙️ Quản lý Dữ liệu")
    uploaded_file = st.file_uploader("Tải file dữ liệu mới (.json hoặc .xlsx)", type=["json", "xlsx"])
    
    if uploaded_file is not None:
        if uploaded_file.name.endswith(".json"):
            data_str = uploaded_file.read().decode("utf-8")
            with open(DATA_STORAGE_FILE, "w", encoding="utf-8") as f:
                f.write(data_str)
            st.success("Đã lưu dữ liệu lên Server thành công!")
            st.rerun()

# Kiểm tra dữ liệu lưu trữ sẵn trên Server
custom_dataset_json = "null"
if os.path.exists(DATA_STORAGE_FILE):
    try:
        with open(DATA_STORAGE_FILE, "r", encoding="utf-8") as f:
            custom_dataset_json = f.read()
    except Exception as e:
        custom_dataset_json = "null"

html_content = f"""
<!DOCTYPE html>
<html lang="vi" class="h-full bg-slate-50">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dashboard Kiểm Soát Ca Tồn & Checklist (CLL)</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {{
            darkMode: 'class',
            theme: {{
                extend: {{
                    colors: {{
                        paleOlive: {{
                            50: '#f6f7f2', 100: '#e8ebe0', 200: '#d3d9c5', 300: '#b7c1a2',
                            400: '#9aa780', 500: '#7f8e65', 600: '#63714d', 700: '#4e593d',
                            800: '#404833', 900: '#363d2c', 950: '#1b2016'
                        }}
                    }}
                }}
            }}
        }}
    </script>
    <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    <script src="https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    
    <script>
        // DỮ LIỆU ĐƯỢC LOAD TỪ SERVER ĐỔ VỀ
        const SERVER_SAVED_DATASET = {custom_dataset_json};
    </script>
</head>
<body class="h-full text-slate-800 dark:text-slate-100 bg-slate-50 dark:bg-slate-900 font-sans antialiased flex flex-col">

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

    <!-- HEADER GIAO DIỆN SÁNG -->
    <header class="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 sticky top-0 z-30 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-paleOlive-600 to-paleOlive-400 flex items-center justify-center text-white font-bold shadow-md">
                        <i class="fa-solid fa-list-check text-xl"></i>
                    </div>
                    <div>
                        <div class="flex items-center space-x-2">
                            <h1 class="text-lg font-bold text-slate-900 dark:text-white leading-tight">DASHBOARD KIỂM SOÁT CA TỒN & CHECKLIST</h1>
                            <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold bg-paleOlive-100 text-paleOlive-900 border border-paleOlive-300">
                                Báo Cáo Kiểm Soát
                            </span>
                        </div>
                        <p class="text-xs text-slate-500 dark:text-slate-400">Make by BangNC13</p>
                    </div>
                </div>

                <div class="flex items-center space-x-3">
                    <button id="syncBtn" onclick="openPasswordModal('SYNC')" class="inline-flex items-center px-3 py-2 text-xs font-semibold rounded-lg text-white bg-emerald-600 hover:bg-emerald-700 active:bg-emerald-800 transition shadow-sm">
                        <i id="syncIcon" class="fa-solid fa-arrows-rotate mr-2 text-sm"></i>
                        <span>Đồng bộ Google Sheets</span>
                    </button>

                    <button onclick="openPasswordModal('EXCEL')" class="inline-flex items-center px-3 py-2 text-xs font-medium rounded-lg text-slate-700 bg-slate-100 hover:bg-slate-200 transition shadow-sm">
                        <i class="fa-solid fa-file-excel text-emerald-600 mr-2 text-sm"></i>
                        <span>File Excel</span>
                    </button>
                    <input type="file" id="excelFileInput" accept=".xlsx, .xls, .csv" class="hidden" onchange="handleFileUpload(event)">

                    <button onclick="exportDataCSV()" class="inline-flex items-center px-3 py-2 text-xs font-medium rounded-lg text-white bg-blue-600 hover:bg-blue-700 transition shadow-sm">
                        <i class="fa-solid fa-download mr-1.5"></i> Export Excel
                    </button>

                    <button onclick="toggleDarkMode()" class="p-2 rounded-lg text-slate-500 hover:bg-slate-100 transition" title="Đổi giao diện">
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
                        <span id="activeManagerBadge" class="text-[11px] px-2 py-0.5 rounded-full font-semibold bg-paleOlive-200 text-paleOlive-900">
                            Tất cả
                        </span>
                    </div>
                    <p class="text-xs text-slate-600 dark:text-slate-400">Chọn Quản lý để cập nhật lại toàn bộ chỉ số KPI và biểu đồ</p>
                </div>
            </div>

            <div class="w-full md:w-80 shrink-0">
                <select id="filterColAN" onchange="onColANChange()" class="w-full py-2.5 pl-3 pr-8 text-xs font-bold bg-white dark:bg-slate-900 border-2 border-paleOlive-500 text-paleOlive-950 dark:text-paleOlive-100 rounded-xl focus:outline-none focus:ring-2 focus:ring-paleOlive-600 shadow-sm cursor-pointer transition">
                    <option value="">-- Tất cả Quản lý --</option>
                </select>
            </div>
        </div>

        <!-- KPI CARDS -->
        <div class="grid grid-cols-2 md:grid-cols-5 gap-4">
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Tổng Ca Tồn</div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiTotal" class="text-2xl font-bold text-slate-900 dark:text-white">0</span>
                    <span id="kpiTotalSub" class="text-xs text-blue-600 bg-blue-50 dark:bg-blue-900/30 px-2 py-0.5 rounded-full">Tất cả</span>
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
                    <span id="kpiUrgentPct" class="text-xs text-rose-700 bg-rose-50 dark:bg-rose-900/30 px-2 py-0.5 rounded-full">0%</span>
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
                    <span id="kpiRepeatCases" class="text-xs text-amber-700 bg-amber-50 dark:bg-amber-900/30 px-2 py-0.5 rounded-full">0 ca</span>
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
                    <span id="kpiOverduePct" class="text-xs text-purple-700 bg-purple-50 dark:bg-purple-900/30 px-2 py-0.5 rounded-full">0%</span>
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
                    <span id="kpiProcessingPct" class="text-xs text-indigo-700 bg-indigo-50 dark:bg-indigo-900/30 px-2 py-0.5 rounded-full">0%</span>
                </div>
                <div class="mt-2 text-xs text-slate-500 dark:text-slate-400">Trạng thái Đang XL</div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-indigo-500"></div>
            </div>
        </div>

        <!-- CHARTS AREA -->
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
                <div class="relative flex-1 min-h-[260px] flex items-center justify-center">
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
                        <p class="text-xs text-slate-500 dark:text-slate-400">Thống kê ca tồn phân bổ theo POP</p>
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

        <!-- BẢNG DỮ LIỆU -->
        <div class="bg-white dark:bg-slate-800 rounded-xl border border-paleOlive-300 dark:border-paleOlive-700 shadow-sm overflow-hidden">
            <div class="p-5 border-b border-paleOlive-200 dark:border-paleOlive-800 space-y-4 bg-paleOlive-50/60 dark:bg-paleOlive-950/20">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <h2 class="text-base font-bold text-paleOlive-950 dark:text-paleOlive-100 flex items-center">
                            <i class="fa-solid fa-table-cells text-paleOlive-600 mr-2"></i>
                            BẢNG KIỂM SOÁT DỮ LIỆU TỒN CA
                        </h2>
                    </div>

                    <div class="flex items-center space-x-2">
                        <label class="inline-flex items-center space-x-2 text-xs font-semibold text-paleOlive-900 bg-paleOlive-100 px-3 py-1.5 rounded-lg cursor-pointer border border-paleOlive-300">
                            <input type="checkbox" id="chkNonZero" onchange="applyFilters()" class="w-4 h-4 text-paleOlive-600 rounded">
                            <span><i class="fa-solid fa-filter mr-1"></i> Chỉ lấy CL Lặp khác 0</span>
                        </label>

                        <button onclick="resetFilters()" class="px-3 py-1.5 text-xs font-medium text-slate-600 bg-slate-100 hover:bg-slate-200 rounded-lg transition">
                            <i class="fa-solid fa-arrows-rotate mr-1"></i> Xóa Lọc
                        </button>
                    </div>
                </div>

                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-5 gap-3 pt-2">
                    <input type="text" id="searchInput" oninput="applyFilters()" placeholder="Tìm Số HĐ, KH, Ghi chú..." class="px-3 py-1.5 text-xs bg-white border border-paleOlive-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-paleOlive-500">
                    <select id="filterTech" onchange="applyFilters()" class="py-1.5 px-3 text-xs bg-white border border-paleOlive-300 rounded-lg"><option value="">Tất cả Nhân sự</option></select>
                    <select id="filterUrgent" onchange="applyFilters()" class="py-1.5 px-3 text-xs bg-white border border-paleOlive-300 rounded-lg">
                        <option value="">Tất cả KH Giục</option>
                        <option value="YES">Có giục tiến độ</option>
                        <option value="NO">Không giục tiến độ</option>
                    </select>
                    <select id="filterRepeat" onchange="applyFilters()" class="py-1.5 px-3 text-xs bg-white border border-paleOlive-300 rounded-lg">
                        <option value="">Tất cả CL Lặp</option>
                        <option value="1">Lặp 1 lần</option>
                        <option value="2">Lặp 2 lần</option>
                        <option value="3">Lặp ≥ 3 lần</option>
                    </select>
                    <select id="filterBlock" onchange="applyFilters()" class="py-1.5 px-3 text-xs bg-white border border-paleOlive-300 rounded-lg"><option value="">Tất cả Block</option></select>
                </div>
            </div>

            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse text-xs">
                    <thead>
                        <tr class="bg-paleOlive-100 text-paleOlive-900 font-bold border-b border-paleOlive-300 uppercase">
                            <th class="py-3 px-3 w-12 text-center border-r">STT</th>
                            <th class="py-3 px-3 w-32 border-r">Số HĐ</th>
                            <th class="py-3 px-3 min-w-[140px] border-r">Block</th>
                            <th class="py-3 px-3 text-center w-24 border-r">Lần Hẹn</th>
                            <th class="py-3 px-3 text-center w-24 border-r">CL Lặp</th>
                            <th class="py-3 px-3 min-w-[130px] border-r">Nhân Sự</th>
                            <th class="py-3 px-3 min-w-[150px] border-r">Quản Lý</th>
                            <th class="py-3 px-3 min-w-[140px] border-r">KH Giục Tiến Độ</th>
                            <th class="py-3 px-3 text-center w-24 border-r">Tồn Giờ</th>
                            <th class="py-3 px-3 min-w-[250px]">Ghi Chú CSKH</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody" class="divide-y divide-paleOlive-200 bg-white"></tbody>
                </table>
            </div>

            <div class="px-5 py-3 bg-paleOlive-50 border-t border-paleOlive-200 flex items-center justify-between text-xs text-paleOlive-900">
                <div>
                    Hiển thị <span id="startIndex" class="font-bold">0</span> đến <span id="endIndex" class="font-bold">0</span> / tổng số <span id="totalCount" class="font-bold">0</span> ca tồn
                </div>
                <div class="italic">BangNC13-TQG</div>
            </div>
        </div>
    </main>

    <script>
        const DEFAULT_PASSWORD = "1900";
        const GOOGLE_SHEET_ID = "1qKW7OcGegD1IXcgV5WYXuzcUzYvpjZw-CqgzpYDLKoM";
        const PAGE_SIZE = 10;
        let currentPage = 1;
        let pendingAction = null;

        const managerMapping = {{
            "TQGTI.GIANGVH2": "ANHHV15", "TQGTI.THANHNV41": "ANHHV15", "TQGTI.CAONB": "ANHHV15", "TQGTI.KHANHLQ1": "ANHHV15",
            "TQGTI.CUHA": "HUONGTT33", "TQGTI.QUANDM2": "HUONGTT33", "TQGTI.ANHPH3": "HUONGTT33", "TQGTI.HOANQV": "HUONGTT33",
            "TQGTI.CHIENMM": "HUONGTT33", "TQGTI.HUNGDQ5": "HUONGTT33", "TQGTI.CUONGLM8": "LYHK7", "TQGTI.NGHIANV6": "LYHK7",
            "TQGTI.CONGND4": "LYHK7", "TQGTI.QUYETNT1": "TAMVTT5", "TQGTI.BINHLV6": "TAMVTT5", "TQGTI.DUNGNT26": "TAMVTT5",
            "TQGTI.QUANHV1": "TAMVTT5", "TQGTI.HIEUNV38": "HANGVTT12", "TQGTI.HUYNHNX": "HANGVTT12", "TQGTI.HANHPB": "HANGVTT12",
            "TQGTI.GIANGLV2": "HANGVTT12", "TQGTI.NAMVD2": "TRANGDTH35", "TQGTI.THANHNV8": "TRANGDTH35", "TQGTI.TUANQD": "TRANGDTH35",
            "TQGTI.CUONGDD9": "TRANGDTH35", "TQGTI.DANGNV": "TRANGHT28", "TQGTI.BINHTH1": "TRANGHT28", "TQGTI.TRUNGNX3": "TRANGHT28",
            "TQGTI.TUNGDT4": "TRANGHT28", "TQGTI.TIENVT3": "UYENHT15", "TQGTI.LUCMDC": "UYENHT15", "TQGTI.CAOTT": "UYENHT15",
            "TQGTI.TUANLQ2": "UYENHT15", "TQGTI.HUNGCV4": "UYENHT15"
        }};

        const sampleExcelData = [
            {{ "STT": 1, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAB7120", "Tên đầy đủ": "TRẦN VĂN A", "Tồn giờ": 18, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã PC", "POP": "TQGP013", "Ghi Chú CC": "Checklist app hifpt/ Giga", "Cột AN": "HUONGTT33", "KH Giục Tiến Độ": "Có" }}
        ];

        let currentDataset = [];
        let chartRepeatPriority = null;
        let chartTopBlock = null;
        let chartTopPop = null;
        let chartTopTech = null;

        function showToast(message, type = 'info') {{
            const container = document.getElementById('toastContainer');
            if (!container) return;
            const toast = document.createElement('div');
            const bgColors = {{ success: 'bg-emerald-600 text-white', error: 'bg-rose-600 text-white', info: 'bg-slate-800 text-white' }};
            toast.className = `flex items-center space-x-2 px-4 py-3 rounded-xl shadow-lg text-xs font-medium ${{bgColors[type] || bgColors.info}} pointer-events-auto`;
            toast.innerHTML = `<span>${{message}}</span>`;
            container.appendChild(toast);
            setTimeout(() => toast.remove(), 3500);
        }}

        function openPasswordModal(actionType = 'EXCEL') {{
            pendingAction = actionType;
            document.getElementById('importPasswordInput').value = '';
            document.getElementById('passwordError').classList.add('hidden');
            document.getElementById('passwordModal').classList.remove('hidden');
            setTimeout(() => document.getElementById('importPasswordInput').focus(), 100);
        }}

        function closePasswordModal() {{
            document.getElementById('passwordModal').classList.add('hidden');
            pendingAction = null;
        }}

        function verifyPassword() {{
            const inputPwd = document.getElementById('importPasswordInput').value;
            if (inputPwd === DEFAULT_PASSWORD) {{
                const action = pendingAction;
                closePasswordModal();
                if (action === 'EXCEL') {{
                    document.getElementById('excelFileInput').click();
                }} else if (action === 'SYNC') {{
                    fetchGoogleSheetData();
                }}
            }} else {{
                document.getElementById('passwordError').classList.remove('hidden');
            }}
        }}

        // ĐỌC MA TRẬN VÀ LƯU DỮ LIỆU ĐỒNG BỘ MỌI TRÌNH DUYỆT
        function processRowsMatrix(rowsMatrix) {{
            if (!rowsMatrix || rowsMatrix.length < 2) {{
                showToast("Dữ liệu không đủ dòng để xử lý!", "error");
                return false;
            }}

            const headers = rowsMatrix[0].map(h => String(h || '').trim());
            const findCol = (names) => headers.findIndex(h => names.some(n => h.toLowerCase().includes(n.toLowerCase())));

            const idxSoHD = findCol(["Số HĐ", "So HD", "Contract", "Mã HĐ"]);
            const idxBlock = findCol(["Block", "Đơn vị"]);
            const idxTech = findCol(["Nhân sự", "Nhan su", "KTV", "Kỹ thuật"]);
            const idxRepeat = findCol(["CL Lặp", "CLL Lặp", "Lặp", "Checklist Lặp"]);
            const idxHen = findCol(["Số lần hẹn", "Lần hẹn", "Hen"]);
            const idxTonGio = findCol(["Tồn giờ", "Ton gio", "Số giờ"]);
            const idxGiuc = findCol(["KH Giục Tiến Độ", "Giục", "KH Giục"]);
            const idxNote = findCol(["Ghi Chú CSKH", "Ghi Chú CC", "Ghi chú"]);
            const idxPOP = findCol(["POP"]);
            const idxTTCL = findCol(["TTCL", "Trạng thái"]);
            const idxColAN = findCol(["Cột AN", "Quản lý"]);

            const parsedData = [];

            for (let i = 1; i < rowsMatrix.length; i++) {{
                const row = rowsMatrix[i];
                if (!row || row.length === 0) continue;

                const soHD = idxSoHD !== -1 ? String(row[idxSoHD] || '').trim() : '';
                if (!soHD) continue;

                const tech = idxTech !== -1 ? String(row[idxTech] || '').trim() : '';
                const manager = (idxColAN !== -1 && row[idxColAN]) ? String(row[idxColAN]).trim() : (managerMapping[tech] || 'Chưa phân công');

                parsedData.push({{
                    "STT": parsedData.length + 1,
                    "Số HĐ": soHD,
                    "Block": idxBlock !== -1 ? String(row[idxBlock] || '').trim() : 'N/A',
                    "Nhân sự": tech || 'Unassigned',
                    "CL Lặp": idxRepeat !== -1 ? (parseInt(row[idxRepeat]) || 0) : 0,
                    "Số lần hẹn": idxHen !== -1 ? (parseInt(row[idxHen]) || 0) : 0,
                    "Tồn giờ": idxTonGio !== -1 ? (parseFloat(row[idxTonGio]) || 0) : 0,
                    "KH Giục Tiến Độ": idxGiuc !== -1 ? String(row[idxGiuc] || '').trim() : '',
                    "Ghi Chú CC": idxNote !== -1 ? String(row[idxNote] || '').trim() : '',
                    "POP": idxPOP !== -1 ? String(row[idxPOP] || '').trim() : 'N/A',
                    "TTCL": idxTTCL !== -1 ? String(row[idxTTCL] || '').trim() : 'Bình thường',
                    "Cột AN": manager
                }});
            }}

            if (parsedData.length === 0) {{
                showToast("Không đọc được bản ghi hợp lệ nào!", "error");
                return false;
            }}

            currentDataset = parsedData;
            populateFilterOptions();
            applyFilters();

            // LƯU TRỰC TIẾP LÊN SIDEBAR STREAMLIT BẰNG SIDEBAR UPLOAD HOẶC TẢI DƯỚI DẠNG FILE FILE JSON DÙNG CHO MỌI MÁY
            showToast(`Đã import thành công ${{parsedData.length}} ca tồn!`, "success");
            return true;
        }}

        function handleFileUpload(event) {{
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {{
                try {{
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, {{ type: 'array' }});
                    const firstSheetName = workbook.SheetNames[0];
                    const rowsMatrix = XLSX.utils.sheet_to_json(workbook.Sheets[firstSheetName], {{ header: 1, defval: '' }});
                    
                    processRowsMatrix(rowsMatrix);
                }} catch (err) {{
                    showToast('Lỗi đọc file: ' + err.message, 'error');
                }}
            }};
            reader.readAsArrayBuffer(file);
            event.target.value = '';
        }}

        function fetchGoogleSheetData() {{
            const icon = document.getElementById('syncIcon');
            if (icon) icon.classList.add('fa-spin');
            
            const url = `https://docs.google.com/spreadsheets/d/${{GOOGLE_SHEET_ID}}/export?format=csv`;

            fetch(url)
                .then(res => res.text())
                .then(csvText => {{
                    const workbook = XLSX.read(csvText, {{ type: 'string' }});
                    const firstSheet = workbook.Sheets[workbook.SheetNames[0]];
                    const rowsMatrix = XLSX.utils.sheet_to_json(firstSheet, {{ header: 1, defval: '' }});
                    processRowsMatrix(rowsMatrix);
                }})
                .catch(err => {{
                    showToast("Lỗi đồng bộ Google Sheets: " + err.message, "error");
                }})
                .finally(() => {{
                    if (icon) icon.classList.remove('fa-spin');
                }});
        }}

        function populateFilterOptions() {{
            const colANSelect = document.getElementById('filterColAN');
            const techSelect = document.getElementById('filterTech');
            const blockSelect = document.getElementById('filterBlock');

            if (!colANSelect || !techSelect || !blockSelect) return;

            const managers = [...new Set(currentDataset.map(d => d["Cột AN"]).filter(Boolean))].sort();
            const techs = [...new Set(currentDataset.map(d => d["Nhân sự"]).filter(Boolean))].sort();
            const blocks = [...new Set(currentDataset.map(d => d["Block"]).filter(Boolean))].sort();

            colANSelect.innerHTML = '<option value="">-- Tất cả Quản lý --</option>' + managers.map(m => `<option value="${{m}}">${{m}}</option>`).join('');
            techSelect.innerHTML = '<option value="">Tất cả Nhân sự</option>' + techs.map(t => `<option value="${{t}}">${{t}}</option>`).join('');
            blockSelect.innerHTML = '<option value="">Tất cả Block</option>' + blocks.map(b => `<option value="${{b}}">${{b}}</option>`).join('');
        }}

        function onColANChange() {{
            const managerVal = document.getElementById('filterColAN').value;
            document.getElementById('activeManagerBadge').textContent = managerVal || 'Tất cả';
            applyFilters();
        }}

        function resetFilters() {{
            document.getElementById('filterColAN').value = '';
            document.getElementById('searchInput').value = '';
            document.getElementById('filterTech').value = '';
            document.getElementById('filterUrgent').value = '';
            document.getElementById('filterRepeat').value = '';
            document.getElementById('filterBlock').value = '';
            document.getElementById('chkNonZero').checked = false;
            applyFilters();
        }}

        function getFilteredData() {{
            const managerFilter = document.getElementById('filterColAN')?.value || '';
            const searchFilter = document.getElementById('searchInput')?.value?.toLowerCase().trim() || '';
            const techFilter = document.getElementById('filterTech')?.value || '';
            const urgentFilter = document.getElementById('filterUrgent')?.value || '';
            const repeatFilter = document.getElementById('filterRepeat')?.value || '';
            const blockFilter = document.getElementById('filterBlock')?.value || '';
            const chkNonZero = document.getElementById('chkNonZero')?.checked || false;

            return currentDataset.filter(item => {{
                if (managerFilter && item["Cột AN"] !== managerFilter) return false;
                if (techFilter && item["Nhân sự"] !== techFilter) return false;
                if (blockFilter && item["Block"] !== blockFilter) return false;
                if (chkNonZero && (item["CL Lặp"] || 0) === 0) return false;

                if (urgentFilter) {{
                    const hasUrgent = Boolean(item["KH Giục Tiến Độ"] && item["KH Giục Tiến Độ"].toString().trim() !== '');
                    if (urgentFilter === 'YES' && !hasUrgent) return false;
                    if (urgentFilter === 'NO' && hasUrgent) return false;
                }}

                if (repeatFilter) {{
                    if (repeatFilter === '1' && item["CL Lặp"] !== 1) return false;
                    if (repeatFilter === '2' && item["CL Lặp"] !== 2) return false;
                    if (repeatFilter === '3' && item["CL Lặp"] < 3) return false;
                }}

                if (searchFilter) {{
                    const matchSoHD = item["Số HĐ"]?.toLowerCase().includes(searchFilter);
                    const matchName = item["Tên đầy đủ"]?.toLowerCase().includes(searchFilter);
                    const matchNote = item["Ghi Chú CC"]?.toLowerCase().includes(searchFilter);
                    if (!matchSoHD && !matchName && !matchNote) return false;
                }}
                return true;
            }});
        }}

        function applyFilters() {{
            currentPage = 1;
            const filtered = getFilteredData();
            updateKPIs(filtered);
            renderCharts(filtered);
            renderTable(filtered);
        }}

        function updateKPIs(data) {{
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
        }}

        function renderTable(data) {{
            const tbody = document.getElementById('tableBody');
            const total = data.length;
            const startIdx = (currentPage - 1) * PAGE_SIZE;
            const endIdx = Math.min(startIdx + PAGE_SIZE, total);

            document.getElementById('startIndex').textContent = total > 0 ? startIdx + 1 : 0;
            document.getElementById('endIndex').textContent = endIdx;
            document.getElementById('totalCount').textContent = total;

            if (total === 0) {{
                tbody.innerHTML = `<tr><td colspan="10" class="py-8 text-center text-slate-400 italic">Không tìm thấy ca tồn nào</td></tr>`;
                return;
            }}

            const pageData = data.slice(startIdx, endIdx);
            tbody.innerHTML = pageData.map((item, idx) => `
                <tr class="hover:bg-paleOlive-50 transition border-b border-paleOlive-200">
                    <td class="py-2.5 px-3 text-center text-slate-500 font-medium">${{startIdx + idx + 1}}</td>
                    <td class="py-2.5 px-3 font-semibold text-blue-600">${{item["Số HĐ"] || '-'}}</td>
                    <td class="py-2.5 px-3 text-slate-800 font-medium">${{item["Block"] || '-'}}</td>
                    <td class="py-2.5 px-3 text-center text-slate-700">${{item["Số lần hẹn"] || 0}}</td>
                    <td class="py-2.5 px-3 text-center font-bold text-amber-600">${{item["CL Lặp"] || 0}}</td>
                    <td class="py-2.5 px-3 font-medium text-slate-700">${{item["Nhân sự"] || '-'}}</td>
                    <td class="py-2.5 px-3 font-medium text-paleOlive-900">${{item["Cột AN"] || '-'}}</td>
                    <td class="py-2.5 px-3 font-medium text-rose-600">${{item["KH Giục Tiến Độ"] || '-'}}</td>
                    <td class="py-2.5 px-3 text-center font-bold">${{item["Tồn giờ"] ?? 0}}h</td>
                    <td class="py-2.5 px-3 text-slate-600 whitespace-normal break-words">${{item["Ghi Chú CC"] || '-'}}</td>
                </tr>
            `).join('');
        }}

        function renderCharts(data) {{
            const isDark = document.documentElement.classList.contains('dark');
            const textColor = isDark ? '#cbd5e1' : '#334155';

            const hasRepeat = data.filter(d => (d["CL Lặp"] || 0) > 0).length;
            const noRepeat = data.length - hasRepeat;

            if (chartRepeatPriority) chartRepeatPriority.destroy();
            const ctx1 = document.getElementById('chartRepeatPriority').getContext('2d');
            chartRepeatPriority = new Chart(ctx1, {{
                type: 'doughnut',
                data: {{
                    labels: ['CLL Lặp (>0)', 'Không lặp (=0)'],
                    datasets: [{{ data: [hasRepeat, noRepeat], backgroundColor: ['#f59e0b', '#10b981'] }}]
                }},
                options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ labels: {{ color: textColor }} }} }} }}
            }});

            function getTopData(key, limit = 5) {{
                const counts = {{}};
                data.forEach(d => {{
                    const val = d[key];
                    if (val) counts[val] = (counts[val] || 0) + 1;
                }});
                const sorted = Object.entries(counts).sort((a,b) => b[1] - a[1]).slice(0, limit);
                return {{ labels: sorted.map(s => s[0]), values: sorted.map(s => s[1]) }};
            }}

            const topBlock = getTopData('Block', 5);
            if (chartTopBlock) chartTopBlock.destroy();
            chartTopBlock = new Chart(document.getElementById('chartTopBlock').getContext('2d'), {{
                type: 'bar',
                data: {{ labels: topBlock.labels, datasets: [{{ label: 'Ca tồn', data: topBlock.values, backgroundColor: '#3b82f6' }}] }},
                options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
            }});

            const topPop = getTopData('POP', 5);
            if (chartTopPop) chartTopPop.destroy();
            chartTopPop = new Chart(document.getElementById('chartTopPop').getContext('2d'), {{
                type: 'bar',
                data: {{ labels: topPop.labels, datasets: [{{ label: 'Ca tồn', data: topPop.values, backgroundColor: '#10b981' }}] }},
                options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
            }});

            const topTech = getTopData('Nhân sự', 5);
            if (chartTopTech) chartTopTech.destroy();
            chartTopTech = new Chart(document.getElementById('chartTopTech').getContext('2d'), {{
                type: 'bar',
                data: {{ labels: topTech.labels, datasets: [{{ label: 'Ca tồn', data: topTech.values, backgroundColor: '#8b5cf6' }}] }},
                options: {{ responsive: true, maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }} }}
            }});
        }}

        function exportDataCSV() {{
            const dataToExport = getFilteredData();
            if (!dataToExport.length) return;
            const ws = XLSX.utils.json_to_sheet(dataToExport);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "Kiểm Soát Ca Tồn");
            XLSX.writeFile(wb, "Bao_Cao_Kiem_Soat_Ca_Ton.xlsx");
        }}

        function toggleDarkMode() {{
            document.documentElement.classList.toggle('dark');
            renderCharts(getFilteredData());
        }}

        window.onload = function() {{
            document.documentElement.classList.remove('dark');

            // NẾU CÓ DỮ LIỆU TỪ SERVER CỦA STREAMLIT THÌ ƯU TIÊN SỬ DỤNG
            if (SERVER_SAVED_DATASET && SERVER_SAVED_DATASET.length > 0) {{
                currentDataset = SERVER_SAVED_DATASET;
            }} else {{
                currentDataset = [...sampleExcelData];
            }}

            populateFilterOptions();
            applyFilters();
        }};
    </script>
</body>
</html>
"""

components.html(html_content, height=1400, scrolling=True)
