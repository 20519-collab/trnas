import streamlit as st
import time

# 이미지 URL 설정
IMG_KITCHEN = "http://googleusercontent.com/image_collection/image_retrieval/1581727923045736788"
IMG_KIMCHI = "http://googleusercontent.com/image_collection/image_retrieval/15942973669017108911"
IMG_PASTA = "http://googleusercontent.com/image_collection/image_retrieval/15445549260731904735"
IMG_BURNT = "http://googleusercontent.com/image_collection/image_retrieval/14707850334929951398"

st.set_page_config(page_title="AI 요리 게임 v2", page_icon="🍳")
st.title("🍳 시각적 AI 요리 시뮬레이터")

if 'stage' not in st.session_state:
    st.session_state.stage = '메뉴선택'

# 1단계: 메뉴 선택
if st.session_state.stage == '메뉴선택':
    st.image(IMG_KITCHEN, caption="오늘의 주방에 오신 것을 환영합니다!")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🍳 김치볶음밥"):
            st.session_state.target = "김치볶음밥"
            st.session_state.stage = '조리'
            st.rerun()
    with col2:
        if st.button("🍝 크림 파스타"):
            st.session_state.target = "크림 파스타"
            st.session_state.stage = '조리'
            st.rerun()

# 2단계: 결과 화면 (단순화된 예시)
elif st.session_state.stage == '결과확인':
    if st.session_state.score >= 80:
        img = IMG_KIMCHI if st.session_state.target == "김치볶음밥" else IMG_PASTA
        st.image(img, width=500)
        st.success(f"성공! {st.session_state.score}점 요리입니다!")
    else:
        st.image(IMG_BURNT, width=500)
        st.error("앗! 요리를 망쳤어요...")
