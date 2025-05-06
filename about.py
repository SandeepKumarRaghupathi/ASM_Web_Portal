
import streamlit as st

st.title("ASM Civil Suppliers and Earthmovers")


col1, col2 = st.columns(2, gap="small", vertical_alignment="center")

with col1:
    st.image("Shed.png",width=600)

with col2:
    st.title("MoulishKumar", anchor=False)
    st.write("With over 15 years of experience in the industry, we specialize in the efficient and reliable "
             "transportation of high-quality sand—a vital material in construction and various industrial applications. "
             "We are committed to delivering top-grade products at "
             "competitive prices, ensuring our valued customers receive both quality and value in every transaction.")

    phone_number = "+91 7708793702"
    if st.button("Call me", key="green"):
        st.markdown(f'''
                <a href="tel:{phone_number}">
                    <button style="padding: 10px 20px; font-size: 20px;">📞 Call {phone_number}</button>
                </a>
                ''', unsafe_allow_html=True)

