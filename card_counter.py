# card_counter.py

import streamlit as st

# Hi-Lo values
hi_lo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

# Initialize session state
if 'running_count' not in st.session_state:
    st.session_state.running_count = 0
    st.session_state.cards_seen = 0
    st.session_state.num_decks = 6
    st.session_state.card_history = []

# 🎴 Function to style card buttons like hearts
def card_button_html(card):
    return f"""
    <div style="
        display: flex;
        justify-content: center;
        align-items: center;
        border: 2px solid black;
        border-radius: 10px;
        height: 80px;
        width: 60px;
        font-size: 26px;
        font-weight: bold;
        background-color: white;
        color: red;
    ">
        {card}♥
    </div>
    """

# 🟩 Set blackjack table background
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://i.imgur.com/zXcy3Gz.png");
            background-size: cover;
            background-position: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title and deck selection
st.title("🃏 Blackjack Hi-Lo Counter")
st.session_state.num_decks = st.selectbox("Select number of decks", [1, 2, 4, 6, 8], index=3)
total_cards = st.session_state.num_decks * 52

# Card grid
st.subheader("Tap a card:")
cards_ordered = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
card_rows = [cards_ordered[i:i+4] for i in range(0, len(cards_ordered), 4)]

for row in card_rows:
    cols = st.columns(len(row))
    for i, card in enumerate(row):
        with cols[i]:
            if st.button(card_button_html(card), use_container_width=True, key=card + str(st.session_state.cards_seen)):
                st.session_state.running_count += hi_lo_values[card]
                st.session_state.cards_seen += 1
                st.session_state.card_history.append(f"{card}♥")

# 🔄 Reset
if st.button("🔄 Reset Count"):
    st.session_state.running_count = 0
    st.session_state.cards_seen = 0
    st.session_state.card_history = []

# 🔢 Count calculations
decks_remaining = max((total_cards - st.session_state.cards_seen) / 52, 1)
true_count = round(st.session_state.running_count / decks_remaining, 2)

# 📊 Display Metrics
st.markdown("---")
st.metric("Running Count", st.session_state.running_count)
st.metric("True Count", true_count)
st.metric("Cards Seen", st.session_state.cards_seen)

# 🧾 Card History Tracker
if st.session_state.card_history:
    st.markdown("### 📜 Card History")
    st.markdown(" ".join(st.session_state.card_history))
