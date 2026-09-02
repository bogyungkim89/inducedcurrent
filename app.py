import streamlit as st
import uuid
import random

# 페이지 기본 설정은 파일 최상단에 위치해야 합니다.
st.set_page_config(page_title="전자기 유도 학습 앱", page_icon="🧲", layout="wide")

# ==========================================
# 공통 기능: 애니메이션 HTML 생성 및 풍선 효과
# ==========================================
def get_animation_html(magnet_action, coil_top_pole, ext_dir, external_device, q1_solved, q2_solved):
    unique_id = uuid.uuid4().hex

    # 자석 색상 및 극성
    if "N극" in magnet_action:
        top_color, bottom_color = "#3498db", "#e74c3c"
        top_text, bottom_text = "S", "N"
    else:
        top_color, bottom_color = "#e74c3c", "#3498db"
        top_text, bottom_text = "N", "S"

    # 애니메이션 움직임 및 '운동 방향' 화살표 (오른쪽)
    if "가까워짐" in magnet_action:
        anim_name = "approach"
        motion_arrow = """
        <line x1="245" y1="50" x2="245" y2="90" stroke="#333" stroke-width="4" stroke-linecap="round"/>
        <polygon points="235,80 255,80 245,100" fill="#333"/>
        <text x="245" y="120" font-size="14" font-weight="bold" fill="#333" text-anchor="middle">운동 방향</text>
        """
    else:
        anim_name = "recede"
        motion_arrow = """
        <line x1="245" y1="90" x2="245" y2="50" stroke="#333" stroke-width="4" stroke-linecap="round"/>
        <polygon points="235,60 255,60 245,40" fill="#333"/>
        <text x="245" y="25" font-size="14" font-weight="bold" fill="#333" text-anchor="middle">운동 방향</text>
        """

    # 1단계 정답 시: 극성 텍스트 및 '자기력' 화살표 (왼쪽)
    if q1_solved:
        pole_display = f"{coil_top_pole}극 유도됨"
        pole_color = "#d32f2f"
        
        # 렌츠의 법칙: 자기력은 운동을 방해하는 방향
        if "가까워짐" in magnet_action:
            force_arrow = """
            <line x1="125" y1="90" x2="125" y2="50" stroke="#d32f2f" stroke-width="4" stroke-linecap="round"/>
            <polygon points="115,60 135,60 125,40" fill="#d32f2f"/>
            <text x="125" y="25" font-size="14" font-weight="bold" fill="#d32f2f" text-anchor="middle">힘 (척력)</text>
            """
        else:
            force_arrow = """
            <line x1="125" y1="50" x2="125" y2="90" stroke="#d32f2f" stroke-width="4" stroke-linecap="round"/>
            <polygon points="115,80 135,80 125,100" fill="#d32f2f"/>
            <text x="125" y="120" font-size="14" font-weight="bold" fill="#d32f2f" text-anchor="middle">힘 (인력)</text>
            """
    else:
        pole_display = "? 극 유도됨"
        pole_color = "#999999"
        force_arrow = ""

    # 외부 회로 기기 시각화 (기호만, 박스 제거, 선 연결)
    if external_device == "검류계":
        device_svg = """
        <line x1="160" y1="460" x2="184" y2="460" stroke="#555" stroke-width="4"/>
        <line x1="216" y1="460" x2="240" y2="460" stroke="#555" stroke-width="4"/>
        <circle cx="200" cy="460" r="16" fill="#f8f9fa" stroke="#333" stroke-width="2"/>
        <text x="200" y="466" font-size="16" font-weight="bold" fill="#333" text-anchor="middle">G</text>
        """
    elif external_device == "전기 저항":
        device_svg = """
        <polyline points="160,460 170,460 175,448 185,472 195,448 205,472 215,448 225,472 230,460 240,460" fill="none" stroke="#333" stroke-width="3"/>
        """
    else: # 전구 (교과서 표준: 위로 볼록한 반원 형태)
        device_svg = """
        <line x1="160" y1="460" x2="185" y2="460" stroke="#555" stroke-width="4"/>
        <line x1="215" y1="460" x2="240" y2="460" stroke="#555" stroke-width="4"/>
        <circle cx="200" cy="460" r="15" fill="#f8f9fa" stroke="#333" stroke-width="2"/>
        <path d="M 185,460 L 190,460 A 10,10 0 0,1 210,460 L 215,460" fill="none" stroke="#333" stroke-width="2"/>
        """

    # 2단계 정답 시: 전류 방향 화살표 (코일 도선 & 회로)
    coil_current_arrows = ""
    if q2_solved:
        base_y_coords = [240, 270, 300, 330] 

        if ext_dir == "A_to_B":
            # 밖에서는 A -> B (왼쪽에서 오른쪽으로 흐름)
            arrows = """
            <text x="200" y="520" font-size="30" fill="#d32f2f" font-weight="bold" text-anchor="middle">→</text>
            <text x="200" y="545" font-size="16" fill="#d32f2f" font-weight="bold" text-anchor="middle">유도 전류: A(왼쪽) → B(오른쪽)</text>
            """
            # 코일 내부에서는 오른쪽에서 왼쪽으로 올라가며 폐회로 형성 (◀ 화살표)
            for y in base_y_coords:
                coil_current_arrows += f'<polygon points="205,{y+5} 190,{y+10} 205,{y+15}" fill="#ffeb3b" stroke="#333" stroke-width="1.5"/>'
        else:
            # 밖에서는 B -> A (오른쪽에서 왼쪽으로 흐름)
            arrows = """
            <text x="200" y="520" font-size="30" fill="#1976d2" font-weight="bold" text-anchor="middle">←</text>
            <text x="200" y="545" font-size="16" fill="#1976d2" font-weight="bold" text-anchor="middle">유도 전류: B(오른쪽) → A(왼쪽)</text>
            """
            # 코일 내부에서는 왼쪽에서 오른쪽으로 내려가며 폐회로 형성 (▶ 화살표)
            for y in base_y_coords:
                coil_current_arrows += f'<polygon points="190,{y+5} 205,{y+10} 190,{y+15}" fill="#ffeb3b" stroke="#333" stroke-width="1.5"/>'
    else:
        arrows = '<text x="200" y="545" font-size="16" fill="#999999" font-weight="bold" text-anchor="middle">유도 전류 방향: ???</text>'

    html_code = f"""
    <style>
        .container {{ display: flex; justify-content: center; background-color: #f8f9fa; border-radius: 10px; border: 2px solid #e0e0e0; padding: 10px; }}
        .magnet {{ animation: {anim_name} 1.2s forwards ease-in-out; }}
        @keyframes approach {{ 0% {{ transform: translateY(0px); }} 100% {{ transform: translateY(60px); }} }}
        @keyframes recede {{ 0% {{ transform: translateY(60px); }} 100% {{ transform: translateY(0px); }} }}
    </style>
    <div class="container" id="wrap-{unique_id}">
        <svg width="400" height="580" viewBox="0 0 400 580">
            <!-- 자석 및 운동방향/힘 화살표 -->
            <g class="magnet">
                <rect x="155" y="30" width="60" height="40" fill="{top_color}"/>
                <rect x="155" y="70" width="60" height="40" fill="{bottom_color}"/>
                <text x="185" y="58" fill="white" font-size="22" font-weight="bold" text-anchor="middle">{top_text}</text>
                <text x="185" y="98" fill="white" font-size="22" font-weight="bold" text-anchor="middle">{bottom_text}</text>
                {motion_arrow}
                {force_arrow}
            </g>

            <!-- 유도 극성 텍스트 -->
            <text x="185" y="210" fill="{pole_color}" font-size="20" font-weight="bold" text-anchor="middle">{pole_display}</text>

            <!-- 원통 -->
            <rect x="135" y="230" width="100" height="130" rx="10" fill="#e0e0e0" stroke="#999" stroke-width="2"/>
            
            <!-- 코일 도선 뼈대 -->
            <path d="M 135,240 Q 185,255 235,250" fill="none" stroke="#d35400" stroke-width="6"/>
            <path d="M 135,270 Q 185,285 235,280" fill="none" stroke="#d35400" stroke-width="6"/>
            <path d="M 135,300 Q 185,315 235,310" fill="none" stroke="#d35400" stroke-width="6"/>
            <path d="M 135,330 Q 185,345 235,340" fill="none" stroke="#d35400" stroke-width="6"/>

            <!-- 도선 위의 전류 화살표 -->
            {coil_current_arrows}

            <!-- 외부 회로 연결선 -->
            <polyline points="135,240 85,240 85,460 160,460" fill="none" stroke="#555" stroke-width="4"/>
            <polyline points="235,340 285,340 285,460 240,460" fill="none" stroke="#555" stroke-width="4"/>
            
            <!-- 단자 A, B -->
            <circle cx="160" cy="460" r="5" fill="#333"/>
            <text x="145" y="450" font-size="16" font-weight="bold" fill="#333" text-anchor="middle">A</text>
            <circle cx="240" cy="460" r="5" fill="#333"/>
            <text x="255" y="450" font-size="16" font-weight="bold" fill="#333" text-anchor="middle">B</text>

            <!-- 외부 기기 -->
            {device_svg}

            <!-- 최종 회로 아래 텍스트 화살표 -->
            {arrows}
        </svg>
    </div>
    """
    return html_code

def show_heart_balloons():
    heart_svg_template = '<svg viewBox="0 0 32 32" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg"><path d="M16,28.261c0,0-14-7.926-14-17.046c0-9.356,13.159-10.399,14-0.454c0.84-9.945,14-8.902,14,0.454C30,20.335,16,28.261,16,28.261z" fill="{color}"/></svg>'
    
    heart_html = """<style>
    @keyframes floatUpFlat {
        0% { bottom: -30%; opacity: 1; transform: translateX(0); }
        50% { transform: translateX(30px); }
        100% { bottom: 120%; opacity: 0; transform: translateX(-30px); }
    }
    .flat-heart { position: fixed; z-index: 9999; }
    </style>"""
    
    colors = ["#e74c3c", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6", "#ff9ff3", "#e67e22"]
    
    for _ in range(40):
        left = f"{random.randint(0, 95)}%"
        size = f"{random.randint(60, 250)}px"
        delay = f"{random.uniform(0, 6.0):.1f}s"
        duration = f"{random.uniform(8.0, 14.0):.1f}s"
        color = random.choice(colors)
        svg_markup = heart_svg_template.format(color=color)
        heart_html += f'<div class="flat-heart" style="left: {left}; width: {size}; animation: floatUpFlat {duration} ease-in-out forwards; animation-delay: {delay};">{svg_markup}</div>'
        
    st.markdown(heart_html, unsafe_allow_html=True)


# ==========================================
# 1번째 페이지: 전자기 유도 요약정리
# ==========================================
def page_summary():
    st.title("📖 전자기 유도 요약정리")
    st.info("여기에 전자기 유도 요약정리 내용이 들어갈 예정입니다.")
    st.write("선생님, 내용을 알려주시면 이 페이지에 알맞게 구현해 드리겠습니다!")


# ==========================================
# 2번째 페이지: 유도 전류 3단계 확인 
# ==========================================
def page_simulation():
    st.title("🧲 유도 전류 방향 3단계로 확인하기")
    st.markdown("자석의 움직임을 설정하고, 3가지 퀴즈를 순서대로 풀며 전자기 유도의 원리를 완성해 보세요!")
    
    # 상단 영역: 실험 세팅 (좌/우 분할)
    st.subheader("⚙️ 실험 세팅")
    col_set1, col_set2 = st.columns(2)
    
    with col_set1:
        magnet_action = st.radio(
            "자석의 극과 운동 상태를 선택하세요.",
            ["N극이 가까워짐", "S극이 가까워짐", "N극이 멀어짐", "S극이 멀어짐"]
        )
        
    with col_set2:
        external_device = st.radio(
            "외부 회로 기기를 선택하세요.",
            ["검류계", "전기 저항", "전구"]
        )

    # 상태 초기화 로직
    if st.session_state.get('prev_action') != magnet_action:
        st.session_state.prev_action = magnet_action
        st.session_state.q1_solved = False
        st.session_state.q2_solved = False
        st.session_state.q3_solved = False
        st.session_state.hearts_shown = False
        for key in ['q1_radio', 'q2_radio', 'q3_radio']:
            if key in st.session_state:
                del st.session_state[key]

    # 정답 판별 로직
    if "N극" in magnet_action:
        approaching = "가까워짐" in magnet_action
        ans_q1 = "밀어내는 힘 (척력)" if approaching else "끌어당기는 힘 (인력)"
        coil_top_pole = "N" if approaching else "S"
    else:
        approaching = "가까워짐" in magnet_action
        ans_q1 = "밀어내는 힘 (척력)" if approaching else "끌어당기는 힘 (인력)"
        coil_top_pole = "S" if approaching else "N"

    ans_q2 = "B(오른쪽)에서 A(왼쪽)로" if coil_top_pole == "N" else "A(왼쪽)에서 B(오른쪽)로"
    ext_dir = "B_to_A" if ans_q2 == "B(오른쪽)에서 A(왼쪽)로" else "A_to_B"

    match_dict = {
        "N극이 가까워짐": "S극이 멀어짐",
        "S극이 멀어짐": "N극이 가까워짐",
        "S극이 가까워짐": "N극이 멀어짐",
        "N극이 멀어짐": "S극이 가까워짐"
    }
    ans_q3 = match_dict[magnet_action]

    st.divider()

    # 하단 영역: 실시간 애니메이션(좌) / 퀴즈 풀기(우)
    col_visual, col_quiz = st.columns([1.2, 1])

    with col_visual:
        st.subheader("👀 실시간 애니메이션")
        if st.button("▶ 애니메이션 다시 재생하기"):
            pass 
        
        animation_html = get_animation_html(
            magnet_action, coil_top_pole, ext_dir, external_device, 
            st.session_state.get('q1_solved', False), 
            st.session_state.get('q2_solved', False)
        )
        st.components.v1.html(animation_html, height=650) 

    with col_quiz:
        st.subheader("📝 확인하기")
        
        q1_options = ["선택하세요", "밀어내는 힘 (척력)", "끌어당기는 힘 (인력)"]
        q1_user = st.radio("💡 **퀴즈 1.** 자석과 코일 사이에는 어떤 방향의 힘이 작용할까요?", q1_options, key="q1_radio")
        
        if q1_user == ans_q1:
            # 정답을 맞힌 즉시 상태를 업데이트하고 페이지를 다시 그려 애니메이션 즉각 반영
            if not st.session_state.get('q1_solved', False):
                st.session_state.q1_solved = True
                st.rerun()
            st.success(f"⭕ 정답! 렌츠의 법칙에 의해 자석의 운동을 방해하므로 코일 위쪽은 **{coil_top_pole}극**이 됩니다.")
        elif q1_user != "선택하세요":
            st.error("❌ 다시 생각해 보세요. 자석의 움직임을 '방해'하려면 어떻게 밀거나 당겨야 할까요?")

        if st.session_state.get('q1_solved', False):
            q2_options = ["선택하세요", "A(왼쪽)에서 B(오른쪽)로", "B(오른쪽)에서 A(왼쪽)로"]
            q2_user = st.radio(f"💡 **퀴즈 2.** 오른손 법칙을 적용할 때, 코일의 도선과 {external_device}에 흐르는 전류 방향은?", q2_options, key="q2_radio")
            
            if q2_user == ans_q2:
                # 정답을 맞힌 즉시 상태를 업데이트하고 페이지를 다시 그려 전류 화살표 즉각 반영
                if not st.session_state.get('q2_solved', False):
                    st.session_state.q2_solved = True
                    st.rerun()
                st.success(f"⭕ 정답! 오른손 엄지를 {coil_top_pole}극 쪽으로 향하게 감아쥐면 코일 및 회로에 전류는 **{ans_q2}** 흐릅니다.")
            elif q2_user != "선택하세요":
                st.error("❌ 다시 생각해 보세요. 엄지손가락을 N극 방향으로 향하게 하고 네 손가락을 감아쥐어 보세요.")

        if st.session_state.get('q2_solved', False):
            q3_options = ["N극이 가까워짐", "S극이 가까워짐", "N극이 멀어짐", "S극이 멀어짐"]
            q3_options.remove(magnet_action)
            q3_options.insert(0, "선택하세요")
            
            q3_user = st.radio("💡 **퀴즈 3.** 지금 선택한 상황과 **유도 전류의 방향이 동일한** 경우는 다음 중 무엇일까요?", q3_options, key="q3_radio")
            
            if q3_user == ans_q3:
                if not st.session_state.get('q3_solved', False):
                    st.session_state.q3_solved = True
                    st.rerun()
                st.success(f"🎉 완벽합니다! '{ans_q3}'일 때도 코일 위쪽이 똑같이 **{coil_top_pole}극**이 되기 때문에 유도 전류의 방향이 일치합니다.")
                
                if not st.session_state.get('hearts_shown', False):
                    show_heart_balloons()  
                    st.session_state.hearts_shown = True
                    
            elif q3_user != "선택하세요":
                st.error("❌ 다시 생각해 보세요. 코일 위쪽이 같은 극이 되려면 자석이 어떻게 움직여야 할까요?")


# ==========================================
# 3번째 페이지: 유도 전류의 특성 확인 퀴즈
# ==========================================
def page_quiz():
    st.title("📝 유도 전류의 특성 확인 퀴즈")
    st.info("여기에 유도 전류의 특성 확인 퀴즈 내용이 들어갈 예정입니다.")
    st.write("선생님, 내용을 알려주시면 이 페이지에 알맞게 구현해 드리겠습니다!")


# ==========================================
# 메인 함수 (사이드바 메뉴 라우팅)
# ==========================================
def main():
    st.sidebar.markdown("원하는 학습 페이지를 선택하세요.")
    
    # 사이드바 라디오 버튼으로 페이지 선택 (라벨 텍스트 숨김 처리)
    menu = st.sidebar.radio(
        "", 
        ["1. 전자기 유도 요약정리", "2. 유도 전류 방향 3단계로 확인하기", "3. 유도 전류의 특성 확인 퀴즈"],
        label_visibility="collapsed"
    )
    
    # 선택된 메뉴에 따라 해당 함수(페이지) 실행
    if menu == "1. 전자기 유도 요약정리":
        page_summary()
    elif menu == "2. 유도 전류 방향 3단계로 확인하기":
        page_simulation()
    elif menu == "3. 유도 전류의 특성 확인 퀴즈":
        page_quiz()

if __name__ == "__main__":
    main()
