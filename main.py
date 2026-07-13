import streamlit as st
st.markdown("## This is a Homepage")
col1, col2,col3,col4, = st.columns(4)

with col1:
    page1 = st.page_link("pages/page_1.py", label=f" Building 2", icon="🏢")
with col2:
    page1 = st.page_link("pages/page_1.py", label=f" Building 7", icon="🏢")
with col3:
    page1 = st.page_link("pages/page_1.py", label=f" Building 9", icon="🏢")
with col4:
    page1 = st.page_link("pages/page_1.py", label=f" Building 12", icon="🏢")
st.image('image/Homepage1.jfif', caption='สถานที่ต่างๆ ภายในมหาลัย')