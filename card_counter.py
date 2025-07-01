# card_counter.py

import streamlit as st

# Hi-Lo card values
hi_lo_values = {
    '2': 1, '3': 1, '4': 1, '5': 1, '6': 1,
    '7': 0, '8': 0, '9': 0,
    '10': -1, 'J': -1, 'Q': -1, 'K': -1, 'A': -1
}

# Setup session state
if 'running_count' not in st.session_state:
    st.session_state.running_count = 0
    st.session_state.cards_seen = 0
    st.session_state.num_decks = 6

# Styling helper
def style_card_label(card):
    return f"🎴 {card} 🎴"

# App title
st.title("🃏 Blackjack Hi-Lo Card Counter")

# Deck selection
st.session_state.num_decks = st.selectbox("Select number of decks", [1, 2, 4, 6, 8], index=3)
total_cards = st.session_state.num_decks * 52

# Card entry section
st.subheader("Tap a card to count it:")
cards_ordered = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
card_rows = [cards_ordered[i:i+4] for i in range(0, len(cards_ordered), 4)]

# Render buttons in rows
for row in card_rows:
    cols = st.columns(len(row))
    for i, card in enumerate(row):
        if cols[i].button(style_card_label(card)):
            st.session_state.running_count += hi_lo_values[card]
            st.session_state.cards_seen += 1

# Reset button
if st.button("🔄 Reset Count"):
    st.session_state.running_count = 0
    st.session_state.cards_seen = 0

# Calculations
decks_remaining = max((total_cards - st.session_state.cards_seen) / 52, 1)
true_count = round(st.session_state.running_count / decks_remaining, 2)

# Output metrics
st.markdown("---")
st.metric("Running Count", st.session_state.running_count)
st.metric("True Count", true_count)
st.metric("Cards Seen", st.session_state.cards_seen)
