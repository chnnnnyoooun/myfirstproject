import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd

st.set_page_config(page_title="친구 매치 프로그램", layout="wide")

st.title("🧑‍🤝‍🧑 또래 친구 매치 프로그램")
st.write("나와 비슷한 관심사와 또래의 친구들을 지도에서 찾아보세요!")

# 데이터 파일명
DATA_FILE = "friends_data.csv"

# 입력 폼
with st.form("user_info_form"):
    st.subheader("📋 나의 정보 입력")
    name = st.text_input("이름")
    age = st.number_input("나이", min_value=10, max_value=100, step=1)
    gender = st.selectbox("성별", ["남성", "여성", "기타"])
    mbti = st.text_input("MBTI (예: INFP, ESTJ 등)").upper()
    region = st.text_input("지역 또는 주소 입력 (지도에서 위치를 지정하세요)")
    latitude = st.number_input("위도 (지도를 클릭해 위치 자동 입력 가능)", format="%.6f")
    longitude = st.number_input("경도", format="%.6f")
    instagram = st.text_input("인스타그램 아이디 (선택사항)", placeholder="@yourid")
    interests = st.text_area("관심 분야 (쉼표로 구분)", placeholder="예: 음악, 영화, 운동")

    submitted = st.form_submit_button("정보 등록하기")

    if submitted:
        if name and mbti and region and latitude and longitude:
            new_data = pd.DataFrame([{
                "이름": name,
                "나이": age,
                "성별": gender,
                "MBTI": mbti,
                "지역": region,
                "위도": latitude,
                "경도": longitude,
                "인스타": instagram,
                "관심분야": interests
            }])
            try:
                existing = pd.read_csv(DATA_FILE)
                updated = pd.concat([existing, new_data], ignore_index=True)
            except FileNotFoundError:
                updated = new_data

            updated.to_csv(DATA_FILE, index=False)
            st.success("정보가 성공적으로 등록되었습니다!")
        else:
            st.error("모든 필수 정보를 입력해주세요!")

# 지도 출력
st.subheader("🗺️ 친구 지도 보기")

# 지도 기본 위치 설정
map_center = [37.5665, 126.9780]  # 서울 중심

m = folium.Map(location=map_center, zoom_start=11)

# 저장된 데이터 로딩 및 마커 표시
try:
    data = pd.read_csv(DATA_FILE)
    for _, row in data.iterrows():
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=(
                f"이름: {row['이름']}<br>"
                f"나이: {row['나이']}<br>"
                f"성별: {row['성별']}<br>"
                f"MBTI: {row['MBTI']}<br>"
                f"관심: {row['관심분야']}<br>"
                f"인스타: {row['인스타']}"
            ),
            tooltip=row["이름"]
        ).add_to(m)
except FileNotFoundError:
    st.warning("아직 등록된 친구 정보가 없습니다.")

# 지도 렌더링
st_folium(m, width=700, height=500)
