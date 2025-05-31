import streamlit as st

st.set_page_config(page_title="오목 게임", layout="wide")
st.title("🎮 오목 게임 (돌 크기 키우기 & 판 작게)")

BOARD_SIZE = 10  # 10x10 판

if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.turn = "●"

def place_stone(i, j):
    if st.session_state.board[i][j] == "":
        st.session_state.board[i][j] = st.session_state.turn
        st.session_state.turn = "○" if st.session_state.turn == "●" else "●"
        st.experimental_rerun()

for i in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for j in range(BOARD_SIZE):
        cell = st.session_state.board[i][j]
        if cell == "":
            if cols[j].button(" ", key=f"{i}-{j}"):
                place_stone(i, j)
        else:
            stone_html = f"<p style='font-size: 32px; text-align:center; margin:0'>{cell}</p>"
            cols[j].markdown(stone_html, unsafe_allow_html=True)

st.markdown("---")
st.write(f"지금은 **{st.session_state.turn}** 차례입니다.")

if st.button("🔄 게임 초기화"):
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.turn = "●"
    st.experimental_rerun()
