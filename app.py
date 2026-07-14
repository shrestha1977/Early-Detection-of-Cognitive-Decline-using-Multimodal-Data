import streamlit as st
import time

from datetime import datetime
from math_test import run_math_test
from stroop_test import run_stroop_test
from mental_rotation_test import run_mental_rotation_test

st.set_page_config(page_title="Cognitive Assessment Tool", layout="centered")


if "current_stage" not in st.session_state:
    st.session_state.current_stage = "consent"

if "stage_lock" not in st.session_state:
    st.session_state.stage_lock = True

if "heartbeat" not in st.session_state:
    st.session_state.heartbeat = time.time()


if st.session_state.current_stage == "consent":

    st.title("Cognitive Assessment Study")

    st.markdown("""
    ### Digital Consent

    - This assessment is conducted solely for academic research purposes.
    - The data collected will be used only for analysis and study related to cognitive performance.
    - No personally identifiable information will be shared with third parties.
    - Your responses will remain confidential and anonymous.
    - Participation in this assessment is voluntary.
    - You may choose to exit the test at any time without any consequences.
    """)

    st.subheader("Eligibility Confirmation")

    c1 = st.checkbox("I confirm that I have passed 12th standard.")
    c2 = st.checkbox("I confirm that I am computer literate and can operate a computer independently.")
    consent = st.checkbox(
        "I agree to participate and allow my data to be used for academic research purposes."
    )

    if c1 and c2 and consent:
        if st.button("Start Test", key="start_test_btn"):
            st.session_state.current_stage = "demographics"
            st.rerun()
    else:
        st.warning("Please confirm all the above statements to continue.")



if st.session_state.current_stage == "demographics":

    st.markdown("### Baseline & Demographic Information")

    name = st.text_input("Name", key="name")
    age = st.selectbox(
        "Age Category",
        ["18-25", "26-35", "36-45", "46-55", "56+"],
        key="age",
    )

    gender = st.selectbox(
        "Gender",
        ["Male", "Female", "Other"],
        key="gender",
    )

    hometown = st.text_input("Home Town", key="hometown")
    current_city = st.text_input("Current City", key="current_city")

    mother_language = st.selectbox(
        "Mother Language",
        [
            "Hindi",
            "English",
            "Bengali",
            "Tamil",
            "Telugu",
            "Marathi",
            "Gujarati",
            "Kannada",
            "Malayalam",
            "Other",
        ],
        key="mother_language",
    )

    academic = st.selectbox(
        "Academic Qualification",
        [
            "Pursuing UG",
            "Pursuing PG",
            "Completed UG",
            "Completed PG",
        ],
        key="academic",
    )

    service = st.selectbox(
        "Service Status",
        [
            "Employed",
            "Not Employed",
            "Retired",
        ],
        key="service",
    )

    handedness = st.selectbox(
        "Handedness",
        [
            "Right",
            "Left",
            "Ambidextrous",
        ],
        key="handedness",
    )

    device = st.selectbox(
        "Device Used",
        [
            "Laptop",
            "Desktop",
            "Mobile",
            "Tablet",
        ],
        key="device",
    )

    vision = st.selectbox(
        "Vision Status",
        [
            "Normal",
            "Corrected to Normal",
        ],
        key="vision",
    )

    prior_exposure = st.selectbox(
        "Prior exposure to any cognitive test recently?",
        [
            "Yes",
            "No",
        ],
        key="prior_exposure",
    )

    if st.button("Continue", key="demo_continue_btn"):

        if name.strip() == "":
            st.warning("Please enter your name.")
            st.stop()

        st.session_state.demographics = {
            "name": name,
            "age": age,
            "gender": gender,
            "hometown": hometown,
            "current_city": current_city,
            "mother_language": mother_language,
            "academic": academic,
            "service": service,
            "handedness": handedness,
            "device": device,
            "vision": vision,
            "prior_exposure": prior_exposure,
        }

        st.session_state.current_stage = "instructions"
        st.rerun()


elif st.session_state.current_stage == "instructions":

    st.title("Instructions")

    st.markdown("""
    You will complete **three cognitive tasks** as part of this assessment:

    ### 🧠 Tasks Included
    1. **Numerical Ability Test**
    2. **Stroop Test**
    3. **Mental Rotation Test**

    ---

    ### ⏱️ Guidelines
    - Respond **as quickly and accurately as possible**.
    - Each task is **time-sensitive**, so avoid delays.
    - Read each question carefully before answering.
    - Do not use any external aids (calculators, pen, paper, etc.) during the test.

    ---

    ### ⚠️ Important Notes
    - Ensure you are in a **quiet and distraction-free environment**.
    - Do not refresh or close the browser during the test.
    - Once started, the test should be completed in one session.

    ---

    Click the button below when you are ready to begin.
    """)

    if st.button("Continue to Test"):

        st.session_state.stage_lock = False
        st.session_state.current_stage = "math"

        st.rerun()


elif st.session_state.current_stage == "math":
    run_math_test()

elif st.session_state.current_stage == "stroop":
    run_stroop_test()

elif st.session_state.current_stage == "mental":
    run_mental_rotation_test()



elif st.session_state.current_stage == "final":

    

    from risk.normalize import (
    normalize_math,
    normalize_stroop,
    normalize_mrt
)

    from risk.calculate_ccs import calculate_ccs
    from risk.expected_score import expected_score
    from risk.age_adjust import age_adjusted_score
    from risk.zscore import calculate_z
    from risk.classify import classify


    def show_final_result():

        age_group = st.session_state["demographics"]["age"]

        age_map = {
            "18-25":22,
            "26-35":30,
            "36-45":40,
            "46-55":50,
            "56+":60
        }

        age = age_map[age_group]


        math_score = st.session_state["num_ability_score"]

        stroop_error = st.session_state["Stroop_error"]
        stroop_mean_rt = st.session_state["stroop_mean_RT"]
        stroop_interference = st.session_state["Stroop_interference"]

        
        mr_acc = st.session_state["MR_acc"]
        mr_reaction = st.session_state["MR_reaction"]
        mr_spatial_score = st.session_state["MR_spatial_score"]
        mr_high_angle_accuracy = st.session_state["MR_high_angle_accuracy"]



        math_norm = normalize_math(math_score)

        stroop_norm = normalize_stroop(
            stroop_error,
            stroop_mean_rt,
            stroop_interference
        )

        mrt_norm = normalize_mrt(
            mr_acc,
            mr_reaction,
            mr_spatial_score,
            mr_high_angle_accuracy
        )



        ccs = calculate_ccs(
            math_norm,
            stroop_norm,
            mrt_norm
        )



        expected = expected_score(age)


        age_adjusted = age_adjusted_score(
            ccs,
            expected
        )


        z = calculate_z(age_adjusted)


        risk = classify(z)


        participant = st.session_state["demographics"]
        current_time = datetime.now()

        st.title("🧠 Cognitive Assessment Report")

        st.markdown("---")

        st.subheader("👤 Participant Information")

        col1, col2 = st.columns(2)

        with col1:
            st.write(f"**Name:** {participant['name']}")
            st.write(f"**Gender:** {participant['gender']}")
            st.write(f"**Age Group:** {participant['age']}")

        with col2:
            st.write(
                f"**Assessment Date:** {current_time.strftime('%d %B %Y')}"
            )

            st.write(
                f"**Assessment Time:** {current_time.strftime('%I:%M %p')}"
            )

            st.write("**Assessment Status:** Completed")

        st.markdown("---")
        

        st.subheader("📋 Assessment Summary")

        st.success("✅ Numerical Ability Test Completed")

        st.success("✅ Stroop Test Completed")

        st.success("✅ Mental Rotation Test Completed")
        st.markdown("""
        The results from all three assessments were combined and compared against age-adjusted cognitive performance benchmarks.
        """)

        st.subheader("Cognitive Risk Zone Classification")

        if risk == "Green":
            st.success("🟢 GREEN ZONE")
            st.markdown("""
        ### Interpretation


Your assessment results indicate that cognitive performance was generally within the expected range for your age group.

Performance across the evaluated domains was consistent with typical cognitive functioning patterns.

### Key Findings

• Attention and cognitive control were generally stable.

• Processing speed was within the expected range.

• Numerical reasoning and spatial reasoning performance were adequate.

• Overall cognitive performance appeared consistent with expected levels.

### Recommendations

• Continue engaging in mentally stimulating activities.

• Maintain healthy sleep habits.

• Stay physically active.

• Support cognitive wellness through regular learning and problem solving.
        """)



        elif risk == "Yellow":
            st.warning("🟡 YELLOW ZONE")
            st.markdown("""
        ### Interpretation

Your assessment results indicate mild deviations from expected cognitive performance levels.

While this does not necessarily indicate impairment, certain aspects of cognitive performance were lower than expected during testing.

### Key Findings

• Some cognitive measures showed variability.

• Temporary factors such as fatigue, stress, distraction, or poor sleep may have influenced performance.

• Continued monitoring and cognitive engagement may be beneficial.

### Recommendations

• Maintain healthy sleep patterns.

• Reduce stress wherever possible.

• Stay physically active.

• Engage regularly in activities that stimulate reasoning, attention and memory.

• Consider repeating the assessment periodically.
        """)


        else:
            st.error("🔴 RED ZONE")
            st.markdown("""
        ### Interpretation

Your assessment results showed notable deviations from expected cognitive performance levels.

One or more cognitive domains demonstrated performance below the age-adjusted benchmark used within this assessment framework.

### Key Findings

• Reduced performance was observed in one or more cognitive domains.

• Performance may have been influenced by fatigue, illness, stress, or other external factors.

• Further monitoring or evaluation may be beneficial.

### Recommendations

• Continue engaging in cognitively stimulating activities.

• Maintain healthy sleep and exercise habits.

• Monitor memory, attention and reasoning performance over time.

• If concerns persist, consider consultation with a qualified healthcare or neuropsychology professional.
        """)
            
            st.markdown("---")

        st.info("""
**Assessment Disclaimer**

This assessment is intended for academic research and cognitive screening purposes only.

It is not a diagnostic instrument and should not be considered a substitute for professional medical or neuropsychological evaluation.
""")

    show_final_result()

    st.success("Thank You for Participating!")
