<!DOCTYPE html>
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
        
        .table-olive-theme {
            background-color: #f7f9f2;
        }
        .dark .table-olive-theme {
            background-color: rgba(117, 153, 72, 0.08);
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

    <header class="bg-white dark:bg-slate-800 border-b border-slate-200 dark:border-slate-700 sticky top-0 z-30 shadow-sm">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex items-center justify-between h-16">
                <!-- Title & Badge -->
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
                        <p class="text-xs text-slate-500 dark:text-slate-400">Khớp chính xác: Số HĐ, Khách Hàng, Block, Lần Hẹn, CL Lặp, Nhân Sự, Quản Lý, Tồn Giờ, Kiểm Soát</p>
                    </div>
                </div>

                <!-- Actions & Dark mode toggle -->
                <div class="flex items-center space-x-3">
                    <label class="cursor-pointer inline-flex items-center px-3 py-2 text-xs font-medium rounded-lg text-slate-700 bg-slate-100 hover:bg-slate-200 dark:text-slate-200 dark:bg-slate-700 dark:hover:bg-slate-600 transition shadow-sm">
                        <i class="fa-solid fa-file-excel text-emerald-600 dark:text-emerald-400 mr-2 text-sm"></i>
                        <span>Cập nhật File Excel</span>
                        <input type="file" id="excelFileInput" accept=".xlsx, .xls, .csv" class="hidden" onchange="handleFileUpload(event)">
                    </label>

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

        <!-- Banner Info for Olive Highlighted Columns -->
        <div class="bg-paleOlive-50 dark:bg-paleOlive-900/30 border-l-4 border-paleOlive-500 p-4 rounded-r-xl shadow-sm flex flex-col md:flex-row md:items-center justify-between gap-3">
            <div class="flex items-start space-x-3">
                <i class="fa-solid fa-circle-info text-paleOlive-700 dark:text-paleOlive-300 text-lg mt-0.5"></i>
                <div class="text-xs text-paleOlive-900 dark:text-paleOlive-200 space-y-1">
                    <p class="font-semibold text-sm">Các trường thông tin kiểm soát trọng yếu:</p>
                    <div class="flex flex-wrap gap-2 pt-1">
                        <span class="bg-paleOlive-200/80 dark:bg-paleOlive-800/60 px-2 py-0.5 rounded text-paleOlive-900 dark:text-paleOlive-100 font-medium">Số HĐ</span>
                        <span class="bg-paleOlive-200/80 dark:bg-paleOlive-800/60 px-2 py-0.5 rounded text-paleOlive-900 dark:text-paleOlive-100 font-medium">Khách Hàng</span>
                        <span class="bg-paleOlive-200/80 dark:bg-paleOlive-800/60 px-2 py-0.5 rounded text-paleOlive-900 dark:text-paleOlive-100 font-medium">Block</span>
                        <span class="bg-paleOlive-200/80 dark:bg-paleOlive-800/60 px-2 py-0.5 rounded text-paleOlive-900 dark:text-paleOlive-100 font-medium">Số Lần Hẹn</span>
                        <span class="bg-paleOlive-200/80 dark:bg-paleOlive-800/60 px-2 py-0.5 rounded text-paleOlive-900 dark:text-paleOlive-100 font-medium">CL Lặp</span>
                        <span class="bg-paleOlive-200/80 dark:bg-paleOlive-800/60 px-2 py-0.5 rounded text-paleOlive-900 dark:text-paleOlive-100 font-medium">Nhân Sự</span>
                        <span class="bg-paleOlive-200/80 dark:bg-paleOlive-800/60 px-2 py-0.5 rounded text-paleOlive-900 dark:text-paleOlive-100 font-medium">Quản Lý</span>
                        <span class="bg-paleOlive-200/80 dark:bg-paleOlive-800/60 px-2 py-0.5 rounded text-paleOlive-900 dark:text-paleOlive-100 font-medium">Tồn Giờ</span>
                        <span class="bg-paleOlive-200/80 dark:bg-paleOlive-800/60 px-2 py-0.5 rounded text-paleOlive-900 dark:text-paleOlive-100 font-medium">Kiểm Soát</span>
                    </div>
                </div>
            </div>
            <div class="text-right text-xs text-slate-500 dark:text-slate-400 whitespace-nowrap self-end md:self-center">
                Dữ liệu hiện tại: <span id="recordCountBadge" class="font-bold text-slate-800 dark:text-slate-200">0</span> ca tồn
            </div>
        </div>

        <div class="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
            <!-- KPI 1: Tổng Ca Tồn -->
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-slate-500 dark:text-slate-400 uppercase tracking-wider">Tổng Ca Tồn</div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiTotal" class="text-2xl font-bold text-slate-900 dark:text-white">0</span>
                    <span class="text-xs text-blue-600 bg-blue-50 dark:bg-blue-900/30 dark:text-blue-300 px-2 py-0.5 rounded-full">Tất cả</span>
                </div>
                <div class="mt-2 text-xs text-slate-500 dark:text-slate-400 truncate">Tổng hợp hợp đồng tồn</div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-blue-500"></div>
            </div>

            <!-- KPI 2: Mức SOS -->
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-rose-600 dark:text-rose-400 uppercase tracking-wider flex items-center justify-between">
                    <span>Mức SOS</span>
                    <i class="fa-solid fa-triangle-exclamation animate-pulse"></i>
                </div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiSos" class="text-2xl font-bold text-rose-600 dark:text-rose-400">0</span>
                    <span id="kpiSosPct" class="text-xs text-rose-700 bg-rose-50 dark:bg-rose-900/30 dark:text-rose-300 px-2 py-0.5 rounded-full">0%</span>
                </div>
                <div class="mt-2 text-xs text-slate-500 dark:text-slate-400">Số ca báo SOS</div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-rose-500"></div>
            </div>

            <!-- KPI 3: CLL Đang Tồn -->
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-amber-600 dark:text-amber-400 uppercase tracking-wider flex items-center justify-between">
                    <span>CLL Đang Tồn</span>
                    <i class="fa-solid fa-rotate-right"></i>
                </div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiRepeat" class="text-2xl font-bold text-amber-600 dark:text-amber-400">0</span>
                    <span id="kpiRepeatCases" class="text-xs text-amber-700 bg-amber-50 dark:bg-amber-900/30 dark:text-amber-300 px-2 py-0.5 rounded-full">0 ca</span>
                </div>
                <div class="mt-2 text-xs text-slate-500 dark:text-slate-400">Tổng lượt lặp (Lặp > 0)</div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-amber-500"></div>
            </div>

            <!-- KPI 4: Tồn Giờ > 24H -->
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

            <!-- KPI 5: Đang Xử Lý -->
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

            <!-- KPI 6: Cần Đánh Giá -->
            <div class="bg-white dark:bg-slate-800 p-4 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm relative overflow-hidden">
                <div class="text-xs font-medium text-emerald-600 dark:text-emerald-400 uppercase tracking-wider flex items-center justify-between">
                    <span>Cần Đánh Giá</span>
                    <i class="fa-solid fa-clipboard-check"></i>
                </div>
                <div class="mt-2 flex items-baseline justify-between">
                    <span id="kpiUnchecked" class="text-2xl font-bold text-emerald-600 dark:text-emerald-400">0</span>
                    <span class="text-xs text-emerald-700 bg-emerald-50 dark:bg-emerald-900/30 dark:text-emerald-300 px-2 py-0.5 rounded-full">Chưa ĐG</span>
                </div>
                <div class="mt-2 text-xs text-slate-500 dark:text-slate-400">Chưa ghi nhận đánh giá</div>
                <div class="absolute bottom-0 left-0 right-0 h-1 bg-emerald-500"></div>
            </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
            
            <!-- Chart 1: CL Lặp vs Độ Ưu Tiên -->
            <div class="bg-white dark:bg-slate-800 p-5 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm flex flex-col">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h2 class="text-sm font-bold text-slate-900 dark:text-white flex items-center">
                            <i class="fa-solid fa-chart-column text-amber-500 mr-2"></i>
                            1. Tỉ trọng Checklist Lặp Theo Mức Độ SOS
                        </h2>
                        <p class="text-xs text-slate-500 dark:text-slate-400">Thống kê ca SOS vs Support lặp lại nhiều lần</p>
                    </div>
                </div>
                <div class="relative flex-1 min-h-[260px]">
                    <canvas id="chartRepeatPriority"></canvas>
                </div>
            </div>

            <!-- Chart 2: Top Block -->
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

            <!-- Chart 3: Top POP Station -->
            <div class="bg-white dark:bg-slate-800 p-5 rounded-xl border border-slate-200 dark:border-slate-700 shadow-sm flex flex-col">
                <div class="flex items-center justify-between mb-4">
                    <div>
                        <h2 class="text-sm font-bold text-slate-900 dark:text-white flex items-center">
                            <i class="fa-solid fa-network-wired text-emerald-500 mr-2"></i>
                            3. Tồn theo POP
                        </h2>
                        <p class="text-xs text-slate-500 dark:text-slate-400">Cụm trạm kỹ thuật quản lý hạ tầng</p>
                    </div>
                </div>
                <div class="relative flex-1 min-h-[260px]">
                    <canvas id="chartTopPop"></canvas>
                </div>
            </div>

            <!-- Chart 4: Top 10 KTV / Nhân sự phụ trách -->
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
            
            <!-- Table Header Toolbar & Filters -->
            <div class="p-5 border-b border-paleOlive-200 dark:border-paleOlive-800 space-y-4 bg-paleOlive-50/60 dark:bg-paleOlive-950/20">
                <div class="flex flex-col md:flex-row md:items-center justify-between gap-4">
                    <div>
                        <h2 class="text-base font-bold text-paleOlive-950 dark:text-paleOlive-100 flex items-center">
                            <i class="fa-solid fa-table-cells text-paleOlive-600 mr-2"></i>
                            BẢNG KIỂM SOÁT DỮ LIỆU TỒN CA
                        </h2>
                        <p class="text-xs text-paleOlive-800/80 dark:text-paleOlive-300/80">Xem, tìm kiếm, lọc và cập nhật trực tiếp trạng thái Kiểm Soát</p>
                    </div>

                    <div class="flex items-center space-x-2">
                        <label class="inline-flex items-center space-x-2 text-xs font-semibold text-paleOlive-900 dark:text-paleOlive-200 bg-paleOlive-100 dark:bg-paleOlive-900/50 px-3 py-1.5 rounded-lg cursor-pointer border border-paleOlive-300 dark:border-paleOlive-700 hover:bg-paleOlive-200 dark:hover:bg-paleOlive-800/60 transition shadow-sm">
                            <input type="checkbox" id="chkNonZero" onchange="applyFilters()" class="w-4 h-4 text-paleOlive-600 rounded border-paleOlive-300 focus:ring-paleOlive-500 dark:bg-slate-800">
                            <span><i class="fa-solid fa-filter mr-1 text-paleOlive-700 dark:text-paleOlive-300"></i> Chỉ lấy CL Lặp khác 0</span>
                        </label>

                        <button onclick="resetFilters()" class="px-3 py-1.5 text-xs font-medium text-slate-600 bg-slate-100 hover:bg-slate-200 dark:text-slate-300 dark:bg-slate-700 dark:hover:bg-slate-600 rounded-lg transition">
                            <i class="fa-solid fa-arrows-rotate mr-1"></i> Xóa Lọc
                        </button>
                    </div>
                </div>

                <!-- Filters Grid -->
                <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-6 gap-3 pt-2">
                    <div class="relative sm:col-span-2 lg:col-span-1">
                        <i class="fa-solid fa-magnifying-glass absolute left-3 top-2.5 text-slate-400 text-xs"></i>
                        <input type="text" id="searchInput" oninput="applyFilters()" placeholder="Tìm Số HĐ, Tên KH, Ghi chú..." class="w-full pl-8 pr-3 py-1.5 text-xs bg-white dark:bg-slate-900 border border-paleOlive-300 dark:border-paleOlive-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-paleOlive-500 dark:text-white">
                    </div>

                    <!-- Filter Quản lý -->
                    <div>
                        <select id="filterColAN" onchange="onColANChange()" class="w-full py-1.5 px-3 text-xs font-semibold bg-paleOlive-100/90 dark:bg-paleOlive-950/40 border border-paleOlive-300 dark:border-paleOlive-700 text-paleOlive-900 dark:text-paleOlive-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-paleOlive-500">
                            <option value="">Tất cả Quản lý</option>
                        </select>
                    </div>

                    <div>
                        <select id="filterTech" onchange="applyFilters()" class="w-full py-1.5 px-3 text-xs bg-white dark:bg-slate-900 border border-paleOlive-300 dark:border-paleOlive-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-paleOlive-500 dark:text-white">
                            <option value="">Tất cả Nhân sự</option>
                        </select>
                    </div>

                    <div>
                        <select id="filterPriority" onchange="applyFilters()" class="w-full py-1.5 px-3 text-xs bg-white dark:bg-slate-900 border border-paleOlive-300 dark:border-paleOlive-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-paleOlive-500 dark:text-white">
                            <option value="">Tất cả Mức SOS</option>
                            <option value="SOS">Chỉ lấy: SOS</option>
                            <option value="Support">Chỉ lấy: Support</option>
                            <option value="EMPTY">Giá trị trống</option>
                        </select>
                    </div>

                    <div>
                        <select id="filterRepeat" onchange="applyFilters()" class="w-full py-1.5 px-3 text-xs bg-white dark:bg-slate-900 border border-paleOlive-300 dark:border-paleOlive-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-paleOlive-500 dark:text-white">
                            <option value="">Tất cả CL Lặp</option>
                            <option value="NON_ZERO">Chỉ khác 0 (Lặp > 0)</option>
                            <option value="0">Bằng 0 (= 0)</option>
                            <option value="1">Lặp 1 lần</option>
                            <option value="2">Lặp 2 lần</option>
                            <option value="3">Lặp ≥ 3 lần</option>
                        </select>
                    </div>

                    <div>
                        <select id="filterBlock" onchange="applyFilters()" class="w-full py-1.5 px-3 text-xs bg-white dark:bg-slate-900 border border-paleOlive-300 dark:border-paleOlive-700 rounded-lg focus:outline-none focus:ring-2 focus:ring-paleOlive-500 dark:text-white">
                            <option value="">Tất cả Block</option>
                        </select>
                    </div>
                </div>
            </div>

            <!-- Table with Pale Olive Theme & Clean Column Names -->
            <div class="overflow-x-auto">
                <table class="w-full text-left border-collapse text-xs">
                    <thead>
                        <tr class="bg-paleOlive-100 dark:bg-paleOlive-900/60 text-paleOlive-900 dark:text-paleOlive-200 font-bold border-b border-paleOlive-300 dark:border-paleOlive-700 uppercase tracking-wider">
                            <th class="py-3 px-3 w-12 text-center border-r border-paleOlive-200/80 dark:border-paleOlive-800/50">STT</th>
                            
                            <!-- Header: Số HĐ -->
                            <th class="py-3 px-3 w-32 border-r border-paleOlive-200/80 dark:border-paleOlive-800/50">
                                <span>Số HĐ</span>
                            </th>
                            
                            <!-- Header: Block -->
                            <th class="py-3 px-3 min-w-[140px] border-r border-paleOlive-200/80 dark:border-paleOlive-800/50">
                                <span>Block</span>
                            </th>
                            
                            <!-- Header: Lần Hẹn -->
                            <th class="py-3 px-3 text-center w-24 border-r border-paleOlive-200/80 dark:border-paleOlive-800/50">
                                <span>Lần Hẹn</span>
                            </th>
                            
                            <!-- Header: CL Lặp -->
                            <th class="py-3 px-3 text-center w-24 border-r border-paleOlive-200/80 dark:border-paleOlive-800/50">
                                <span>CL Lặp</span>
                            </th>
                            
                            <!-- Header: Nhân Sự -->
                            <th class="py-3 px-3 min-w-[130px] border-r border-paleOlive-200/80 dark:border-paleOlive-800/50">
                                <span>Nhân Sự</span>
                            </th>

                            <!-- Header: Quản Lý -->
                            <th class="py-3 px-3 min-w-[150px] border-r border-paleOlive-200/80 dark:border-paleOlive-800/50">
                                <span>Quản Lý</span>
                            </th>
                            
                            <!-- Header: Tồn Giờ -->
                            <th class="py-3 px-3 text-center w-24 border-r border-paleOlive-200/80 dark:border-paleOlive-800/50">
                                <span>Tồn Giờ</span>
                            </th>
                            
                            <!-- Header: Kiểm Soát -->
                            <th class="py-3 px-3 border-r border-paleOlive-200/80 dark:border-paleOlive-800/50 min-w-[160px]">
                                <div class="flex items-center space-x-1">
                                    <span>Kiểm Soát</span>
                                    <i class="fa-solid fa-pen-to-square text-paleOlive-700 dark:text-paleOlive-300 ml-1"></i>
                                </div>
                            </th>
                            
                            <!-- Header: Ghi Chú CSKH -->
                            <th class="py-3 px-3 min-w-[220px]">Ghi Chú CSKH</th>
                        </tr>
                    </thead>
                    <tbody id="tableBody" class="divide-y divide-paleOlive-200/60 dark:divide-paleOlive-800/40 bg-paleOlive-50/30 dark:bg-paleOlive-950/20">
                        <!-- Dynamic table rows -->
                    </tbody>
                </table>
            </div>

            <div class="px-5 py-3 bg-paleOlive-100/50 dark:bg-paleOlive-950/40 border-t border-paleOlive-200 dark:border-paleOlive-800 flex flex-col sm:flex-row items-center justify-between gap-2 text-xs text-paleOlive-900/80 dark:text-paleOlive-300">
                <div>
                    Hiển thị <span id="displayedCount" class="font-bold text-paleOlive-950 dark:text-paleOlive-100">0</span> / <span id="totalCount" class="font-bold text-paleOlive-950 dark:text-paleOlive-100">0</span> ca tồn
                </div>
                <div class="italic">
                    BangNC13-TQG.
                </div>
            </div>
        </div>

    </main>

    <footer class="bg-white dark:bg-slate-800 border-t border-slate-200 dark:border-slate-700 mt-8 py-4">
        <div class="max-w-7xl mx-auto px-4 text-center text-xs text-slate-500 dark:text-slate-400">
            Dashboard Kiểm Soát Ca Tồn & Checklist &bull; BangNC13-TQG
        </div>
    </footer>

    <script>
        // Sample dataset populated from real contracts shown in Excel mapped to Column AN (Quản lý)
        const sampleExcelData = [
            { "STT": 1, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAB7120", "Tên đầy đủ": "TRẦN VĂN", "Thời gian tạo": "2026-09-23 16:08:45", "Tồn giờ": -7, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã PC", "Độ Ưu Tiên": "Support", "POP": "TQGP013", "Kiểm soát": "", "Ghi Chú CC": "Checklist app hifpt/ Giga", "Cột AN": "Trần Văn Nam (QL-01)" },
            { "STT": 2, "Block": "Phuong My Lam-001", "Số HĐ": "TQFD10048", "Tên đầy đủ": "DƯƠNG V", "Thời gian tạo": "2026-09-23 21:47:48", "Tồn giờ": 13, "Số lần hẹn": 3, "CL Lặp": 1, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã PC", "Độ Ưu Tiên": "Support", "POP": "TQGP013", "Kiểm soát": "", "Ghi Chú CC": "TQAAB1004 >> TQGTI.ANHPH3", "Cột AN": "Trần Văn Nam (QL-01)" },
            { "STT": 3, "Block": "Xa Yen Son-001", "Số HĐ": "TQUAA3290", "Tên đầy đủ": "PHAM THI", "Thời gian tạo": "2026-09-19 08:49:45", "Tồn giờ": -5, "Số lần hẹn": 6, "CL Lặp": 1, "Nhân sự": "TQGTI.BINHLV6", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP026", "Kiểm soát": "", "Ghi Chú CC": "Khách hãn hò >> TQGTI.BINHLV6", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
            { "STT": 4, "Block": "Xa Yen Son-001", "Số HĐ": "TQUAA3853", "Tên đầy đủ": "NGÔ THỊ T", "Thời gian tạo": "2026-09-21 14:48:57", "Tồn giờ": -7, "Số lần hẹn": 5, "CL Lặp": 1, "Nhân sự": "TQGTI.BINHLV6", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP026", "Kiểm soát": "", "Ghi Chú CC": "0986265586 >> TQGTI.BINHLV6", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
            { "STT": 5, "Block": "Xa Nhu Khe-001", "Số HĐ": "TQFD00989", "Tên đầy đủ": "NGUYEN H", "Thời gian tạo": "2026-09-20 21:49:01", "Tồn giờ": 65, "Số lần hẹn": 2, "CL Lặp": 1, "Nhân sự": "TQGTI.CAONB", "TTCL": "Đang XL", "Độ Ưu Tiên": "Support", "POP": "TQGP005", "Kiểm soát": "", "Ghi Chú CC": "TQFD0098 >> TQGTI.CAONB", "Cột AN": "Trần Văn Nam (QL-01)" },
            { "STT": 6, "Block": "Xa Yen Son-001", "Số HĐ": "TQFD13450", "Tên đầy đủ": "TRỊNH KẾ", "Thời gian tạo": "2026-09-23 14:45:09", "Tồn giờ": -7, "Số lần hẹn": 1, "CL Lặp": 3, "Nhân sự": "TQGTI.CUHA", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP001", "Kiểm soát": "", "Ghi Chú CC": "Hỏng điều khiển Sky", "Cột AN": "Lê Hoàng Long (QL-03)" },
            { "STT": 7, "Block": "Xa Yen Son-001", "Số HĐ": "TQAAE9218", "Tên đầy đủ": "NGUYỄN N", "Thời gian tạo": "2026-09-24 08:35:09", "Tồn giờ": -24, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.CUHA", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP002", "Kiểm soát": "", "Ghi Chú CC": "TQAAE9218 - 0968561111", "Cột AN": "Lê Hoàng Long (QL-03)" },
            { "STT": 8, "Block": "Xa Chiem Hoa-001", "Số HĐ": "TQAAE3435", "Tên đầy đủ": "NGUYỄN T", "Thời gian tạo": "2026-09-15 16:27:27", "Tồn giờ": -29, "Số lần hẹn": 8, "CL Lặp": 1, "Nhân sự": "TQGTI.CUONGDD9", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP038", "Kiểm soát": "", "Ghi Chú CC": "KH báo trễ >> NghiaVT", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
            { "STT": 9, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAB6659", "Tên đầy đủ": "TỔNG THỊ", "Thời gian tạo": "2026-09-23 13:38:57", "Tồn giờ": -5, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.DANGNV", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP006", "Kiểm soát": "", "Ghi Chú CC": "0369759687 KH mkn", "Cột AN": "Trần Văn Nam (QL-01)" },
            { "STT": 10, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAE0730", "Tên đầy đủ": "LÝ THỊ LỰC", "Thời gian tạo": "2026-09-24 10:19:43", "Tồn giờ": -24, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.DUNGNT26", "TTCL": "Đã PC", "Độ Ưu Tiên": "Support", "POP": "TQGP027", "Kiểm soát": "", "Ghi Chú CC": "TQAAE0730 - 034654", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
            { "STT": 11, "Block": "Xa Dong Tho-001", "Số HĐ": "TQAAC9017", "Tên đầy đủ": "Vũ Đình Khải", "Thời gian tạo": "2026-09-17 08:56:48", "Tồn giờ": 137, "Số lần hẹn": 2, "CL Lặp": 2, "Nhân sự": "TQGTI.HIEUNV38", "TTCL": "Đang XL", "Độ Ưu Tiên": "Support", "POP": "TQGP030", "Kiểm soát": "", "Ghi Chú CC": "TQGP030.0094/HO-2", "Cột AN": "Lê Hoàng Long (QL-03)" },
            { "STT": 12, "Block": "Xa Chiem Hoa-001", "Số HĐ": "TQAAE0435", "Tên đầy đủ": "Lý Văn Đô", "Thời gian tạo": "2026-09-18 12:24:07", "Tồn giờ": -2, "Số lần hẹn": 9, "CL Lặp": 2, "Nhân sự": "TQGTI.HUNGCV4", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP037", "Kiểm soát": "", "Ghi Chú CC": "KH báo mất mạng", "Cột AN": "Lê Hoàng Long (QL-03)" },
            { "STT": 13, "Block": "Xa Ham Yen-001", "Số HĐ": "TQFD22905", "Tên đầy đủ": "NGUYỄN N", "Thời gian tạo": "2026-09-21 00:12:59", "Tồn giờ": -2, "Số lần hẹn": 3, "CL Lặp": 2, "Nhân sự": "TQGTI.LUCMDC", "TTCL": "Đã XL-Đang TD", "Độ Ưu Tiên": "Support", "POP": "TQGP024", "Kiểm soát": "", "Ghi Chú CC": "TQFD2290 >> TQGTI.LUCMDC", "Cột AN": "Trần Văn Nam (QL-01)" },
            { "STT": 14, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAE8568", "Tên đầy đủ": "ĐỖ DUY H", "Thời gian tạo": "2026-09-19 11:57:53", "Tồn giờ": -7, "Số lần hẹn": 7, "CL Lặp": 1, "Nhân sự": "TQGTI.QUYETNT1", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP031", "Kiểm soát": "", "Ghi Chú CC": "Checklist app hifpt", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
            { "STT": 15, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAE0407", "Tên đầy đủ": "TRƯƠNG", "Thời gian tạo": "2026-09-23 17:09:04", "Tồn giờ": -2, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.THANHNV41", "TTCL": "Đã PC", "Độ Ưu Tiên": "Support", "POP": "TQGP014", "Kiểm soát": "", "Ghi Chú CC": "0388061208 báo mkn", "Cột AN": "Lê Hoàng Long (QL-03)" },
            { "STT": 16, "Block": "Xa Yen Son-001", "Số HĐ": "TQFD01751", "Tên đầy đủ": "Cao Hong", "Thời gian tạo": "2026-09-24 08:57:55", "Tồn giờ": -2, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.THANHNV8", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP004", "Kiểm soát": "", "Ghi Chú CC": "TQFD01751 - 097876", "Cột AN": "Trần Văn Nam (QL-01)" },
            { "STT": 17, "Block": "Xa Yen Son-001", "Số HĐ": "TQAAB7146", "Tên đầy đủ": "LƯU ĐÌNH", "Thời gian tạo": "2026-09-23 16:53:44", "Tồn giờ": -24, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.THANHNV8", "TTCL": "Đang XL", "Độ Ưu Tiên": "Support", "POP": "TQGP006", "Kiểm soát": "", "Ghi Chú CC": "097971496 >> TQGTI.THANHNV8", "Cột AN": "Trần Văn Nam (QL-01)" },
            { "STT": 18, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAF1512", "Tên đầy đủ": "Triệu Thị", "Thời gian tạo": "2026-09-23 07:56:09", "Tồn giờ": -2, "Số lần hẹn": 3, "CL Lặp": 1, "Nhân sự": "TQGTI.TUANQD", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP009", "Kiểm soát": "", "Ghi Chú CC": "Checklist >> TQGTI.TUANQD", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
            { "STT": 19, "Block": "Xa Ham Yen-001", "Số HĐ": "TQFD12722", "Tên đầy đủ": "Nguyễn V", "Thời gian tạo": "2026-09-24 08:04:07", "Tồn giờ": 2, "Số lần hẹn": 2, "CL Lặp": 1, "Nhân sự": "TQGTI.TUANQD", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP009", "Kiểm soát": "", "Ghi Chú CC": "KH mkn nhờ KT xử lý", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
            { "STT": 20, "Block": "Xa Ham Yen-001", "Số HĐ": "TQFD21035", "Tên đầy đủ": "ĐÌNH VĂN", "Thời gian tạo": "2026-09-23 18:01:15", "Tồn giờ": -24, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.TUANQD", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP009", "Kiểm soát": "", "Ghi Chú CC": "0852269868 kh báo r", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
            { "STT": 21, "Block": "Xa Yen Son-001", "Số HĐ": "TQFD22274", "Tên đầy đủ": "PHẠM XUÂ", "Thời gian tạo": "2026-09-16 09:30:16", "Tồn giờ": 193, "Số lần hẹn": 4, "CL Lặp": 1, "Nhân sự": "TQGTI.TUNGDT4", "TTCL": "Đang XL", "Độ Ưu Tiên": "Support", "POP": "TQGP008", "Kiểm soát": "", "Ghi Chú CC": "085659332 >> TQGTI.TUNGDT4", "Cột AN": "Lê Hoàng Long (QL-03)" },
            { "STT": 22, "Block": "Xa Yen Son-001", "Số HĐ": "TQAAC4072", "Tên đầy đủ": "ĐẶNG THỊ", "Thời gian tạo": "2026-09-23 13:30:17", "Tồn giờ": -7, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.TUNGDT4", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP008", "Kiểm soát": "", "Ghi Chú CC": "0379639154 mất kết", "Cột AN": "Lê Hoàng Long (QL-03)" },
            { "STT": 23, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAE4800", "Tên đầy đủ": "Hoàng Văn", "Thời gian tạo": "2026-09-23 11:10:12", "Tồn giờ": 23, "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP013", "Kiểm soát": "", "Ghi Chú CC": "TQAEC48C >> TQGTI.ANHPH3", "Cột AN": "Trần Văn Nam (QL-01)" },
            { "STT": 24, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAE5855", "Tên đầy đủ": "Trần Thị H", "Thời gian tạo": "2026-09-23 11:42:15", "Tồn giờ": -7, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã PC", "Độ Ưu Tiên": "SOS", "POP": "TQGP013", "Kiểm soát": "", "Ghi Chú CC": "TQAAE5855 - 098768", "Cột AN": "Trần Văn Nam (QL-01)" },
            { "STT": 25, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAB1811", "Tên đầy đủ": "LÝ VĂN DŨ", "Thời gian tạo": "2026-09-23 15:23:30", "Tồn giờ": -24, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã PC", "Độ Ưu Tiên": "SOS", "POP": "TQGP013", "Kiểm soát": "", "Ghi Chú CC": "TQAAB1811 - 037519 FTTH", "Cột AN": "Trần Văn Nam (QL-01)" },
            { "STT": 26, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAE7704", "Tên đầy đủ": "NGA VĂN", "Thời gian tạo": "2026-09-23 13:27:32", "Tồn giờ": -24, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã PC", "Độ Ưu Tiên": "SOS", "POP": "TQGP013", "Kiểm soát": "", "Ghi Chú CC": "TQAAE7704 - 097767", "Cột AN": "Trần Văn Nam (QL-01)" },
            { "STT": 27, "Block": "Xa Yen Son-001", "Số HĐ": "TQAAA6787", "Tên đầy đủ": "NGUYỄN T", "Thời gian tạo": "2026-09-23 18:06:26", "Tồn giờ": -7, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.BINHLV6", "TTCL": "Đang XL", "Độ Ưu Tiên": "SOS", "POP": "TQGP026", "Kiểm soát": "", "Ghi Chú CC": "TQAAA6787 - 038570", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
            { "STT": 28, "Block": "Xa Dong Tho-001", "Số HĐ": "TQAAC5689", "Tên đầy đủ": "HOÀNG V", "Thời gian tạo": "2026-09-24 09:21:16", "Tồn giờ": -26, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.CHIENMM", "TTCL": "Đã PC", "Độ Ưu Tiên": "SOS", "POP": "TQGP033", "Kiểm soát": "", "Ghi Chú CC": "TQAAC5689 - 039248", "Cột AN": "Lê Hoàng Long (QL-03)" },
            { "STT": 29, "Block": "Xa Dong Tho-001", "Số HĐ": "TQFD22609", "Tên đầy đủ": "TRẦN THỊ", "Thời gian tạo": "2026-09-23 17:18:55", "Tồn giờ": -5, "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.HIEUNV38", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP021", "Kiểm soát": "", "Ghi Chú CC": "TQFD22609 - 0989711", "Cột AN": "Lê Hoàng Long (QL-03)" },
            { "STT": 30, "Block": "Xa Dong Tho-001", "Số HĐ": "TQAAC6077", "Tên đầy đủ": "RIÊU VĂN", "Thời gian tạo": "2026-09-23 18:50:25", "Tồn giờ": -7, "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.HIEUNV38", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP018", "Kiểm soát": "", "Ghi Chú CC": "TQAAC6077 - 098649", "Cột AN": "Lê Hoàng Long (QL-03)" },
            { "STT": 31, "Block": "Xa Chiem Hoa-001", "Số HĐ": "TQAAE4058", "Tên đầy đủ": "TRẦN THỊ", "Thời gian tạo": "2026-09-24 06:38:46", "Tồn giờ": -7, "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.HUNGDT5", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP035", "Kiểm soát": "", "Ghi Chú CC": "TQAAE4058 - 097806", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
            { "STT": 32, "Block": "Xa Dong Tho-001", "Số HĐ": "TQAAE1876", "Tên đầy đủ": "NINH VĂN", "Thời gian tạo": "2026-09-23 20:05:45", "Tồn giờ": 14, "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.NGHIANV6", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP032", "Kiểm soát": "", "Ghi Chú CC": "TQAAE1876 - 034763", "Cột AN": "Trần Văn Nam (QL-01)" },
            { "STT": 33, "Block": "Xa Dong Tho-001", "Số HĐ": "TQAAB0488", "Tên đầy đủ": "LÊ TRUNG", "Thời gian tạo": "2026-09-24 08:38:51", "Tồn giờ": -26, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.NGHIANV6", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP030", "Kiểm soát": "", "Ghi Chú CC": "TQGP030.0172/HO-1", "Cột AN": "Trần Văn Nam (QL-01)" },
            { "STT": 34, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAF1555", "Tên đầy đủ": "Trần Lệ Tri", "Thời gian tạo": "2026-09-23 08:55:18", "Tồn giờ": -2, "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.QUANHV1", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP027", "Kiểm soát": "", "Ghi Chú CC": "TQAAF1555 - 091719", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
            { "STT": 35, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAB1352", "Tên đầy đủ": "CHU VĂN", "Thời gian tạo": "2026-09-23 21:18:41", "Tồn giờ": -5, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.QUANHV1", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP027", "Kiểm soát": "", "Ghi Chú CC": "TQAAB1352 - 097454", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
            { "STT": 36, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAE6009", "Tên đầy đủ": "ĐẰNG VĂN", "Thời gian tạo": "2026-09-23 10:54:23", "Tồn giờ": -24, "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.QUANHV1", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP027", "Kiểm soát": "", "Ghi Chú CC": "TQAAE6009 - 083219", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
            { "STT": 37, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAB6047", "Tên đầy đủ": "NGUYỄN V", "Thời gian tạo": "2026-09-23 20:35:51", "Tồn giờ": -5, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.QUYETNT1", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP031", "Kiểm soát": "", "Ghi Chú CC": "TQAAB6047 - 097711", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
            { "STT": 38, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAE7703", "Tên đầy đủ": "Lò Thị Ngăn", "Thời gian tạo": "2026-09-20 21:27:28", "Tồn giờ": 85, "Số lần hẹn": 4, "CL Lặp": 0, "Nhân sự": "TQGTI.THANHNV41", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP014", "Kiểm soát": "", "Ghi Chú CC": "TQAAE7703 - 039252", "Cột AN": "Lê Hoàng Long (QL-03)" },
            { "STT": 39, "Block": "Phuong My Lam-001", "Số HĐ": "TQFD13770", "Tên đầy đủ": "NGUYỄN T", "Thời gian tạo": "2026-09-21 15:31:48", "Tồn giờ": 24, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.THANHNV41", "TTCL": "Đang XL", "Độ Ưu Tiên": "SOS", "POP": "TQGP014", "Kiểm soát": "", "Ghi Chú CC": "TQFD13770 - 039537", "Cột AN": "Lê Hoàng Long (QL-03)" },
            { "STT": 40, "Block": "Xa Chiem Hoa-001", "Số HĐ": "TQAAC8160", "Tên đầy đủ": "CHU VĂN", "Thời gian tạo": "2026-09-23 13:50:45", "Tồn giờ": 21, "Số lần hẹn": 3, "CL Lặp": 0, "Nhân sự": "TQGTI.TIENVT3", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP033", "Kiểm soát": "", "Ghi Chú CC": "TQAAC8160 - 034971", "Cột AN": "Trần Văn Nam (QL-01)" },
            { "STT": 41, "Block": "Xa Yen Son-001", "Số HĐ": "TQAAC7840", "Tên đầy đủ": "PHẠM ĐÌN", "Thời gian tạo": "2026-09-23 07:30:30", "Tồn giờ": -5, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.TUNGDT4", "TTCL": "Đang XL", "Độ Ưu Tiên": "SOS", "POP": "TQGP008", "Kiểm soát": "", "Ghi Chú CC": "TQAAC7840 - 096321", "Cột AN": "Lê Hoàng Long (QL-03)" }
        ];

        let currentDataset = [];
        let chartRepeatPriority = null;
        let chartTopBlock = null;
        let chartTopPop = null;
        let chartTopTech = null;

        // Custom notification helper replacing native alert
        function showToast(message, type = 'info') {
            const container = document.getElementById('toastContainer');
            const toast = document.createElement('div');
            
            const bgClass = type === 'success' ? 'bg-emerald-600' : (type === 'error' ? 'bg-rose-600' : 'bg-slate-800 dark:bg-slate-700');
            const iconClass = type === 'success' ? 'fa-circle-check' : (type === 'error' ? 'fa-circle-xmark' : 'fa-circle-info');

            toast.className = `pointer-events-auto flex items-center space-x-2 px-4 py-3 rounded-lg text-white shadow-lg text-xs ${bgClass} animate-toast`;
            toast.innerHTML = `<i class="fa-solid ${iconClass} text-sm"></i> <span>${message}</span>`;

            container.appendChild(toast);
            setTimeout(() => {
                toast.classList.add('opacity-0', 'transition-opacity', 'duration-300');
                setTimeout(() => toast.remove(), 300);
            }, 3500);
        }

        // Helper to safely parse numbers
        function parseTonGio(val) {
            if (val === undefined || val === null || val === '') return 0;
            if (typeof val === 'number') return Math.round(val * 10) / 10;
            const parsed = parseFloat(String(val).replace(',', '.').trim());
            return isNaN(parsed) ? 0 : Math.round(parsed * 10) / 10;
        }

        function getTonGioRealtime(row) {
            if (row['Thời gian tạo']) {
                let createdDate = null;
                const rawDate = row['Thời gian tạo'];

                if (typeof rawDate === 'number') {
                    createdDate = new Date(Math.round((rawDate - 25569) * 86400 * 1000));
                } else if (typeof rawDate === 'string' && rawDate.trim()) {
                    const parts = rawDate.trim().split(/[\s/:-]+/);
                    if (parts.length >= 3) {
                        if (parts[0].length === 4) { // YYYY-MM-DD
                            createdDate = new Date(parts[0], parts[1] - 1, parts[2], parts[3] || 0, parts[4] || 0, parts[5] || 0);
                        } else { // DD/MM/YYYY
                            createdDate = new Date(parts[2], parts[1] - 1, parts[0], parts[3] || 0, parts[4] || 0, parts[5] || 0);
                        }
                    }
                }

                if (createdDate && !isNaN(createdDate.getTime())) {
                    const diffMs = new Date() - createdDate;
                    if (diffMs > 0) {
                        return Math.floor(diffMs / (1000 * 60 * 60));
                    }
                }
            }
            return parseTonGio(row['Tồn giờ']);
        }

        function updateKPICards(data) {
            const total = data.length;
            
            // Column AA: Exact count of values equal or containing "SOS"
            const sosCount = data.filter(d => {
                const priorityVal = String(d['Độ Ưu Tiên'] || '').trim().toUpperCase();
                return priorityVal === 'SOS' || priorityVal.includes('SOS');
            }).length;

            // Column P > 0: Calculate total repeat sum and repeat case count
            const repeatCases = data.filter(d => (parseInt(d['CL Lặp'], 10) || 0) > 0);
            const repeatCountSum = repeatCases.reduce((sum, d) => sum + (parseInt(d['CL Lặp'], 10) || 0), 0);
            const repeatCasesCount = repeatCases.length;

            const overdueCount = data.filter(d => getTonGioRealtime(d) >= 24).length;
            const processingCount = data.filter(d => String(d['TTCL'] || '').includes('Đang XL')).length;
            const uncheckedCount = data.filter(d => !String(d['Kiểm soát'] || '').trim()).length;

            document.getElementById('kpiTotal').innerText = total;
            document.getElementById('recordCountBadge').innerText = total;

            document.getElementById('kpiSos').innerText = sosCount;
            document.getElementById('kpiSosPct').innerText = total ? ((sosCount / total) * 100).toFixed(1) + '%' : '0%';

            // Column P > 0: Sum of Column P values (27) and case count (22)
            document.getElementById('kpiRepeat').innerText = repeatCountSum;
            document.getElementById('kpiRepeatCases').innerText = `${repeatCasesCount} ca tồn`;

            document.getElementById('kpiOverdue').innerText = overdueCount;
            document.getElementById('kpiOverduePct').innerText = total ? ((overdueCount / total) * 100).toFixed(1) + '%' : '0%';

            document.getElementById('kpiProcessing').innerText = processingCount;
            document.getElementById('kpiProcessingPct').innerText = total ? ((processingCount / total) * 100).toFixed(1) + '%' : '0%';

            document.getElementById('kpiUnchecked').innerText = uncheckedCount;
        }

        function populateFilterOptions() {
            const blockSelect = document.getElementById('filterBlock');
            const techSelect = document.getElementById('filterTech');
            const colANSelect = document.getElementById('filterColAN');

            const blocks = [...new Set(currentDataset.map(d => d['Block']).filter(Boolean))].sort();
            const colANs = [...new Set(currentDataset.map(d => d['Cột AN']).filter(Boolean))].sort();

            // Populate Quản lý Dropdown
            const selectedAN = colANSelect ? colANSelect.value : '';
            colANSelect.innerHTML = '<option value="">Tất cả Quản lý</option>';
            colANs.forEach(an => {
                colANSelect.innerHTML += `<option value="${an}" ${an === selectedAN ? 'selected' : ''}>${an}</option>`;
            });

            // Populate Tech Filter
            updateTechDropdownOptions(selectedAN);

            blockSelect.innerHTML = '<option value="">Tất cả Block</option>';
            blocks.forEach(b => {
                blockSelect.innerHTML += `<option value="${b}">${b}</option>`;
            });
        }

        function updateTechDropdownOptions(selectedAN) {
            const techSelect = document.getElementById('filterTech');
            const currentTechVal = techSelect.value;

            let filteredTechData = currentDataset;
            if (selectedAN) {
                filteredTechData = currentDataset.filter(d => d['Cột AN'] === selectedAN);
            }

            const techs = [...new Set(filteredTechData.map(d => d['Nhân sự']).filter(Boolean))].sort();

            techSelect.innerHTML = '<option value="">Tất cả Nhân sự</option>';
            techs.forEach(t => {
                techSelect.innerHTML += `<option value="${t}" ${t === currentTechVal ? 'selected' : ''}>${t}</option>`;
            });
        }

        function onColANChange() {
            const selectedAN = document.getElementById('filterColAN').value;
            updateTechDropdownOptions(selectedAN);
            applyFilters();

            if (selectedAN) {
                const mappedTechs = [...new Set(currentDataset.filter(d => d['Cột AN'] === selectedAN).map(d => d['Nhân sự']))];
                showToast(`Đã lọc Quản lý: ${selectedAN} (${mappedTechs.length} Nhân sự)`, 'info');
            }
        }

        function applyFilters() {
            const filtered = getFilteredData();
            renderTable(filtered);
            renderCharts(filtered);
        }

        function getFilteredData() {
            const searchVal = document.getElementById('searchInput').value.toLowerCase().trim();
            const priorityVal = document.getElementById('filterPriority').value;
            const repeatVal = document.getElementById('filterRepeat').value;
            const blockVal = document.getElementById('filterBlock').value;
            const techVal = document.getElementById('filterTech').value;
            const colANVal = document.getElementById('filterColAN') ? document.getElementById('filterColAN').value : '';
            const onlyNonZero = document.getElementById('chkNonZero')?.checked;

            return currentDataset.filter(d => {
                const repeatNum = parseInt(d['CL Lặp'], 10) || 0;

                // Checkbox "Chỉ lấy CL Lặp khác 0" (Cột P > 0)
                if (onlyNonZero && repeatNum === 0) {
                    return false;
                }

                // Filter Cột AN (Quản lý / Leader)
                if (colANVal && d['Cột AN'] !== colANVal) return false;

                // Search query matching contract code, customer name, notes, block, technician, leader
                if (searchVal) {
                    const matchText = `${d['Số HĐ']} ${d['Tên đầy đủ']} ${d['Ghi Chú CC']} ${d['Block']} ${d['Nhân sự']} ${d['Cột AN'] || ''}`.toLowerCase();
                    if (!matchText.includes(searchVal)) return false;
                }

                // Column AA (SOS priority filter)
                const priorityStr = String(d['Độ Ưu Tiên'] || '').trim().toUpperCase();
                if (priorityVal === 'SOS' && !priorityStr.includes('SOS')) return false;
                if (priorityVal === 'Support' && priorityStr.includes('SOS')) return false;
                if (priorityVal === 'EMPTY' && priorityStr !== '') return false;

                // Column P (CL Lặp filter)
                if (repeatVal === 'NON_ZERO' && repeatNum === 0) return false;
                if (repeatVal === '0' && repeatNum !== 0) return false;
                if (repeatVal === '1' && repeatNum !== 1) return false;
                if (repeatVal === '2' && repeatNum !== 2) return false;
                if (repeatVal === '3' && repeatNum < 3) return false;

                // Column E (Block filter)
                if (blockVal && d['Block'] !== blockVal) return false;

                // Column S (Technician filter)
                if (techVal && d['Nhân sự'] !== techVal) return false;

                return true;
            });
        }

        function resetFilters() {
            document.getElementById('searchInput').value = '';
            document.getElementById('filterPriority').value = '';
            document.getElementById('filterRepeat').value = '';
            document.getElementById('filterBlock').value = '';
            document.getElementById('filterTech').value = '';
            if (document.getElementById('filterColAN')) document.getElementById('filterColAN').value = '';
            
            const chk = document.getElementById('chkNonZero');
            if (chk) chk.checked = false;

            populateFilterOptions();
            const filtered = getFilteredData();
            renderTable(filtered);
            renderCharts(filtered);
        }

        function renderTable(data) {
            const tbody = document.getElementById('tableBody');
            tbody.innerHTML = '';

            document.getElementById('displayedCount').innerText = data.length;
            document.getElementById('totalCount').innerText = currentDataset.length;

            if (data.length === 0) {
                tbody.innerHTML = `
                    <tr>
                        <td colspan="10" class="py-8 text-center text-paleOlive-600/70 dark:text-paleOlive-400/70">
                            <i class="fa-solid fa-folder-open text-3xl mb-2"></i>
                            <p>Không tìm thấy ca tồn nào khớp với bộ lọc</p>
                        </td>
                    </tr>
                `;
                return;
            }

            data.forEach((row, index) => {
                const tr = document.createElement('tr');
                tr.className = "hover:bg-paleOlive-100/70 dark:hover:bg-paleOlive-900/50 transition border-b border-paleOlive-200/60 dark:border-paleOlive-800/40 bg-paleOlive-50/40 dark:bg-paleOlive-950/20";

                // Column P Badge (CL Lặp)
                const repeatVal = parseInt(row['CL Lặp'], 10) || 0;
                let repeatBadge = `<span class="text-paleOlive-700/60 dark:text-paleOlive-400/60 font-mono">0</span>`;
                if (repeatVal === 1) {
                    repeatBadge = `<span class="px-2 py-0.5 rounded font-bold bg-amber-100 text-amber-800 dark:bg-amber-900/50 dark:text-amber-300 border border-amber-300">1</span>`;
                } else if (repeatVal === 2) {
                    repeatBadge = `<span class="px-2 py-0.5 rounded font-bold bg-orange-100 text-orange-800 dark:bg-orange-900/50 dark:text-orange-300 border border-orange-400">2</span>`;
                } else if (repeatVal >= 3) {
                    repeatBadge = `<span class="px-2 py-0.5 rounded font-bold bg-rose-200 text-rose-900 dark:bg-rose-900 dark:text-rose-100 border border-rose-400">${repeatVal}</span>`;
                }

                // Column O Badge (Số Lần Hẹn)
                const henVal = parseInt(row['Số lần hẹn'], 10) || 0;
                const henBadge = `<span class="px-2 py-0.5 rounded font-mono font-semibold bg-white/80 dark:bg-slate-800 text-slate-800 dark:text-slate-200 border border-paleOlive-300 dark:border-paleOlive-700">${henVal}</span>`;

                // Realtime Tồn Giờ
                const tonGio = getTonGioRealtime(row);
                let tonGioBadge = `<span class="font-semibold ${tonGio >= 24 ? 'text-purple-600 dark:text-purple-400 font-bold' : 'text-slate-700 dark:text-slate-300'}">${tonGio}h</span>`;

                const currentControl = String(row['Kiểm soát'] || '').trim();
                
                tr.innerHTML = `
                    <td class="py-3 px-3 text-center text-paleOlive-700 dark:text-paleOlive-300 font-mono border-r border-paleOlive-200/50 dark:border-paleOlive-800/40">${index + 1}</td>
                    
                    <!-- Clean Column: Số HĐ -->
                    <td class="py-3 px-3 font-bold text-paleOlive-950 dark:text-paleOlive-100 font-mono border-r border-paleOlive-200/50 dark:border-paleOlive-800/40">
                        ${row['Số HĐ'] || ''}
                    </td>

                    <!-- Clean Column: Block -->
                    <td class="py-3 px-3 font-medium text-slate-800 dark:text-paleOlive-100 border-r border-paleOlive-200/50 dark:border-paleOlive-800/40">
                        ${row['Block'] || ''}
                    </td>

                    <!-- Clean Column: Số Lần Hẹn -->
                    <td class="py-3 px-3 text-center border-r border-paleOlive-200/50 dark:border-paleOlive-800/40">
                        ${henBadge}
                    </td>

                    <!-- Clean Column: CL Lặp -->
                    <td class="py-3 px-3 text-center border-r border-paleOlive-200/50 dark:border-paleOlive-800/40">
                        ${repeatBadge}
                    </td>

                    <!-- Clean Column: Nhân sự -->
                    <td class="py-3 px-3 font-mono font-medium text-paleOlive-900 dark:text-paleOlive-200 border-r border-paleOlive-200/50 dark:border-paleOlive-800/40">
                        <i class="fa-solid fa-user-circle mr-1 text-paleOlive-600"></i> ${row['Nhân sự'] || ''}
                    </td>

                    <!-- Clean Column: Quản lý -->
                    <td class="py-3 px-3 font-medium text-paleOlive-900 dark:text-paleOlive-200 border-r border-paleOlive-200/50 dark:border-paleOlive-800/40">
                        <i class="fa-solid fa-user-shield mr-1 text-paleOlive-600"></i> ${row['Cột AN'] || ''}
                    </td>

                    <!-- Clean Column: Tồn Giờ -->
                    <td class="py-3 px-3 text-center border-r border-paleOlive-200/50 dark:border-paleOlive-800/40">${tonGioBadge}</td>

                    <!-- Clean Column: Kiểm Soát -->
                    <td class="py-3 px-3 border-r border-paleOlive-200/50 dark:border-paleOlive-800/40">
                        <select onchange="updateControlStatus(${row['STT']}, this.value)" class="w-full py-1 px-2 text-xs border border-paleOlive-300 dark:border-paleOlive-600 rounded bg-white dark:bg-slate-800 text-slate-800 dark:text-white font-medium focus:ring-2 focus:ring-paleOlive-500 shadow-sm">
                            <option value="" ${currentControl === '' ? 'selected' : ''}>-- Chưa Đánh Giá --</option>
                            <option value="Đạt" ${currentControl === 'Đạt' ? 'selected' : ''}>✅ Đã tiếp nhận</option>
                            <option value="Cần Hỗ Trợ" ${currentControl === 'Cần Hỗ Trợ' ? 'selected' : ''}>⚠️ Cần hỗ trợ</option>
                            <option value="Cảnh Báo" ${currentControl === 'Cảnh Báo' ? 'selected' : ''}>🚨 Cảnh báo trễ</option>
                            <option value="Vi Phạm" ${currentControl === 'Vi Phạm' ? 'selected' : ''}>❌ Khách giục</option>
                            <option value="Đã Xử Lý" ${currentControl === 'Đã Xử Lý' ? 'selected' : ''}>🎉 Đã giải quyết</option>
                        </select>
                    </td>

                    <!-- Clean Column: Ghi Chú CSKH -->
                    <td class="py-3 px-3 text-slate-600 dark:text-slate-300" title="${row['Ghi Chú CC'] || ''}">
                        ${row['Ghi Chú CC'] || ''}
                    </td>
                `;

                tbody.appendChild(tr);
            });
        }

        function updateControlStatus(stt, statusVal) {
            const item = currentDataset.find(d => d.STT === stt);
            if (item) {
                item['Kiểm soát'] = statusVal;
                updateKPICards(currentDataset);
                showToast(`Đã cập nhật kiểm soát ca #${stt} thành: ${statusVal || 'Chưa đánh giá'}`, 'success');
            }
        }

        function renderCharts(data) {
            const isDark = document.documentElement.classList.contains('dark');
            const textColor = isDark ? '#cbd5e1' : '#475569';
            const gridColor = isDark ? 'rgba(255, 255, 255, 0.08)' : 'rgba(0, 0, 0, 0.05)';

            // 1. Chart Repeat vs Priority
            const repeatCounts = { '0': { SOS: 0, Support: 0 }, '1': { SOS: 0, Support: 0 }, '2': { SOS: 0, Support: 0 }, '3+': { SOS: 0, Support: 0 } };
            
            data.forEach(d => {
                const r = parseInt(d['CL Lặp'], 10) || 0;
                const rKey = r >= 3 ? '3+' : String(r);
                const p = String(d['Độ Ưu Tiên'] || '').trim().toUpperCase().includes('SOS') ? 'SOS' : 'Support';
                if (repeatCounts[rKey]) {
                    repeatCounts[rKey][p]++;
                }
            });

            const ctx1 = document.getElementById('chartRepeatPriority').getContext('2d');
            if (chartRepeatPriority) chartRepeatPriority.destroy();
            chartRepeatPriority = new Chart(ctx1, {
                type: 'bar',
                data: {
                    labels: ['Không Lặp (0)', 'Lặp 1 lần', 'Lặp 2 lần', 'Lặp ≥ 3 lần'],
                    datasets: [
                        {
                            label: 'SOS (Cấp Thiết)',
                            data: [repeatCounts['0'].SOS, repeatCounts['1'].SOS, repeatCounts['2'].SOS, repeatCounts['3+'].SOS],
                            backgroundColor: '#f43f5e',
                            borderRadius: 6
                        },
                        {
                            label: 'Support (Hỗ Trợ)',
                            data: [repeatCounts['0'].Support, repeatCounts['1'].Support, repeatCounts['2'].Support, repeatCounts['3+'].Support],
                            backgroundColor: '#3b82f6',
                            borderRadius: 6
                        }
                    ]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { labels: { color: textColor, font: { family: 'Inter', size: 11 } } } },
                    scales: {
                        x: { ticks: { color: textColor }, grid: { color: gridColor } },
                        y: { ticks: { color: textColor }, grid: { color: gridColor } }
                    }
                }
            });

            // 2. Chart Top Block (Column E)
            const blockMap = {};
            data.forEach(d => {
                const b = d['Block'] || 'Chưa gán';
                blockMap[b] = (blockMap[b] || 0) + 1;
            });
            const topBlocks = Object.entries(blockMap).sort((a, b) => b[1] - a[1]).slice(0, 8);

            const ctx2 = document.getElementById('chartTopBlock').getContext('2d');
            if (chartTopBlock) chartTopBlock.destroy();
            chartTopBlock = new Chart(ctx2, {
                type: 'bar',
                data: {
                    labels: topBlocks.map(b => b[0]),
                    datasets: [{
                        label: 'Số ca tồn',
                        data: topBlocks.map(b => b[1]),
                        backgroundColor: '#0284c7',
                        borderRadius: 6
                    }]
                },
                options: {
                    indexAxis: 'y',
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { ticks: { color: textColor }, grid: { color: gridColor } },
                        y: { ticks: { color: textColor }, grid: { color: gridColor } }
                    }
                }
            });

            // 3. Chart Top POP (Column AL)
            const popMap = {};
            data.forEach(d => {
                const p = d['POP'] || 'Chưa gán';
                popMap[p] = (popMap[p] || 0) + 1;
            });
            const topPops = Object.entries(popMap).sort((a, b) => b[1] - a[1]).slice(0, 8);

            const ctx3 = document.getElementById('chartTopPop').getContext('2d');
            if (chartTopPop) chartTopPop.destroy();
            chartTopPop = new Chart(ctx3, {
                type: 'bar',
                data: {
                    labels: topPops.map(p => p[0]),
                    datasets: [{
                        label: 'Số ca tồn tại POP',
                        data: topPops.map(p => p[1]),
                        backgroundColor: '#10b981',
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { ticks: { color: textColor }, grid: { color: gridColor } },
                        y: { ticks: { color: textColor }, grid: { color: gridColor } }
                    }
                }
            });

            // 4. Chart Top 10 Tech Personnel (Column S)
            const techMap = {};
            data.forEach(d => {
                const t = d['Nhân sự'] || 'Chưa phân công';
                techMap[t] = (techMap[t] || 0) + 1;
            });
            // TOP 10 KTV có số tồn ca nhiều nhất
            const topTechs = Object.entries(techMap).sort((a, b) => b[1] - a[1]).slice(0, 10);

            const ctx4 = document.getElementById('chartTopTech').getContext('2d');
            if (chartTopTech) chartTopTech.destroy();
            chartTopTech = new Chart(ctx4, {
                type: 'bar',
                data: {
                    labels: topTechs.map(t => t[0]),
                    datasets: [{
                        label: 'Số ca tồn gánh',
                        data: topTechs.map(t => t[1]),
                        backgroundColor: '#a855f7',
                        borderRadius: 6
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: { legend: { display: false } },
                    scales: {
                        x: { ticks: { color: textColor }, grid: { color: gridColor } },
                        y: { ticks: { color: textColor }, grid: { color: gridColor } }
                    }
                }
            });
        }

        function handleFileUpload(event) {
            const file = event.target.files[0];
            if (!file) return;

            const reader = new FileReader();
            reader.onload = function(e) {
                try {
                    const data = new Uint8Array(e.target.result);
                    const workbook = XLSX.read(data, { type: 'array' });
                    const firstSheetName = workbook.SheetNames[0];
                    const worksheet = workbook.Sheets[firstSheetName];
                    
                    const rowsMatrix = XLSX.utils.sheet_to_json(worksheet, { header: 1, defval: '' });
                    if (!rowsMatrix || rowsMatrix.length <= 1) {
                        showToast('File Excel không có dữ liệu!', 'error');
                        return;
                    }

                    // Locate header row containing key fields
                    let headerRowIdx = 0;
                    for (let r = 0; r < Math.min(10, rowsMatrix.length); r++) {
                        const rowStr = rowsMatrix[r].map(c => String(c).toUpperCase()).join(' ');
                        if (rowStr.includes('SỐ HĐ') || rowStr.includes('TỒN GIỜ') || rowStr.includes('BLOCK')) {
                            headerRowIdx = r;
                            break;
                        }
                    }

                    const headers = rowsMatrix[headerRowIdx].map(h => String(h).trim());

                    function getColIndex(candidateNames, fallbackIndex) {
                        const idx = headers.findIndex(h => {
                            const cleanH = String(h).trim().toLowerCase();
                            return candidateNames.some(name => {
                                const cleanName = name.toLowerCase().trim();
                                if (cleanName === 'an' || cleanName === 'cột an') {
                                    return cleanH === 'an' || cleanH === 'cột an' || cleanH === 'cot an';
                                }
                                return cleanH.includes(cleanName);
                            });
                        });
                        return idx !== -1 ? idx : fallbackIndex;
                    }

                    // Excel exact positional indices: 
                    // Block=E(4), Số HĐ=F(5), Tên KH=G(6), CreatedTime=H(7), Tồn giờ=I(8), Số lần hẹn=O(14), CL Lặp=P(15), Nhân sự=S(18), SOS=AA(26), POP=AL(37), Kiểm soát=AM(38), Cột AN=AN(39)
                    const colBlockIdx = getColIndex(['Block', 'Mã Block'], 4);
                    const colSoHDIdx = getColIndex(['Số HĐ', 'So HD', 'Mã HĐ', 'Số HD'], 5);
                    const colTenKHIdx = getColIndex(['Tên đầy đủ', 'Khách hàng', 'Tên KH'], 6);
                    const colTimeIdx = getColIndex(['Thời gian tạo', 'Thoi gian tao', 'Ngày tạo'], 7);
                    const colTonGioIdx = getColIndex(['Tồn giờ', 'Ton gio'], 8);
                    const colHenIdx = getColIndex(['Số lần hẹn', 'Số lần hò', 'Lần hẹn'], 14);
                    const colCLLapIdx = getColIndex(['CL Lặp', 'CL Lap', 'Lặp'], 15);
                    const colTechIdx = getColIndex(['Nhân sự', 'KTV', 'Nhân sự xử lý'], 18);
                    const colPriorityIdx = getColIndex(['Độ Ưu Tiên', 'Độ Ưu', 'SOS'], 26);
                    const colPopIdx = getColIndex(['POP', 'Trạm POP'], 37);
                    const colControlIdx = getColIndex(['Kiểm soát', 'Đánh giá'], 38);
                    const colANIdx = getColIndex(['cột an', 'an', 'quản lý', 'leader', 'giám sát'], 39);
                    const colTtclIdx = getColIndex(['TTCL', 'Trạng Thái', 'Trạng thái'], 19);
                    const colNoteIdx = getColIndex(['Ghi Chú CC', 'Ghi Chú', 'Ghi chú'], 20);

                    const parsedRecords = [];
                    for (let r = headerRowIdx + 1; r < rowsMatrix.length; r++) {
                        const row = rowsMatrix[r];
                        if (!row || row.length === 0) continue;

                        const soHD = String(row[colSoHDIdx] || '').trim();
                        const block = String(row[colBlockIdx] || '').trim();
                        
                        if (!soHD && !block) continue;

                        parsedRecords.push({
                            "STT": parsedRecords.length + 1,
                            "Block": block,
                            "Số HĐ": soHD,
                            "Tên đầy đủ": String(row[colTenKHIdx] || '').trim(),
                            "Thời gian tạo": row[colTimeIdx] || '',
                            "Tồn giờ": parseTonGio(row[colTonGioIdx]),
                            "Số lần hẹn": parseInt(row[colHenIdx], 10) || 0,
                            "CL Lặp": parseInt(row[colCLLapIdx], 10) || 0,
                            "Nhân sự": String(row[colTechIdx] || '').trim(),
                            "TTCL": String(row[colTtclIdx] || 'Đang XL').trim(),
                            "Độ Ưu Tiên": String(row[colPriorityIdx] || '').trim(),
                            "POP": String(row[colPopIdx] || '').trim(),
                            "Kiểm soát": String(row[colControlIdx] || '').trim(),
                            "Cột AN": String(row[colANIdx] || '').trim(),
                            "Ghi Chú CC": String(row[colNoteIdx] || '').trim()
                        });
                    }

                    if (parsedRecords.length > 0) {
                        currentDataset = parsedRecords;
                        populateFilterOptions();
                        renderDashboard();
                        showToast(`Nạp thành công ${currentDataset.length} ca tồn từ Excel!`, 'success');
                    } else {
                        showToast('Không đọc được bản ghi hợp lệ nào từ file!', 'error');
                    }
                } catch (err) {
                    showToast('Lỗi khi xử lý file Excel: ' + err.message, 'error');
                }
            };
            reader.readAsArrayBuffer(file);
        }

        function exportDataCSV() {
            const dataToExport = getFilteredData();
            if (!dataToExport.length) {
                showToast('Không có dữ liệu để xuất!', 'error');
                return;
            }

            const ws = XLSX.utils.json_to_sheet(dataToExport);
            const wb = XLSX.utils.book_new();
            XLSX.utils.book_append_sheet(wb, ws, "Kiểm Soát Ca Tồn");
            XLSX.writeFile(wb, "Bao_Cao_Kiem_Soat_Ca_Ton.xlsx");
            showToast('Đã xuất file Excel báo cáo!', 'success');
        }

        function toggleDarkMode() {
            document.documentElement.classList.toggle('dark');
            const filtered = getFilteredData();
            renderCharts(filtered);
        }

        function renderDashboard() {
            const filtered = getFilteredData();
            updateKPICards(currentDataset);
            renderTable(filtered);
            renderCharts(filtered);
        }

        window.onload = function() {
            currentDataset = [...sampleExcelData];
            populateFilterOptions();
            renderDashboard();
        };
    </script>
</body>
</html>
