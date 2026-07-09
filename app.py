import streamlit as st
import time

# --- 페이지 기본 설정 ---
st.set_page_config(page_title="스트림릿 요리 게임", page_icon="👨‍🍳", layout="centered")

# --- 세션 상태 초기화 (게임 진행 상황 저장) ---
if 'stage' not in st.session_state:
    st.session_state.stage = '메뉴선택'
if 'target_menu' not in st.session_state:
    st.session_state.target_menu = ''
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'cook_method' not in st.session_state:
    st.session_state.cook_method = ''

def reset_game():
    """게임을 초기화하는 함수"""
    st.session_state.stage = '메뉴선택'
    st.session_state.target_menu = ''
    st.session_state.inventory = []
    st.session_state.cook_method = ''

# --- 게임 화면 구성 ---
st.title("👨‍🍳 내 맘대로 요리하기 게임!")
st.write("메뉴를 고르고, 재료와 조리법을 선택해 완벽한 요리를 만들어보세요.")
st.divider()

# 1단계: 메뉴 선택
if st.session_state.stage == '메뉴선택':
    st.subheader("1. 오늘 도전할 요리를 선택하세요!")
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🍳 김치볶음밥"):
            st.session_state.target_menu = "김치볶음밥"
            st.session_state.stage = '재료선택'
            st.rerun()
    with col2:
        if st.button("🍝 크림 파스타"):
            st.session_state.target_menu = "크림 파스타"
            st.session_state.stage = '재료선택'
            st.rerun()
    with col3:
        if st.button("🍲 마라탕"):
            st.session_state.target_menu = "마라탕"
            st.session_state.stage = '재료선택'
            st.rerun()

# 2단계: 재료 선택
elif st.session_state.stage == '재료선택':
    st.subheader(f"도전 요리: {st.session_state.target_menu}")
    st.write("2. 냉장고에서 요리에 넣을 재료를 골라보세요. (괴식이 탄생할 수도 있습니다!)")
    
    # 🌟 새로운 재료 대거 추가!
    ingredients_list = [
        "김치", "밥", "스팸", "파스타 면", "생크림", "베이컨", "마늘", 
        "마라 소스", "중국당면", "청경채", "푸주", "소고기", "팽이버섯", "고수",
        "초콜릿", "딸기잼", "민트초코"
    ]
    selected = st.multiselect("재료 선택", ingredients_list)
    
    if st.button("재료 준비 완료"):
        if len(selected) > 0:
            st.session_state.inventory = selected
            st.session_state.stage = '조리방법'
            st.rerun()
        else:
            st.warning("재료를 최소 하나 이상 선택해주세요!")
            
    if st.button("돌아가기"):
        reset_game()
        st.rerun()

# 3단계: 조리 방법 선택
elif st.session_state.stage == '조리방법':
    st.subheader("3. 어떻게 조리할까요?")
    st.info(f"선택한 재료: {', '.join(st.session_state.inventory)}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button("🔥 프라이팬에 볶기"):
            st.session_state.cook_method = "볶기"
            st.session_state.stage = '결과확인'
            st.rerun()
    with col2:
        if st.button("💧 냄비에 끓이기"):
            st.session_state.cook_method = "끓이기"
            st.session_state.stage = '결과확인'
            st.rerun()
    with col3:
        if st.button("🧊 차갑게 얼리기"):
            st.session_state.cook_method = "얼리기"
            st.session_state.stage = '결과확인'
            st.rerun()

# 4단계: 결과 확인 및 채점
elif st.session_state.stage == '결과확인':
    st.subheader("요리 결과는...?! 🥁")
    
    # 로딩 애니메이션 연출
    with st.spinner("요리하는 중... 치익... 보글보글..."):
        time.sleep(2)
        
    menu = st.session_state.target_menu
    items = set(st.session_state.inventory)
    method = st.session_state.cook_method
    
    score = 0
    msg = ""
    
    # 요리 채점 로직
    if menu == "김치볶음밥":
        if {"김치", "밥"}.issubset(items):
            score += 50
        if "스팸" in items or "베이컨" in items:
            score += 20
        if method == "볶기":
            score += 50
            
    elif menu == "크림 파스타":
        if {"파스타 면", "생크림"}.issubset(items):
            score += 50
        if "베이컨" in items or "마늘" in items:
            score += 20
        if method == "끓이기" or method == "볶기":
            score += 50
            
    # 🌟 마라탕 채점 로직 추가!
    elif menu == "마라탕":
        if "마라 소스" in items:
            score += 30
            # 마라탕에 어울리는 재료들 중 2개 이상 들어가면 추가 점수
            mara_ingredients = {"중국당면", "청경채", "푸주", "소고기", "팽이버섯"}
            if len(items.intersection(mara_ingredients)) >= 2:
                score += 30
        if "고수" in items:
            score += 10 # 고수 매니아를 위한 가산점!
        if method == "끓이기":
            score += 40
            
    # 괴식 페널티
    if "초콜릿" in items or "딸기잼" in items or "민트초코" in items:
        score -= 100
        msg = "우웩! 음식물 쓰레기가 연성되었습니다! 🤢"
        
    # 얼리기 페널티 (특수 상황)
    if method == "얼리기":
        score -= 50
        msg = "요리가 꽁꽁 얼어버렸습니다. 이가 부러질 것 같아요! 🥶"
        
    # 최종 결과 출력
    st.divider()
    if score >= 100:
        st.success(f"⭐⭐⭐⭐⭐ 대성공! 완벽한 {menu}입니다! 당장 식당을 차리셔도 좋겠어요! 😋")
    elif score >= 60:
        st.info(f"⭐⭐⭐ 꽤 괜찮네요! 한 끼 식사로 든든한 {menu}입니다. 🙂")
    elif score >= 30:
        st.warning(f"⭐ 약간 아쉽네요. 배고플 때 억지로 먹을 수는 있는 {menu}입니다. 😐")
    else:
        st.error(f"☠️ 실패... 요리라고 부를 수 없는 무언가가 탄생했습니다. {msg}")
        
    st.write(f"**내가 쓴 재료:** {', '.join(st.session_state.inventory)}")
    st.write(f"**조리 방식:** {method}")
    st.write(f"**최종 점수:** {score}점")
    
    if st.button("다시 요리하기"):
        reset_game()
        st.rerun()
