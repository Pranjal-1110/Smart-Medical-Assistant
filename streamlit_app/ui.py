import streamlit as st
import requests
import json

def get_user_location():
    try:
        response = requests.get('https://ipinfo.io/json')
        if response.status_code == 200:
            data = response.json()
            return data.get('city')
    except:
        pass
    return None

st.set_page_config(page_title="Smart Medical Assistant", layout="centered")
st.title("Smart Medical Assistant")

# Try to detect location
detected_city = get_user_location()

with st.form("symptom_form"):
    patient_id = st.text_input("Enter Patient ID")
    symptoms = st.text_area("Describe Symptoms")

    if detected_city:
        st.write(f"Detected Location: {detected_city}")
        location = detected_city
    else:
        location = st.text_input("Enter your Location")

    submitted = st.form_submit_button("Analyze")

if submitted:
    if not patient_id or not symptoms:
        st.warning("Please fill all fields.")
    else:
        response = requests.post(
            "http://localhost:8000/api/analyze",
            headers={"Content-Type": "application/json"},
            data=json.dumps({"patient_id": patient_id, "symptoms": symptoms, "location": location})
        )
        if response.status_code == 200:
            result = response.json()
            st.success("Prediction completed.")

            st.subheader("Recommended Action")
            st.info(result.get("recommended_action", "No recommendation."))

            st.subheader("Suggested Doctor Specialization")
            st.success(result.get("recommended_doctor", "Not found."))

            st.subheader("Nearby Doctors")
            doctors = result.get("nearby_doctors", [])
            if doctors:
                for doc in doctors:
                    st.write(f"- {doc}")
            else:
                st.warning("No nearby doctors found.")
            
            st.json(result)

        else:
            st.error("Error analyzing symptoms. Please try again.")
