import streamlit as st

st.set_page_config(page_title="유도 전류 방향 찾기 (애니메이션 버전)", page_icon="🧲", layout="wide")

def get_animation_html(magnet_action, winding_dir, coil_top_pole, ext_current):
    # 자석의 움직임과 극성에 따른 CSS 애니메이션 설정
    if "N극" in magnet_action:
        top_color, bottom_color = "blue", "red"  # 위 S, 아래 N
        pole_text = "N"
    else:
        top_color, bottom_color = "red", "blue"  # 위 N, 아래 S
        pole_text = "S"

    if "가까워짐" in magnet_action:
        anim_name = "moveDown"
    else:
        anim_name = "moveUp"

    # 화살표 방향 설정 (전류 방향)
    if "A → B" in ext_current:
        arrow_dir = "⬇️ 아래로 흐름 (A → B)"
    else:
        arrow_dir = "⬆️ 위로 흐름 (B → A)"

    html_code = f"""
    <style>
        .container {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            height: 400px;
            background-color: #f8f9fa;
            border-radius: 15px;
            position: relative;
            overflow: hidden;
            border: 2px solid #e0e0e0;
        }}
        .magnet {{
            width: 80px;
            height: 140px;
            border-radius: 5px;
            position: absolute;
            display: flex;
            flex-direction: column;
            animation: {anim_name} 2s infinite alternate ease-in-out;
            box-shadow: 2px 2px 10px rgba(0,0,0,0.2);
        }}
        .magnet .top {{
            flex: 1; background-color: {top_color};
            border-top-left-radius: 5px; border-top-right-radius: 5px;
            display: flex; align-items: center; justify-content: center;
            color: white; font-weight: bold; font-size: 24px;
        }}
        .magnet .bottom {{
            flex: 1; background-color: {bottom_color};
            border-bottom-left-radius: 5px; border-bottom-right-radius: 5px;
            display: flex; align-items: center; justify-content: center;
            color: white; font-weight: bold; font-size: 24px;
        }}
        .coil {{
            width: 140px;
            height: 100px;
            border: 8px solid #FF9800;
            border-radius: 50%;
            position: absolute;
            bottom: 50px;
            box-shadow: 0 10px 15px rgba(0,0,0,0.1);
            display: flex;
            align-items: center;
            justify-content: center;
            flex-direction: column;
            background-color: rgba(255, 152, 0, 0.1);
        }}
        .induced-pole {{
            font-size: 30px;
            font-weight: bold;
            color: #d32f2f;
            margin-top: -60px;
            text-shadow: 1px 1px 2px white;
        }}
        .current-arrow {{
            position: absolute;
            bottom: 10px;
            font-size: 20px;
            font-weight: bold;
            color: #388e3c;
            background: white;
            padding: 5px 10px;
            border-radius: 10px;
            border: 2px solid #388e3c;
        }}
        
        @keyframes moveDown {{
            0% {{ top: -20px; }}
            100% {{ top: 120px; }}
        }}
        @keyframes moveUp {{
            0% {{ top: 120px; }}
            100% {{ top: -20px; }}
        }}
    </style>

    <div class="container">
        <div class="magnet">
            <div class="top">{"S" if pole_text=="N" else "N"}</div>
            <div class="bottom">{pole_text}</div>
        </div>
        
        <div class="coil">
            <div class="induced-pole">{coil_top_pole}극 유도됨</div>
        </div>
        
        <div class="current-arrow">전류: {arrow_dir}</div>
    </div>
    """
    return html_code

def main():
    st.title("🧲 유도 전류 방향 찾기 (애니메이션)")
    st.markdown("자석의 움직임을 선택하고, 생성되는 애니메이션을 통해 전자기 유도 현상을 눈으로 확인하세요!")
    
    col_settings, col_visual = st.columns([1, 1.5])

    with col_settings:
        st.subheader("⚙️ 실험 조건 설정")
        
        # 1단계: 자석 움직임
        magnet_action = st.radio(
            "1. 자석의 극과 움직임",
            ["N극이 가까워짐", "S극이 가까워짐", "N극이 멀어짐", "S극이 멀어짐"]
        )
        
        # 추가 옵션 (코일 방향, 기기)
        winding_dir = st.radio(
            "2. 코일이 감긴 방향",
            ["시계 방향", "반시계 방향"]
        )
        external_device = st.radio(
            "3. 외부 회로 기기",
            ["검류계", "전기 저항", "전구"]
        )

        st.divider()
        
        # 논리 연산
        if "N극" in magnet_action:
            approaching = "가까워짐" in magnet_action
            coil_top_pole = "N" if approaching else "S"
            force_type = "밀어내는 힘(척력)" if approaching else "끌어당기는 힘(인력)"
        else:
            approaching = "가까워짐" in magnet_action
            coil_top_pole = "S" if approaching else "N"
            force_type = "밀어내는 힘(척력)" if approaching else "끌어당기는 힘(인력)"

        if winding_dir == "시계 방향":
            if coil_top_pole == "N":
                ext_current = "위쪽에서 아래쪽 (A → B)"
            else:
                ext_current = "아래쪽에서 위쪽 (B → A)"
        else: 
            if coil_top_pole == "N":
                ext_current = "아래쪽에서 위쪽 (B → A)"
            else:
                ext_current = "위쪽에서 아래쪽 (A → B)"

        # 해설 부분
        st.subheader("💡 실험 결과 분석")
        st.info(f"**[힘의 작용]** 렌츠의 법칙에 따라 코일은 자석을 방해합니다. 따라서 **{force_type}**이 작용하여 코일 위쪽은 **{coil_top_pole}극**이 됩니다.")
        st.success(f"**[전류 방향]** 코일이 {winding_dir}으로 감겨있으므로, 오른손 법칙에 의해 {external_device}에는 **{ext_current}** 방향으로 유도 전류가 흐릅니다.")

    with col_visual:
        st.subheader("👀 애니메이션 시각화")
        st.markdown("자석이 움직이면서 코일에 유도되는 극성과 전류의 방향을 확인하세요.")
        
        # 생성된 HTML/CSS 애니메이션을 화면에 렌더링
        animation_html = get_animation_html(magnet_action, winding_dir, coil_top_pole, ext_current)
        st.components.v1.html(animation_html, height=450)

if __name__ == "__main__":
    main()
