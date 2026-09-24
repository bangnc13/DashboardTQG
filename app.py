import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CẤU HÌNH TRANG STREAMLIT
st.set_page_config(
    page_title="DASHBOARD KIỂM SOÁT CA TỒN & CHECKLIST",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. CSS TINH CHỈNH GIAO DIỆN CHUẨN MẪU 100%
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif; }
    
    /* Ẩn bớt các element dư thừa của Streamlit */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    .main .block-container {
        max-width: 96% !important;
        padding: 0.8rem 1rem !important;
    }

    /* Nền trang xám rất nhạt */
    .stApp { background-color: #f8fafc; color: #1e293b; }
    
    /* Header chính */
    .main-header {
        display: flex;
        align-items: center;
        justify-content: space-between;
        background-color: #ffffff;
        padding: 8px 16px;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        box-shadow: 0 1px 2px rgba(0,0,0,0.03);
        margin-bottom: 12px;
    }
    .header-left { display: flex; align-items: center; gap: 10px; }
    .header-icon {
        background-color: #65a30d;
        color: white;
        border-radius: 50%;
        width: 32px;
        height: 32px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 16px;
    }
    .header-title { font-size: 17px; font-weight: 800; color: #0f172a; }
    .badge-sub {
        background-color: #ecfccb;
        color: #4d7c0f;
        font-size: 11px;
        font-weight: 700;
        padding: 2px 8px;
        border-radius: 12px;
        border: 1px solid #bef264;
    }
    .header-desc { font-size: 11px; color: #64748b; margin-top: 1px; }

    /* Top KPI Cards */
    .kpi-container { display: flex; gap: 8px; margin-bottom: 12px; }
    .kpi-card {
        flex: 1;
        background-color: #ffffff;
        border-radius: 8px;
        padding: 8px 6px;
        text-align: center;
        box-shadow: 0 1px 2px rgba(0,0,0,0.04);
        background-clip: padding-box;
    }
    .kpi-blue { border-top: 3.5px solid #3b82f6; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; }
    .kpi-pink { border-top: 3.5px solid #f43f5e; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; }
    .kpi-orange { border-top: 3.5px solid #f97316; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; }
    .kpi-purple { border-top: 3.5px solid #a855f7; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; }
    .kpi-cyan { border-top: 3.5px solid #06b6d4; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; }
    .kpi-green { border-top: 3.5px solid #10b981; border-left: 1px solid #e2e8f0; border-right: 1px solid #e2e8f0; border-bottom: 1px solid #e2e8f0; }

    .kpi-label { font-size: 10.5px; font-weight: 600; color: #475569; white-space: nowrap; }
    
    /* Biểu đồ Cards */
    .chart-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        padding: 12px 14px;
        margin-bottom: 12px;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
    }
    .chart-title { font-size: 13px; font-weight: 700; color: #0f172a; display: flex; align-items: center; gap: 6px; }
    .chart-sub { font-size: 10px; color: #94a3b8; margin-bottom: 4px; }

    /* Bảng dữ liệu Khung xanh lá nhạt */
    .table-wrapper {
        background-color: #f7fee7;
        border: 1.5px solid #bef264;
        border-radius: 12px;
        padding: 12px 16px;
        margin-top: 10px;
    }
    .table-header-title {
        font-size: 14px;
        font-weight: 800;
        color: #1e293b;
        display: flex;
        align-items: center;
        gap: 6px;
    }
    .table-header-sub { font-size: 11px; color: #65a30d; margin-bottom: 8px; }

    /* Custom CSS Styling cho Streamlit Inputs */
    div[data-baseweb="select"] > div {
        background-color: #ffffff !important;
        border-radius: 6px !important;
        border: 1px solid #cbd5e1 !important;
        font-size: 12px !important;
    }
    </style>
""", unsafe_allow_html=True)

# 3. HÀM NẠP VÀ DỌN DẸP DỮ LIỆU
@st.cache_data
def load_excel_data(file):
    try:
        xls = pd.ExcelFile(file)
        sheet_name = 'BT' if 'BT' in xls.sheet_names else xls.sheet_names[0]
        df = pd.read_excel(xls, sheet_name=sheet_name)

        # Cột Quản lý từ Cột AN (Index 39)
        if 'Trưởng bầy' in df.columns:
            df['QUẢN LÝ'] = df['Trưởng bầy']
        elif len(df.columns) >= 40:
            df['QUẢN LÝ'] = df.iloc[:, 39]
        else:
            df['QUẢN LÝ'] = 'Chưa phân loại'

        # Đổi tên cột chuẩn
        rename_map = {
            'Số HĐ': 'SỐ HĐ',
            'Block': 'BLOCK',
            'Số lần hẹn': 'LẦN HẸN',
            'CL Lặp': 'CL LẶP',
            'Nhân sự': 'NHÂN SỰ',
            'Tồn giờ': 'TỒN GIỜ',
            'Kiểm soát': 'KIỂM SOÁT',
            'Ghi Chú CC': 'GHI CHÚ CSKH'
        }
        df = df.rename(columns=rename_map)

        # Bỏ trùng tên cột
        df = df.loc[:, ~df.columns.duplicated()]

        # Mặc định dữ liệu trống
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
        st.error(f"Lỗi đọc file Excel: {e}")
        return pd.DataFrame()

# 4. HEADER TRÊN CÙNG
h_col1, h_col2 = st.columns([3.5, 1])

with h_col1:
    st.markdown("""
    <div class="main-header">
        <div class="header-left">
            <div class="header-icon">📑</div>
            <div>
                <div style="display: flex; align-items: center; gap: 8px;">
                    <span class="header-title">DASHBOARD KIỂM SOÁT CA TỒN & CHECKLIST</span>
                    <span class="badge-sub">Báo Cáo Kiểm Soát</span>
                </div>
                <div class="header-desc">Khớp chính xác: Số HĐ, Khách Hàng, Block, Lần Hẹn, CL Lặp, Nhân Sự, Quản Lý, Tồn Giờ, Kiểm Soát</div>
            </div>
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
        st.info("👆 Hãy bấm Import File Excel để xem dữ liệu.")
        st.stop()

# 5. KHU VỰC TOP KPI
total_cases = len(df_raw)
sos_cases = len(df_raw[df_raw['Độ Ưu Tiên'].astype(str).str.contains('SOS', na=False)])
repeat_cases = len(df_raw[pd.to_numeric(df_raw['CL LẶP'], errors='coerce').fillna(0) > 0])

st.markdown(f"""
<div class="kpi-container">
    <div class="kpi-card kpi-blue"><div class="kpi-label">Tổng hợp hợp đồng tồn</div></div>
    <div class="kpi-card kpi-pink"><div class="kpi-label">Số ca báo SOS</div></div>
    <div class="kpi-card kpi-orange"><div class="kpi-label">Tổng lượt lặp (Lặp > 0)</div></div>
    <div class="kpi-card kpi-purple"><div class="kpi-label">Ca quá hạn 1 ngày</div></div>
    <div class="kpi-card kpi-cyan"><div class="kpi-label">Trạng thái Đang XL</div></div>
    <div class="kpi-card kpi-green"><div class="kpi-label">Chưa ghi nhận đánh giá</div></div>
</div>
""", unsafe_allow_html=True)

# 6. KHU VỰC 4 BIỂU ĐỒ (CHARTS MẦU CHUẨN MẪU)
chart_style = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'color': '#475569', 'size': 10},
    'margin': dict(l=10, r=10, t=10, b=10)
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
    fig1.update_layout(**chart_style, height=190, showlegend=True, legend=dict(orientation="h", y=1.1, x=0.2))
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
    fig2.update_layout(**chart_style, height=190, yaxis={'categoryorder':'total ascending'})
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
    fig3.update_layout(**chart_style, height=190)
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
    fig4.update_layout(**chart_style, height=190)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

# 7. KHU VỰC BẢNG DỮ LIỆU TỒN CA (VIỀN XANH LÁ MẠ CỰC CHUẨN)
st.markdown("""
<div style="background-color: #f7fee7; border: 1.5px solid #bef264; border-radius: 12px; padding: 14px 16px;">
    <div class="table-header-title">📊 BẢNG KIỂM SOÁT DỮ LIỆU TỒN CA</div>
    <div class="table-header-sub">Xem, tìm kiếm, lọc và cập nhật trực tiếp trạng thái Kiểm Soát</div>
""", unsafe_allow_html=True)

list_mgr = sorted([str(x).strip() for x in df_raw['QUẢN LÝ'].unique() if pd.notna(x) and str(x).strip() != ''])

# BỘ LỌC TẬP TRUNG DÒNG NGANG
f1, f2, f3, f4, f5, f6 = st.columns([2, 1.5, 1.5, 1.5, 1.5, 1.5])

with f1:
    search_input = st.text_input("Search", placeholder="🔍 Tìm Số HĐ, Tên KH, Ghi...", label_visibility="collapsed")
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

# TẠO DATAFRAME RÕ RÀNG
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

# DATA EDITOR VỚI COLUMN CONFIG TẠO ĐÚNG ĐỊNH DẠNG MẮT NHÌN
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

st.markdown(f"<div style='font-size: 11px; color: #4d7c0f; margin-top: 6px;'>Hiển thị <b>{len(df_display)}</b> / <b>{len(df_raw)}</b> ca tồn</div></div>", unsafe_allow_html=True)
