# card_counter.py

import streamlit as st

hi_lo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

if 'running_count' not in st.session_state:
    st.session_state.running_count = 0
    st.session_state.cards_seen = 0
    st.session_state.num_decks = 6

st.title("🃏 Blackjack Hi-Lo Card Counter")

st.session_state.num_decks = st.selectbox("Select number of decks", [1, 2, 4, 6, 8], index=3)
total_cards = st.session_state.num_decks * 52

st.subheader("Tap a card:")
cols = st.columns(4)
cards = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
for i, card in enumerate(cards):
    if cols[i % 4].button(card):
        st.session_state.running_count += hi_lo_values[card]
        st.session_state.cards_seen += 1

if st.button("🔄 Reset Count"):
    st.session_state.running_count = 0
    st.session_state.cards_seen = 0

decks_remaining = max((total_cards - st.session_state.cards_seen) / 52, 1)
true_count = round(st.session_state.running_count / decks_remaining, 2)

st.markdown("---")
st.metric("Running Count", st.session_state.running_count)
st.metric("True Count", true_count)
st.metric("Cards Seen", st.session_state.cards_seen)
