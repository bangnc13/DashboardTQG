import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CẤU HÌNH TRANG: TỰ ĐỘNG THU GỌN SIDEBAR
st.set_page_config(
    page_title="DASHBOARD KIỂM SOÁT CA TỒN & CHECKLIST",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS: Ẩn hoàn toàn Sidebar + CSS Giao diện Light Theme
st.markdown("""
    <style>
    /* Ẩn hoàn toàn Sidebar bên trái */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    
    /* Mở rộng khung nội dung chính tràn màn hình */
    .main .block-container {
        max-width: 100% !important;
        padding-left: 1.5rem !important;
        padding-right: 1.5rem !important;
        padding-top: 1rem !important;
    }

    /* Nền trang sáng */
    .stApp { background-color: #f8fafc; color: #1e293b; }
    
    /* Header chính */
    .main-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #ffffff;
        padding: 10px 16px;
        border-radius: 8px;
        border: 1px solid #e2e8f0;
        margin-bottom: 12px;
    }
    .header-title {
        font-size: 18px;
        font-weight: 800;
        color: #1e293b;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .badge-sub {
        background-color: #fef08a;
        color: #854d0e;
        font-size: 11px;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 12px;
    }

    /* KPI Cards Styling */
    .kpi-card {
        background-color: #ffffff;
        border-radius: 8px;
        padding: 10px;
        text-align: center;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .kpi-blue { border-top: 4px solid #3b82f6; border-bottom: 1px solid #e2e8f0; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; }
    .kpi-pink { border-top: 4px solid #f43f5e; border-bottom: 1px solid #e2e8f0; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; }
    .kpi-orange { border-top: 4px solid #f97316; border-bottom: 1px solid #e2e8f0; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; }
    .kpi-purple { border-top: 4px solid #a855f7; border-bottom: 1px solid #e2e8f0; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; }
    .kpi-cyan { border-top: 4px solid #06b6d4; border-bottom: 1px solid #e2e8f0; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; }
    .kpi-green { border-top: 4px solid #10b981; border-bottom: 1px solid #e2e8f0; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; }

    .kpi-label { font-size: 11px; font-weight: 700; color: #64748b; margin-bottom: 2px; }
    .kpi-val { font-size: 20px; font-weight: 800; color: #0f172a; }

    /* Khung Chart Card */
    .chart-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 12px;
        margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
    }
    .chart-title { font-size: 13px; font-weight: 700; color: #1e293b; margin-bottom: 1px; }
    .chart-sub { font-size: 10px; color: #94a3b8; margin-bottom: 8px; }
    </style>
""", unsafe_allow_html=True)

# 2. HÀM NẠP VÀ XỬ LÝ DỮ LIỆU TỪ FILE EXCEL
@st.cache_data
def load_excel_data(file):
    try:
        xls = pd.ExcelFile(file)
        sheet_name = 'BT' if 'BT' in xls.sheet_names else xls.sheet_names[0]
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # Lấy Quản lý từ Cột AN (Index 39)
        if 'Trưởng bầy' in df.columns:
            df['QUẢN LÝ'] = df['Trưởng bầy']
        elif len(df.columns) >= 40:
            df['QUẢN LÝ'] = df.iloc[:, 39]
        else:
            df['QUẢN LÝ'] = 'Chưa phân loại'

        # Đổi tên các cột chính
        col_rename = {
            'Số HĐ': 'SỐ HĐ',
            'Block': 'BLOCK',
            'Số lần hẹn': 'LẦN HẸN',
            'CL Lặp': 'CL LẶP',
            'Nhân sự': 'NHÂN SỰ',
            'Tồn giờ': 'TỒN GIỜ',
            'Kiểm soát': 'KIỂM SOÁT',
            'Ghi Chú CC': 'GHI CHÚ CSKH'
        }
        df = df.rename(columns=col_rename)

        # Loại bỏ các cột trùng tên nếu có
        df = df.loc[:, ~df.columns.duplicated()]

        # Gán giá trị mặc định cho cột thiếu
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

# 3. HEADER TRÊN CÙNG + NÚT IMPORT EXCEL GÓC TRÊN BÊN PHẢI
head_left, head_right = st.columns([3, 1])

with head_left:
    st.markdown("""
    <div class="main-header">
        <div class="header-title">
            <span>📊 DASHBOARD KIỂM SOÁT CA TỒN & CHECKLIST</span>
            <span class="badge-sub">Báo Cáo Kiểm Soát</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with head_right:
    uploaded_file = st.file_uploader("📂 Import File Excel (CLL2.xlsx)", type=["xlsx", "xls"], label_visibility="collapsed")

# Nạp dữ liệu
if uploaded_file is not None:
    df_raw = load_excel_data(uploaded_file)
else:
    try:
        df_raw = load_excel_data('CLL2.xlsx')
    except:
        st.info("👆 Vui lòng bấm nút 'Browse files' ở góc trên bên phải để nạp file Excel.")
        st.stop()

# 4. KHU VỰC 6 THẺ TOP KPI
total_cases = len(df_raw)
sos_cases = len(df_raw[df_raw['Độ Ưu Tiên'].astype(str).str.contains('SOS', na=False)])
repeat_cases = len(df_raw[pd.to_numeric(df_raw['CL LẶP'], errors='coerce').fillna(0) > 0])

k1, k2, k3, k4, k5, k6 = st.columns(6)

with k1:
    st.markdown(f'<div class="kpi-card kpi-blue"><div class="kpi-label">Tổng hợp hợp đồng tồn</div><div class="kpi-val">{total_cases}</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="kpi-card kpi-pink"><div class="kpi-label">Số ca báo SOS</div><div class="kpi-val">{sos_cases}</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="kpi-card kpi-orange"><div class="kpi-label">Tổng lượt lặp (Lặp > 0)</div><div class="kpi-val">{repeat_cases}</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="kpi-card kpi-purple"><div class="kpi-label">Ca quá hạn 1 ngày</div><div class="kpi-val">0</div></div>', unsafe_allow_html=True)
with k5:
    st.markdown(f'<div class="kpi-card kpi-cyan"><div class="kpi-label">Trạng thái Đang XL</div><div class="kpi-val">{total_cases}</div></div>', unsafe_allow_html=True)
with k6:
    st.markdown(f'<div class="kpi-card kpi-green"><div class="kpi-label">Chưa ghi nhận đánh giá</div><div class="kpi-val">0</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 5. KHU VỰC 4 BIỂU ĐỒ (CHARTS)
chart_theme = {
    'paper_bgcolor': '#ffffff',
    'plot_bgcolor': '#ffffff',
    'font': {'color': '#475569', 'size': 11},
    'margin': dict(l=15, r=15, t=15, b=15)
}

c1, c2 = st.columns(2)

with c1:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">📊 1. Tỉ trọng Checklist Lặp Theo Mức Độ SOS</div>
        <div class="chart-sub">Thống kê ca SOS vs Support lặp lại nhiều lần</div>
    """, unsafe_allow_html=True)
    df_chart1 = df_raw.groupby(['CL LẶP', 'Độ Ưu Tiên']).size().reset_index(name='Số ca')
    fig1 = px.bar(
        df_chart1, x='CL LẶP', y='Số ca', color='Độ Ưu Tiên', barmode='group',
        color_discrete_map={'SOS': '#f43f5e', 'Support': '#3b82f6'}
    )
    fig1.update_layout(**chart_theme, height=200, showlegend=True, legend=dict(orientation="h", y=1.1, x=0.2))
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">📊 2. Top Block Tồn Ca Nhiều Nhất</div>
        <div class="chart-sub">Đơn vị địa bàn phát sinh sự cố</div>
    """, unsafe_allow_html=True)
    df_chart2 = df_raw['BLOCK'].value_counts().head(5).reset_index()
    df_chart2.columns = ['BLOCK', 'Số ca']
    fig2 = px.bar(df_chart2, y='BLOCK', x='Số ca', orientation='h', color_discrete_sequence=['#0284c7'])
    fig2.update_layout(**chart_theme, height=200, yaxis={'categoryorder':'total ascending'})
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

c3, c4 = st.columns(2)

with c3:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">📍 3. Tồn theo POP</div>
        <div class="chart-sub">Cụm trạm kỹ thuật quản lý hạ tầng</div>
    """, unsafe_allow_html=True)
    df_chart3 = df_raw['POP'].value_counts().head(5).reset_index()
    df_chart3.columns = ['POP', 'Số ca']
    fig3 = px.bar(df_chart3, x='POP', y='Số ca', color_discrete_sequence=['#10b981'])
    fig3.update_layout(**chart_theme, height=200)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="chart-card">
        <div class="chart-title">👥 4. Top KTV Tồn Ca nhiều nhất</div>
        <div class="chart-sub">Xếp hạng nhân sự có số tồn case vụ cao nhất</div>
    """, unsafe_allow_html=True)
    df_chart4 = df_raw['NHÂN SỰ'].value_counts().head(5).reset_index()
    df_chart4.columns = ['NHÂN SỰ', 'Số ca']
    fig4 = px.bar(df_chart4, x='NHÂN SỰ', y='Số ca', color_discrete_sequence=['#a855f7'])
    fig4.update_layout(**chart_theme, height=200)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 6. KHU VỰC BẢNG DỮ LIỆU & BỘ LỌC NGANG
st.markdown("### 📊 BẢNG KIỂM SOÁT DỮ LIỆU TỒN CA")

# LẤY DANH SÁCH QUẢN LÝ TỪ CỘT AN (SHEET BT)
list_mgr = sorted([str(x).strip() for x in df_raw['QUẢN LÝ'].unique() if pd.notna(x) and str(x).strip() != ''])

# THANH BỘ LỌC
f_col1, f_col2, f_col3, f_col4, f_col5, f_col6 = st.columns([2, 1.5, 1.5, 1.5, 1.5, 1.5])

with f_col1:
    search_input = st.text_input("🔍 Tìm kiếm", placeholder="Nhập Số HĐ, Block...", label_visibility="collapsed")

with f_col2:
    selected_mgr = st.selectbox("Quản lý (AN)", options=["Tất cả Quản lý"] + list_mgr, label_visibility="collapsed")

# Lọc theo Quản lý trước
if selected_mgr != "Tất cả Quản lý":
    df_sub = df_raw[df_raw['QUẢN LÝ'].astype(str) == selected_mgr]
else:
    df_sub = df_raw.copy()

with f_col3:
    list_tech = sorted([str(x).strip() for x in df_sub['NHÂN SỰ'].unique() if pd.notna(x)])
    selected_tech = st.selectbox("Nhân sự", options=["Tất cả Nhân sự"] + list_tech, label_visibility="collapsed")

with f_col4:
    list_prio = sorted([str(x).strip() for x in df_sub['Độ Ưu Tiên'].unique() if pd.notna(x)])
    selected_prio = st.selectbox("Mức SOS", options=["Tất cả Mức SOS"] + list_prio, label_visibility="collapsed")

with f_col5:
    selected_repeat = st.selectbox("CL Lặp", options=["Tất cả CL Lặp", "Chỉ lấy CL Lặp > 0", "Bằng 0"], label_visibility="collapsed")

with f_col6:
    list_block = sorted([str(x).strip() for x in df_sub['BLOCK'].unique() if pd.notna(x)])
    selected_block = st.selectbox("Block", options=["Tất cả Block"] + list_block, label_visibility="collapsed")

# LỌC DỮ LIỆU BẢNG
df_table = df_sub.copy()

if selected_tech != "Tất cả Nhân sự":
    df_table = df_table[df_table['NHÂN SỰ'].astype(str) == selected_tech]

if selected_prio != "Tất cả Mức SOS":
    df_table = df_table[df_table['Độ Ưu Tiên'].astype(str) == selected_prio]

if selected_repeat == "Chỉ lấy CL Lặp > 0":
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

# TẠO VÀ CHUẨN HÓA BẢNG ĐỂ TRÁNH LỖI DATA_EDITOR
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

# HIỂN THỊ BẢNG AN TOÀN
st.data_editor(
    df_display,
    column_config={
        "STT": st.column_config.NumberColumn("STT", width="small"),
        "SỐ HĐ": st.column_config.TextColumn("SỐ HĐ", disabled=True),
        "BLOCK": st.column_config.TextColumn("BLOCK"),
        "LẦN HẸN": st.column_config.NumberColumn("LẦN HẸN", width="small"),
        "CL LẶP": st.column_config.NumberColumn("CL LẶP", width="small"),
        "NHÂN SỰ": st.column_config.TextColumn("NHÂN SỰ"),
        "QUẢN LÝ": st.column_config.TextColumn("QUẢN LÝ (AN)"),
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

st.caption(f"Hiển thị **{len(df_display)}** / **{len(df_raw)}** ca tồn")
