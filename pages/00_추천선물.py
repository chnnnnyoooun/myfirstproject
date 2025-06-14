import streamlit as st

# MBTI별 선물 추천 데이터
mbti_gift_data = {
    "INTJ": [
        ("전략 보드게임", "논리적 사고를 즐기는 INTJ에게 창의적인 전략 보드게임은 도전정신을 자극합니다."),
        ("프리미엄 노트북 스탠드", "효율성을 중시하는 INTJ에게 생산성을 높이는 아이템은 최고의 선물입니다."),
        ("SF 소설 세트", "지적 탐구를 즐기는 INTJ는 공상과학 세계관에 빠지는 것을 좋아합니다."),
    ],
    "INTP": [
        ("철학책", "호기심 많은 INTP에게는 깊이 있는 철학서가 사고력을 자극합니다."),
        ("미니 드론", "기술과 실험을 좋아하는 INTP에게 새로운 장난감은 탐구의 대상입니다."),
        ("프로그래밍 키트", "창의력과 논리를 동시에 만족시켜주는 DIY 키트입니다."),
    ],
    "ENTJ": [
        ("고급 수첩", "계획과 전략에 강한 ENTJ에게는 품질 좋은 수첩이 필수입니다."),
        ("시간 관리 플래너", "효율을 중시하는 ENTJ에게 일정 관리 도구는 최고의 무기입니다."),
        ("비즈니스 서적", "리더십을 지향하는 ENTJ는 성장과 성공에 대한 책을 선호합니다."),
    ],
    "ENTP": [
        ("아이디어 노트", "창의력 넘치는 ENTP에게 자유롭게 아이디어를 정리할 수 있는 노트는 필수입니다."),
        ("독특한 퍼즐", "지적 호기심이 강한 ENTP는 새로운 도전을 즐깁니다."),
        ("모바일 게임 기프트카드", "새롭고 다양한 것을 시도하길 좋아하는 ENTP에게는 게임도 실험의 장입니다."),
    ],
    "INFJ": [
        ("감성 소설", "깊은 내면의 세계를 탐험하는 INFJ는 감정을 자극하는 이야기를 좋아합니다."),
        ("아로마 디퓨저", "내면의 평화를 중시하는 INFJ에게 향기는 안정감을 줍니다."),
        ("명상 가이드북", "조용한 자기 성찰을 위한 좋은 선물이 됩니다."),
    ],
    "INFP": [
        ("감성적인 다이어리", "감정을 표현하고 기록하는 것을 좋아하는 INFP에게 감성적인 다이어리는 좋은 동반자입니다."),
        ("캔들 세트", "내면의 평화를 중시하는 INFP에게 향기로운 캔들은 힐링을 선사합니다."),
        ("수제 초콜릿", "작고 정성스러운 선물은 INFP의 따뜻한 마음에 깊은 인상을 남깁니다."),
    ],
    "ENFJ": [
        ("감사 카드 세트", "사람들과의 관계를 중시하는 ENFJ에게는 감사를 표현할 수 있는 도구가 좋습니다."),
        ("리더십 서적", "타인을 이끄는 데 관심이 많은 ENFJ에게는 자기계발서가 좋은 선택입니다."),
        ("고급 펜 세트", "세심한 표현을 중시하는 ENFJ에게 어울리는 선물입니다."),
    ],
    "ENFP": [
        ("여행 용품 세트", "자유로운 ENFP에게 여행은 최고의 경험이자 선물입니다."),
        ("컬러링 북", "창의적인 감성을 표현할 수 있는 즐거운 활동입니다."),
        ("DIY 키트", "무언가를 직접 만들며 창의력을 발휘할 수 있는 선물입니다."),
    ],
    "ISTJ": [
        ("고급 펜", "실용적이고 정확한 ISTJ는 기능성과 품질을 중요시합니다."),
        ("정리함", "정돈된 것을 좋아하는 ISTJ에게는 실용적인 수납 아이템이 적합합니다."),
        ("클래식 시계", "시간 약속을 중요하게 생각하는 ISTJ에게 어울리는 선물입니다."),
    ],
    "ISFJ": [
        ("따뜻한 담요", "배려심이 깊은 ISFJ에게는 포근한 선물이 잘 어울립니다."),
        ("가족 앨범", "소중한 사람들과의 추억을 담는 것을 좋아합니다."),
        ("홈카페 머그세트", "잔잔한 일상을 즐기는 ISFJ에게 딱 맞는 선물입니다."),
    ],
    "ESTJ": [
        ("데스크 정리 도구", "체계적인 ESTJ에게는 사무 환경을 깔끔하게 정리할 수 있는 아이템이 좋습니다."),
        ("비즈니스 백", "실용성과 전문성을 동시에 만족시키는 선물입니다."),
        ("실용적인 전자기기", "ESTJ는 실용적인 기능을 중요하게 생각합니다."),
    ],
    "ESFJ": [
        ("플래너 세트", "계획 세우는 것을 좋아하는 ESFJ에게 잘 꾸며진 플래너는 좋은 친구가 됩니다."),
        ("홈파티 식기세트", "사교적인 ESFJ는 사람들과의 시간을 소중히 여깁니다."),
        ("감사 카드 세트", "배려심 깊은 ESFJ는 감사 표현을 자주 하는 편입니다."),
    ],
    "ISTP": [
        ("멀티툴 키트", "도구를 다루는 데 능숙한 ISTP는 실용적인 장비를 선호합니다."),
        ("스포츠 액세서리", "액티브한 활동을 즐기는 ISTP에게 적합한 선물입니다."),
        ("DIY 조립 키트", "손으로 만드는 것을 좋아하는 ISTP에게 재미를 선사합니다."),
    ],
    "ISFP": [
        ("예술용 스케치북", "감성적이고 표현을 중시하는 ISFP에게는 창작도구가 제격입니다."),
        ("자연 테마 향초", "자연과 조화를 이루는 삶을 즐기는 ISFP에게 편안함을 줍니다."),
        ("핸드메이드 액세서리", "유니크한 아이템을 선호하는 ISFP의 취향에 맞습니다."),
    ],
    "ESTP": [
        ("스마트워치", "즉흥적인 활동을 즐기는 ESTP에게 활동을 추적하는 아이템은 실용적입니다."),
        ("액션 카메라", "모험을 기록할 수 있는 카메라는 ESTP에게 잘 맞습니다."),
        ("게임 콘솔", "에너지 넘치는 ESTP에게는 빠르고 재미있는 게임이 잘 어울립니다."),
    ],
    "ESFP": [
        ("무선 스피커", "즐거움을 추구하는 ESFP는 음악과 함께하는 순간을 사랑합니다."),
        ("폴라로이드 카메라", "순간을 기록하고 공유하는 것을 좋아합니다."),
        ("화려한 액세서리", "자기 표현에 적극적인 ESFP에게는 눈에 띄는 선물이 좋습니다."),
    ],
}

# Streamlit UI
st.title("🎁 MBTI 선물 추천기")
st.write("당신의 MBTI를 선택하면, 어울리는 선물 3가지를 추천해드립니다!")

selected_mbti = st.selectbox("MBTI를 선택하세요", list(mbti_gift_data.keys()))

if selected_mbti:
    st.subheader(f"{selected_mbti} 유형을 위한 선물 추천 🎉")
    gifts = mbti_gift_data[selected_mbti]
    for idx, (gift, description) in enumerate(gifts, start=1):
        st.markdown(f"**{idx}. {gift}**")
        st.write(f"- {description}")
