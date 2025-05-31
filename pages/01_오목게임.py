import streamlit as st

st.set_page_config(page_title="오목 게임", layout="wide")
st.title("🎮 오목 게임 (Streamlit만 사용)")

# 보드 크기 정의
BOARD_SIZE = 15

# 초기 세션 상태 설정
if "board" not in st.session_state:
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.turn = "●"  # 흑돌 먼저

# 보드 그리기
for i in range(BOARD_SIZE):
    cols = st.columns(BOARD_SIZE)
    for j in range(BOARD_SIZE):
        cell = st.session_state.board[i][j]
        if cell == "":
            if cols[j].button(" ", key=f"{i}-{j}"):
                st.session_state.board[i][j] = st.session_state.turn
                # 턴 변경
                st.session_state.turn = "○" if st.session_state.turn == "●" else "●"
                st.rerun()  # 즉시 반영되도록 새로고침
        else:
            cols[j].markdown(f"**{cell}**")

# 현재 턴 표시
st.markdown("---")
st.write(f"지금은 **{st.session_state.turn}** 차례입니다.")

# 리셋 버튼
if st.button("🔄 게임 초기화"):
    st.session_state.board = [["" for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    st.session_state.turn = "●"
    st.rerun()
