import streamlit as st

st.set_page_config(page_title="Smart Campus Dashboard", page_icon="🏫", layout="wide")

st.markdown("""
<style>
    .main-header {
        font-size: 2.8rem;
        font-weight: bold;
        color: #1E3A8A;
        text-align: center;
        margin-bottom: 10px;
    }
    .sub-header {
        text-align: center;
        color: #6B7280;
        margin-bottom: 40px;
        font-size: 1.2rem;
    }
    div[data-testid="column"] {
        background-color: #F8FAFC;
        border-radius: 12px;
        padding: 10px;
        border: 1px solid #E2E8F0;
        transition: 0.3s;
    }
    div[data-testid="column"]:hover {
        background-color: #EFF6FF;
        border-color: #BFDBFE;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='main-header'>🏫 Smart Campus Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='sub-header'>ระบบตรวจสอบและจัดการอาคารเรียนอัจฉริยะ (Smart Building Management System)</div>", unsafe_allow_html=True)

st.markdown("#### 🏢 เลือกอาคารที่ต้องการตรวจสอบ")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.page_link("pages/page_1.py", label="Building 2", icon="🏢")
with col2:
    st.page_link("pages/page_1.py", label="Building 7", icon="🏢")
with col3:
    st.page_link("pages/page_1.py", label="Building 9", icon="🏢")
with col4:
    st.page_link("pages/page_1.py", label="Building 12", icon="🏢")

st.write("---")

# จัดให้อยู่ตรงกลางด้วย Columns
col_img1, col_img2, col_img3 = st.columns([1, 2, 1])
with col_img2:
    st.image('image/Homepage1.jfif', caption='บรรยากาศและสถานที่ต่างๆ ภายในมหาวิทยาลัย', use_container_width=True)