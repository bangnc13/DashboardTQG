import streamlit as st
import pandas as pd
import plotly.express as px

# 1. CẤU HÌNH TRANG STREAMLIT
st.set_page_config(
    page_title="Dashboard Kiểm Soát Ca Tồn & Checklist",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS Dark Theme Minimalist
st.markdown("""
    <style>
    .stApp { background-color: #090a10; color: #f1f5f9; }
    section[data-testid="stSidebar"] { background-color: #13141f; border-right: 1px solid #232538; }
    .kpi-card { background-color: #181926; border: 1px solid #232538; border-radius: 8px; padding: 16px; text-align: left; }
    .kpi-title { font-size: 11px; font-weight: 600; color: #8f93a8; text-transform: uppercase; letter-spacing: 0.5px; }
    .kpi-value { font-size: 28px; font-weight: 800; color: #ffffff; margin-top: 4px; }
    .kpi-badge { display: inline-block; padding: 2px 8px; font-size: 10px; font-weight: 700; color: #34d399; background-color: rgba(52, 211, 153, 0.1); border: 1px solid rgba(52, 211, 153, 0.3); border-radius: 12px; margin-top: 6px; }
    </style>
""", unsafe_allow_html=True)

# 2. HÀM NẠP VÀ CHUẨN HÓA DỮ LIỆU TỪ SHEET 'BT'
@st.cache_data
def load_data(file):
    try:
        # Ưu tiên đọc từ Sheet BT
        xls = pd.ExcelFile(file)
        sheet_name = 'BT' if 'BT' in xls.sheet_names else xls.sheet_names[0]
        df = pd.read_excel(xls, sheet_name=sheet_name)
        
        # Xử lý Cột AN (Quản lý/Trưởng bầy): Cột thứ 40 (Index 39)
        if 'Trưởng bầy' in df.columns:
            df['Quản lý'] = df['Trưởng bầy']
        elif len(df.columns) >= 40:
            df['Quản lý'] = df.iloc[:, 39]
        else:
            df['Quản lý'] = 'Chưa phân loại'
            
        # Chuẩn hóa các cột bắt buộc khác
        cols_check = {
            'Nhân sự': 'Chưa gán',
            'Độ Ưu Tiên': 'Support',
            'CL Lặp': 0,
            'Block': 'Khác',
            'POP': 'Khác',
            'Số HĐ': '',
            'Ghi Chú CC': '',
            'Tồn giờ': 0,
            'Kiểm soát': 'Chưa duyệt'
        }
        for col, default_val in cols_check.items():
            if col not in df.columns:
                df[col] = default_val
            else:
                df[col] = df[col].fillna(default_val)
                
        return df
    except Exception as e:
        st.error(f"Lỗi đọc dữ liệu: {e}")
        return pd.DataFrame()

# 3. SIDEBAR - BỘ LỌC LIÊN KẾT ĐỘNG
st.sidebar.markdown("### ⚙️ Cấu Hình & Bộ Lọc")

uploaded_file = st.sidebar.file_uploader("📂 Upload File Excel (CLL2.xlsx)", type=["xlsx", "xls"])

if uploaded_file is not None:
    df_raw = load_data(uploaded_file)
else:
    st.sidebar.warning("⚠️ Vui lòng upload file Excel 'CLL2.xlsx' để xem dữ liệu.")
    st.stop()

# 1️⃣ BỘ LỌC QUẢN LÝ (LẤY TỪ CỘT AN SHEET BT)
mgr_list = sorted([str(x).strip() for x in df_raw['Quản lý'].unique() if pd.notna(x) and str(x).strip() != ""])
selected_mgr = st.sidebar.selectbox("👨‍💼 Chọn Quản Lý (Cột AN - BT)", ["Tất cả Quản lý"] + mgr_list)

# 🛠️ LỌC DỮ LIỆU BƯỚC 1 THEO QUẢN LÝ
if selected_mgr != "Tất cả Quản lý":
    df_filtered_mgr = df_raw[df_raw['Quản lý'].astype(str) == selected_mgr]
else:
    df_filtered_mgr = df_raw.copy()

# 2️⃣ BỘ LỌC NHÂN SỰ (Chỉ hiển thị các bạn thuộc Quản lý đã chọn)
tech_list = sorted([str(x).strip() for x in df_filtered_mgr['Nhân sự'].unique() if pd.notna(x) and str(x).strip() != ""])
selected_tech = st.sidebar.selectbox("👷 Chọn Nhân Sự", ["Tất cả"] + tech_list)

# 3️⃣ BỘ LỌC ĐỘ ƯU TIÊN (Chỉ chứa giá trị có trong Quản lý đã chọn)
prio_list = sorted([str(x).strip() for x in df_filtered_mgr['Độ Ưu Tiên'].unique() if pd.notna(x) and str(x).strip() != ""])
selected_priority = st.sidebar.selectbox("🔥 Độ Ưu Tiên / SOS", ["Tất cả"] + prio_list)

# 4️⃣ BỘ LỌC CHECKLIST LẶP
repeat_options = ["Tất cả", "Lặp > 0", "Bằng 0", "Lặp 1 lần", "Lặp 2 lần", "Lặp ≥ 3 lần"]
selected_repeat = st.sidebar.selectbox("🔄 Checklist Lặp", repeat_options)

# 5️⃣ BỘ LỌC BLOCK (Chỉ hiển thị Block thuộc Quản lý đã chọn)
block_list = sorted([str(x).strip() for x in df_filtered_mgr['Block'].unique() if pd.notna(x) and str(x).strip() != ""])
selected_block = st.sidebar.selectbox("📦 Chọn Block", ["Tất cả"] + block_list)

search_term = st.sidebar.text_input("🔍 Tìm kiếm (Số HĐ, Ghi chú...)", "")

# 4. ÁP DỤNG TẤT CẢ BỘ LỌC VÀO DATAFRAME
df = df_filtered_mgr.copy()

if selected_tech != "Tất cả":
    df = df[df['Nhân sự'].astype(str) == selected_tech]

if selected_priority != "Tất cả":
    df = df[df['Độ Ưu Tiên'].astype(str) == selected_priority]

df['CL Lặp'] = pd.to_numeric(df['CL Lặp'], errors='coerce').fillna(0)
if selected_repeat == "Lặp > 0":
    df = df[df['CL Lặp'] > 0]
elif selected_repeat == "Bằng 0":
    df = df[df['CL Lặp'] == 0]
elif selected_repeat == "Lặp 1 lần":
    df = df[df['CL Lặp'] == 1]
elif selected_repeat == "Lặp 2 lần":
    df = df[df['CL Lặp'] == 2]
elif selected_repeat == "Lặp ≥ 3 lần":
    df = df[df['CL Lặp'] >= 3]

if selected_block != "Tất cả":
    df = df[df['Block'].astype(str) == selected_block]

if search_term:
    search_lower = search_term.lower()
    df = df[
        df['Số HĐ'].astype(str).str.lower().str.contains(search_lower) |
        df['Ghi Chú CC'].astype(str).str.lower().str.contains(search_lower) |
        df['Block'].astype(str).str.lower().str.contains(search_lower)
    ]

# 5. HEADER DASHBOARD
st.markdown("<h2 style='color: #a3e635; font-weight: 800; margin-bottom: 0px;'>DASHBOARD KIỂM SOÁT CA TỒN & CHECKLIST</h2>", unsafe_allow_html=True)
st.markdown(f"<p style='color: #65a30d; font-size: 13px;'>Đang xem dữ liệu của: <b>{selected_mgr}</b></p>", unsafe_allow_html=True)
st.markdown("---")

# 6. HIỂN THỊ KPI CARDS
total_cases = len(df)
sos_cases = len(df[df['Độ Ưu Tiên'].astype(str).str.contains("SOS", na=False)])
sos_pct = round((sos_cases / total_cases * 100), 1) if total_cases > 0 else 0

repeat_cases = len(df[df['CL Lặp'] > 0])

df['Tồn giờ'] = pd.to_numeric(df['Tồn giờ'], errors='coerce').fillna(0)
overdue_cases = len(df[df['Tồn giờ'] >= 24])
overdue_pct = round((overdue_cases / total_cases * 100), 1) if total_cases > 0 else 0

kpi_col1, kpi_col2, kpi_col3, kpi_col4, kpi_col5, kpi_col6 = st.columns(6)

with kpi_col1:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">TỔNG CA TỒN</div><div class="kpi-value">{total_cases}</div></div>""", unsafe_allow_html=True)

with kpi_col2:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">MỨC SOS</div><div class="kpi-value">{sos_cases}</div><div class="kpi-badge">↑ {sos_pct}%</div></div>""", unsafe_allow_html=True)

with kpi_col3:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">CLL ĐANG TỒN</div><div class="kpi-value">{repeat_cases}</div><div class="kpi-badge">↑ {repeat_cases} ca</div></div>""", unsafe_allow_html=True)

with kpi_col4:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">TỒN GIỜ ≥ 24H</div><div class="kpi-value">{overdue_cases}</div><div class="kpi-badge">↑ {overdue_pct}%</div></div>""", unsafe_allow_html=True)

with kpi_col5:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">ĐANG XỬ LÝ</div><div class="kpi-value">{total_cases}</div></div>""", unsafe_allow_html=True)

with kpi_col6:
    st.markdown(f"""<div class="kpi-card"><div class="kpi-title">CẦN ĐÁNH GIÁ</div><div class="kpi-value">0</div></div>""", unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# 7. VẼ 4 BIỂU ĐỒ CHARTS
chart_theme = {
    'paper_bgcolor': 'rgba(0,0,0,0)',
    'plot_bgcolor': 'rgba(0,0,0,0)',
    'font': {'color': '#8f93a8', 'size': 11},
    'margin': dict(l=20, r=20, t=30, b=20)
}

c1, c2 = st.columns(2)

with c1:
    st.markdown("##### 1. Tỉ trọng Checklist Lặp Theo Mức Độ SOS")
    if not df.empty:
        repeat_sos = df.groupby(['CL Lặp', 'Độ Ưu Tiên']).size().reset_index(name='Số ca')
        fig1 = px.bar(
            repeat_sos, x='CL Lặp', y='Số ca', color='Độ Ưu Tiên', barmode='group',
            color_discrete_map={'SOS': '#f43f5e', 'Support': '#3b82f6'}
        )
        fig1.update_layout(**chart_theme, height=260)
        st.plotly_chart(fig1, use_container_width=True)
    else:
        st.info("Không có dữ liệu phù hợp")

with c2:
    st.markdown("##### 2. Top Block Tồn Ca Nhiều Nhất")
    if not df.empty:
        block_counts = df['Block'].value_counts().head(7).reset_index()
        block_counts.columns = ['Block', 'Số ca']
        fig2 = px.bar(block_counts, y='Block', x='Số ca', orientation='h', color_discrete_sequence=['#38bdf8'])
        fig2.update_layout(**chart_theme, height=260, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)
    else:
        st.info("Không có dữ liệu phù hợp")

c3, c4 = st.columns(2)

with c3:
    st.markdown("##### 3. Tồn Theo POP")
    if not df.empty:
        pop_counts = df['POP'].value_counts().head(6).reset_index()
        pop_counts.columns = ['POP', 'Số ca']
        fig3 = px.bar(pop_counts, x='POP', y='Số ca', color_discrete_sequence=['#34d399'])
        fig3.update_layout(**chart_theme, height=260)
        st.plotly_chart(fig3, use_container_width=True)
    else:
        st.info("Không có dữ liệu phù hợp")

with c4:
    st.markdown("##### 4. Top KTV Tồn Ca Nhiều Nhất")
    if not df.empty:
        tech_counts = df['Nhân sự'].value_counts().head(6).reset_index()
        tech_counts.columns = ['Nhân sự', 'Số ca']
        fig4 = px.bar(tech_counts, x='Nhân sự', y='Số ca', color_discrete_sequence=['#a855f7'])
        fig4.update_layout(**chart_theme, height=260)
        st.plotly_chart(fig4, use_container_width=True)
    else:
        st.info("Không có dữ liệu phù hợp")

# 8. BẢNG DỮ LIỆU HIỂN THỊ CÁC CỘT THEO YÊU CẦU
st.markdown("### 📋 BẢNG DỮ LIỆU KIỂM SOÁT CA TỒN")
st.markdown(f"Hiển thị **{len(df)}** / **{len(df_raw)}** ca")

# Hiển thị các cột thông tin trọng tâm
display_cols = ['Số HĐ', 'Quản lý', 'Nhân sự', 'Độ Ưu Tiên', 'CL Lặp', 'Block', 'Tồn giờ', 'POP', 'Kiểm soát', 'Ghi Chú CC']
available_cols = [c for c in display_cols if c in df.columns]

edited_df = st.data_editor(
    df[available_cols],
    column_config={
        "Quản lý": st.column_config.TextColumn("Trưởng bầy (Cột AN)", disabled=True),
        "Kiểm soát": st.column_config.SelectboxColumn(
            "Kiểm Soát",
            options=["Chưa duyệt", "✅ Đã xử lý", "🚨 Cảnh báo"],
            required=True,
        ),
        "Số HĐ": st.column_config.TextColumn("Số HĐ", disabled=True),
        "Tồn giờ": st.column_config.NumberColumn("Tồn giờ (h)", format="%d h"),
    },
    hide_index=True,
    use_container_width=True
)

st.download_button(
    label="📥 Export Báo Cáo Excel",
    data=edited_df.to_csv(index=False).encode('utf-8-sig'),
    file_name='Bao_Cao_Kiem_Soat_Ca_Ton.csv',
    mime='text/csv'
)
