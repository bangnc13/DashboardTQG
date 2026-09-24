import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Cấu hình trang Streamlit
st.set_page_config(
    page_title="Dashboard Kiểm Soát Ca Tồn & Checklist",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS tùy chỉnh
st.markdown("""
<style>
    .main-header { font-size: 24px; font-weight: bold; color: #30411d; }
    .sub-header { font-size: 13px; color: #5c7b35; }
</style>
""", unsafe_allow_html=True)

# 2. Dữ liệu mẫu khởi tạo
@st.cache_data
def load_sample_data():
    return pd.DataFrame([
        { "STT": 1, "Số HĐ": "TQAAE4800", "Block": "Phuong My Lam-001", "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.ANHPH3", "Quản lý": "HUONGTT33", "Tồn giờ": 26, "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CSKH": "TQAAE4800 - 0326192565 - Báo hỏng dịch vụ", "Độ Ưu Tiên": "Support", "POP": "Phuong My Lam-001" },
        { "STT": 2, "Số HĐ": "TQAAE5855", "Block": "Phuong My Lam-001", "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.ANHPH3", "Quản lý": "HUONGTT33", "Tồn giờ": 26, "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CSKH": "TQAAE5855 - 0987682243 - Báo hỏng dịch vụ", "Độ Ưu Tiên": "Support", "POP": "Phuong My Lam-001" },
        { "STT": 3, "Số HĐ": "TQAAE4058", "Block": "Xa Chiem Hoa-001", "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.HUNGDQ5", "Quản lý": "HUONGTT33", "Tồn giờ": 7, "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CSKH": "TQAAE4058 - 0978063651 - Báo hỏng dịch vụ", "Độ Ưu Tiên": "Support", "POP": "Xa Chiem Hoa-001" },
        { "STT": 4, "Số HĐ": "TQFD13450", "Block": "Phuong An Tuong-001", "Số lần hẹn": 1, "CL Lặp": 3, "Nhân sự": "TQGTI.CUHA", "Quản lý": "HUONGTT33", "Tồn giờ": 23, "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CSKH": "Hỏng điều khiển", "Độ Ưu Tiên": "Support", "POP": "Phuong An Tuong-001" },
        { "STT": 5, "Số HĐ": "TQFD20613", "Block": "Phuong My Lam-001", "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.QUANDM2", "Quản lý": "HUONGTT33", "Tồn giờ": 18, "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CSKH": "TQFD20613 - 0385365241 - Mất kết nối", "Độ Ưu Tiên": "Support", "POP": "Phuong My Lam-001" },
        { "STT": 6, "Số HĐ": "TQAAE7704", "Block": "Phuong My Lam-001", "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.ANHPH3", "Quản lý": "HUONGTT33", "Tồn giờ": 24, "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CSKH": "TQAAE7704 - Báo hỏng dịch vụ", "Độ Ưu Tiên": "SOS", "POP": "Phuong My Lam-001" },
        { "STT": 7, "Số HĐ": "TQAAE9218", "Block": "Phuong An Tuong-001", "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.CUHA", "Quản lý": "HUONGTT33", "Tồn giờ": 5, "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CSKH": "TQAAE9218 - Lắp đường truyền quốc tế", "Độ Ưu Tiên": "Support", "POP": "Phuong An Tuong-001" }
    ])

# Hàm chuẩn hóa dữ liệu upload để tránh lỗi KeyError
def normalize_dataframe(df):
    # Loại bỏ khoảng trắng ở tên cột
    df.columns = [str(col).strip() for col in df.columns]
    
    # Bảng ánh xạ các tên cột hay gặp về cột chuẩn
    column_mapping = {
        'Cột AN': 'Quản lý', 'Quan ly': 'Quản lý', 'QUẢN LÝ': 'Quản lý', 'QuanLy': 'Quản lý',
        'So HD': 'Số HĐ', 'SỐ HĐ': 'Số HĐ', 'Contract': 'Số HĐ',
        'Nhan su': 'Nhân sự', 'NHÂN SỰ': 'Nhân sự', 'KTV': 'Nhân sự',
        'So lan hen': 'Số lần hẹn', 'Số Lần Hẹn': 'Số lần hẹn', 'LẦN HẸN': 'Số lần hẹn',
        'CL Lap': 'CL Lặp', 'CL LẶP': 'CL Lặp', 'Checklist Lap': 'CL Lặp',
        'Ton gio': 'Tồn giờ', 'TỒN GIỜ': 'Tồn giờ',
        'Kiem soat': 'Kiểm soát', 'KIỂM SOÁT': 'Kiểm soát',
        'Ghi chu': 'Ghi Chú CSKH', 'Ghi chú': 'Ghi Chú CSKH', 'GHI CHÚ CSKH': 'Ghi Chú CSKH',
        'Do uu tien': 'Độ Ưu Tiên', 'ĐỘ ƯU TIÊN': 'Độ Ưu Tiên'
    }
    df = df.rename(columns=column_mapping)
    
    # Danh sách các cột bắt buộc phải có
    required_defaults = {
        "STT": range(1, len(df) + 1),
        "Số HĐ": "",
        "Block": "Khác",
        "Số lần hẹn": 1,
        "CL Lặp": 0,
        "Nhân sự": "Chưa phân công",
        "Quản lý": "Chưa phân công",
        "Tồn giờ": 0,
        "Kiểm soát": "Chưa Đánh Giá",
        "Ghi Chú CSKH": "",
        "Độ Ưu Tiên": "Support",
        "POP": "Chưa xác định"
    }
    
    for col, default_val in required_defaults.items():
        if col not in df.columns:
            df[col] = default_val
            
    # Ép kiểu dữ liệu an toàn
    df['CL Lặp'] = pd.to_numeric(df['CL Lặp'], errors='coerce').fillna(0).astype(int)
    df['Số lần hẹn'] = pd.to_numeric(df['Số lần hẹn'], errors='coerce').fillna(1).astype(int)
    df['Tồn giờ'] = pd.to_numeric(df['Tồn giờ'], errors='coerce').fillna(0).astype(int)
    df['Quản lý'] = df['Quản lý'].fillna('Chưa phân công').astype(str)
    df['Nhân sự'] = df['Nhân sự'].fillna('Chưa phân công').astype(str)
    
    return df

# Khởi tạo session state
if "df" not in st.session_state:
    st.session_state.df = load_sample_data()

# 3. Sidebar: Upload & Lọc
st.sidebar.title("⚙️ Cấu Hình & Bộ Lọc")

uploaded_file = st.sidebar.file_uploader("📥 Tải lên File Excel mới", type=["xlsx", "xls", "csv"])
if uploaded_file:
    try:
        if uploaded_file.name.endswith('.csv'):
            uploaded_df = pd.read_csv(uploaded_file)
        else:
            uploaded_df = pd.read_excel(uploaded_file)
        
        st.session_state.df = normalize_dataframe(uploaded_df)
        st.sidebar.success("Đã nạp file Excel thành công!")
    except Exception as e:
        st.sidebar.error(f"Lỗi đọc file: {e}")

df_raw = st.session_state.df

# Lọc Quản lý
list_quan_ly = ["Tất cả"] + sorted([x for x in df_raw["Quản lý"].unique() if x])
sel_quan_ly = st.sidebar.selectbox("👨‍💼 Chọn Quản Lý Trực Tiếp", list_quan_ly, index=0)

# Lọc Nhân sự
list_nhan_su = ["Tất cả"] + sorted([x for x in df_raw["Nhân sự"].unique() if x])
sel_nhan_su = st.sidebar.selectbox("👷 Chọn Nhân Sự", list_nhan_su, index=0)

# Lọc Mức Ưu Tiên
list_uu_tien = ["Tất cả", "SOS", "Support"]
sel_uu_tien = st.sidebar.selectbox("🚨 Độ Ưu Tiên / SOS", list_uu_tien, index=0)

# Lọc CL Lặp
list_lap = ["Tất cả", "Chỉ lấy Lặp > 0", "Bằng 0 (= 0)"]
sel_lap = st.sidebar.selectbox("🔄 Checklist Lặp", list_lap, index=0)

# Lọc Block
list_block = ["Tất cả"] + sorted([x for x in df_raw["Block"].astype(str).unique() if x])
sel_block = st.sidebar.selectbox("🏘️ Chọn Block", list_block, index=0)

# Tìm kiếm
search_term = st.sidebar.text_input("🔍 Tìm kiếm (Số HĐ, Ghi chú...)", "")

# Xử lý lọc dữ liệu
df_filtered = df_raw.copy()

if sel_quan_ly != "Tất cả":
    df_filtered = df_filtered[df_filtered["Quản lý"] == sel_quan_ly]

if sel_nhan_su != "Tất cả":
    df_filtered = df_filtered[df_filtered["Nhân sự"] == sel_nhan_su]

if sel_uu_tien != "Tất cả":
    df_filtered = df_filtered[df_filtered["Độ Ưu Tiên"].astype(str).str.contains(sel_uu_tien, case=False, na=False)]

if sel_lap == "Chỉ lấy Lặp > 0":
    df_filtered = df_filtered[df_filtered["CL Lặp"] > 0]
elif sel_lap == "Bằng 0 (= 0)":
    df_filtered = df_filtered[df_filtered["CL Lặp"] == 0]

if sel_block != "Tất cả":
    df_filtered = df_filtered[df_filtered["Block"] == sel_block]

if search_term:
    search_mask = (
        df_filtered["Số HĐ"].astype(str).str.contains(search_term, case=False, na=False) |
        df_filtered["Ghi Chú CSKH"].astype(str).str.contains(search_term, case=False, na=False)
    )
    df_filtered = df_filtered[search_mask]

# 4. Header
st.markdown('<div class="main-header">DASHBOARD KIỂM SOÁT CA TỒN & CHECKLIST</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Báo Cáo Kiểm Soát | Bảng dữ liệu chuẩn 8 cột kiểm soát ca tồn</div><br>', unsafe_allow_html=True)

# 5. Cards KPI
kpi1, kpi2, kpi3, kpi4, kpi5, kpi6 = st.columns(6)

total_cases = len(df_filtered)
sos_cases = len(df_filtered[df_filtered["Độ Ưu Tiên"].astype(str).str.contains("SOS", case=False, na=False)])
repeat_sum = df_filtered["CL Lặp"].sum()
overdue_cases = len(df_filtered[df_filtered["Tồn giờ"] >= 24])
unchecked_cases = len(df_filtered[df_filtered["Kiểm soát"].isin(["Chưa Đánh Giá", "", None])])

kpi1.metric("TỔNG CA TỒN", total_cases)
kpi2.metric("MỨC SOS", sos_cases, f"{(sos_cases/total_cases*100):.1f}%" if total_cases else "0%")
kpi3.metric("CLL ĐANG TỒN", repeat_sum, f"{len(df_filtered[df_filtered['CL Lặp'] > 0])} ca")
kpi4.metric("TỒN GIỜ ≥ 24H", overdue_cases, f"{(overdue_cases/total_cases*100):.1f}%" if total_cases else "0%")
kpi5.metric("ĐANG XỬ LÝ", total_cases - unchecked_cases)
kpi6.metric("CẦN ĐÁNH GIÁ", unchecked_cases)

st.markdown("---")

# 6. Biểu đồ Plotly
col_c1, col_c2 = st.columns(2)

with col_c1:
    st.subheader("1. Tỉ trọng Checklist Lặp Theo Mức Độ SOS")
    if not df_filtered.empty:
        df_chart1 = df_filtered.groupby(['CL Lặp', 'Độ Ưu Tiên']).size().reset_index(name='Số lượng')
        fig1 = px.bar(df_chart1, x="CL Lặp", y="Số lượng", color="Độ Ưu Tiên", barmode="group",
                     color_discrete_map={"SOS": "#f43f5e", "Support": "#3b82f6"})
        fig1.update_layout(height=280, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig1, use_container_width=True)

with col_c2:
    st.subheader("2. Top Block Tồn Ca Nhiều Nhất")
    if not df_filtered.empty:
        df_chart2 = df_filtered['Block'].value_counts().reset_index()
        df_chart2.columns = ['Block', 'Số ca']
        fig2 = px.bar(df_chart2.head(10), y="Block", x="Số ca", orientation='h', color_discrete_sequence=['#0284c7'])
        fig2.update_layout(height=280, margin=dict(l=20, r=20, t=20, b=20), yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig2, use_container_width=True)

col_c3, col_c4 = st.columns(2)

with col_c3:
    st.subheader("3. Tồn Theo POP")
    if not df_filtered.empty:
        df_chart3 = df_filtered['POP'].value_counts().reset_index()
        df_chart3.columns = ['POP', 'Số ca']
        fig3 = px.bar(df_chart3.head(10), x="POP", y="Số ca", color_discrete_sequence=['#10b981'])
        fig3.update_layout(height=280, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig3, use_container_width=True)

with col_c4:
    st.subheader("4. Top KTV Tồn Ca Nhiều Nhất")
    if not df_filtered.empty:
        df_chart4 = df_filtered['Nhân sự'].value_counts().reset_index()
        df_chart4.columns = ['Nhân sự', 'Số ca']
        fig4 = px.bar(df_chart4.head(10), x="Nhân sự", y="Số ca", color_discrete_sequence=['#a855f7'])
        fig4.update_layout(height=280, margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")

# 7. Bảng Dữ Liệu Chỉnh Sửa Dạng Table
st.subheader("📋 BẢNG KIỂM SOÁT DỮ LIỆU TỒN CA")

display_columns = ["STT", "Số HĐ", "Block", "Số lần hẹn", "CL Lặp", "Nhân sự", "Quản lý", "Tồn giờ", "Kiểm soát", "Ghi Chú CSKH"]
df_display = df_filtered[[c for c in display_columns if c in df_filtered.columns]]

edited_df = st.data_editor(
    df_display,
    column_config={
        "STT": st.column_config.NumberColumn("STT", width="small"),
        "Số HĐ": st.column_config.TextColumn("SỐ HĐ", width="medium"),
        "Block": st.column_config.TextColumn("BLOCK", width="medium"),
        "Số lần hẹn": st.column_config.NumberColumn("LẦN HẸN", width="small"),
        "CL Lặp": st.column_config.NumberColumn("CL LẶP", width="small"),
        "Nhân sự": st.column_config.TextColumn("NHÂN SỰ", width="medium"),
        "Quản lý": st.column_config.TextColumn("QUẢN LÝ", width="medium"),
        "Tồn giờ": st.column_config.NumberColumn("TỒN GIỜ", width="small"),
        "Kiểm soát": st.column_config.SelectboxColumn(
            "KIỂM SOÁT",
            options=["Chưa Đánh Giá", "✅ Đã tiếp nhận", "⚠️ Cần hỗ trợ"],
            required=True,
            width="medium"
        ),
        "Ghi Chú CSKH": st.column_config.TextColumn("GHI CHÚ CSKH", width="large"),
    },
    disabled=["STT", "Số HĐ", "Block", "Số lần hẹn", "CL Lặp", "Nhân sự", "Quản lý", "Tồn giờ", "Ghi Chú CSKH"],
    hide_index=True,
    use_container_width=True
)

# Export Excel
@st.cache_data
def convert_df_to_excel(df):
    from io import BytesIO
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='KiemSoatCaTon')
    return output.getvalue()

st.download_button(
    label="📥 Export Bảng Dữ Liệu Xuất Excel",
    data=convert_df_to_excel(edited_df),
    file_name='Bao_Cao_Kiem_Soat_Ca_Ton.xlsx',
    mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
)
