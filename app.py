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

# Custom CSS Dark Theme
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

# 2. KHỞI TẠO DỮ LIỆU MẪU
@st.cache_data
def get_sample_data():
    return pd.DataFrame([
        {"STT": 1, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAB7120", "Tên đầy đủ": "TRẦN VĂN", "Thời gian tạo": "2026-09-23 16:08:45", "Tồn giờ": -7, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã PC", "Độ Ưu Tiên": "Support", "POP": "TQGP013", "Kiểm soát": "Chưa duyệt", "Ghi Chú CC": "Checklist app hifpt/ Giga", "Cột AN": "Trần Văn Nam (QL-01)"},
        {"STT": 2, "Block": "Phuong My Lam-001", "Số HĐ": "TQFD10048", "Tên đầy đủ": "DƯƠNG V", "Thời gian tạo": "2026-09-23 21:47:48", "Tồn giờ": 13, "Số lần hẹn": 3, "CL Lặp": 1, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã PC", "Độ Ưu Tiên": "Support", "POP": "TQGP013", "Kiểm soát": "Chưa duyệt", "Ghi Chú CC": "TQAAB1004 >> TQGTI.ANHPH3", "Cột AN": "Trần Văn Nam (QL-01)"},
        {"STT": 3, "Block": "Xa Yen Son-001", "Số HĐ": "TQUAA3290", "Tên đầy đủ": "PHAM THI", "Thời gian tạo": "2026-09-19 08:49:45", "Tồn giờ": -5, "Số lần hẹn": 6, "CL Lặp": 1, "Nhân sự": "TQGTI.BINHLV6", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP026", "Kiểm soát": "Chưa duyệt", "Ghi Chú CC": "Khách hãn hò >> TQGTI.BINHLV6", "Cột AN": "Phạm Quốc Hùng (QL-02)"},
        {"STT": 4, "Block": "Xa Yen Son-001", "Số HĐ": "TQUAA3853", "Tên đầy đủ": "NGÔ THỊ T", "Thời gian tạo": "2026-09-21 14:48:57", "Tồn giờ": -7, "Số lần hẹn": 5, "CL Lặp": 1, "Nhân sự": "TQGTI.BINHLV6", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP026", "Kiểm soát": "Chưa duyệt", "Ghi Chú CC": "0986265586 >> TQGTI.BINHLV6", "Cột AN": "Phạm Quốc Hùng (QL-02)"},
        {"STT": 5, "Block": "Xa Nhu Khe-001", "Số HĐ": "TQFD00989", "Tên đầy đủ": "NGUYEN H", "Thời gian tạo": "2026-09-20 21:49:01", "Tồn giờ": 65, "Số lần hẹn": 2, "CL Lặp": 1, "Nhân sự": "TQGTI.CAONB", "TTCL": "Đang XL", "Độ Ưu Tiên": "Support", "POP": "TQGP005", "Kiểm soát": "Chưa duyệt", "Ghi Chú CC": "TQFD0098 >> TQGTI.CAONB", "Cột AN": "Trần Văn Nam (QL-01)"},
        {"STT": 6, "Block": "Xa Yen Son-001", "Số HĐ": "TQFD13450", "Tên đầy đủ": "TRỊNH KẾ", "Thời gian tạo": "2026-09-23 14:45:09", "Tồn giờ": -7, "Số lần hẹn": 1, "CL Lặp": 3, "Nhân sự": "TQGTI.CUHA", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP001", "Kiểm soát": "Chưa duyệt", "Ghi Chú CC": "Hỏng điều khiển Sky", "Cột AN": "Lê Hoàng Long (QL-03)"},
        {"STT": 7, "Block": "Xa Yen Son-001", "Số HĐ": "TQAAE9218", "Tên đầy đủ": "NGUYỄN N", "Thời gian tạo": "2026-09-24 08:35:09", "Tồn giờ": -24, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.CUHA", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP002", "Kiểm soát": "Chưa duyệt", "Ghi Chú CC": "TQAAE9218 - 0968561111", "Cột AN": "Lê Hoàng Long (QL-03)"}
    ])

# Hàm chuẩn hóa và bảo vệ các cột bắt buộc trong DataFrame
def sanitize_dataframe(df):
    required_columns = {
        'Cột AN': 'Chưa phân loại',
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
    for col, default_val in required_columns.items():
        if col not in df.columns:
            df[col] = default_val
        else:
            df[col] = df[col].fillna(default_val)
    return df

# 3. SIDEBAR - BỘ LỌC DỮ LIỆU
st.sidebar.markdown("### ⚙️ Cấu Hình & Bộ Lọc")

uploaded_file = st.sidebar.file_uploader("📂 Upload File Excel mới", type=["xlsx", "xls", "csv"])

if uploaded_file is not None:
    try:
        if uploaded_file.name.endswith('.csv'):
            df_raw = pd.read_csv(uploaded_file)
        else:
            df_raw = pd.read_excel(uploaded_file)
        df_raw = sanitize_dataframe(df_raw)
        st.sidebar.success("Đã nạp file Excel thành công!")
    except Exception as e:
        st.sidebar.error(f"Lỗi đọc file Excel: {e}")
        df_raw = sanitize_dataframe(get_sample_data())
else:
    df_raw = sanitize_dataframe(get_sample_data())

# Bộ Lọc
mgr_list = [x for x in df_raw['Cột AN'].unique() if pd.notna(x) and str(x).strip() != ""]
mgr_options = ["Tất cả Quản lý"] + mgr_list
selected_mgr = st.sidebar.selectbox("👨‍💼 Chọn Quản Lý Trực Tiếp", mgr_options)

if selected_mgr != "Tất cả Quản lý":
    filtered_tech_df = df_raw[df_raw['Cột AN'] == selected_mgr]
else:
    filtered_tech_df = df_raw

tech_list = [x for x in filtered_tech_df['Nhân sự'].unique() if pd.notna(x) and str(x).strip() != ""]
tech_options = ["Tất cả"] + tech_list
selected_tech = st.sidebar.selectbox("👷 Chọn Nhân Sự", tech_options)

selected_priority = st.sidebar.selectbox("🔥 Độ Ưu Tiên / SOS", ["Tất cả", "Chỉ lấy: SOS", "Chỉ lấy: Support"])

repeat_options = ["Tất cả", "Lặp > 0", "Bằng 0", "Lặp 1 lần", "Lặp 2 lần", "Lặp ≥ 3 lần"]
selected_repeat = st.sidebar.selectbox("🔄 Checklist Lặp", repeat_options)

block_list = [x for x in df_raw['Block'].unique() if pd.notna(x) and str(x).strip() != ""]
block_options = ["Tất cả"] + block_list
selected_block = st.sidebar.selectbox("📦 Chọn Block", block_options)

search_term = st.sidebar.text_input("🔍 Tìm kiếm (Số HĐ, Ghi chú...)", "")

# 4. XỬ LÝ LỌC DỮ LIỆU
df = df_raw.copy()

if selected_mgr != "Tất cả Quản lý":
    df = df[df['Cột AN'] == selected_mgr]

if selected_tech != "Tất cả":
    df = df[df['Nhân sự'] == selected_tech]

if selected_priority == "Chỉ lấy: SOS":
    df = df[df['Độ Ưu Tiên'].astype(str).str.contains("SOS", case=False, na=False)]
elif selected_priority == "Chỉ lấy: Support":
    df = df[~df['Độ Ưu Tiên'].astype(str).str.contains("SOS", case=False, na=False)]

# Ép kiểu CL Lặp về dạng số để lọc chính xác
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
    df = df[df['Block'] == selected_block]

if search_term:
    search_lower = search_term.lower()
    df = df[
        df['Số HĐ'].astype(str).str.lower().str.contains(search_lower) |
        df['Ghi Chú CC'].astype(str).str.lower().str.contains(search_lower) |
        df['Block'].astype(str).str.lower().str.contains(search_lower)
    ]

# 5. HEADER TIÊU ĐỀ
st.markdown("<h2 style='color: #a3e635; font-weight: 800; margin-bottom: 0px;'>DASHBOARD KIỂM SOÁT CA TỒN & CHECKLIST</h2>", unsafe_allow_html=True)
st.markdown("<p style='color: #65a30d; font-size: 13px;'>Báo Cáo Kiểm Soát | Bảng dữ liệu chuẩn kiểm soát ca tồn</p>", unsafe_allow_html=True)
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

# 8. BẢNG DỮ LIỆU BÁO CÁO
st.markdown("### 📋 BẢNG DỮ LIỆU KIỂM SOÁT CA TỒN")
st.markdown(f"Hiển thị **{len(df)}** / **{len(df_raw)}** ca")

edited_df = st.data_editor(
    df,
    column_config={
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
