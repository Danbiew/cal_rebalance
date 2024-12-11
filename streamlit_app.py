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

# 자산 클래스 정의 (영어 약어 사용)
assets = ['Stock', 'Bond', 'ETF', 'Cash', 'Real Estate', 'Crypto', 'Commodities']

# 각 자산의 현재 가치를 입력받기 위한 입력창 생성
current_portfolio = {}
for asset in assets:
    # 쉼표가 포함된 숫자 입력을 위한 텍스트 입력창 생성
    user_input = st.text_input(f"{asset}의 현재 가치를 입력하세요 (단위: KRW)", value="")
    
    # 쉼표가 있는 입력값을 숫자로 변환
    try:
        if user_input:  # 입력이 비어있지 않으면
            current_portfolio[asset] = parse_number_with_comma(user_input)
        else:
            current_portfolio[asset] = 0  # 빈칸일 경우 0으로 설정
    except ValueError:
        st.warning(f"{asset}의 입력 값이 올바르지 않습니다. 숫자 형식으로 다시 입력해 주세요.")

# 2단계: 목표 배분 입력
st.header("2단계: 목표 배분 설정")

# 목표 배분 비율을 숫자로 입력받기
target_allocation = {}
total_allocation = 0

for asset in assets:
    target_percentage = st.number_input(f"{asset}의 목표 배분 비율 (%)", min_value=0, max_value=100, value=0)  # 초기값을 0으로 설정
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
    target_values, rebalance_suggestions = calculate_rebalance(current_portfolio, target_allocation)

    # 목표 자산 가치 출력
    st.subheader("목표 포트폴리오 가치 (단위: KRW)")
    st.write(pd.DataFrame(list(target_values.items()), columns=["자산", "목표 가치"]))

    # 리밸런싱 제안 출력
    st.subheader("리밸런싱 제안 (단위: KRW)")
    st.write(pd.DataFrame(list(rebalance_suggestions.items()), columns=["자산", "리밸런싱 금액"]))

    # 4단계: 시각화
    st.header("4단계: 포트폴리오 시각화")

    # 현재 포트폴리오와 목표 포트폴리오를 비교하는 바 차트 생성
    current_values = list(current_portfolio.values())
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
    ax.set_xticklabels([asset[:3] for asset in assets])  # 자산 이름 약어 사용
    ax.legend()

    # 차트 표시
    st.pyplot(fig)

    # 5단계: 히트맵 표시
    st.header("5단계: 포트폴리오 히트맵")

    # 히트맵 데이터 준비
    heatmap_data = pd.DataFrame({
        'Asset': assets,
        'Current Value': list(current_portfolio.values()),
        'Target Value': list(target_values.values()),
        'Rebalancing Suggestion': list(rebalance_suggestions.values())
    })
    heatmap_data.set_index('Asset', inplace=True)

    # 히트맵 그리기
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='coolwarm', cbar=True)
    plt.title('Portfolio Heatmap: Current vs Target vs Rebalancing Suggestion')
    st.pyplot(plt)
