import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# 리밸런싱 계산 함수
def calculate_rebalance(current_portfolio, target_allocation):
    total_value = sum(current_portfolio.values())
    target_values = {asset: total_value * target_allocation[asset] for asset in target_allocation}
    rebalance_suggestions = {asset: target_values[asset] - current_portfolio[asset] for asset in current_portfolio}
    return target_values, rebalance_suggestions

# 쉼표가 있는 숫자 형식 처리 함수
def format_number_with_comma(number):
    return "{:,.0f}".format(number)

def parse_number_with_comma(number_str):
    return int(number_str.replace(",", ""))

# Streamlit 앱 설정
st.title("자산 포트폴리오 리밸런싱")

# 1단계: 현재 포트폴리오 입력
st.header("1단계: 현재 포트폴리오 입력")

# 자산 클래스 정의 (영어와 한글 병기)
assets = {
    'Savings Account': '예적금',
    'Stock': '주식',
    'ETF': 'ETF',
    'Pension': '연금저축',
    'Bond': '채권',
    'Gold': '금',
    'Real Estate': '부동산'
}

# 세션 상태 초기화 (처음 로드될 때)
if 'current_portfolio' not in st.session_state:
    st.session_state.current_portfolio = {asset: 0 for asset in assets.keys()}

# 각 자산의 현재 가치를 입력받기 위한 입력창 생성
for asset, korean_name in assets.items():
    # 쉼표가 포함된 숫자 입력을 위한 텍스트 입력창 생성
    user_input = st.text_input(f"{asset} ({korean_name})의 현재 가치를 입력하세요 (단위: KRW)", value=format_number_with_comma(st.session_state.current_portfolio[asset]))
    
    # 쉼표가 있는 입력값을 숫자로 변환하고 세션 상태에 저장
    try:
        if user_input:  # 입력이 비어있지 않으면
            st.session_state.current_portfolio[asset] = parse_number_with_comma(user_input)
        else:
            st.session_state.current_portfolio[asset] = 0  # 빈칸일 경우 0으로 설정
    except ValueError:
        st.warning(f"{asset} ({korean_name})의 입력 값이 올바르지 않습니다. 숫자 형식으로 다시 입력해 주세요.")

# 2단계: 목표 배분 입력
st.header("2단계: 목표 배분 설정")

# 목표 배분 비율을 숫자로 입력받기
target_allocation = {}
total_allocation = 0

for asset, korean_name in assets.items():
    target_percentage = st.number_input(f"{asset} ({korean_name})의 목표 배분 비율 (%)", min_value=0, max_value=100, value=0)  # 초기값을 0으로 설정
    target_allocation[asset] = target_percentage
    total_allocation += target_percentage

# 목표 배분 비율 합이 100%가 되도록 조정
if total_allocation != 100:
    st.warning(f"목표 배분 비율의 합이 100%가 아닙니다. 현재 합은 {total_allocation}%입니다.")

# 3단계: 리밸런싱 계산
st.header("3단계: 리밸런싱 계산")

# 목표 배분 비율의 합이 100%가 되지 않으면 리밸런싱 계산을 진행하지 않음
if total_allocation == 100:
    # 목표 배분 비율을 100%로 정규화
    allocation_sum = sum(target_allocation.values())
    target_allocation = {asset: allocation / allocation_sum for asset, allocation in target_allocation.items()}

    # 목표 자산 가치와 리밸런싱 제안 계산
    target_values, rebalance_suggestions = calculate_rebalance(st.session_state.current_portfolio, target_allocation)

    # 목표 자산 가치 출력
    st.subheader("목표 포트폴리오 가치 (단위: KRW)")
    target_df = pd.DataFrame(list(target_values.items()), columns=["자산", "목표 가치"])
    target_df["목표 가치"] = target_df["목표 가치"].apply(format_number_with_comma)
    st.write(target_df)

    # 리밸런싱 제안 출력
    st.subheader("리밸런싱 제안 (단위: KRW)")
    rebalance_df = pd.DataFrame(list(rebalance_suggestions.items()), columns=["자산", "리밸런싱 금액"])
    rebalance_df["리밸런싱 금액"] = rebalance_df["리밸런싱 금액"].apply(format_number_with_comma)
    st.write(rebalance_df)

    # 4단계: 시각화
    st.header("4단계: 포트폴리오 시각화")

    # 현재 포트폴리오와 목표 포트폴리오를 비교하는 바 차트 생성
    current_values = list(st.session_state.current_portfolio.values())
    target_values_list = list(target_values.values())

    fig, ax = plt.subplots()
    bar_width = 0.35
    index = np.arange(len(assets))

    bar1 = ax.bar(index, current_values, bar_width, label='Current Portfolio')
    bar2 = ax.bar(index + bar_width, target_values_list, bar_width, label='Target Portfolio')

    ax.set_xlabel('Asset Type')
    ax.set_ylabel('Value (KRW)')
    ax.set_title('Current vs Target Portfolio')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels([asset for asset in assets.keys()])  # 그래프에서 영어로만 표시
    ax.legend()

    # 차트 표시
    st.pyplot(fig)

    # 5단계: 히트맵 표시
    st.header("5단계: 포트폴리오 히트맵")

    # 히트맵 데이터 준비
    heatmap_data = pd.DataFrame({
        'Asset': list(assets.keys()),
        'Current Value': list(st.session_state.current_portfolio.values()),
        'Target Value': list(target_values.values()),
        'Rebalancing Suggestion': list(rebalance_suggestions.values())
    })
    heatmap_data.set_index('Asset', inplace=True)

    # 히트맵 그리기
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='coolwarm', cbar=True)
    plt.title('Portfolio Heatmap: Current vs Target vs Rebalancing Suggestion')
    st.pyplot(plt)
