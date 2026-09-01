import streamlit as st
import uuid

st.set_page_config(page_title="유도 전류 방향 찾기 (심화 애니메이션)", page_icon="🧲", layout="wide")

def get_animation_html(magnet_action, winding_dir, coil_top_pole, ext_dir, external_device):
    # 매번 렌더링될 때마다 새로운 ID를 부여하여 애니메이션이 다시 한 번 재생되도록 함
    unique_id = uuid.uuid4().hex

    # 자석 색상 및 극성 설정
    if "N극" in magnet_action:
        top_color, bottom_color = "#3498db", "#e74c3c" # 파랑(S), 빨강(N)
        top_text, bottom_text = "S", "N"
    else:
        top_color, bottom_color = "#e74c3c", "#3498db" # 빨강(N), 파랑(S)
        top_text, bottom_text = "N", "S"

    # 애니메이션 움직임 방향 설정
    if "가까워짐" in magnet_action:
        anim_name = "approach"
    else:
        anim_name = "recede"

    # 코일 감긴 방향에 따른 SVG 경로 생성
    if winding_dir == "반시계 방향":
        # 원통 앞면에서 왼쪽 -> 오른쪽으로 감겨 내려감
        coil_paths = """
        <!-- 앞면 도선 (왼쪽 -> 오른쪽) -->
        <path d="M 150,190 Q 200,205 250,200" fill="none" stroke="#d35400" stroke-width="6"/>
        <path d="M 150,220 Q 200,235 250,230" fill="none" stroke="#d35400" stroke-width="6"/>
        <path d="M 150,250 Q 200,265 250,260" fill="none" stroke="#d35400" stroke-width="6"/>
        <path d="M 150,280 Q 200,295 250,290" fill="none" stroke="#d35400" stroke-width="6"/>
        """
    else:
        # 원통 뒷면을 먼저 지나 앞면에서 오른쪽 -> 왼쪽으로 감겨 내려감
        coil_paths = """
        <!-- 뒷면 점선 (왼쪽 -> 오른쪽 뒤로 넘어감) -->
        <path d="M 150,190 Q 200,180 250,205" fill="none" stroke="#a0522d" stroke-width="3" stroke-dasharray="4,4"/>
        <path d="M 150,275 Q 200,295 250,290" fill="none" stroke="#a0522d" stroke-width="3" stroke-dasharray="4,4"/>
        <!-- 앞면 도선 (오른쪽 -> 왼쪽) -->
        <path d="M 250,205 Q 200,220 150,215" fill="none" stroke="#d35400" stroke-width="6"/>
        <path d="M 250,235 Q 200,250 150,245" fill="none" stroke="#d35400" stroke-width="6"/>
        <path d="M 250,265 Q 200,280 150,275" fill="none" stroke="#d35400" stroke-width="6"/>
        """

    # 외부 회로 전류 화살표 방향
    if ext_dir == "A_to_B":
        arrows = """
        <text x="80" y="295" font-size="24" fill="#d32f2f" font-weight="bold">↑</text>
        <text x="305" y="295" font-size="24" fill="#d32f2f" font-weight="bold">↓</text>
        <text x="200" y="425" font-size="16" fill="#d32f2f" font-weight="bold" text-anchor="middle">유도 전류 방향: A(왼쪽) → B(오른쪽)</text>
        """
    else:
        arrows = """
        <text x="80" y="295" font-size="24" fill="#1976d2" font-weight="bold">↓</text>
        <text x="305" y="295" font-size="24" fill="#1976d2" font-weight="bold">↑</text>
        <text x="200" y="425" font-size="16" fill="#1976d2" font-weight="bold" text-anchor="middle">유도 전류 방향: B(오른쪽) → A(왼쪽)</text>
        """

    # HTML/CSS 구조 (1회만 재생되도록 forwards 적용)
    html_code = f"""
    <style>
        .container {{
            display: flex; justify-content: center; background-color: #f8f9fa;
            border-radius: 10px; border: 2px solid #e0e0e0; padding: 10px;
        }}
        .magnet {{
            animation: {anim_name} 1.2s forwards ease-in-out;
        }}
        @keyframes approach {{
            0% {{ transform: translateY(0px); }}
            100% {{ transform: translateY(55px); }}
        }}
        @keyframes recede {{
            0% {{ transform: translateY(55px); }}
            100% {{ transform: translateY(0px); }}
        }}
    </style>
    <div class="container" id="wrap-{unique_id}">
        <svg width="400" height="450" viewBox="0 0 400 450">
            <!-- 막대 자석 -->
            <g class="magnet">
                <rect x="170" y="20" width="60" height="40" fill="{top_color}"/>
                <rect x="170" y="60" width="60" height="40" fill="{bottom_color}"/>
                <text x="200" y="48" fill="white" font-size="22" font-weight="bold" text-anchor="middle">{top_text}</text>
                <text x="200" y="88" fill="white" font-size="22" font-weight="bold" text-anchor="middle">{bottom_text}</text>
            </g>

            <!-- 유도된 극성 표시 -->
            <text x="200" y="170" fill="#d32f2f" font-size="20" font-weight="bold" text-anchor="middle">{coil_top_pole}극 유도됨</text>

            <!-- 원통 -->
            <rect x="150" y="180" width="100" height="120" rx="10" fill="#e0e0e0" stroke="#999" stroke-width="2"/>
            
            <!-- 코일 연결선 (터미널 A, B) -->
            <polyline points="150,190 100,190 100,380 170,380" fill="none" stroke="#555" stroke-width="4"/>
            <polyline points="250,290 300,290 300,380 230,380" fill="none" stroke="#555" stroke-width="4"/>
            <text x="100" y="175" font-size="16" font-weight="bold" text-anchor="middle">A</text>
            <text x="300" y="275" font-size="16" font-weight="bold" text-anchor="middle">B</text>

            <!-- 감긴 코일 -->
            {coil_paths}

            <!-- 외부 기기 -->
            <rect x="170" y="360" width="60" height="40" fill="#fff" stroke="#333" stroke-width="2" rx="5"/>
            <text x="200" y="385" font-size="14" font-weight="bold" text-anchor="middle">{external_device}</text>

            <!-- 전류 방향 화살표 및 텍스트 -->
            {arrows}
        </svg>
    </div>
    """
    return html_code


def main():
    st.title("🧲 코일에 흐르는 유도 전류 방향 찾기")
    st.markdown("자석의 운동과 코일의 감긴 방향에 따라 전류가 어느 쪽으로 흐르는지 3단계로 알아봅시다.")
    
    col_settings, col_visual = st.columns([1, 1.3])

    with col_settings:
        st.subheader("⚙️ 실험 세팅")
        
        magnet_action = st.radio(
            "1. 자석의 극과 운동 상태",
            ["N극이 가까워짐", "S극이 가까워짐", "N극이 멀어짐", "S극이 멀어짐"]
        )
        
        winding_dir = st.radio(
            "2. 코일 감긴 방향 (위에서 볼 때)",
            ["반시계 방향", "시계 방향"],
            help="반시계 방향은 원통 앞면 도선이 왼쪽에서 오른쪽으로 내려가고, 시계 방향은 오른쪽에서 왼쪽으로 내려갑니다."
        )
        
        external_device = st.radio(
            "3. 외부 회로 기기",
            ["검류계", "전기 저항", "전구"]
        )

        # 상태 및 논리 연산
        if "N극" in magnet_action:
            approaching = "가까워짐" in magnet_action
            coil_top_pole = "N" if approaching else "S"
            force_type = "밀어내는 힘 (척력)" if approaching else "끌어당기는 힘 (인력)"
        else:
            approaching = "가까워짐" in magnet_action
            coil_top_pole = "S" if approaching else "N"
            force_type = "밀어내는 힘 (척력)" if approaching else "끌어당기는 힘 (인력)"

        # 전류 방향 판별 로직
        # N극 유도 시 코일 앞면의 전류는 왼쪽 -> 오른쪽으로 흐르려고 함
        if coil_top_pole == "N":
            if winding_dir == "반시계 방향":
                ext_dir = "B_to_A"  # 도선과 전류 방향이 일치하여 위에서 아래로 흐름
            else:
                ext_dir = "A_to_B"  # 도선과 전류 방향이 엇갈려 아래에서 위로 흐름
        else: # S극 유도 시
            if winding_dir == "반시계 방향":
                ext_dir = "A_to_B"
            else:
                ext_dir = "B_to_A"
        
        ext_text = "A(왼쪽)에서 B(오른쪽)로" if ext_dir == "A_to_B" else "B(오른쪽)에서 A(왼쪽)로"

        st.divider()
        st.subheader("💡 3단계 물리적 해석")
        st.info(f"**[1단계: 힘의 방향]** 렌츠의 법칙에 의해 자석의 운동을 방해하는 **{force_type}**이 작용합니다.")
        st.info(f"**[2단계: 코일의 극성]** 방해하는 힘을 만들기 위해 코일 위쪽은 **{coil_top_pole}극**이 됩니다.")
        st.success(f"**[3단계: 유도 전류]** 오른손 법칙과 코일이 감긴 방향({winding_dir})을 고려할 때, {external_device}에는 **{ext_text}** 유도 전류가 흐릅니다.")

    with col_visual:
        st.subheader("👀 실시간 애니메이션 시각화")
        
        # 다시 보기 버튼
        if st.button("▶ 애니메이션 다시 재생하기"):
            pass # 버튼을 누르면 Streamlit이 리렌더링되며 애니메이션이 다시 1회 플레이됨
            
        animation_html = get_animation_html(magnet_action, winding_dir, coil_top_pole, ext_dir, external_device)
        st.components.v1.html(animation_html, height=500)

if __name__ == "__main__":
    main()
