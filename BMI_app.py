import streamlit as st
import google.genai as genai

# -----------------------------
# Read API key from custom file format
# -----------------------------
with open("secrets.txt", "r") as f:
    lines = f.readlines()

api_key = None

for line in lines:
    if "api_key" in line:
        api_key = line.split("=")[1].strip().replace('"', '')

# Safety check
if api_key is None:
    st.error("API key not found in secrets.txt")
    st.stop()

# -----------------------------
# Gemini client
# -----------------------------
c = genai.Client(api_key=api_key)

# -----------------------------
# UI
# -----------------------------
st.title("BMI Calculator with AI Nutritionist")

# Inputs
height = st.slider(
    "Enter your height in meters:",
    min_value=1.0,
    max_value=2.5,
    step=0.1
)

weight = st.slider(
    "Enter your weight in kg:",
    min_value=28,
    max_value=300,
    step=1
)

# -----------------------------
# BMI Calculation
# -----------------------------
bmi = round(weight / (height * height), 2)

st.subheader(f"Your BMI: {bmi}")

# Category
if bmi < 18.5:
    category = "Underweight"
elif bmi < 25:
    category = "Normal weight"
elif bmi < 30:
    category = "Overweight"
else:
    category = "Obese"

st.write("Category:", category)

# -----------------------------
# AI Prompt
# -----------------------------
prompt = f"""
You are a professional nutritionist.

User details:
- Height: {height} m
- Weight: {weight} kg
- BMI: {bmi}
- Category: {category}

Give:
1. Diet plan
2. Workout tips
3. Health advice
"""

# -----------------------------
# AI Button
# -----------------------------
if st.button("Get AI Nutrition Advice"):

    response = c.models.generate_content(
        model="gemini-3.5-flash",
        contents=prompt
    )

    st.subheader("AI Nutrition Advice")
    st.write(response.text)