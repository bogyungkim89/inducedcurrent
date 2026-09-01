import streamlit as st

# 페이지 설정
st.set_page_config(page_title="유도 전류 방향 찾기", page_icon="🧲")

def main():
    st.title("🧲 유도 전류 방향 확인하기")
    st.markdown("전자기 유도 현상에 의해 코일에 흐르는 **유도 전류의 방향**을 3단계에 걸쳐 알아봅시다.")
    st.divider()

    # --- 옵션 설정 (사이드바) ---
    st.sidebar.header("⚙️ 추가 옵션 설정")
    winding_dir = st.sidebar.radio(
        "1. 코일이 감긴 방향 (위에서 봤을 때)",
        ["시계 방향", "반시계 방향"],
        help="위에서 아래로 감겨 내려갈 때 코일 앞면을 지나는 도선의 방향을 결정합니다."
    )
    
    external_device = st.sidebar.radio(
        "2. 외부 회로 연결 기기",
        ["검류계", "전기 저항", "전구"],
        help="코일 양 끝에 연결될 기기를 선택하세요."
    )

    # 상태 관리를 위한 세션 초기화
    if 'step2_clicked' not in st.session_state:
        st.session_state.step2_clicked = False
    if 'step3_clicked' not in st.session_state:
        st.session_state.step3_clicked = False
    if 'current_magnet' not in st.session_state:
        st.session_state.current_magnet = "N극이 가까워짐"

    # --- 1단계: 자석 움직임 선택 ---
    st.header("1단계: 자석의 움직임 선택")
    magnet_action = st.radio(
        "원통 위쪽에 있는 막대자석의 극과 움직임을 선택하세요.",
        ["N극이 가까워짐", "S극이 가까워짐", "N극이 멀어짐", "S극이 멀어짐"]
    )

    # 자석 움직임이 바뀌면 하위 단계 초기화
    if magnet_action != st.session_state.current_magnet:
        st.session_state.current_magnet = magnet_action
        st.session_state.step2_clicked = False
        st.session_state.step3_clicked = False

    # 물리적 로직 처리
    if "N극" in magnet_action:
        approaching = "가까워짐" in magnet_action
        coil_top_pole = "N극" if approaching else "S극"
        force_type = "밀어내는 힘 (척력)" if approaching else "끌어당기는 힘 (인력)"
    else: # S극
        approaching = "가까워짐" in magnet_action
        coil_top_pole = "S극" if approaching else "N극"
        force_type = "밀어내는 힘 (척력)" if approaching else "끌어당기는 힘 (인력)"

    # --- 2단계: 힘과 전자석의 극 확인 ---
    st.header("2단계: 자석과 코일 사이의 힘 (렌츠의 법칙)")
    if st.button("코일에 작용하는 힘 확인하기"):
        st.session_state.step2_clicked = True
        st.session_state.step3_clicked = False # 2단계를 다시 누르면 3단계는 초기화

    if st.session_state.step2_clicked:
        st.info(f"""
        **렌츠의 법칙**에 의해 코일은 자석의 움직임을 **방해하는 방향**으로 자기장을 만듭니다.
        * 현재 자석의 움직임: {magnet_action}
        * 발생하는 힘: **{force_type}**
        * 코일 위쪽의 극: 자석을 밀어내거나 당기기 위해 코일 위쪽은 **{coil_top_pole}**이 됩니다.
        """)

        # --- 3단계: 유도 전류의 방향 확인 ---
        st.header("3단계: 유도 전류의 방향 (오른손 법칙)")
        if st.button("오른손 법칙으로 전류 방향 확인하기"):
            st.session_state.step3_clicked = True

        if st.session_state.step3_clicked:
            # 전류 방향 계산 로직
            # 엄지 손가락 방향 (위=N극, 아래=S극)
            thumb_dir = "위쪽" if coil_top_pole == "N극" else "아래쪽"
            
            # 코일 앞면에서의 전류 방향 (손가락 감아쥐는 방향)
            if coil_top_pole == "N극":
                front_current = "오른쪽에서 왼쪽"
            else:
                front_current = "왼쪽에서 오른쪽"

            # 외부 회로(위쪽 A, 아래쪽 B라고 가정)의 전류 방향
            # 감긴 방향에 따라 외부 회로 전류 방향이 달라짐
            if winding_dir == "시계 방향":
                if coil_top_pole == "N극":
                    ext_current = "위쪽에서 아래쪽 (A → B)"
                else:
                    ext_current = "아래쪽에서 위쪽 (B → A)"
            else: # 반시계 방향
                if coil_top_pole == "N극":
                    ext_current = "아래쪽에서 위쪽 (B → A)"
                else:
                    ext_current = "위쪽에서 아래쪽 (A → B)"

            st.success(f"""
            오른손의 엄지손가락을 N극이 생기는 **{thumb_dir}**으로 향하게 하고, 나머지 네 손가락으로 원통을 감아쥡니다.
            
            1. **코일 앞면 도선의 전류 방향:** 네 손가락이 가리키는 방향인 **{front_current}**으로 전류가 흐릅니다.
            2. **코일 감긴 방향 고려:** 현재 코일은 위에서 볼 때 **{winding_dir}**으로 감겨 있습니다.
            3. **최종 결과:** 코일 양 끝과 연결된 **{external_device}**를 통해서는 전류가 **{ext_current}** 방향으로 흐릅니다!
            """)

if __name__ == "__main__":
    main()
