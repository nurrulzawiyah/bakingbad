import streamlit as st
import pandas as pd
from datetime import datetime

st.set_page_config(page_title="Scone Order Form", page_icon="🍪")

# --- Add your logo here ---
st.image("logo.png", width=300)  # Change "logo.png" to your actual file name

# Storage for orders
if "orders" not in st.session_state:
    st.session_state.orders = []

st.title("🍪 Scone Order Form for Sunday 27 April 2025!")

st.markdown("""
Order your fresh, homemade scones for this Sunday!  
Fill in your details below and we'll WhatsApp you for confirmation & payment.
""")

# --- Order Form ---
with st.form("order_form"):
    name = st.text_input("Your Name")
    phone = st.text_input("WhatsApp Number")
    scone_set = st.number_input("Scone Set (6 pcs scones + 2 matangshire cream) RM20 per set", min_value=0, step=1)
    scone_individual = st.number_input("Individual Scones (RM2 each)", min_value=0, step=1)
    delivery = st.selectbox(
        "Delivery Method",
        ["Self-pickup", "Runner – PJ area (RM5)", "Runner – Kuching (RM7)"]
    )
    notes = st.text_area("Additional Notes (optional)")
    submit = st.form_submit_button("Place Order")

    if submit:
        if name and phone and (scone_set > 0 or scone_individual > 0):
            order = {
                "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "Name": name,
                "Phone": phone,
                "Scone Set": scone_set,
                "Individual Scones": scone_individual,
                "Delivery": delivery,
                "Notes": notes
            }
            st.session_state.orders.append(order)
            st.success("Order submitted! We'll WhatsApp you soon. Thank you!")
        else:
            st.error("Please fill in your name, phone number, and order at least one scone.")

# --- Admin Section for Download ---
st.markdown("---")
with st.expander("🍪 Admin Only: Download Orders (Protected)"):
    admin_pw = st.text_input("Enter admin password:", type="password")
    if admin_pw == "h3ib3rg":  # Change this to your own password!
        if st.session_state.orders:
            df = pd.DataFrame(st.session_state.orders)
            st.dataframe(df)
            csv = df.to_csv(index=False).encode('utf-8')
            st.download_button(
                label="Download Orders as CSV",
                data=csv,
                file_name="scone_orders.csv",
                mime="text/csv"
            )
        else:
            st.info("No orders yet!")
    elif admin_pw:
        st.error("Wrong password.")


