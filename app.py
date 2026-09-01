import streamlit as st
import uuid
import random

st.set_page_config(page_title="유도 전류 방향 퀴즈", page_icon="🧲", layout="wide")

def get_animation_html(magnet_action, coil_top_pole, ext_dir, external_device, q1_solved, q2_solved):
    unique_id = uuid.uuid4().hex

    # 자석 색상 및 극성
    if "N극" in magnet_action:
        top_color, bottom_color = "#3498db", "#e74c3c"
        top_text, bottom_text = "S", "N"
    else:
        top_color, bottom_color = "#e74c3c", "#3498db"
        top_text, bottom_text = "N", "S"

    # 애니메이션 움직임 및 자석 오른쪽 운동방향 화살표 설정
    if "가까워짐" in magnet_action:
        anim_name = "approach"
        motion_arrow = """
        <line x1="250" y1="35" x2="250" y2="75" stroke="#333" stroke-width="4" stroke-linecap="round"/>
        <polygon points="240,65 260,65 250,85" fill="#333"/>
        <text x="250" y="105" font-size="14" font-weight="bold" fill="#333" text-anchor="middle">운동 방향</text>
        """
    else:
        anim_name = "recede"
        motion_arrow = """
        <line x1="250" y1="85" x2="250" y2="45" stroke="#333" stroke-width="4" stroke-linecap="round"/>
        <polygon points="240,55 260,55 250,35" fill="#333"/>
        <text x="250" y="25" font-size="14" font-weight="bold" fill="#333" text-anchor="middle">운동 방향</text>
        """

    # 퀴즈1 정답 여부에 따른 유도 극성 표시
    if q1_solved:
        pole_display = f"{coil_top_pole}극 유도됨"
        pole_color = "#d32f2f"
    else:
        pole_display = "? 극 유도됨"
        pole_color = "#999999"

    # 퀴즈2 정답 여부에 따른 전류 방향 표시
    if q2_solved:
        if ext_dir == "A_to_B":
            arrows = f"""
            <text x="80" y="295" font-size="24" fill="#d32f2f" font-weight="bold">↑</text>
            <text x="305" y="295" font-size="24" fill="#d32f2f" font-weight="bold">↓</text>
            <text x="200" y="425" font-size="16" fill="#d32f2f" font-weight="bold" text-anchor="middle">유도 전류: A(왼쪽) → B(오른쪽)</text>
            """
        else:
            arrows = f"""
            <text x="80" y="295" font-size="24" fill="#1976d2" font-weight="bold">↓</text>
            <text x="305" y="295" font-size="24" fill="#1976d2" font-weight="bold">↑</text>
            <text x="200" y="425" font-size="16" fill="#1976d2" font-weight="bold" text-anchor="middle">유도 전류: B(오른쪽) → A(왼쪽)</text>
            """
    else:
        arrows = """
        <text x="200" y="425" font-size="16" fill="#999999" font-weight="bold" text-anchor="middle">유도 전류 방향: ???</text>
        """

    html_code = f"""
    <style>
        .container {{ display: flex; justify-content: center; background-color: #f8f9fa; border-radius: 10px; border: 2px solid #e0e0e0; padding: 10px; }}
        .magnet {{ animation: {anim_name} 1.2s forwards ease-in-out; }}
        @keyframes approach {{ 0% {{ transform: translateY(0px); }} 100% {{ transform: translateY(55px); }} }}
        @keyframes recede {{ 0% {{ transform: translateY(55px); }} 100% {{ transform: translateY(0px); }} }}
    </style>
    <div class="container" id="wrap-{unique_id}">
        <svg width="400" height="450" viewBox="0 0 400 450">
            <g class="magnet">
                <rect x="170" y="20" width="60" height="40" fill="{top_color}"/>
                <rect x="170" y="60" width="60" height="40" fill="{bottom_color}"/>
                <text x="200" y="48" fill="white" font-size="22" font-weight="bold" text-anchor="middle">{top_text}</text>
                <text x="200" y="88" fill="white" font-size="22" font-weight="bold" text-anchor="middle">{bottom_text}</text>
                {motion_arrow}
            </g>

            <text x="200" y="170" fill="{pole_color}" font-size="20" font-weight="bold" text-anchor="middle">{pole_display}</text>

            <rect x="150" y="180" width="100" height="120" rx="10" fill="#e0e0e0" stroke="#999" stroke-width="2"/>
            
            <polyline points="150,190 100,190 100,380 170,380" fill="none" stroke="#555" stroke-width="4"/>
            <polyline points="250,290 300,290 300,380 230,380" fill="none" stroke="#555" stroke-width="4"/>
            <text x="100" y="175" font-size="16" font-weight="bold" text-anchor="middle">A</text>
            <text x="300" y="275" font-size="16" font-weight="bold" text-anchor="middle">B</text>

            <path d="M 150,190 Q 200,205 250,200" fill="none" stroke="#d35400" stroke-width="6"/>
            <path d="M 150,220 Q 200,235 250,230" fill="none" stroke="#d35400" stroke-width="6"/>
            <path d="M 150,250 Q 200,265 250,260" fill="none" stroke="#d35400" stroke-width="6"/>
            <path d="M 150,280 Q 200,295 250,290" fill="none" stroke="#d35400" stroke-width="6"/>

            <rect x="170" y="360" width="60" height="40" fill="#fff" stroke="#333" stroke-width="2" rx="5"/>
            <text x="200" y="385" font-size="14" font-weight="bold" text-anchor="middle">{external_device}</text>

            {arrows}
        </svg>
    </div>
    """
    return html_code


def show_heart_balloons():
    """개수가 많고 오래 지속되며 코드가 노출되지 않는 하트 애니메이션"""
    
    # 텍스트 노출(마크다운 오작동)을 방지하기 위해 띄어쓰기(들여쓰기)를 완전히 없앤 한 줄 SVG
    heart_svg_template = '<svg viewBox="0 0 32 32" width="100%" height="100%" xmlns="http://www.w3.org/2000/svg"><path d="M16,28.261c0,0-14-7.926-14-17.046c0-9.356,13.159-10.399,14-0.454c0.84-9.945,14-8.902,14,0.454C30,20.335,16,28.261,16,28.261z" fill="{color}"/></svg>'
    
    # 애니메이션 지속시간을 늘리고 스타일을 지정
    heart_html = """<style>
    @keyframes floatUpFlat {
        0% { bottom: -30%; opacity: 1; transform: translateX(0); }
        50% { transform: translateX(30px); }
        100% { bottom: 120%; opacity: 0; transform: translateX(-30px); }
    }
    .flat-heart {
        position: fixed; 
        z-index: 9999; 
    }
    </style>"""
    
    colors = ["#e74c3c", "#f1c40f", "#2ecc71", "#3498db", "#9b59b6", "#ff9ff3", "#e67e22"]
    
    # 총 40개의 하트를 랜덤한 위치, 크기, 시간차로 생성
    for _ in range(40):
        left = f"{random.randint(0, 95)}%"
        size = f"{random.randint(60, 250)}px" # 60px에서 250px까지 다양한 크기
        delay = f"{random.uniform(0, 6.0):.1f}s" # 0초부터 6초에 걸쳐 순차적으로 출발
        duration = f"{random.uniform(8.0, 14.0):.1f}s" # 8초~14초 동안 천천히 떠오름 (오래 유지)
        color = random.choice(colors)
        
        svg_markup = heart_svg_template.format(color=color)
        
        # HTML 태그 작성 시 줄바꿈 없이 한 줄로 이어서 작성하여 마크다운 오류 원천 차단
        heart_html += f'<div class="flat-heart" style="left: {left}; width: {size}; animation: floatUpFlat {duration} ease-in-out forwards; animation-delay: {delay};">{svg_markup}</div>'
        
    st.markdown(heart_html, unsafe_allow_html=True)


def main():
    st.title("🧲 유도 전류 3단계 퀴즈")
    st.markdown("자석의 움직임을 설정하고, 3가지 퀴즈를 순서대로 풀며 전자기 유도의 원리를 완성해 보세요!")
    
    col_settings, col_visual = st.columns([1, 1.2])

    with col_settings:
        st.subheader("⚙️ 1. 실험 세팅")
        
        magnet_action = st.radio(
            "자석의 극과 운동 상태를 선택하세요.",
            ["N극이 가까워짐", "S극이 가까워짐", "N극이 멀어짐", "S극이 멀어짐"]
        )
        
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
        st.subheader("📝 2. 퀴즈 풀기")
        
        q1_options = ["선택하세요", "밀어내는 힘 (척력)", "끌어당기는 힘 (인력)"]
        q1_user = st.radio("💡 **퀴즈 1.** 자석과 코일 사이에는 어떤 방향의 힘이 작용할까요?", q1_options, key="q1_radio")
        
        if q1_user == ans_q1:
            st.success(f"⭕ 정답! 렌츠의 법칙에 의해 자석의 운동을 방해하므로 코일 위쪽은 **{coil_top_pole}극**이 됩니다.")
            st.session_state.q1_solved = True
        elif q1_user != "선택하세요":
            st.error("❌ 다시 생각해 보세요. 자석의 움직임을 '방해'하려면 어떻게 밀거나 당겨야 할까요?")

        if st.session_state.q1_solved:
            q2_options = ["선택하세요", "A(왼쪽)에서 B(오른쪽)로", "B(오른쪽)에서 A(왼쪽)로"]
            q2_user = st.radio(f"💡 **퀴즈 2.** 오른손 법칙을 적용할 때, {external_device}에 흐르는 전류 방향은?", q2_options, key="q2_radio")
            
            if q2_user == ans_q2:
                st.success(f"⭕ 정답! 오른손 엄지를 {coil_top_pole}극 쪽으로 향하게 감아쥐면 전류는 **{ans_q2}** 흐릅니다.")
                st.session_state.q2_solved = True
            elif q2_user != "선택하세요":
                st.error("❌ 다시 생각해 보세요. 엄지손가락을 N극 방향으로 향하게 하고 네 손가락을 감아쥐어 보세요.")

        if st.session_state.q2_solved:
            q3_options = ["N극이 가까워짐", "S극이 가까워짐", "N극이 멀어짐", "S극이 멀어짐"]
            q3_options.remove(magnet_action)
            q3_options.insert(0, "선택하세요")
            
            q3_user = st.radio("💡 **퀴즈 3.** 지금 선택한 상황과 **유도 전류의 방향이 동일한** 경우는 다음 중 무엇일까요?", q3_options, key="q3_radio")
            
            if q3_user == ans_q3:
                st.success(f"🎉 완벽합니다! '{ans_q3}'일 때도 코일 위쪽이 똑같이 **{coil_top_pole}극**이 되기 때문에 유도 전류의 방향이 일치합니다.")
                st.session_state.q3_solved = True
                
                if not st.session_state.get('hearts_shown', False):
                    show_heart_balloons()  
                    st.session_state.hearts_shown = True
                    
            elif q3_user != "선택하세요":
                st.error("❌ 다시 생각해 보세요. 코일 위쪽이 같은 극이 되려면 자석이 어떻게 움직여야 할까요?")

    with col_visual:
        st.subheader("👀 실시간 애니메이션")
        if st.button("▶ 애니메이션 다시 재생하기"):
            pass 
        
        animation_html = get_animation_html(
            magnet_action, coil_top_pole, ext_dir, external_device, 
            st.session_state.get('q1_solved', False), 
            st.session_state.get('q2_solved', False)
        )
        st.components.v1.html(animation_html, height=500)

if __name__ == "__main__":
    main()
