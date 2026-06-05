import streamlit as st

st.set_page_config(page_title="BMI Calculator", page_icon="⚖️", layout="centered")

st.title("⚖️ BMI Calculator")
st.write("Enter your details below to calculate your Body Mass Index (BMI).")


def bmi_category(bmi):
    """Return the WHO weight category and a color for a given BMI value."""
    if bmi < 18.5:
        return "Underweight", "blue"
    elif bmi < 25:
        return "Normal weight", "green"
    elif bmi < 30:
        return "Overweight", "orange"
    else:
        return "Obese", "red"


units = st.radio("Choose your units", ("Metric (kg, cm)", "Imperial (lb, in)"), horizontal=True)

col1, col2 = st.columns(2)

if units == "Metric (kg, cm)":
    with col1:
        weight = st.number_input("Weight (kg)", min_value=1.0, max_value=500.0, value=70.0, step=0.5)
    with col2:
        height = st.number_input("Height (cm)", min_value=30.0, max_value=300.0, value=170.0, step=0.5)
    bmi = weight / ((height / 100) ** 2)
else:
    with col1:
        weight = st.number_input("Weight (lb)", min_value=1.0, max_value=1100.0, value=154.0, step=0.5)
    with col2:
        height = st.number_input("Height (in)", min_value=12.0, max_value=120.0, value=67.0, step=0.5)
    bmi = (weight / (height ** 2)) * 703

if st.button("Calculate BMI", type="primary"):
    category, color = bmi_category(bmi)
    st.markdown(f"### Your BMI is :{color}[{bmi:.1f}]")
    st.markdown(f"#### Category: :{color}[{category}]")
    st.progress(min(bmi / 40, 1.0))

    with st.expander("BMI categories (WHO)"):
        st.markdown(
            """
            | BMI | Category |
            | --- | --- |
            | Below 18.5 | Underweight |
            | 18.5 – 24.9 | Normal weight |
            | 25.0 – 29.9 | Overweight |
            | 30.0 and above | Obese |
            """
        )

    st.caption("BMI is a general indicator and does not account for muscle mass, age, or sex. Consult a healthcare professional for advice.")
