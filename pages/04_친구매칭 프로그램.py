import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from geopy.geocoders import Nominatim

st.set_page_config(page_title="친구 매치 프로그램", layout="wide")

st.title("🧑‍🤝‍🧑 또래 친구 매치 프로그램")
st.write("지도에서 위치를 선택하고, 친구 정보를 입력하세요!")

DATA_FILE = "friends_data.csv"
geolocator = Nominatim(user_agent="friend_match_app")

# 지도 클릭으로 위치 선택
st.subheader("🗺️ 지도에서 내 위치를 선택하세요")
map_center = [37.5665, 126.9780]  # 서울 중심
m = folium.Map(location=map_center, zoom_start=11)
location_info = st_folium(m, width=700, height=500)

clicked_lat = None
clicked_lon = None
clicked_address = ""

if location_info and location_info["last_clicked"]:
    clicked_lat = location_info["last_clicked"]["lat"]
    clicked_lon = location_info["last_clicked"]["lng"]
    try:
        location = geolocator.reverse((clicked_lat, clicked_lon))
        clicked_address = location.address
        st.success(f"선택된 위치 주소: {clicked_address}")
    except:
        st.error("주소 변환에 실패했습니다. 다시 시도해주세요.")

# 입력 폼
with st.form("user_info_form"):
    st.subheader("📋 나의 정보 입력")
    name = st.text_input("👩이름")
    age = st.number_input("🍰나이", min_value=10, max_value=100, step=1)
    gender = st.selectbox("👩🏻‍🤝‍🧑🏻성별", ["남성", "여성", "기타"])
    mbti = st.text_input("🧠MBTI (예: INFP, ESTJ 등)").upper()
    instagram = st.text_input("📷인스타그램 아이디 (선택사항)", placeholder="@yourid").replace("@", "")
    interests = st.text_area("🎯관심 분야 (쉼표로 구분)", placeholder="예: 음악, 영화, 운동")

    submitted = st.form_submit_button("정보 등록하기")

    if submitted:
        if name and mbti and clicked_lat and clicked_lon:
            new_data = pd.DataFrame([{
                "이름": name,
                "나이": age,
                "성별": gender,
                "MBTI": mbti,
                "지역": clicked_address,
                "위도": clicked_lat,
                "경도": clicked_lon,
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
            st.error("모든 필수 정보를 입력하고 지도를 클릭해주세요.")

# 친구 마커 지도
st.subheader("👥 등록된 친구 보기")
friend_map = folium.Map(location=map_center, zoom_start=11)

try:
    data = pd.read_csv(DATA_FILE)
    for _, row in data.iterrows():
        insta_id = row['인스타']
        insta_link = f"https://instagram.com/{insta_id}" if insta_id else "없음"

        popup_html = f"""
        <b>이름:</b> {row['이름']}<br>
        <b>나이:</b> {row['나이']}<br>
        <b>성별:</b> {row['성별']}<br>
        <b>MBTI:</b> {row['MBTI']}<br>
        <b>지역:</b> {row['지역']}<br>
        <b>관심분야:</b> {row['관심분야']}<br>
        <b>인스타그램:</b> {"<a href='" + insta_link + "' target='_blank'>@" + insta_id + "</a>" if insta_id else "없음"}
        """
        folium.Marker(
            location=[row["위도"], row["경도"]],
            popup=folium.Popup(popup_html, max_width=300),
            tooltip=row["이름"]
        ).add_to(friend_map)
except FileNotFoundError:
    st.warning("등록된 친구가 없습니다.")

location_info = st_folium(m, width=700, height=500, key="location_picker")
...
st_folium(friend_map, width=700, height=500, key="friend_map")
