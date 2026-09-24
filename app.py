import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime

# ==========================================
# 1. CẤU HÌNH TRANG STREAMLIT
# ==========================================
st.set_page_config(
    page_title="Dashboard Kiểm Soát Ca Tồn & Checklist",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS giao diện Pale Olive & Modern UI
st.markdown("""
<style>
    /* Theme màu Pale Olive */
    :root {
        --olive-bg: #f7f9f2;
        --olive-border: #d4e1bd;
        --olive-header: #465e28;
        --olive-accent: #759948;
    }
    
    .stApp {
        background-color: #f8fafc;
    }
    
    /* Style KPI Cards */
    .kpi-card {
        background-color: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 16px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        position: relative;
        overflow: hidden;
    }
    .kpi-title {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        color: #64748b;
        letter-spacing: 0.05em;
    }
    .kpi-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: #0f172a;
        margin-top: 4px;
    }
    .kpi-badge {
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 12px;
        font-weight: 600;
        float: right;
    }
    .kpi-sub {
        font-size: 0.75rem;
        color: #94a3b8;
        margin-top: 4px;
    }
    .kpi-bar {
        position: absolute;
        bottom: 0;
        left: 0;
        right: 0;
        height: 4px;
    }

    /* Banner Olive */
    .olive-banner {
        background-color: #f7f9f2;
        border-left: 4px solid #759948;
        border-radius: 8px;
        padding: 12px 16px;
        margin-bottom: 20px;
        color: #30411d;
    }
    .olive-tag {
        background-color: #e9efdc;
        color: #30411d;
        padding: 2px 8px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-weight: 600;
        margin-right: 6px;
        display: inline-block;
        margin-top: 4px;
    }
</style>
""", unsafe_allow_html=True)

# ==========================================
# 2. DỮ LIỆU MẪU (SAMPLE DATASET)
# ==========================================
@st.cache_data
def get_sample_data():
    data = [
        { "STT": 1, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAB7120", "Tên đầy đủ": "TRẦN VĂN", "Thời gian tạo": "2026-09-23 16:08:45", "Tồn giờ": -7, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã PC", "Độ Ưu Tiên": "Support", "POP": "TQGP013", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "Checklist app hifpt/ Giga", "Cột AN": "Trần Văn Nam (QL-01)" },
        { "STT": 2, "Block": "Phuong My Lam-001", "Số HĐ": "TQFD10048", "Tên đầy đủ": "DƯƠNG V", "Thời gian tạo": "2026-09-23 21:47:48", "Tồn giờ": 13, "Số lần hẹn": 3, "CL Lặp": 1, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã PC", "Độ Ưu Tiên": "Support", "POP": "TQGP013", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAB1004 >> TQGTI.ANHPH3", "Cột AN": "Trần Văn Nam (QL-01)" },
        { "STT": 3, "Block": "Xa Yen Son-001", "Số HĐ": "TQUAA3290", "Tên đầy đủ": "PHAM THI", "Thời gian tạo": "2026-09-19 08:49:45", "Tồn giờ": -5, "Số lần hẹn": 6, "CL Lặp": 1, "Nhân sự": "TQGTI.BINHLV6", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP026", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "Khách hãn hò >> TQGTI.BINHLV6", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
        { "STT": 4, "Block": "Xa Yen Son-001", "Số HĐ": "TQUAA3853", "Tên đầy đủ": "NGÔ THỊ T", "Thời gian tạo": "2026-09-21 14:48:57", "Tồn giờ": -7, "Số lần hẹn": 5, "CL Lặp": 1, "Nhân sự": "TQGTI.BINHLV6", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP026", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "0986265586 >> TQGTI.BINHLV6", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
        { "STT": 5, "Block": "Xa Nhu Khe-001", "Số HĐ": "TQFD00989", "Tên đầy đủ": "NGUYEN H", "Thời gian tạo": "2026-09-20 21:49:01", "Tồn giờ": 65, "Số lần hẹn": 2, "CL Lặp": 1, "Nhân sự": "TQGTI.CAONB", "TTCL": "Đang XL", "Độ Ưu Tiên": "Support", "POP": "TQGP005", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQFD0098 >> TQGTI.CAONB", "Cột AN": "Trần Văn Nam (QL-01)" },
        { "STT": 6, "Block": "Xa Yen Son-001", "Số HĐ": "TQFD13450", "Tên đầy đủ": "TRỊNH KẾ", "Thời gian tạo": "2026-09-23 14:45:09", "Tồn giờ": -7, "Số lần hẹn": 1, "CL Lặp": 3, "Nhân sự": "TQGTI.CUHA", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP001", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "Hỏng điều khiển Sky", "Cột AN": "Lê Hoàng Long (QL-03)" },
        { "STT": 7, "Block": "Xa Yen Son-001", "Số HĐ": "TQAAE9218", "Tên đầy đủ": "NGUYỄN N", "Thời gian tạo": "2026-09-24 08:35:09", "Tồn giờ": -24, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.CUHA", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP002", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAE9218 - 0968561111", "Cột AN": "Lê Hoàng Long (QL-03)" },
        { "STT": 8, "Block": "Xa Chiem Hoa-001", "Số HĐ": "TQAAE3435", "Tên đầy đủ": "NGUYỄN T", "Thời gian tạo": "2026-09-15 16:27:27", "Tồn giờ": -29, "Số lần hẹn": 8, "CL Lặp": 1, "Nhân sự": "TQGTI.CUONGDD9", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP038", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "KH báo trễ >> NghiaVT", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
        { "STT": 9, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAB6659", "Tên đầy đủ": "TỔNG THỊ", "Thời gian tạo": "2026-09-23 13:38:57", "Tồn giờ": -5, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.DANGNV", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP006", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "0369759687 KH mkn", "Cột AN": "Trần Văn Nam (QL-01)" },
        { "STT": 10, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAE0730", "Tên đầy đủ": "LÝ THỊ LỰC", "Thời gian tạo": "2026-09-24 10:19:43", "Tồn giờ": -24, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.DUNGNT26", "TTCL": "Đã PC", "Độ Ưu Tiên": "Support", "POP": "TQGP027", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAE0730 - 034654", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
        { "STT": 11, "Block": "Xa Dong Tho-001", "Số HĐ": "TQAAC9017", "Tên đầy đủ": "Vũ Đình Khải", "Thời gian tạo": "2026-09-17 08:56:48", "Tồn giờ": 137, "Số lần hẹn": 2, "CL Lặp": 2, "Nhân sự": "TQGTI.HIEUNV38", "TTCL": "Đang XL", "Độ Ưu Tiên": "Support", "POP": "TQGP030", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQGP030.0094/HO-2", "Cột AN": "Lê Hoàng Long (QL-03)" },
        { "STT": 12, "Block": "Xa Chiem Hoa-001", "Số HĐ": "TQAAE0435", "Tên đầy đủ": "Lý Văn Đô", "Thời gian tạo": "2026-09-18 12:24:07", "Tồn giờ": -2, "Số lần hẹn": 9, "CL Lặp": 2, "Nhân sự": "TQGTI.HUNGCV4", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP037", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "KH báo mất mạng", "Cột AN": "Lê Hoàng Long (QL-03)" },
        { "STT": 13, "Block": "Xa Ham Yen-001", "Số HĐ": "TQFD22905", "Tên đầy đủ": "NGUYỄN N", "Thời gian tạo": "2026-09-21 00:12:59", "Tồn giờ": -2, "Số lần hẹn": 3, "CL Lặp": 2, "Nhân sự": "TQGTI.LUCMDC", "TTCL": "Đã XL-Đang TD", "Độ Ưu Tiên": "Support", "POP": "TQGP024", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQFD2290 >> TQGTI.LUCMDC", "Cột AN": "Trần Văn Nam (QL-01)" },
        { "STT": 14, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAE8568", "Tên đầy đủ": "ĐỖ DUY H", "Thời gian tạo": "2026-09-19 11:57:53", "Tồn giờ": -7, "Số lần hẹn": 7, "CL Lặp": 1, "Nhân sự": "TQGTI.QUYETNT1", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP031", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "Checklist app hifpt", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
        { "STT": 15, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAE0407", "Tên đầy đủ": "TRƯƠNG", "Thời gian tạo": "2026-09-23 17:09:04", "Tồn giờ": -2, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.THANHNV41", "TTCL": "Đã PC", "Độ Ưu Tiên": "Support", "POP": "TQGP014", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "0388061208 báo mkn", "Cột AN": "Lê Hoàng Long (QL-03)" },
        { "STT": 16, "Block": "Xa Yen Son-001", "Số HĐ": "TQFD01751", "Tên đầy đủ": "Cao Hong", "Thời gian tạo": "2026-09-24 08:57:55", "Tồn giờ": -2, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.THANHNV8", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP004", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQFD01751 - 097876", "Cột AN": "Trần Văn Nam (QL-01)" },
        { "STT": 17, "Block": "Xa Yen Son-001", "Số HĐ": "TQAAB7146", "Tên đầy đủ": "LƯU ĐÌNH", "Thời gian tạo": "2026-09-23 16:53:44", "Tồn giờ": -24, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.THANHNV8", "TTCL": "Đang XL", "Độ Ưu Tiên": "Support", "POP": "TQGP006", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "097971496 >> TQGTI.THANHNV8", "Cột AN": "Trần Văn Nam (QL-01)" },
        { "STT": 18, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAF1512", "Tên đầy đủ": "Triệu Thị", "Thời gian tạo": "2026-09-23 07:56:09", "Tồn giờ": -2, "Số lần hẹn": 3, "CL Lặp": 1, "Nhân sự": "TQGTI.TUANQD", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP009", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "Checklist >> TQGTI.TUANQD", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
        { "STT": 19, "Block": "Xa Ham Yen-001", "Số HĐ": "TQFD12722", "Tên đầy đủ": "Nguyễn V", "Thời gian tạo": "2026-09-24 08:04:07", "Tồn giờ": 2, "Số lần hẹn": 2, "CL Lặp": 1, "Nhân sự": "TQGTI.TUANQD", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP009", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "KH mkn nhờ KT xử lý", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
        { "STT": 20, "Block": "Xa Ham Yen-001", "Số HĐ": "TQFD21035", "Tên đầy đủ": "ĐÌNH VĂN", "Thời gian tạo": "2026-09-23 18:01:15", "Tồn giờ": -24, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.TUANQD", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP009", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "0852269868 kh báo r", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
        { "STT": 21, "Block": "Xa Yen Son-001", "Số HĐ": "TQFD22274", "Tên đầy đủ": "PHẠM XUÂ", "Thời gian tạo": "2026-09-16 09:30:16", "Tồn giờ": 193, "Số lần hẹn": 4, "CL Lặp": 1, "Nhân sự": "TQGTI.TUNGDT4", "TTCL": "Đang XL", "Độ Ưu Tiên": "Support", "POP": "TQGP008", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "085659332 >> TQGTI.TUNGDT4", "Cột AN": "Lê Hoàng Long (QL-03)" },
        { "STT": 22, "Block": "Xa Yen Son-001", "Số HĐ": "TQAAC4072", "Tên đầy đủ": "ĐẶNG THỊ", "Thời gian tạo": "2026-09-23 13:30:17", "Tồn giờ": -7, "Số lần hẹn": 1, "CL Lặp": 1, "Nhân sự": "TQGTI.TUNGDT4", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "Support", "POP": "TQGP008", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "0379639154 mất kết", "Cột AN": "Lê Hoàng Long (QL-03)" },
        { "STT": 23, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAE4800", "Tên đầy đủ": "Hoàng Văn", "Thời gian tạo": "2026-09-23 11:10:12", "Tồn giờ": 23, "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP013", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAEC48C >> TQGTI.ANHPH3", "Cột AN": "Trần Văn Nam (QL-01)" },
        { "STT": 24, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAE5855", "Tên đầy đủ": "Trần Thị H", "Thời gian tạo": "2026-09-23 11:42:15", "Tồn giờ": -7, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã PC", "Độ Ưu Tiên": "SOS", "POP": "TQGP013", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAE5855 - 098768", "Cột AN": "Trần Văn Nam (QL-01)" },
        { "STT": 25, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAB1811", "Tên đầy đủ": "LÝ VĂN DŨ", "Thời gian tạo": "2026-09-23 15:23:30", "Tồn giờ": -24, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã PC", "Độ Ưu Tiên": "SOS", "POP": "TQGP013", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAB1811 - 037519 FTTH", "Cột AN": "Trần Văn Nam (QL-01)" },
        { "STT": 26, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAE7704", "Tên đầy đủ": "NGA VĂN", "Thời gian tạo": "2026-09-23 13:27:32", "Tồn giờ": -24, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.ANHPH3", "TTCL": "Đã PC", "Độ Ưu Tiên": "SOS", "POP": "TQGP013", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAE7704 - 097767", "Cột AN": "Trần Văn Nam (QL-01)" },
        { "STT": 27, "Block": "Xa Yen Son-001", "Số HĐ": "TQAAA6787", "Tên đầy đủ": "NGUYỄN T", "Thời gian tạo": "2026-09-23 18:06:26", "Tồn giờ": -7, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.BINHLV6", "TTCL": "Đang XL", "Độ Ưu Tiên": "SOS", "POP": "TQGP026", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAA6787 - 038570", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
        { "STT": 28, "Block": "Xa Dong Tho-001", "Số HĐ": "TQAAC5689", "Tên đầy đủ": "HOÀNG V", "Thời gian tạo": "2026-09-24 09:21:16", "Tồn giờ": -26, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.CHIENMM", "TTCL": "Đã PC", "Độ Ưu Tiên": "SOS", "POP": "TQGP033", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAC5689 - 039248", "Cột AN": "Lê Hoàng Long (QL-03)" },
        { "STT": 29, "Block": "Xa Dong Tho-001", "Số HĐ": "TQFD22609", "Tên đầy đủ": "TRẦN THỊ", "Thời gian tạo": "2026-09-23 17:18:55", "Tồn giờ": -5, "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.HIEUNV38", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP021", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQFD22609 - 0989711", "Cột AN": "Lê Hoàng Long (QL-03)" },
        { "STT": 30, "Block": "Xa Dong Tho-001", "Số HĐ": "TQAAC6077", "Tên đầy đủ": "RIÊU VĂN", "Thời gian tạo": "2026-09-23 18:50:25", "Tồn giờ": -7, "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.HIEUNV38", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP018", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAC6077 - 098649", "Cột AN": "Lê Hoàng Long (QL-03)" },
        { "STT": 31, "Block": "Xa Chiem Hoa-001", "Số HĐ": "TQAAE4058", "Tên đầy đủ": "TRẦN THỊ", "Thời gian tạo": "2026-09-24 06:38:46", "Tồn giờ": -7, "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.HUNGDT5", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP035", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAE4058 - 097806", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
        { "STT": 32, "Block": "Xa Dong Tho-001", "Số HĐ": "TQAAE1876", "Tên đầy đủ": "NINH VĂN", "Thời gian tạo": "2026-09-23 20:05:45", "Tồn giờ": 14, "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.NGHIANV6", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP032", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAE1876 - 034763", "Cột AN": "Trần Văn Nam (QL-01)" },
        { "STT": 33, "Block": "Xa Dong Tho-001", "Số HĐ": "TQAAB0488", "Tên đầy đủ": "LÊ TRUNG", "Thời gian tạo": "2026-09-24 08:38:51", "Tồn giờ": -26, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.NGHIANV6", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP030", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQGP030.0172/HO-1", "Cột AN": "Trần Văn Nam (QL-01)" },
        { "STT": 34, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAF1555", "Tên đầy đủ": "Trần Lệ Tri", "Thời gian tạo": "2026-09-23 08:55:18", "Tồn giờ": -2, "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.QUANHV1", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP027", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAF1555 - 091719", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
        { "STT": 35, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAB1352", "Tên đầy đủ": "CHU VĂN", "Thời gian tạo": "2026-09-23 21:18:41", "Tồn giờ": -5, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.QUANHV1", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP027", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAB1352 - 097454", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
        { "STT": 36, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAE6009", "Tên đầy đủ": "ĐẰNG VĂN", "Thời gian tạo": "2026-09-23 10:54:23", "Tồn giờ": -24, "Số lần hẹn": 2, "CL Lặp": 0, "Nhân sự": "TQGTI.QUANHV1", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP027", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAE6009 - 083219", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
        { "STT": 37, "Block": "Xa Ham Yen-001", "Số HĐ": "TQAAB6047", "Tên đầy đủ": "NGUYỄN V", "Thời gian tạo": "2026-09-23 20:35:51", "Tồn giờ": -5, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.QUYETNT1", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP031", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAB6047 - 097711", "Cột AN": "Phạm Quốc Hùng (QL-02)" },
        { "STT": 38, "Block": "Phuong My Lam-001", "Số HĐ": "TQAAE7703", "Tên đầy đủ": "Lò Thị Ngăn", "Thời gian tạo": "2026-09-20 21:27:28", "Tồn giờ": 85, "Số lần hẹn": 4, "CL Lặp": 0, "Nhân sự": "TQGTI.THANHNV41", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP014", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAE7703 - 039252", "Cột AN": "Lê Hoàng Long (QL-03)" },
        { "STT": 39, "Block": "Phuong My Lam-001", "Số HĐ": "TQFD13770", "Tên đầy đủ": "NGUYỄN T", "Thời gian tạo": "2026-09-21 15:31:48", "Tồn giờ": 24, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.THANHNV41", "TTCL": "Đang XL", "Độ Ưu Tiên": "SOS", "POP": "TQGP014", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQFD13770 - 039537", "Cột AN": "Lê Hoàng Long (QL-03)" },
        { "STT": 40, "Block": "Xa Chiem Hoa-001", "Số HĐ": "TQAAC8160", "Tên đầy đủ": "CHU VĂN", "Thời gian tạo": "2026-09-23 13:50:45", "Tồn giờ": 21, "Số lần hẹn": 3, "CL Lặp": 0, "Nhân sự": "TQGTI.TIENVT3", "TTCL": "Đã nhận ca", "Độ Ưu Tiên": "SOS", "POP": "TQGP033", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAC8160 - 034971", "Cột AN": "Trần Văn Nam (QL-01)" },
        { "STT": 41, "Block": "Xa Yen Son-001", "Số HĐ": "TQAAC7840", "Tên đầy đủ": "PHẠM ĐÌN", "Thời gian tạo": "2026-09-23 07:30:30", "Tồn giờ": -5, "Số lần hẹn": 1, "CL Lặp": 0, "Nhân sự": "TQGTI.TUNGDT4", "TTCL": "Đang XL", "Độ Ưu Tiên": "SOS", "POP": "TQGP008", "Kiểm soát": "Chưa Đánh Giá", "Ghi Chú CC": "TQAAC7840 - 096321", "Cột AN": "Lê Hoàng Long (QL-03)" }
    ]
    return pd.DataFrame(data)

# Khởi tạo Session State dữ liệu
if 'df_data' not in st.session_state:
    st.session_state.df_data = get_sample_data()

# ==========================================
# 3. SIDEBAR: TẢI FILE EXCEL & TRỌNG YẾU
# ==========================================
with st.sidebar:
    st.title("⚙️ Cấu Hình & Dữ Liệu")
    
    # Upload Excel File
    uploaded_file = st.file_uploader("📂 Cập nhật File Excel", type=["xlsx", "xls", "csv"])
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_upload = pd.read_csv(uploaded_file)
            else:
                df_upload = pd.read_excel(uploaded_file)
            
            # Đảm bảo có các cột cơ bản
            required_cols = ["Block", "Số HĐ", "Tên đầy đủ", "Tồn giờ", "Số lần hẹn", "CL Lặp", "Nhân sự", "Cột AN"]
            st.session_state.df_data = df_upload
            st.success(f"Nạp thành công {len(df_upload)} dòng dữ liệu!")
        except Exception as e:
            st.error(f"Lỗi đọc file: {e}")
            
    st.divider()
    st.markdown("**BangNC13-TQG**")

# ==========================================
# 4. HEADER & BANNER THÔNG TIN
# ==========================================
st.markdown("""
<div style="display: flex; align-items: center; justify-content: space-between; margin-bottom: 10px;">
    <div>
        <h2 style="margin: 0; color: #0f172a; font-weight: 700;">DASHBOARD KIỂM SOÁT CA TỒN & CHECKLIST</h2>
        <p style="margin: 0; color: #64748b; font-size: 0.85rem;">Khớp chính xác: Số HĐ, Khách Hàng, Block, Lần Hẹn, CL Lặp, Nhân Sự, Quản Lý, Tồn Giờ, Kiểm Soát</p>
    </div>
</div>
""", unsafe_allow_html=True)

df = st.session_state.df_data.copy()

st.markdown(f"""
<div class="olive-banner">
    <div style="font-weight: 600; font-size: 0.9rem; margin-bottom: 4px;">Các trường thông tin kiểm soát trọng yếu:</div>
    <div>
        <span class="olive-tag">Số HĐ</span>
        <span class="olive-tag">Khách Hàng</span>
        <span class="olive-tag">Block</span>
        <span class="olive-tag">Số Lần Hẹn</span>
        <span class="olive-tag">CL Lặp</span>
        <span class="olive-tag">Nhân Sự</span>
        <span class="olive-tag">Quản Lý</span>
        <span class="olive-tag">Tồn Giờ</span>
        <span class="olive-tag">Kiểm Soát</span>
    </div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# 5. TÍNH TOÁN KPI METRICS
# ==========================================
total_cases = len(df)
sos_cases = len(df[df['Độ Ưu Tiên'].astype(str).str.upper().str.contains('SOS', na=False)])
sos_pct = (sos_cases / total_cases * 100) if total_cases > 0 else 0

repeat_df = df[df['CL Lặp'] > 0]
repeat_sum = repeat_df['CL Lặp'].sum()
repeat_cases_count = len(repeat_df)

overdue_cases = len(df[df['Tồn giờ'] >= 24])
overdue_pct = (overdue_cases / total_cases * 100) if total_cases > 0 else 0

processing_cases = len(df[df['TTCL'].astype(str).str.contains('Đang XL', na=False)])
processing_pct = (processing_cases / total_cases * 100) if total_cases > 0 else 0

unchecked_cases = len(df[(df['Kiểm soát'].isna()) | (df['Kiểm soát'] == '') | (df['Kiểm soát'] == 'Chưa Đánh Giá')])

# ==========================================
# 6. HIỂN THỊ KPI CARDS
# ==========================================
col1, col2, col3, col4, col5, col6 = st.columns(6)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-badge" style="background:#eff6ff; color:#2563eb;">Tất cả</span>
        <div class="kpi-title">Tổng Ca Tồn</div>
        <div class="kpi-value">{total_cases}</div>
        <div class="kpi-sub">Tổng hợp hợp đồng tồn</div>
        <div class="kpi-bar" style="background:#3b82f6;"></div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-badge" style="background:#fff1f2; color:#e11d48;">{sos_pct:.1f}%</span>
        <div class="kpi-title" style="color:#e11d48;">Mức SOS ⚠️</div>
        <div class="kpi-value" style="color:#e11d48;">{sos_cases}</div>
        <div class="kpi-sub">Số ca báo SOS</div>
        <div class="kpi-bar" style="background:#f43f5e;"></div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-badge" style="background:#fffbebf; color:#d97706;">{repeat_cases_count} ca</span>
        <div class="kpi-title" style="color:#d97706;">CLL Đang Tồn 🔄</div>
        <div class="kpi-value" style="color:#d97706;">{repeat_sum}</div>
        <div class="kpi-sub">Tổng lượt lặp (Lặp > 0)</div>
        <div class="kpi-bar" style="background:#f59e0b;"></div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-badge" style="background:#f3e8ff; color:#7e22ce;">{overdue_pct:.1f}%</span>
        <div class="kpi-title" style="color:#7e22ce;">Tồn Giờ ≥ 24H ⏰</div>
        <div class="kpi-value" style="color:#7e22ce;">{overdue_cases}</div>
        <div class="kpi-sub">Ca quá hạn 1 ngày</div>
        <div class="kpi-bar" style="background:#a855f7;"></div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-badge" style="background:#e0e7ff; color:#4338ca;">{processing_pct:.1f}%</span>
        <div class="kpi-title" style="color:#4338ca;">Đang Xử Lý ⚙️</div>
        <div class="kpi-value" style="color:#4338ca;">{processing_cases}</div>
        <div class="kpi-sub">Trạng thái Đang XL</div>
        <div class="kpi-bar" style="background:#6366f1;"></div>
    </div>
    """, unsafe_allow_html=True)

with col6:
    st.markdown(f"""
    <div class="kpi-card">
        <span class="kpi-badge" style="background:#ecfdf5; color:#047857;">Chưa ĐG</span>
        <div class="kpi-title" style="color:#047857;">Cần Đánh Giá 📋</div>
        <div class="kpi-value" style="color:#047857;">{unchecked_cases}</div>
        <div class="kpi-sub">Chưa ghi nhận đánh giá</div>
        <div class="kpi-bar" style="background:#10b981;"></div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ==========================================
# 7. BỘ LỌC DỮ LIỆU
# ==========================================
st.subheader("🔍 Bộ Lọc Dữ Liệu Tồn Ca")
f_col1, f_col2, f_col3, f_col4, f_col5, f_col6 = st.columns(6)

with f_col1:
    search_text = st.text_input("Tìm kiếm", placeholder="Số HĐ, KH, Ghi chú...")

with f_col2:
    all_managers = ["Tất cả Quản lý"] + sorted(list(df['Cột AN'].dropna().unique()))
    selected_manager = st.selectbox("Quản Lý", all_managers)

with f_col3:
    if selected_manager != "Tất cả Quản lý":
        tech_list = sorted(list(df[df['Cột AN'] == selected_manager]['Nhân sự'].dropna().unique()))
    else:
        tech_list = sorted(list(df['Nhân sự'].dropna().unique()))
    all_techs = ["Tất cả Nhân sự"] + tech_list
    selected_tech = st.selectbox("Nhân Sự", all_techs)

with f_col4:
    selected_priority = st.selectbox("Mức SOS", ["Tất cả Mức SOS", "Chỉ lấy: SOS", "Chỉ lấy: Support"])

with f_col5:
    selected_repeat = st.selectbox("CL Lặp", ["Tất cả CL Lặp", "Chỉ khác 0 (Lặp > 0)", "Bằng 0 (= 0)", "Lặp 1 lần", "Lặp 2 lần", "Lặp ≥ 3 lần"])

with f_col6:
    all_blocks = ["Tất cả Block"] + sorted(list(df['Block'].dropna().unique()))
    selected_block = st.selectbox("Block", all_blocks)

# Áp dụng bộ lọc
filtered_df = df.copy()

if search_text:
    st_lower = search_text.lower()
    filtered_df = filtered_df[
        filtered_df['Số HĐ'].astype(str).str.lower().str.contains(st_lower) |
        filtered_df['Tên đầy đủ'].astype(str).str.lower().str.contains(st_lower) |
        filtered_df['Ghi Chú CC'].astype(str).str.lower().str.contains(st_lower) |
        filtered_df['Block'].astype(str).str.lower().str.contains(st_lower)
    ]

if selected_manager != "Tất cả Quản lý":
    filtered_df = filtered_df[filtered_df['Cột AN'] == selected_manager]

if selected_tech != "Tất cả Nhân sự":
    filtered_df = filtered_df[filtered_df['Nhân sự'] == selected_tech]

if selected_priority == "Chỉ lấy: SOS":
    filtered_df = filtered_df[filtered_df['Độ Ưu Tiên'].astype(str).str.upper().str.contains("SOS", na=False)]
elif selected_priority == "Chỉ lấy: Support":
    filtered_df = filtered_df[~filtered_df['Độ Ưu Tiên'].astype(str).str.upper().str.contains("SOS", na=False)]

if selected_repeat == "Chỉ khác 0 (Lặp > 0)":
    filtered_df = filtered_df[filtered_df['CL Lặp'] > 0]
elif selected_repeat == "Bằng 0 (= 0)":
    filtered_df = filtered_df[filtered_df['CL Lặp'] == 0]
elif selected_repeat == "Lặp 1 lần":
    filtered_df = filtered_df[filtered_df['CL Lặp'] == 1]
elif selected_repeat == "Lặp 2 lần":
    filtered_df = filtered_df[filtered_df['CL Lặp'] == 2]
elif selected_repeat == "Lặp ≥ 3 lần":
    filtered_df = filtered_df[filtered_df['CL Lặp'] >= 3]

if selected_block != "Tất cả Block":
    filtered_df = filtered_df[filtered_df['Block'] == selected_block]

# ==========================================
# 8. ĐỒ THỊ BÁO CÁO (CHARTS)
# ==========================================
c_col1, c_col2 = st.columns(2)

with c_col1:
    st.markdown("##### 1. Tỉ trọng Checklist Lặp Theo Mức Độ SOS")
    
    # Chuẩn bị dữ liệu nhóm lặp
    def map_repeat(val):
        if val == 0: return 'Không Lặp (0)'
        elif val == 1: return 'Lặp 1 lần'
        elif val == 2: return 'Lặp 2 lần'
        else: return 'Lặp ≥ 3 lần'

    chart1_df = filtered_df.copy()
    chart1_df['Group_Repeat'] = chart1_df['CL Lặp'].apply(map_repeat)
    chart1_df['Type_SOS'] = chart1_df['Độ Ưu Tiên'].apply(lambda x: 'SOS (Cấp Thiết)' if 'SOS' in str(x).upper() else 'Support (Hỗ Trợ)')
    
    grouped1 = chart1_df.groupby(['Group_Repeat', 'Type_SOS']).size().reset_index(name='Số ca')
    
    fig1 = px.bar(
        grouped1, 
        x='Group_Repeat', 
        y='Số ca', 
        color='Type_SOS',
        barmode='group',
        color_discrete_map={'SOS (Cấp Thiết)': '#f43f5e', 'Support (Hỗ Trợ)': '#3b82f6'},
        category_orders={"Group_Repeat": ['Không Lặp (0)', 'Lặp 1 lần', 'Lặp 2 lần', 'Lặp ≥ 3 lần']}
    )
    fig1.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300, legend_title_text="")
    st.plotly_chart(fig1, use_container_width=True)

with c_col2:
    st.markdown("##### 2. Top Block Tồn Ca Nhiều Nhất")
    block_counts = filtered_df['Block'].value_counts().reset_index()
    block_counts.columns = ['Block', 'Số ca tồn']
    top_blocks = block_counts.head(8)
    
    fig2 = px.bar(
        top_blocks, 
        y='Block', 
        x='Số ca tồn', 
        orientation='h',
        color_discrete_sequence=['#0284c7']
    )
    fig2.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300, yaxis=dict(autorange="reverse"))
    st.plotly_chart(fig2, use_container_width=True)

c_col3, c_col4 = st.columns(2)

with c_col3:
    st.markdown("##### 3. Tồn theo POP Station")
    pop_counts = filtered_df['POP'].value_counts().reset_index()
    pop_counts.columns = ['POP', 'Số ca tồn']
    top_pops = pop_counts.head(8)
    
    fig3 = px.bar(
        top_pops, 
        x='POP', 
        y='Số ca tồn',
        color_discrete_sequence=['#10b981']
    )
    fig3.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300)
    st.plotly_chart(fig3, use_container_width=True)

with c_col4:
    st.markdown("##### 4. Top KTV Tồn Ca Nhiều Nhất")
    tech_counts = filtered_df['Nhân sự'].value_counts().reset_index()
    tech_counts.columns = ['Nhân sự', 'Số ca tồn']
    top_techs = tech_counts.head(10)
    
    fig4 = px.bar(
        top_techs, 
        x='Nhân sự', 
        y='Số ca tồn',
        color_discrete_sequence=['#a855f7']
    )
    fig4.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=300)
    st.plotly_chart(fig4, use_container_width=True)

# ==========================================
# 9. BẢNG DỮ LIỆU ĐIỀU CHỈNH CỤ THỂ
# ==========================================
st.markdown("---")
st.markdown(f"### 📋 BẢNG KIỂM SOÁT DỮ LIỆU TỒN CA ({len(filtered_df)} / {len(df)} ca)")

# Cấu hình các cột hiển thị đúng tên người dùng yêu cầu
display_cols = ["STT", "Số HĐ", "Block", "Số lần hẹn", "CL Lặp", "Nhân sự", "Cột AN", "Tồn giờ", "Kiểm soát", "Ghi Chú CC"]

# Cho phép người dùng chỉnh sửa trực tiếp cột 'Kiểm soát' trên Streamlit Data Editor
control_options = ["Chưa Đánh Giá", "✅ Đã tiếp nhận", "⚠️ Cần hỗ trợ", "🚨 Cảnh báo trễ", "❌ Khách giục", "🎉 Đã giải quyết"]

edited_df = st.data_editor(
    filtered_df[display_cols],
    column_config={
        "STT": st.column_config.NumberColumn("STT", width="small", disabled=True),
        "Số HĐ": st.column_config.TextColumn("Số HĐ", disabled=True),
        "Block": st.column_config.TextColumn("Block", disabled=True),
        "Số lần hẹn": st.column_config.NumberColumn("Lần Hẹn", disabled=True),
        "CL Lặp": st.column_config.NumberColumn("CL Lặp", disabled=True),
        "Nhân sự": st.column_config.TextColumn("Nhân Sự", disabled=True),
        "Cột AN": st.column_config.TextColumn("Quản Lý", disabled=True),
        "Tồn giờ": st.column_config.NumberColumn("Tồn Giờ", disabled=True),
        "Kiểm soát": st.column_config.SelectboxColumn(
            "Kiểm Soát",
            options=control_options,
            required=True
        ),
        "Ghi Chú CC": st.column_config.TextColumn("Ghi Chú CSKH", disabled=True)
    },
    use_container_width=True,
    hide_index=True
)

# Cập nhật lại trạng thái vào session state nếu có chỉnh sửa
if not edited_df.equals(filtered_df[display_cols]):
    for index, row in edited_df.iterrows():
        st.session_state.df_data.loc[st.session_state.df_data['STT'] == row['STT'], 'Kiểm soát'] = row['Kiểm soát']

# ==========================================
# 10. XUẤT BÁO CÁO EXCEL
# ==========================================
st.markdown("<br>", unsafe_allow_html=True)

@st.cache_data
def convert_df_to_csv(df_to_export):
    return df_to_export.to_csv(index=False).encode('utf-8-sig')

csv_data = convert_df_to_csv(filtered_df)

st.download_button(
    label="📥 Export Excel Báo Cáo (CSV)",
    data=csv_data,
    file_name="Bao_Cao_Kiem_Soat_Ca_Ton.csv",
    mime="text/csv",
)
