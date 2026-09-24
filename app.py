import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CẤU HÌNH TRANG STREAMLIT (CẤU HÌNH THEME LIGHT BẮT BUỘC)
st.set_page_config(
    page_title="DASHBOARD KIỂM SOÁT CA TỒN & CHECKLIST",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. OVERRIDE CSS CỰC MẠNH ĐỂ DIỆT DỰT DARK MODE & ĐỔI BẢNG SANG MÀU XANH OLIU NHẠT
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', -apple-system, sans-serif !important; }

    /* Ẩn Sidebar & Header thừa */
    [data-testid="stSidebar"], [data-testid="collapsedControl"], #MainMenu, footer { display: none !important; }
    
    .main .block-container {
        max-width: 98% !important;
        padding: 0.8rem 1rem !important;
    }

    /* Ép nền toàn trang sang màu trắng/xanh sáng nhạt */
    html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stHeader"] {
        background-color: #f7faf3 !important;
        color: #1a2e05 !important;
    }
    
    /* Header chính */
    .main-header {
        display: flex;
        align-items: center;
        background-color: #ffffff;
        padding: 10px 18px;
        border-radius: 12px;
        border: 1px solid #d0e1a9;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        margin-bottom: 12px;
    }
    .header-icon {
        background-color: #709214;
        color: white;
        border-radius: 50%;
        width: 34px;
        height: 34px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
        margin-right: 12px;
    }
    .header-title { font-size: 17px; font-weight: 800; color: #233703; }
    .badge-sub {
        background-color: #eaf3d6;
        color: #4a6708;
        font-size: 11px;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 12px;
        border: 1px solid #c0d982;
    }
    .header-desc { font-size: 11px; color: #586e2e; margin-top: 2px; }

    /* Top 6 KPI Cards */
    .kpi-container { display: flex; gap: 8px; margin-bottom: 12px; }
    .kpi-card {
        flex: 1;
        background-color: #ffffff;
        border-radius: 8px;
        padding: 10px 6px;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        border: 1px solid #dce8be;
    }
    .kpi-blue { border-top: 3.5px solid #3b82f6; }
    .kpi-pink { border-top: 3.5px solid #f43f5e; }
    .kpi-orange { border-top: 3.5px solid #f97316; }
    .kpi-purple { border-top: 3.5px solid #a855f7; }
    .kpi-cyan { border-top: 3.5px solid #06b6d4; }
    .kpi-green { border-top: 3.5px solid #10b981; }
    .kpi-label { font-size: 11px; font-weight: 600; color: #3d5214; white-space: nowrap; }

    /* KHU VỰC BẢNG & BỘ LỌC (MÀU XANH OLIU NHẠT CỰC NỔI) */
    .table-container-box {
        background-color: #eef5e2 !important;
        border: 1.5px solid #9bbd38 !important;
        border-radius: 12px;
        padding: 16px;
        margin-top: 10px;
    }
    .table-header-title { font-size: 15px; font-weight: 800; color: #2c3e0a; display: flex; align-items: center; gap: 6px; }
    .table-header-sub { font-size: 11px; color: #577519; margin-bottom: 12px; }

    /* 1. Ép màu các ô Input & Selectbox sang Xanh Oliu Nhạt */
    div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, input {
        background-color: #dceabb !important;
        color: #1c2b04 !important;
        border-radius: 6px !important;
        border: 1px solid #8eaf28 !important;
        font-weight: 600 !important;
    }
    div[data-baseweb="select"] span, div[data-baseweb="select"] div {
        color: #1c2b04 !important;
    }
    /* Đổi màu icon mũi tên trong dropdown */
    div[data-baseweb="select"] svg {
        fill: #2c3e0a !important;
    }

    /* 2. Ép màu Bảng data_editor / dataframe nền sáng Xanh Oliu Nhạt */
    [data-testid="stDataFrame"], [data-testid="stDataEditor"] {
        background-color: #eef5e2 !important;
        border: 1px solid #a8c74d !important;
        border-radius: 8px !important;
    }
    
    /* Can thiệp shadow canvas của bảng st.data_editor */
    [data-testid="stDataFrame"] canvas, [data-testid="stDataEditor"] canvas {
        filter: invert(0) !important; /* Đảm bảo không bị dính Dark Mode trình duyệt */
    }

    /* Text thông báo phía dưới */
    .table-footer-text {
        font-size: 11px;
        color: #4a6612;
        margin-top: 8px;
        font-weight: 700;
    }
    </style>
""", unsafe_allow_html=True)

# 3. NẠP VÀ XỬ LÝ DỮ LIỆU FILE EXCEL
@st.cache_data
def load_excel_data(file):
    try:
        xls = pd.ExcelFile(file)
        sheet_name = 'BT' if 'BT' in xls.sheet_names else xls.sheet_names[0]
        df = pd.read_excel(xls, sheet_name=sheet_name)

        if 'Trưởng bầy' in df.columns:
            df['QUẢN LÝ'] = df['Trưởng bầy']
        elif len(df.columns) >= 40:
            df['QUẢN LÝ'] = df.iloc[:, 39]
        else:
            df['QUẢN LÝ'] = 'Chưa phân loại'

        rename_map = {
            'Số HĐ': 'SỐ HĐ', 'Block': 'BLOCK', 'Số lần hẹn': 'LẦN HẸN',
            'CL Lặp': 'CL LẶP', 'Nhân sự': 'NHÂN SỰ', 'Tồn giờ': 'TỒN GIỜ',
            'Kiểm soát': 'KIỂM SOÁT', 'Ghi Chú CC': 'GHI CHÚ CSKH'
        }
        df = df.rename(columns=rename_map)
        df = df.loc[:, ~df.columns.duplicated()]

        defaults = {
            'SỐ HĐ': '', 'BLOCK': 'Khác', 'LẦN HẸN': 0, 'CL LẶP': 0,
            'NHÂN SỰ': 'Chưa gán', 'QUẢN LÝ': 'Chưa gán', 'TỒN GIỜ': '0h',
            'KIỂM SOÁT': '-- Chưa Đánh Giá --', 'GHI CHÚ CSKH': '',
            'Độ Ưu Tiên': 'Support', 'POP': 'Khác'
        }
        for col, val in defaults.items():
            if col not in df.columns:
                df[col] = val
            else:
                df[col] = df[col].fillna(val)

        return df
    except Exception as e:
        st.error(f"Lỗi đọc file: {e}")
        return pd.DataFrame()

# 4. HEADER TRÊN CÙNG
h_col1, h_col2 = st.columns([3.5, 1])

with h_col1:
    st.markdown("""
    <div class="main-header">
        <div class="header-icon">📑</div>
        <div>
            <div style="display: flex; align-items: center; gap: 8px;">
                <span class="header-title">DASHBOARD KIỂM SOÁT CA TỒN & CHECKLIST</span>
                <span class="badge-sub">Báo Cáo Kiểm Soát</span>
            </div>
            <div class="header-desc">Khớp chính xác: Số HĐ, Khách Hàng, Block, Lần Hẹn, CL Lặp, Nhân Sự, Quản Lý, Tồn Giờ, Kiểm Soát</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with h_col2:
    uploaded_file = st.file_uploader("📂 Import File Excel", type=["xlsx", "xls"], label_visibility="collapsed")

if uploaded_file is not None:
    df_raw = load_excel_data(uploaded_file)
else:
    try:
        df_raw = load_excel_data('CLL2.xlsx')
    except:
        st.info("👆 Vui lòng bấm nạp file Excel ở góc trên bên phải.")
        st.stop()

# 5. TOP KPI CARDS
st.markdown("""
<div class="kpi-container">
    <div class="kpi-card kpi-blue"><div class="kpi-label">Tổng hợp hợp đồng tồn</div></div>
    <div class="kpi-card kpi-pink"><div class="kpi-label">Số ca báo SOS</div></div>
    <div class="kpi-card kpi-orange"><div class="kpi-label">Tổng lượt lặp (Lặp > 0)</div></div>
    <div class="kpi-card kpi-purple"><div class="kpi-label">Ca quá hạn 1 ngày</div></div>
    <div class="kpi-card kpi-cyan"><div class="kpi-label">Trạng thái Đang XL</div></div>
    <div class="kpi-card kpi-green"><div class="kpi-label">Chưa ghi nhận đánh giá</div></div>
</div>
""", unsafe_allow_html=True)

# 6. KHU VỰC 4 BIỂU ĐỒ (SÁNG)
chart_style = {
    'paper_bgcolor': '#ffffff',
    'plot_bgcolor': '#ffffff',
    'font': {'color': '#2c3e0a', 'size': 11, 'family': 'Inter'},
    'margin': dict(l=10, r=10, t=10, b=10)
}

c1, c2 = st.columns(2)

with c1:
    df_chart1 = df_raw.groupby(['CL LẶP', 'Độ Ưu Tiên']).size().reset_index(name='Số ca')
    fig1 = px.bar(df_chart1, x='CL LẶP', y='Số ca', color='Độ Ưu Tiên', barmode='group', color_discrete_map={'SOS': '#f43f5e', 'Support': '#709214'})
    fig1.update_layout(**chart_style, height=180, showlegend=True, legend=dict(orientation="h", y=1.1, x=0.2))
    fig1.update_xaxes(showgrid=True, gridcolor='#f1f5f9')
    fig1.update_yaxes(showgrid=True, gridcolor='#f1f5f9')
    st.plotly_chart(fig1, use_container_width=True)

with c2:
    df_chart2 = df_raw['BLOCK'].value_counts().head(5).reset_index()
    df_chart2.columns = ['BLOCK', 'Số ca']
    fig2 = px.bar(df_chart2, y='BLOCK', x='Số ca', orientation='h', color_discrete_sequence=['#4d7c0f'])
    fig2.update_layout(**chart_style, height=180)
    fig2.update_xaxes(showgrid=True, gridcolor='#f1f5f9')
    fig2.update_yaxes(categoryorder='total ascending', showgrid=True, gridcolor='#f1f5f9')
    st.plotly_chart(fig2, use_container_width=True)

# 7. KHU VỰC BẢNG DỮ LIỆU (XANH OLIU NHẠT CHUẨN)
st.markdown("""
<div class="table-container-box">
    <div class="table-header-title">📊 BẢNG KIỂM SOÁT DỮ LIỆU TỒN CA</div>
    <div class="table-header-sub">Xem, tìm kiếm, lọc và cập nhật trực tiếp trạng thái Kiểm Soát</div>
""", unsafe_allow_html=True)

list_mgr = sorted([str(x).strip() for x in df_raw['QUẢN LÝ'].unique() if pd.notna(x) and str(x).strip() != ''])

# BỘ LỌC NGANG
f1, f2, f3, f4, f5, f6 = st.columns([2, 1.5, 1.5, 1.5, 1.5, 1.5])

with f1:
    search_input = st.text_input("Search", placeholder="🔍 Tìm Số HĐ, Block...", label_visibility="collapsed")
with f2:
    selected_mgr = st.selectbox("Mgr", options=["Tất cả Quản lý"] + list_mgr, label_visibility="collapsed")

if selected_mgr != "Tất cả Quản lý":
    df_sub = df_raw[df_raw['QUẢN LÝ'].astype(str) == selected_mgr]
else:
    df_sub = df_raw.copy()

with f3:
    list_tech = sorted([str(x).strip() for x in df_sub['NHÂN SỰ'].unique() if pd.notna(x)])
    selected_tech = st.selectbox("Tech", options=["Tất cả Nhân sự"] + list_tech, label_visibility="collapsed")
with f4:
    list_prio = sorted([str(x).strip() for x in df_sub['Độ Ưu Tiên'].unique() if pd.notna(x)])
    selected_prio = st.selectbox("SOS", options=["Tất cả Mức SOS"] + list_prio, label_visibility="collapsed")
with f5:
    selected_repeat = st.selectbox("Repeat", options=["Tất cả CL Lặp", "Chỉ lấy CL Lặp khác 0", "Bằng 0"], label_visibility="collapsed")
with f6:
    list_block = sorted([str(x).strip() for x in df_sub['BLOCK'].unique() if pd.notna(x)])
    selected_block = st.selectbox("Block", options=["Tất cả Block"] + list_block, label_visibility="collapsed")

# LỌC DỮ LIỆU
df_table = df_sub.copy()
if selected_tech != "Tất cả Nhân sự":
    df_table = df_table[df_table['NHÂN SỰ'].astype(str) == selected_tech]
if selected_prio != "Tất cả Mức SOS":
    df_table = df_table[df_table['Độ Ưu Tiên'].astype(str) == selected_prio]
if selected_repeat == "Chỉ lấy CL Lặp khác 0":
    df_table = df_table[pd.to_numeric(df_table['CL LẶP'], errors='coerce').fillna(0) > 0]
elif selected_repeat == "Bằng 0":
    df_table = df_table[pd.to_numeric(df_table['CL LẶP'], errors='coerce').fillna(0) == 0]
if selected_block != "Tất cả Block":
    df_table = df_table[df_table['BLOCK'].astype(str) == selected_block]
if search_input:
    s_val = search_input.lower()
    df_table = df_table[
        df_table['SỐ HĐ'].astype(str).str.lower().str.contains(s_val) |
        df_table['BLOCK'].astype(str).str.lower().str.contains(s_val) |
        df_table['GHI CHÚ CSKH'].astype(str).str.lower().str.contains(s_val)
    ]

# TẠO DATAFRAME RENDER BẢNG
df_display = pd.DataFrame()
df_display['STT'] = range(1, len(df_table) + 1)
df_display['SỐ HĐ'] = df_table['SỐ HĐ'].astype(str).values
df_display['BLOCK'] = df_table['BLOCK'].astype(str).values
df_display['LẦN HẸN'] = pd.to_numeric(df_table['LẦN HẸN'], errors='coerce').fillna(0).astype(int).values
df_display['CL LẶP'] = pd.to_numeric(df_table['CL LẶP'], errors='coerce').fillna(0).astype(int).values
df_display['NHÂN SỰ'] = df_table['NHÂN SỰ'].astype(str).values
df_display['QUẢN LÝ'] = df_table['QUẢN LÝ'].astype(str).values
df_display['TỒN GIỜ'] = df_table['TỒN GIỜ'].astype(str).values
df_display['KIỂM SOÁT'] = df_table['KIỂM SOÁT'].astype(str).values
df_display['GHI CHÚ CSKH'] = df_table['GHI CHÚ CSKH'].astype(str).values

# BẢNG HIỂN THỊ
st.data_editor(
    df_display,
    column_config={
        "STT": st.column_config.NumberColumn("STT", width="small"),
        "SỐ HĐ": st.column_config.TextColumn("SỐ HĐ", disabled=True),
        "BLOCK": st.column_config.TextColumn("BLOCK"),
        "LẦN HẸN": st.column_config.NumberColumn("LẦN HẸN", width="small"),
        "CL LẶP": st.column_config.NumberColumn("CL LẶP", width="small"),
        "NHÂN SỰ": st.column_config.TextColumn("NHÂN SỰ"),
        "QUẢN LÝ": st.column_config.TextColumn("QUẢN LÝ"),
        "TỒN GIỜ": st.column_config.TextColumn("TỒN GIỜ"),
        "KIỂM SOÁT": st.column_config.SelectboxColumn(
            "KIỂM SOÁT ✍️",
            options=["-- Chưa Đánh Giá --", "✅ Đã Kiểm Soát", "🚨 Cảnh Báo Lặp"],
            required=True,
        ),
        "GHI CHÚ CSKH": st.column_config.TextColumn("GHI CHÚ CSKH", width="large"),
    },
    hide_index=True,
    use_container_width=True
)

st.markdown(f"<div class='table-footer-text'>Hiển thị <b>{len(df_display)}</b> / <b>{len(df_raw)}</b> ca tồn</div></div>", unsafe_allow_html=True)
