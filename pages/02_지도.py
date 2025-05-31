import streamlit as st
import folium
from streamlit_folium import st_folium

# 여행지 데이터 (이름, 간단 설명, 위도, 경도)
places = [
    {"name": "서울 (N서울타워)", "desc": "한국의 수도, 멋진 전망대와 도시 풍경", "lat": 37.5512, "lon": 126.9882},
    {"name": "부산 (해운대 해변)", "desc": "아름다운 해변과 활기찬 도시 분위기", "lat": 35.1587, "lon": 129.1604},
    {"name": "제주도 (성산일출봉)", "desc": "자연경관과 신비로운 일출 명소", "lat": 33.4586, "lon": 126.9407},
    {"name": "경주 (불국사)", "desc": "역사와 문화의 보고, 유네스코 세계유산", "lat": 35.7904, "lon": 129.3780},
    {"name": "강릉 (경포대)", "desc": "바다와 호수가 어우러진 휴양지", "lat": 37.7519, "lon": 128.8959},
    {"name": "인천 (월미도)", "desc": "바다를 즐기고 맛집도 많은 관광지", "lat": 37.4761, "lon": 126.6155},
    {"name": "전주 (한옥마을)", "desc": "전통 한옥과 맛있는 음식의 고장", "lat": 35.8151, "lon": 127.1190},
    {"name": "속초 (설악산)", "desc": "사계절 내내 아름다운 산과 자연", "lat": 38.1198, "lon": 128.4650},
    {"name": "여수 (오동도)", "desc": "바다와 섬의 조화로운 풍경", "lat": 34.7600, "lon": 127.6620},
    {"name": "대구 (동성로)", "desc": "쇼핑과 먹거리가 풍부한 도시 중심가", "lat": 35.8714, "lon": 128.6014}
]

st.set_page_config(page_title="한국인이 사랑하는 여행지 TOP10", layout="wide")

st.markdown("<h1 style='text-align: center; color: #f72585;'>한국인이 사랑하는 여행지 TOP 10</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; font-size:18px; color:#720026;'>아름다운 여행지들을 소개합니다 💖</p>", unsafe_allow_html=True)

# 지도 초기 위치 (한국 중심)
m = folium.Map(location=[36.5, 127.5], zoom_start=7)

# 각 여행지 마커 찍기 + 팝업 스타일링
for place in places:
    folium.Marker(
        location=[place["lat"], place["lon"]],
        popup=f"<b>{place['name']}</b><br>{place['desc']}",
        icon=folium.Icon(color="pink", icon="heart", prefix='fa')
    ).add_to(m)

# 지도 출력 (streamlit_folium 활용)
st_folium(m, width=700, height=500)

# 여행지 리스트 예쁘게 출력
st.markdown("---")
st.markdown("<h3 style='color:#f72585;'>여행지 소개</h3>", unsafe_allow_html=True)

for i, place in enumerate(places, 1):
    st.markdown(f"""
    <div style="background: #ffe4f0; border-radius: 15px; padding: 15px; margin-bottom: 10px;">
    <h4 style='color:#d0006f;'>{i}. {place['name']}</h4>
    <p style='font-size:16px; color:#720026;'>{place['desc']}</p>
    </div>
    """, unsafe_allow_html=True)
