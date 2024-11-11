import streamlit as st
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

st.set_page_config(page_title="Loan Prediction App", layout="wide")


st.title("🏦 Loan Approval Prediction App")
st.markdown("""
Welcome to the **Loan Approval Prediction App**! This application helps predict loan approvals based on an applicant's details.
Fill in the form below to check the loan approval probability.
""")
st.write("---")  


@st.cache_data
def load_data():
    data = pd.read_csv('loan_data.csv')
    data['Gender'].fillna(data['Gender'].mode()[0], inplace=True)
    data['Dependents'].fillna(data['Dependents'].mode()[0], inplace=True)
    data['Self_Employed'].fillna(data['Self_Employed'].mode()[0], inplace=True)
    data['LoanAmount'].fillna(data['LoanAmount'].median(), inplace=True)
    data['Loan_Amount_Term'].fillna(data['Loan_Amount_Term'].median(), inplace=True)
    data['Credit_History'].fillna(data['Credit_History'].median(), inplace=True)
    return data

data = load_data()


with st.sidebar:
    st.header("📊 Data Visualization")


    with st.expander("Distribution of Applicant Income"):
        fig, ax = plt.subplots()
        sns.histplot(data['ApplicantIncome'], kde=True, ax=ax, color="blue")
        ax.set_title("Applicant Income Distribution")
        st.pyplot(fig)

    with st.expander("Distribution of Loan Amount"):
        fig, ax = plt.subplots()
        sns.histplot(data['LoanAmount'], kde=True, ax=ax, color="purple")
        ax.set_title("Loan Amount Distribution")
        st.pyplot(fig)

    with st.expander("Correlation Heatmap"):
        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(data.select_dtypes(include=[np.number]).corr(), annot=True, cmap='coolwarm', ax=ax)
        ax.set_title("Correlation Matrix")
        st.pyplot(fig)


    with st.expander("Loan Status by Education Level"):
        fig, ax = plt.subplots()
        sns.countplot(x='Education', hue='Loan_Status', data=data, palette="viridis", ax=ax)
        ax.set_title("Loan Status by Education Level")
        st.pyplot(fig)

    with st.expander("Loan Status by Credit History"):
        fig, ax = plt.subplots()
        sns.countplot(x='Credit_History', hue='Loan_Status', data=data, palette="magma", ax=ax)
        ax.set_title("Loan Status by Credit History")
        st.pyplot(fig)
        
        
    with st.expander("Loan status by Gender"):
        fig, ax = plt.subplots()
        sns.countplot(x='Gender', hue='Loan_Status', data=data, ax=ax)  # Corrected column name
        ax.set_title("Loan Status by Gender")
        st.pyplot(fig)

st.header("Enter Applicant Details")
st.write("Fill out the form below to get the loan approval prediction.")


def loan_approval_rule(applicant_income, coapplicant_income, loan_amount, credit_history):

    income_threshold = 5000
    loan_amount_threshold = 500
    if (applicant_income + coapplicant_income >= income_threshold) and (credit_history == 1.0) and (loan_amount <= loan_amount_threshold):
        return "Approved"
    else:
        return "Not Approved"

with st.form("loan_form"):
    gender = st.selectbox("Gender", ["None","Male", "Female","TransGender"])
    married = st.selectbox("Married", ["None","No", "Yes"])
    dependents = st.selectbox("Dependents", ["0", "1", "2", "3+"])
    education = st.selectbox("Education", ["None","Graduate", "Not Graduate"])
    self_employed = st.selectbox("Self Employed", ["None","No", "Yes"])
    applicant_income = st.number_input("Applicant Income", min_value=0)
    coapplicant_income = st.number_input("Coapplicant Income", min_value=0)
    loan_amount = st.number_input("Loan Amount", min_value=0)
    loan_amount_term = st.selectbox("Loan Amount Term", [0,360, 180, 120, 84, 60])
    credit_history = st.selectbox("Credit History", [0.0, 1.0])
    property_area = st.selectbox("Property Area", ["None","Urban", "Semiurban", "Rural"])
    submit_button = st.form_submit_button(label="Predict Loan Approval")




if submit_button:
    if gender == "None" or married == "None" or education == "None" or self_employed == "None" or property_area == "None" or loan_amount_term == 0:
        st.error("Please fill out all fields before submitting.")
    elif applicant_income == 0 or loan_amount == 0:
        st.error("Applicant Income and Loan Amount must be greater than zero.")
    else:

        result = loan_approval_rule(applicant_income, coapplicant_income, loan_amount, credit_history)
        if result == "Approved":
            st.success("🎉 Loan Prediction: Approved")
        else:
            st.error("🚫 Loan Prediction: Not Approved")

