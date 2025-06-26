import streamlit as st
import random

#You can choose any emojis you like for the game.
# Here is a full list of emojis that can be used in the game.
# You can add more emojis to this list as per your preference.
full_list_of_emojis = [
        # Smileys
        "😀", "😃", "😄", "😁", "😆", "😅", "😂", "🤣", "😊", "😇",
        "🙂", "🙃", "😉", "😌", "😍", "🥰", "😘", "😗", "😙", "😚",
        "😋", "😜", "😝", "😛", "🤑", "🤗", "🤩", "🤔", "🤨", "😐",
        "😑", "😶", "🙄", "😏", "😒", "😞", "😔", "😟", "😕", "🙁",
        "☹️", "😣", "😖", "😫", "😩", "🥺", "😢", "😭", "😤", "😠",
        "😡", "🤬", "🤯", "😳", "🥵", "🥶", "😱", "😨", "😰", "😥",
        "😓", "🤭", "🤫", "🤥", "😶‍🌫️", "😴", "🤤", "😪", "😵",
        "🤐", "🥴", "🤢", "🤮", "🤧", "😷", "🤒", "🤕", "🤠", "😎",
        "🤓", "🧐", "😮", "😯", "😲", "🥱", "😦", "😧", "😨", "😰",
        # Hearts
        "❤️", "🧡", "💛", "💚", "💙", "💜", "🖤", "🤍", "🤎", "💔",
        "❣️", "💕", "💞", "💓", "💗", "💖", "💘", "💝", "💟",
        # Home/House
        "🏠", "🏡", "🏘️", "🏚️", "🏢", "🏣", "🏤", "🏥", "🏦", "🏨",
        # Stars
        "⭐", "🌟", "✨", "💫", "🌠",
        # Misc
        "🎉", "🎊", "🎈", "🎂", "🍰", "🍕", "🍔", "🍟", "🍎", "🍉"
    ]
#------------------------------------------------ GAME LOGIC ------------------------------------------------#
# This code implements a simple memory match game using emojis.
# The game consists of a grid of cards, each displaying an emoji.
# Players click on cards to reveal them and try to find matching pairs.
#------------------------------------------------ GAME CODE------------------------------------------------#
# Streamlit app for Emoji Memory Match Game
st.set_page_config(page_title="Emoji Flipper - Game", page_icon="🎮")


# Inject custom CSS
st.markdown(
"""
<style>
    .stApp {
            background-image: url("https://img.freepik.com/free-vector/dark-hexagonal-background-with-gradient-color_79603-1409.jpg");
            background-size: cover;
            background-repeat: no-repeat;
            background-attachment: fixed;
        }
    import streamlit as st

    div.stButton  {
        background-image: linear-gradient(to right, #6a11cb 0%, #2575fc 100%);
        color: white;
        padding: 0.5em 1.5em;
        border-radius: 8px;
        border: none;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }

    div.stButton > button:first-child:hover {
        background-image: linear-gradient(to right, #2575fc 0%, #6a11cb 100%);
        transform: scale(1.05);
        cursor: pointer;
    }

</style>
""",
 unsafe_allow_html=True
)


#------------------------------------------------ GAME INITIALIZATION ------------------------------------------------#
# Initialize session state variables
if 'cards' not in st.session_state:
    emojis = ["🍰", "❤️", "💔", "🤠", "🍎", "💚", "⭐", "🤣", "💞", "🏨"]
    # Full list of emojis for the game, including hearts, homes, etc.

    st.session_state.cards = emojis * 2
    random.shuffle(st.session_state.cards)
    st.session_state.revealed = [False] * len(st.session_state.cards)
    st.session_state.moves = 0
    st.session_state.first_card = None
    st.session_state.second_card = None
    st.session_state.matched_pairs = 0

# Function to reset the game
def reset_game():
    random.shuffle(st.session_state.cards)
    st.session_state.revealed = [False] * len(st.session_state.cards)
    st.session_state.moves = 0
    st.session_state.first_card = None
    st.session_state.second_card = None
    st.session_state.matched_pairs = 0

# Function to handle card click
def card_click(index):
    if st.session_state.revealed[index]:
        return

    if st.session_state.first_card is None:
        st.session_state.first_card = index
    elif st.session_state.second_card is None:
        st.session_state.second_card = index
        st.session_state.moves += 1

        if st.session_state.cards[st.session_state.first_card] == st.session_state.cards[st.session_state.second_card]:
            st.session_state.revealed[st.session_state.first_card] = True
            st.session_state.revealed[st.session_state.second_card] = True
            st.session_state.matched_pairs += 1
            st.session_state.first_card = None
            st.session_state.second_card = None
        else:
            #st.rerun()
            st.session_state.trigger_rerun = True # Set flag instead of calling st.rerun() directly to avoid issues with Streamlit's rerun behavior
    else:
        st.session_state.first_card = index
        st.session_state.second_card = None

# Title
st.title("Match Emoji - A Memory Game")

# Display the grid of cards
cols = st.columns(4)
for i, card in enumerate(st.session_state.cards):
    with cols[i % 4]:
        if st.session_state.revealed[i] or i == st.session_state.first_card or i == st.session_state.second_card:
            st.button(card, key=i, on_click=card_click, args=(i,))
        else:
            st.button("❓", key=i, on_click=card_click, args=(i,))

# Display the number of moves
st.write(f"Moves: {st.session_state.moves}")

# Display the reset button
if st.button("Reset Game"):
    reset_game()

# Check if the rerun flag is set and reset it

# Trigger rerun if needed
if st.session_state.get("trigger_rerun", False):
    # Reset the flag to avoid infinite reruns
    st.session_state.trigger_rerun = False # Reset the flag after using it
    st.rerun() # This will trigger a rerun of the app to update the UI after a card click

# Display the win message
if st.session_state.matched_pairs == len(st.session_state.cards) // 2:
    st.balloons()
    st.write("🎉 You Win! 🎉")
    st.toast("Congrats, You Win! 🎉", icon="🎉")


