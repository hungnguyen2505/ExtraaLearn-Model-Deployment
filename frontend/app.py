
import os
import requests
import streamlit as st

# Backend API URL
API_URL = os.getenv(
    "API_URL",
    "http://localhost:5000/predict"
)

st.set_page_config(
    page_title="ExtraaLearn Lead Conversion",
    layout="centered"
)

st.title("ExtraaLearn Lead Conversion Prediction")

st.write(
    "Enter the lead details below to predict "
    "the likelihood of conversion into a paid customer."
)

with st.form("prediction_form"):

    st.subheader("Lead Information")

    age = st.number_input(
        "Age",
        min_value=18,
        max_value=100,
        value=35,
        step=1
    )

    current_occupation = st.selectbox(
        "Current Occupation",
        ["Professional", "Unemployed", "Student"]
    )

    first_interaction = st.selectbox(
        "First Interaction",
        ["Website", "Mobile App"]
    )

    profile_completed = st.selectbox(
        "Profile Completed",
        ["High", "Medium", "Low"]
    )

    st.subheader("Website Engagement")

    website_visits = st.number_input(
        "Website Visits",
        min_value=0,
        value=3,
        step=1
    )

    time_spent_on_website = st.number_input(
        "Time Spent on Website (seconds)",
        min_value=0,
        value=600,
        step=1
    )

    page_views_per_visit = st.number_input(
        "Page Views per Visit",
        min_value=0.0,
        value=3.0,
        step=0.1
    )

    last_activity = st.selectbox(
        "Last Activity",
        [
            "Website Activity",
            "Email Activity",
            "Phone Activity"
        ]
    )

    st.subheader("Marketing Channels")

    print_media_type1 = st.selectbox(
        "Print Media Type 1",
        ["No", "Yes"]
    )

    print_media_type2 = st.selectbox(
        "Print Media Type 2",
        ["No", "Yes"]
    )

    digital_media = st.selectbox(
        "Digital Media",
        ["No", "Yes"]
    )

    educational_channels = st.selectbox(
        "Educational Channels",
        ["No", "Yes"]
    )

    referral = st.selectbox(
        "Referral",
        ["No", "Yes"]
    )

    submitted = st.form_submit_button(
        "Predict Conversion"
    )


if submitted:

    lead_data = {
        "age": age,
        "current_occupation": current_occupation,
        "first_interaction": first_interaction,
        "profile_completed": profile_completed,
        "website_visits": website_visits,
        "time_spent_on_website": time_spent_on_website,
        "page_views_per_visit": page_views_per_visit,
        "last_activity": last_activity,
        "print_media_type1": print_media_type1,
        "print_media_type2": print_media_type2,
        "digital_media": digital_media,
        "educational_channels": educational_channels,
        "referral": referral
    }

    try:
        response = requests.post(
            API_URL,
            json=lead_data,
            timeout=20
        )

        response.raise_for_status()

        result = response.json()

        prediction = result["prediction"]
        probability = result["conversion_probability"]

        st.subheader("Prediction Result")

        st.metric(
            "Conversion Probability",
            f"{probability * 100:.2f}%"
        )

        if prediction == 1:
            st.success(
                "This lead is predicted to convert "
                "into a paid customer."
            )
        else:
            st.warning(
                "This lead is predicted not to convert "
                "into a paid customer."
            )

    except requests.exceptions.RequestException as e:
        st.error(f"Unable to connect to the prediction API: {e}")

    except (ValueError, KeyError, TypeError):
        st.error("Invalid response received from the API.")
