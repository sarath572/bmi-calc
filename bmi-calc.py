import streamlit as st
import datetime

suggested_bmi_ranges = {
    "male": {
        "5-10": (14.5, 19.5),
        "11-17": (16.5, 23.5),
        "18-24": (18.5, 24.9),
        "25-34": (19.0, 25.9),
        "35-44": (20.0, 26.9),
        "45-54": (21.0, 27.9),
        "55-64": (22.0, 28.9),
        "65+": (23.0, 29.9),
    },
    "female": {
        "5-10": (14.5, 19.5),
        "10-18": (16.5, 23.5),
        "18-24": (18.5, 24.9),
        "25-34": (19.0, 25.9),
        "35-44": (20.0, 26.9),
        "45-54": (21.0, 27.9),
        "55-64": (22.0, 28.9),
        "65+": (23.0, 29.9),
    },
}

def calculate_bmi(height_meters, weight):
    return weight / (height_meters ** 2)

def main():
    st.title("BMI Calculator")

    dob = st.date_input("Enter your birth date:", min_value=datetime.date(1900, 1, 1),
                        max_value=datetime.date(2023, 12, 31))
    gender = st.radio("Select your gender:", ["Male", "Female"])
    height_feet = st.selectbox("Enter your height in feet:", list(range(2, 10)))
    height_inches = st.selectbox("Enter your height in inches:", list(range(12)))
    weight = st.number_input("Enter your weight in kilograms (4 to 150 kg):", min_value=4, max_value=150)

    calculate_button = st.button("Calculate BMI")

    if calculate_button:
        try:
            birthdate = dob
            today = datetime.date.today()
            if (today.month, today.day) < (birthdate.month, birthdate.day):
                year = today.year - 1
                month = today.month + 12
            else:
                year = today.year
                month = today.month
            age = year - birthdate.year
            months = month - birthdate.month
            if today.day < birthdate.day:
                months -= 1
                days = today.day + (30 if birthdate.month in [4, 6, 9, 11] else 31 if birthdate.month != 2 else 29 if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0) else 28) - birthdate.day
            else:
                days = today.day - birthdate.day

            if age < 0 or (age == 0 and months < 0) or (months == 0 and days < 0):
                st.write("Invalid birthdate. Enter a valid birthdate.")
                return

            st.write(f"Your age is {age} years, {months} months, and {days} days")

            height_meters = (height_feet * 0.3048) + (height_inches * 0.0254)
            st.write(f"Your height: {height_feet} feet {height_inches} inches")
            
            bmi = calculate_bmi(height_meters, weight)
            st.write(f"Your BMI (Body Mass Index): {bmi:.2f}")

            age_group = None
            if 5 <= age < 10:
                age_group = "5-10"
            elif 10 <= age < 18:
                age_group = "10-18" if gender == "Male" else "10-18"
            elif 18 <= age < 25:
                age_group = "18-24"
            elif 25 <= age < 35:
                age_group = "25-34"
            elif 35 <= age < 45:
                age_group = "35-44"
            elif 45 <= age < 55:
                age_group = "45-54"
            elif 55 <= age < 65:
                age_group = "55-64"
            else:
                age_group = "65+"

            suggested_range = suggested_bmi_ranges.get(gender.lower(), {}).get(age_group, None)
            if suggested_range:
                suggested_weight_min = suggested_range[0] * (height_meters ** 2)
                suggested_weight_max = suggested_range[1] * (height_meters ** 2)
                st.write(f"Suggested BMI range for your age and gender: {suggested_range[0]} - {suggested_range[1]}")
                st.write(f"Suggested weight range: {suggested_weight_min:.2f} kg - {suggested_weight_max:.2f} kg")
            else:
                st.write("Suggested BMI range not available for your age and gender.")

            if bmi < suggested_range[0]:
                st.write("Your BMI is below the suggested range. You are underweight.")
            elif bmi >= suggested_range[0] and bmi <= suggested_range[1]:
                st.write("Your BMI is within the suggested range.")
            else:
                st.write("Your BMI is above the suggested range. You are overweight.")
        except ValueError:
            st.write("Invalid input. Please enter valid data.")

if __name__ == "__main__":
    main()
