# card_counter.py


import streamlit as st
import matplotlib.pyplot as plt

# Hi-Lo values
hi_lo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

# Init session state
if 'running_count' not in st.session_state:
    st.session_state.running_count = 0
    st.session_state.cards_seen = 0
    st.session_state.num_decks = 6
    st.session_state.true_count_history = []
    st.session_state.hand = []

# 🎴 Playing card emoji format
def render_card(card):
    return f"<span style='display:inline-block;border:2px solid black;border-radius:8px;padding:12px;margin:4px;font-size:28px;background:white;color:red;width:50px;text-align:center;'>{card}♥</span>"

# 📈 Plot true count history
def plot_graph(history):
    fig, ax = plt.subplots()
    ax.plot(history, marker='o')
    ax.set_title("True Count Over Time")
    ax.set_xlabel("Cards Played")
    ax.set_ylabel("True Count")
    st.pyplot(fig)

# 🎲 Blackjack table background
st.markdown("""
    <style>
        .stApp {
            background-image: url("https://i.imgur.com/zXcy3Gz.png");
            background-size: cover;
        }
    </style>
""", unsafe_allow_html=True)

# Title & deck select
st.title("🃏 Blackjack Hi-Lo Counter")
st.session_state.num_decks = st.selectbox("Select number of decks", [1, 2, 4, 6, 8], index=3)
total_cards = st.session_state.num_decks * 52

# Dealing cards
st.subheader("Tap a card:")
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
card_rows = [cards[i:i+4] for i in range(0, len(cards), 4)]

for row in card_rows:
    cols = st.columns(len(row))
    for i, card in enumerate(row):
        if cols[i].button(card + "♥"):
            st.session_state.running_count += hi_lo_values[card]
            st.session_state.cards_seen += 1
            st.session_state.hand.append(card)
            decks_remaining = max((total_cards - st.session_state.cards_seen) / 52, 1)
            true_count = round(st.session_state.running_count / decks_remaining, 2)
            st.session_state.true_count_history.append(true_count)

# ♻️ Reset hand only
if st.button("♻️ Reset Hand"):
    st.session_state.hand = []

# 🔢 Count Calculations
decks_remaining = max((total_cards - st.session_state.cards_seen) / 52, 1)
true_count = round(st.session_state.running_count / decks_remaining, 2)

# 💰 Bet suggestion logic
def bet_suggestion(tc):
    if tc <= 0:
        return "Minimum Bet"
    elif tc == 1:
        return "1× Base Bet"
    elif tc == 2:
        return "2× Base Bet"
    else:
        return "4× (Max Aggressive)"

# 🧾 Card Hand Display
if st.session_state.hand:
    st.markdown("### ✋ Current Hand")
    hand_html = "".join([render_card(card) for card in st.session_state.hand])
    st.markdown(hand_html, unsafe_allow_html=True)

# 🔁 Count Info
st.markdown("---")
st.metric("Running Count", st.session_state.running_count)
st.metric("True Count", true_count)
st.metric("Cards Seen", st.session_state.cards_seen)
st.metric("💸 Suggested Bet", bet_suggestion(true_count))

# 📈 Graph
if st.session_state.true_count_history:
    st.markdown("### 📈 True Count Over Time")
    plot_graph(st.session_state.true_count_history)
