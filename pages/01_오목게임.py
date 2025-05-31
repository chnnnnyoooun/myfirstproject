import streamlit as st

st.title("🎮 오목 게임 (돌 크기만 키우기)")

BOARD_SIZE = 15

if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.turn = "●"

for i in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for j in range(BOARD_SIZE):
        cell = st.session_state.board[i][j]
        display_text = cell if cell != "" else " "
        # 버튼 텍스트 크기 키우기 위해 유니코드 돌 이모지로 대체해보겠습니다.
        if cell == "●":
            display_text = "⬤"  # 검은 큰 원
        elif cell == "○":
            display_text = "◯"  # 하얀 큰 원

        if display_text == " ":
            if cols[j].button(" ", key=f"{i}-{j}"):
                st.session_state.board[i][j] = st.session_state.turn
                st.session_state.turn = "○" if st.session_state.turn == "●" else "●"
                st.experimental_rerun()
        else:
            # 버튼 대신 마크다운으로 크게 보여주기 (돌은 클릭 불가)
            cols[j].markdown(f"<p style='font-size:30px; text-align:center; margin:0'>{display_text}</p>", unsafe_allow_html=True)

st.markdown("---")
st.write(f"지금은 **{st.session_state.turn}** 차례입니다.")

if st.button("🔄 게임 초기화"):
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.turn = "●"
    st.experimental_rerun()
