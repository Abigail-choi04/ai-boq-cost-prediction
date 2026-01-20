import streamlit as st
import requests

st.set_page_config(page_title="AI BOQ Cost Estimator", layout = "wide")

st.title("Smart BOQ Cost Estimator")
st.write("AI-powered construction cost predictor")
st.sidebar.header("Project Details")

project_type = st.sidebar.selectbox("Project Type",["Residential", "Apartment", "Commercial"])
area = st.sidebar.number_input("Built-up Area (sq ft)", 500, 10000, 1200)
floors = st.sidebar.number_input("Number of floors", 1, 5, 1)

city = st.sidebar.selectbox("Location", ["Rural", "Metro"])
quality = st.sidebar.selectbox("Construction Quality", ["Basic", "Standard", "Premium"])

#mapping ui inputs to ml features
city_type = 1 if city == "Metro" else 0
quality_map = {"Basic":1, "Standard":2, "Premium":3}
quality_val = quality_map[quality]

cement = area * floors * (0.04 if quality == "Basic" else 0.05 if quality == "Standard" else 0.06)
steel = area * floors * (0.02 if quality == "Basic" else 0.03 if quality == "Standard" else 0.04)
bricks = area * floors * 0.8
sand = area * floors * 0.05
labor = area * floors * (0.15 if quality == "Basic" else 0.2 if quality == "Standard" else 0.25)

if st.sidebar.button("Estimate Cost"):
    data = {
    "cement_cum": cement,
    "steel_mt": steel,
    "brickwork_cum": bricks,
    "sand_cum": sand,
    "labor_cost": labor,
    }


    response = requests.post("http://127.0.0.1:5000/predict", json=data)

    if response.status_code == 200:
        result = response.json()
        cost = int(result['predicted_cost'])
        
        st.subheader("Estimated Project Cost")
        st.success(f"₹ {cost:,}")
        
        st.write("### Cost Breakdown (Approx.)")
        st.write(f"Materials: ₹ {int(cost * 0.65):,}")
        st.write(f"Labor: ₹ {int(cost * 0.25):,}")
        st.write(f"Other: ₹ {int(cost * 0.10):,}")
    else:
        st.error("Server error")
