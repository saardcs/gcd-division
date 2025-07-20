import streamlit as st
import random

st.set_page_config(page_title="Euclidian Division Practice", layout="centered")
st.title("🧮 Euclidian Division Practice")

# Initialize session state
if "problems" not in st.session_state:
    # Generate 5 problems with numbers between 20 and 100, ensure a >= b and b > 0
    problems = []
    while len(problems) < 5:
        a = random.randint(20, 100)
        b = random.randint(10, 90)
        if a >= b and b > 0:
            problems.append((a, b))
    st.session_state.problems = problems
    st.session_state.index = 0
    st.session_state.score = 0
    st.session_state.steps = []
    st.session_state.a = None
    st.session_state.b = None
    st.session_state.done = False
    st.session_state.gcd_checked = False
    st.session_state.gcd_correct = False

def reset_problem():
    a, b = st.session_state.problems[st.session_state.index]
    st.session_state.a = a
    st.session_state.b = b
    st.session_state.steps = []
    st.session_state.done = False
    st.session_state.gcd_checked = False
    st.session_state.gcd_correct = False

def full_reset():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.rerun()

# If all problems done
if st.session_state.index >= 5:
    st.success(f"🎉 All done! Your final score: {st.session_state.score} / 5")
    if st.button("🔁 Restart Practice"):
        full_reset()
else:
    # Start new problem if needed
    if st.session_state.a is None or st.session_state.b is None:
        reset_problem()

    a = st.session_state.a
    b = st.session_state.b
    orig_a, orig_b = st.session_state.problems[st.session_state.index]

    st.markdown(f"### Problem {st.session_state.index + 1} of 5")
    st.markdown(f"Find the GCD of **{orig_a}** and **{orig_b}** using Euclidean division steps.")

    # Show previous steps
    if st.session_state.steps:
        col1, col2, col3 = st.columns([1, 1, 1])
        col1.markdown("**Division**")
        col2.markdown("**Result**")
        col3.markdown("**Remainder**")
        for (x, y, q, r) in st.session_state.steps:
            col1.markdown(f"{x} / {y}")
            col2.markdown(f"{q}")
            col3.markdown(f"{r}")

    if not st.session_state.done:
        current_a = st.session_state.a
        current_b = st.session_state.b

        # Ensure current_a >= current_b
        if current_a < current_b:
            current_a, current_b = current_b, current_a

        st.markdown(f"### Step {len(st.session_state.steps) + 1}")

        col1, col2, col3 = st.columns([1, 1, 1])
        with col1:
            st.markdown(f"**Division**")
            st.markdown(f"**{current_a} / {current_b} =**")
        with col2:
            user_q = st.number_input("Result", step=1, key=f"q_{len(st.session_state.steps)}")
        with col3:
            user_r = st.number_input("Remainder", min_value=0, step=1, key=f"r_{len(st.session_state.steps)}")

        if st.button("✅ Check Step", key=f"check_step_{len(st.session_state.steps)}"):
            correct_q = current_a // current_b
            correct_r = current_a % current_b

            if user_q == correct_q and user_r == correct_r:
                st.success("Correct!")
                st.session_state.steps.append((current_a, current_b, correct_q, correct_r))
                if correct_r == 0:
                    st.session_state.done = True
                else:
                    st.session_state.a = current_b
                    st.session_state.b = correct_r
                st.rerun()
            else:
                st.error("Incorrect. Try again.")

    # Final GCD input after done
    if st.session_state.done:
        st.markdown("---")
        st.markdown("### ✅ Final Step")
        st.markdown("What is the GCD of the two numbers? Type your answer below:")
        user_gcd = st.text_input("Your Answer:", key=f"gcd_input_{st.session_state.index}")

        if st.button("🎯 Check GCD", key=f"check_gcd_{st.session_state.index}"):
            try:
                user_value = int(user_gcd.strip())
                correct_value = st.session_state.b  # last non-zero remainder (the GCD)
                st.session_state.gcd_checked = True
                if user_value == correct_value:
                    st.success(f"🎉 Correct! The GCD is **{correct_value}**.")
                    st.session_state.score += 1
                    st.session_state.gcd_correct = True
                else:
                    st.error("❌ That’s not correct. Try again.")
                    st.session_state.gcd_correct = False
            except ValueError:
                st.error("Please enter a valid integer.")

        if st.session_state.gcd_checked and st.session_state.gcd_correct:
            if st.button("➡️ Next Problem"):
                st.session_state.index += 1
                reset_problem()
                st.rerun()
