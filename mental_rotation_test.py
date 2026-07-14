import streamlit as st
import random
import time


image_sets = [
    ("images/target1.png", "images/correct1.png", "images/wrong1.png", 45),
    ("images/target2.png", "images/correct2.png", "images/wrong2.png", 90),
    ("images/target3.png", "images/correct3.png", "images/wrong3.png", 45),
    ("images/target4.png", "images/correct4.png", "images/wrong4.png", 90),
    ("images/target5.png", "images/correct5.png", "images/wrong5.png", 90),
    ("images/target6.png", "images/correct6.png", "images/wrong6.png", 90),
    ("images/target7.png", "images/correct7.png", "images/wrong7.png", 90),
    ("images/target8.png", "images/correct8.png", "images/wrong8.png", 0),
    ("images/target9.png", "images/correct9.png", "images/wrong9.png", 45),
    ("images/target10.png", "images/correct10.png", "images/wrong10.png", 90),
    ("images/target11.png", "images/correct11.png", "images/wrong11.png", 135),
    ("images/target12.png", "images/correct12.png", "images/wrong12.png", 45),
    ("images/target13.png", "images/correct13.png", "images/wrong13.png", 0),
    ("images/target14.png", "images/correct14.png", "images/wrong14.png", 45),
    ("images/target15.png", "images/correct15.png", "images/wrong15.png", 90),
]

TOTAL_QUESTIONS = 15
QUESTION_TIME_LIMIT = 15


def handle_answer(option):

    rt = time.time() - st.session_state.mrt_question_start

    st.session_state.mrt_results.append({

        "correct": option["correct"],
        "time": rt,
        "angle": st.session_state.current_angle,
        "timed_out": False

    })

    st.session_state.mrt_question += 1
    st.session_state.mrt_question_start = None
    st.session_state.mrt_options = None

    st.rerun()


def run_mental_rotation_test():

    st.title("🧠 Mental Rotation Test")


    if "mrt_started" not in st.session_state:
        st.session_state.mrt_started = False


    if not st.session_state.mrt_started:

        st.subheader("📋 Instructions")

        st.markdown("""

You will see a reference image and two options.

• Select the correct rotated version.

• Total Questions : 15

• Time Limit : 15 seconds per question

• Respond quickly and accurately.

### 🧪 Sample

""")

        sample_target = "images/s1.png"
        sample_option_a = "images/s2.png"
        sample_option_b = "images/s3.png"

        c1,c2,c3 = st.columns([1,2,1])

        with c2:
            st.image(
                sample_target,
                caption="Reference Image",
                width=150
            )

        a,b = st.columns(2)

        with a:
            st.image(
                sample_option_a,
                caption="Option A",
                width=130
            )

        with b:
            st.image(
                sample_option_b,
                caption="Option B",
                width=130
            )

        st.markdown("""

### ⚖️ Guidance

• Focus on shape

• Ignore orientation

• Only one option is correct

### 🧠 Cognitive Domains

• Spatial Ability

• Mental Rotation

• Visual Processing

• Working Memory

""")

        st.markdown("---")

        if st.button("Start Mental Rotation Test"):

            st.session_state.mrt_started = True

            st.rerun()

        return


    if "mrt_initialized" not in st.session_state:

        st.session_state.mrt_initialized = True

        st.session_state.mrt_question = 0

        st.session_state.mrt_results = []

        st.session_state.mrt_randomized = random.sample(

            range(len(image_sets)),

            TOTAL_QUESTIONS

        )

        st.session_state.mrt_question_start = None

        st.session_state.mrt_options = None

        st.session_state.current_angle = 0


    if st.session_state.mrt_question >= TOTAL_QUESTIONS:

        results = st.session_state.mrt_results

        correct = sum(

            r["correct"]

            for r in results

        )

        accuracy = (

            correct

            /

            TOTAL_QUESTIONS

        ) * 100

        avg_time = (

            sum(

                r["time"]

                for r in results

            )

            /

            TOTAL_QUESTIONS

        )

        timed_out = sum(

            r["timed_out"]

            for r in results

        )


    if st.session_state.mrt_question >= TOTAL_QUESTIONS:

        results = st.session_state.mrt_results


        correct = sum(r["correct"] for r in results)

        accuracy = (correct / TOTAL_QUESTIONS) * 100

        avg_time = sum(r["time"] for r in results) / TOTAL_QUESTIONS

        timed_out = sum(r["timed_out"] for r in results)


        high_angle_trials = [
            r for r in results
            if r["angle"] >= 90
        ]

        if len(high_angle_trials) > 0:
            high_angle_acc = (
                sum(r["correct"] for r in high_angle_trials)
                / len(high_angle_trials)
            )
        else:
            high_angle_acc = 0


        weighted_score = 0
        total_weight = 0

        for r in results:

            weight = 1 + (r["angle"] / 180)

            total_weight += weight

            if r["correct"]:
                weighted_score += weight

        spatial_score = (
            weighted_score / total_weight
            if total_weight > 0 else 0
        )


        st.session_state["MR_acc"] = accuracy

        st.session_state["MR_reaction"] = avg_time

        st.session_state["mrt_timeout"] = timed_out

        st.session_state["MR_high_angle_accuracy"] = high_angle_acc

        st.session_state["MR_spatial_score"] = spatial_score


        st.subheader("📊 Performance Metrics")

        st.markdown("---")

        col1, col2 = st.columns(2)

        col3, col4 = st.columns(2)

        col1.metric(
            "Accuracy",
            f"{accuracy:.2f}%"
        )

        col2.metric(
            "Average Reaction Time",
            f"{avg_time:.2f}s"
        )

        col3.metric(
            "High Angle Accuracy",
            f"{high_angle_acc:.2f}"
        )

        col4.metric(
            "Timed Out",
            f"{timed_out}/{TOTAL_QUESTIONS}"
        )

        st.metric(
            "Spatial Ability Score",
            f"{spatial_score:.3f}"
        )

        st.markdown("---")

        if st.button(
            "Continue",
            type="primary",
            use_container_width=True
        ):

            # Keep scores

            keep = [
                "MR_acc",
                "MR_reaction",
                "mrt_timeout",
                "MR_high_angle_accuracy",
                "MR_spatial_score"
            ]

            for key in list(st.session_state.keys()):

                if key.startswith("mrt_") and key not in keep:
                    del st.session_state[key]

            st.session_state.current_stage = "final"

            st.rerun()

        return
        

    if st.session_state.mrt_question_start is None:
        st.session_state.mrt_question_start = time.time()

    elapsed = time.time() - st.session_state.mrt_question_start

    remaining = max(
        0.0,
        QUESTION_TIME_LIMIT - elapsed
    )

    
    if remaining <= 0:

        st.session_state.mrt_results.append({
            "correct": False,
            "time": QUESTION_TIME_LIMIT,
            "angle": st.session_state.current_angle,
            "timed_out": True
        })

        st.session_state.mrt_question += 1

        st.session_state.mrt_question_start = None
        st.session_state.mrt_options = None

        st.rerun()

        return

   

    st.markdown(
        f"### Question {st.session_state.mrt_question + 1} / {TOTAL_QUESTIONS}"
    )

    timer_color = (
        "🔴" if remaining < 5
        else "🟡" if remaining < 10
        else "🟢"
    )

    st.markdown(
        f"### {timer_color} Time Remaining: {remaining:.1f}s"
    )

    st.progress(
        remaining / QUESTION_TIME_LIMIT,
        text=f"⏳ {remaining:.1f}s left"
    )

    

    trial_idx = st.session_state.mrt_randomized[
        st.session_state.mrt_question
    ]

    target_img, correct_img, wrong_img, angle = image_sets[trial_idx]

    st.session_state.current_angle = angle

    

    if st.session_state.mrt_options is None:

        options = [
            {
                "img": correct_img,
                "correct": True
            },
            {
                "img": wrong_img,
                "correct": False
            }
        ]

        random.shuffle(options)

        st.session_state.mrt_options = options

    else:

        options = st.session_state.mrt_options


    st.markdown("---")

    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:
        st.image(
            target_img,
            width=180
        )

    st.markdown("---")

    st.markdown(
        "### 👆 Select the Correct Rotated Image"
    )

   

    colA, colB = st.columns(2)

    with colA:

        st.image(
            options[0]["img"],
            width=150
        )

        if st.button(
            "Option A",
            key=f"mrt_a_{st.session_state.mrt_question}"
        ):

            handle_answer(options[0])

    with colB:

        st.image(
            options[1]["img"],
            width=150
        )

        if st.button(
            "Option B",
            key=f"mrt_b_{st.session_state.mrt_question}"
        ):

            handle_answer(options[1])

    

    if st.session_state.mrt_question < TOTAL_QUESTIONS:

        time.sleep(0.1)

        st.rerun()
