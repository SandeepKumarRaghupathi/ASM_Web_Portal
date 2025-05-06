import streamlit as st

st.title("Samples")

col1, col2 = st.columns(2, gap="small", vertical_alignment="center")
col3, col4 = st.columns(2, gap="small", vertical_alignment="center")
col5, col6 = st.columns(2, gap="small", vertical_alignment="center")

with col1:
    st.write("Shed")
    st.image("Lorryplant1.png",width=400)

with col2:
    st.write("Chips 20 MM")
    st.image("Chips 20 MM.png",width=400)

with col3:
    st.write("Chips 40 MM")
    st.image("Chips 40 MM.png",width=400)

with col4:
    st.write("Gravel")
    st.image("Gravel.png",width=400)

with col5:
    st.write("Offloading Material")
    st.image("Load_1.png", width=400)

with col6:
    st.write("Offloading Material")
    st.image("Load_2.png", width=400)
