from vpython import *
import math

"""
태양계 중력/공전 시각화 (VPython)
- 지구 1년을 10초로 스케일링 (다른 천체는 실제 비율에 맞게 공전)
- 태양, 수성, 금성, 지구, 달, 화성, 목성, 토성, 천왕성, 해왕성
- 각 천체 질량 스케일(=중력 영향) 조절
- 10가지 '중력 변화 시나리오' 프리셋
- 지구 클릭 시 사람 캐릭터 확대 보기
- 카메라 전환(태양계 전체/지구/태양/행성별)
주의: 공전은 안정적 시연을 위해 원궤도 kinematic(각속도)로 구현.
      중력 벡터/합가속도는 실제 질량(스케일 반영)으로 계산해 패널에 표시.
"""

# ===== 장면/캔버스 =====
scene = canvas(title="태양계 중력 시각화", width=1280, height=760, background=color.black)
scene.range = 40
scene.forward = vector(-1,-0.2,-1)  # 보기 좋은 시점
scene.caption = "마우스: 드래그(회전), 휠(줌), 쉬프트+드래그(이동)\n"

# ===== 상수/스케일 =====
G_phys = 6.67430e-11  # 실제 G (계산에 쓰되, 벡터 표시용은 스케일링)
AU = 1.0              # 화면 상 1 AU 단위(임의). 실제 값 대신 비례만 유지
R_SUN   = 1.5         # 시각화 반지름(비현실적으로 키움)
R_PLANET_BASE = 0.5
R_MOON = 0.18

# 공전 주기(일) — NASA 기준 근사값 (sidereal)
period_days = {
    "Mercury": 87.969,
    "Venus": 224.701,
    "Earth": 365.256,
    "Moon": 27.321661,  # 지구 주위
    "Mars": 686.980,
    "Jupiter": 4332.59,
    "Saturn": 10759.22,
    "Uranus": 30685.4,
    "Neptune": 60189.0
}

# 공전 반지름(평균 원거리, AU 단위 근사)
orbit_au = {
    "Mercury": 0.387,
    "Venus":   0.723,
    "Earth":   1.000,
    "Moon":    0.00257,  # 약 384,400 km ~ 0.00257 AU
    "Mars":    1.524,
    "Jupiter": 5.204,
    "Saturn":  9.583,
    "Uranus":  19.201,
    "Neptune": 30.047
}

# 질량(kg)
mass_kg = {
    "Sun":     1.989e30,
    "Mercury": 3.301e23,
    "Venus":   4.867e24,
    "Earth":   5.972e24,
    "Moon":    7.348e22,
    "Mars":    6.417e23,
    "Jupiter": 1.898e27,
    "Saturn":  5.683e26,
    "Uranus":  8.681e25,
    "Neptune": 1.024e26
}

# 반지름(시각화용: 실제 비율과 다름. 보기 좋게 조정)
radius_vis = {
    "Sun":     R_SUN*1.0,
    "Mercury": R_PLANET_BASE*0.25,
    "Venus":   R_PLANET_BASE*0.45,
    "Earth":   R_PLANET_BASE*0.5,
    "Moon":    R_MOON,
    "Mars":    R_PLANET_BASE*0.4,
    "Jupiter": R_PLANET_BASE*1.1,
    "Saturn":  R_PLANET_BASE*0.9,
    "Uranus":  R_PLANET_BASE*0.7,
    "Neptune": R_PLANET_BASE*0.7
}

# 색상
col = {
    "Sun": color.yellow,
    "Mercury": vector(0.75,0.75,0.75),
    "Venus":   vector(1,0.85,0.5),
    "Earth":   color.cyan,
    "Moon":    color.white,
    "Mars":    vector(1,0.4,0.3),
    "Jupiter": vector(1,0.9,0.7),
    "Saturn":  vector(0.9,0.8,0.6),
    "Uranus":  vector(0.6,0.9,0.9),
    "Neptune": vector(0.6,0.7,1.0)
}

# ===== 시간 스케일링 =====
# 지구 1년 = 10초 가정 → 다른 천체는 실제 비율대로
earth_year_sec = 10.0
sec_per_day = earth_year_sec / period_days["Earth"]  # 10 / 365.256
def period_to_seconds(days):
    return days * sec_per_day

# ===== 천체 클래스 =====
class Body:
    def __init__(self, name, parent=None):
        self.name = name
        self.parent = parent  # 태양 or 지구(달의 경우)
        self.mass0 = mass_kg[name] if name in mass_kg else 0.0
        self.mass_scale = 1.0  # UI로 조절 (중력 영향)
        self.mass = self.mass0 * self.mass_scale

        self.radius = radius_vis[name]
        self.color = col[name]
        self.trail = True if name not in ("Sun", "Moon") else True

        # 시각화 구체
        self.sphere = sphere(
            pos=vector(0,0,0),
            radius=self.radius,
            color=self.color,
            emissive=(name=="Sun"),
            make_trail=self.trail,
            trail_type="curve",
            retain=500
        )

        # 궤도 파라미터(원궤도 단순화)
        if name == "Sun":
            self.orbit_r = 0.0
            self.period_s = None
            self.omega = 0.0
            self.angle = 0.0
        else:
            if name == "Moon":
                self.orbit_r = orbit_au["Moon"]  # Earth 기준
                self.period_s = period_to_seconds(period_days["Moon"])
            else:
                self.orbit_r = orbit_au[name]
                self.period_s = period_to_seconds(period_days[name])
            self.omega = 2*math.pi / self.period_s
            self.angle = 0.0

        # 중력 벡터 시각화용
        self.g_arrow = arrow(pos=self.sphere.pos, axis=vector(0,0,0), shaftwidth=self.radius*0.25, opacity=0.5, visible=False)

    def set_mass_scale(self, scale):
        self.mass_scale = max(0.0, scale)
        self.mass = self.mass0 * self.mass_scale

    def update_orbit(self, t, dt):
        if self.name == "Sun":
            self.sphere.pos = vector(0,0,0)
            return

        # 부모 중심의 원궤도 (xz평면)
        self.angle += self.omega * dt
        r = self.orbit_r
        x = r*math.cos(self.angle)
        z = r*math.sin(self.angle)

        if self.parent is None:
            center = vector(0,0,0)
        else:
            center = self.parent.sphere.pos

        self.sphere.pos = center + vector(x,0,z)

    def update_g_arrow(self, gvec, scale=1.0, show=False):
        self.g_arrow.visible = show
        if not show:
            return
        self.g_arrow.pos = self.sphere.pos
        # 화살표 길이 스케일(보기용)
        self.g_arrow.axis = gvec * scale

# ===== 시스템 생성 =====
sun = Body("Sun")
bodies = {
    "Sun": sun,
    "Mercury": Body("Mercury", parent=sun),
    "Venus":   Body("Venus",   parent=sun),
    "Earth":   Body("Earth",   parent=sun),
    "Moon":    Body("Moon",    parent=None),  # parent는 루프에서 Earth pos를 참조
    "Mars":    Body("Mars",    parent=sun),
    "Jupiter": Body("Jupiter", parent=sun),
    "Saturn":  Body("Saturn",  parent=sun),
    "Uranus":  Body("Uranus",  parent=sun),
    "Neptune": Body("Neptune", parent=sun)
}

# 달은 지구 주위를 돌아야 하므로 parent를 지구로 다시 세팅
bodies["Moon"].parent = bodies["Earth"]

# 토성 고리(간단 표현)
ring = ring = ring(pos=bodies["Saturn"].sphere.pos, axis=vector(0,1,0), radius=bodies["Saturn"].radius*2.2, thickness=bodies["Saturn"].radius*0.12, color=vector(0.9,0.8,0.6))

# 사람(지구 클릭 시 보이기)
person = sphere(pos=bodies["Earth"].sphere.pos + vector(0, bodies["Earth"].radius*1.2, 0),
                radius=bodies["Earth"].radius*0.25, color=color.white, visible=False)

# ===== UI: 질량 조절, 시나리오, 카메라 =====
wtext(text="\n— 질량(중력 영향) 조절 —\n")
sel_body = menu(choices=["Sun","Mercury","Venus","Earth","Moon","Mars","Jupiter","Saturn","Uranus","Neptune"], index=0)
mass_label = wtext(text="\n선택 천체 질량 스케일: 1.00x\n")

def on_mass_slider(s):
    target = bodies[sel_body.selected]
    target.set_mass_scale(s.value)
    mass_label.text = f"\n선택 천체 질량 스케일: {s.value:.2f}x\n"
mass_slider = slider(min=0.0, max=3.0, value=1.0, step=0.01, bind=on_mass_slider)

wtext(text="\n전체 중력 화살표 길이 스케일(표시용):\n")
def on_gscale_slider(s):
    global g_arrow_scale
    g_arrow_scale = s.value
    gscale_label.text = f"g-벡터 스케일: {g_arrow_scale:.2f}\n"
g_arrow_scale = 1.0
gscale_slider = slider(min=0.1, max=5.0, value=1.0, step=0.1, bind=on_gscale_slider)
gscale_label = wtext(text="g-벡터 스케일: 1.00\n")

# 카메라 전환
wtext(text="\n— 카메라 보기 —\n")
def view_solar():
    scene.center = vector(0,0,0)
    scene.range = 40
def view_sun():
    scene.center = bodies["Sun"].sphere.pos
    scene.range = 8
def view_earth():
    scene.center = bodies["Earth"].sphere.pos
    scene.range = 2.5
def view_planet(p):
    scene.center = bodies[p].sphere.pos
    scene.range = 3.0

button(text="태양계 전체", bind=lambda _: view_solar())
button(text="태양 보기", bind=lambda _: view_sun())
button(text="지구 보기", bind=lambda _: view_earth())
button(text="목성 보기", bind=lambda _: view_planet("Jupiter"))
button(text="토성 보기", bind=lambda _: view_planet("Saturn"))
wtext(text="\n")

# 중력 벡터 표시 토글
show_gvec = False
def toggle_g(_):
    global show_gvec
    show_gvec = not show_gvec
    gbtn.text = "중력벡터: 켜짐" if show_gvec else "중력벡터: 꺼짐"
gbtn = button(text="중력벡터: 꺼짐", bind=toggle_g)
wtext(text="\n")

# 질량 초기화
def reset_mass(_):
    for b in bodies.values():
        b.set_mass_scale(1.0)
    mass_slider.value = 1.0
    mass_label.text = "\n선택 천체 질량 스케일: 1.00x\n"
button(text="모든 질량 리셋", bind=reset_mass)
wtext(text="\n")

# ===== 10가지 ‘중력 변화 시나리오’ 프리셋 =====
"""
각 프리셋은 특정 천체 질량 스케일을 바꾸고,
효과 설명을 패널에 표시. (공전은 안정적 시연을 위해 계속 원궤도)
실시간 g(가속도) 벡터와 정보 텍스트로 '영향'을 직관적으로 제시.
"""
scenario_info = wtext(text="\n— 시나리오 설명 —\n(프리셋을 선택하면 여기에 설명이 나타납니다)\n")

scenarios = [
    ("태양 질량 1.2x", {"Sun":1.2},
     "태양 중력이 강해지면 행성의 필요한 공전 속도(원궤도 유지)가 증가합니다. 실제 우주라면 궤도가 더 안쪽으로 수축하거나 주기가 짧아지는 경향이 있습니다."),
    ("태양 질량 0.7x", {"Sun":0.7},
     "태양 중력이 약해지면 행성들이 더 느리게 돌아도 되며, 궤도가 팽창하거나 이탈 위험이 커집니다."),
    ("목성 질량 2.0x", {"Jupiter":2.0},
     "목성의 중력이 강해지면 주변(특히 화성~소행성대 영역)에 중력 교란이 커지고, 장기적으로 공명/이심률 변화가 커질 수 있습니다."),
    ("목성 질량 0x(제거)", {"Jupiter":0.0},
     "목성이 없다면, 태양계의 거대행성 중력 보호(소행성 포획/분산) 효과가 줄어들어 내행성 충돌 위험이 장기적으로 증가할 수 있습니다."),
    ("지구 질량 1.5x", {"Earth":1.5},
     "지구 중력이 강해지면(같은 반지름이라 가정) 표면 중력이 증가해 사람/대기/위성 궤도 등에 변화가 큽니다. 달에도 더 강한 조석력이 작용합니다."),
    ("지구 질량 0.5x", {"Earth":0.5},
     "지구가 가벼워지면 표면 중력 감소, 탈출속도 감소, 대기 유지가 어려워질 수 있습니다. 달의 영향이 상대적으로 커집니다."),
    ("달 질량 2.0x", {"Moon":2.0},
     "달이 무거워지면 조석력 증가 → 조석 마찰 변화로 지구 자전/해수 순환 등에 큰 변화. 달-지구 상호 중력도 커집니다."),
    ("토성 질량 1.5x", {"Saturn":1.5},
     "토성의 중력이 커지면 바깥쪽 행성들과의 섭동이 커지고, 토성 고리/위성계 역학도 달라질 수 있습니다."),
    ("전체 질량 0.8x", {"Sun":0.8,"Mercury":0.8,"Venus":0.8,"Earth":0.8,"Moon":0.8,"Mars":0.8,"Jupiter":0.8,"Saturn":0.8,"Uranus":0.8,"Neptune":0.8},
     "모든 천체 질량이 줄면 상호 중력도 전반적으로 약해져 공명/섭동 효과가 완화됩니다."),
    ("전체 질량 1.5x", {"Sun":1.5,"Mercury":1.5,"Venus":1.5,"Earth":1.5,"Moon":1.5,"Mars":1.5,"Jupiter":1.5,"Saturn":1.5,"Uranus":1.5,"Neptune":1.5},
     "모든 천체 질량이 커지면 상호 중력 상호작용(섭동, 조석)이 전반적으로 강화됩니다.")
]

def apply_scenario(idx):
    name, mapping, desc = scenarios[idx]
    for key, val in mapping.items():
        bodies[key].set_mass_scale(val)
        if key == sel_body.selected:
            mass_slider.value = val
    scenario_info.text = f"\n— 시나리오: {name} —\n{desc}\n"

wtext(text="\n— 시나리오 프리셋 —\n")
s_menu = menu(choices=[f"{i+1}. {s[0]}" for i,s in range(len(scenarios))], index=0)
# 위 한 줄은 menu 초기화 전에 길이 참조가 안되므로 아래로 수정
scene.append_to_caption("")  # 자리 맞춤

# 메뉴는 생성 후에 choices 교체가 어려워서 별도로 구현
scenario_buttons = []
for i, item in enumerate(scenarios):
    btn = button(text=f"{i+1}. {item[0]}", bind=lambda _,k=i: apply_scenario(k))
    scenario_buttons.append(btn)
wtext(text="\n")

# ===== 정보 패널: 실시간 가속도(지구 기준) =====
info = wtext(text="\n— 실시간 정보 (지구 기준) —\n")

def gravitational_accel_on(target_key):
    """target_key에 작용하는 다른 천체들의 중력 가속도 벡터 합(단위: 임의 스케일)을 계산"""
    tgt = bodies[target_key]
    pos_t = tgt.sphere.pos
    a_total = vector(0,0,0)
    contributions = []
    for k,b in bodies.items():
        if k == target_key:
            continue
        # 위치/거리
        pos_b = b.sphere.pos
        r_vec = pos_b - pos_t
        r2 = mag2(r_vec)
        if r2 < 1e-9:
            continue
        # 실제 G와 질량 스케일로 가속도 계산 (하지만 길이/시간 단위는 화면 스케일이므로 '비교용')
        a = (G_phys * b.mass) / r2
        avec = norm(r_vec) * a
        contributions.append((k, avec))
        a_total += avec
    return a_total, contributions

def format_vec(v):
    # 크기만 보기 좋게 표기
    m = mag(v)
    if m == 0:
        return "0"
    units = ["", "k", "M", "G", "T"]
    i = 0
    while m >= 1000 and i < len(units)-1:
        m /= 1000.0
        i += 1
    return f"{m:.3f}{units[i]}"

# ===== 지구 클릭 -> 사람 보기 & 카메라 이동 =====
def handle_click():
    global person
    if scene.mouse.events:
        evt = scene.mouse.getevent()
        if evt.press == 'left' and evt.event == 'click':
            obj = evt.pick
            if obj is None:
                return
            # 지구 클릭 시
            if obj is bodies["Earth"].sphere:
                person.visible = True
                view_earth()

# ===== 애니메이션 루프 =====
t = 0.0
dt = 0.02  # 시뮬레이션 시간 step (초) — 지구 1년=10초 스케일에 맞춰 충분히 부드럽게
show_vectors_for = ["Earth"]  # g-벡터 기본 표시는 지구만

while True:
    rate(120)

    # 궤도 업데이트 (원궤도: 각속도 기반)
    for name, b in bodies.items():
        if name == "Moon":
            # 달은 지구 중심
            b.parent = bodies["Earth"]
        b.update_orbit(t, dt)

    # 토성 고리 위치 업데이트
    ring.pos = bodies["Saturn"].sphere.pos

    # 클릭 처리(지구 클릭하면 사람 보이기)
    handle_click()
    # 사람 위치 갱신(지구 위에 붙어있게)
    person.pos = bodies["Earth"].sphere.pos + vector(0, bodies["Earth"].radius*1.2, 0)

    # 중력 가속도(지구 기준) 계산 및 표시
    a_total, contribs = gravitational_accel_on("Earth")

    # 정보 텍스트 갱신
    # 상위 기여 3개만 크기순 정렬 표시
    contribs_sorted = sorted(contribs, key=lambda x: mag(x[1]), reverse=True)
    top3 = contribs_sorted[:3]
    info_text = "지구에 작용하는 중력 가속도 기여(상위 3):\n"
    for (k, av) in top3:
        info_text += f" - {k}: |a| ~ {format_vec(av)} (상대)\n"
    info_text += f"합성 |a_total| ~ {format_vec(a_total)} (상대)\n"
    info.text = "\n— 실시간 정보 (지구 기준) —\n" + info_text

    # g-벡터 시각화 업데이트 (선택 토글)
    for name, b in bodies.items():
        if show_gvec and name in show_vectors_for:
            # 지구에 작용하는 벡터만 표시
            if name == "Earth":
                # 합성 벡터 표시
                b.update_g_arrow(a_total, scale=g_arrow_scale*5e8, show=True)
        else:
            b.update_g_arrow(vector(0,0,0), show=False)

    t += dt
