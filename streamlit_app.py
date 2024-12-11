import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import rcParams

# 리밸런싱 계산 함수
def calculate_rebalance(current_portfolio, target_allocation):
    total_value = sum(current_portfolio.values())
    target_values = {asset: total_value * target_allocation[asset] for asset in target_allocation}
    rebalance_suggestions = {asset: target_values[asset] - current_portfolio[asset] for asset in current_portfolio}
    return target_values, rebalance_suggestions

# Streamlit 앱 설정
st.title("Asset Portfolio Rebalancing")

# 1단계: 현재 포트폴리오 입력
st.header("Step 1: Enter Current Portfolio")

# 자산 클래스 정의
assets = ['Stock', 'Bond', 'ETF', 'Cash', 'Real Estate', 'Cryptocurrency', 'Commodities']

# 각 자산의 현재 가치를 입력받기 위한 입력창 생성
current_portfolio = {}
for asset in assets:
    # 금액을 1000단위로 쉼표(,)가 표시되게 하기
    current_portfolio[asset] = st.number_input(
        f"Enter the current value of {asset} (Unit: KRW)",
        min_value=0,
        value=1000000,
        step=100000,
        format="%d"
    )

# 2단계: 목표 배분 입력
st.header("Step 2: Set Target Allocation")

# 목표 배분 비율을 숫자로 입력받기
target_allocation = {}
total_allocation = 0

for asset in assets:
    target_percentage = st.number_input(f"Target allocation for {asset} (%)", min_value=0, max_value=100, value=15)
    target_allocation[asset] = target_percentage
    total_allocation += target_percentage

# 목표 배분 비율 합이 100%가 되도록 조정
if total_allocation != 100:
    st.warning(f"Total target allocation is not 100%. The current sum is {total_allocation}%.")

# 3단계: 리밸런싱 계산
st.header("Step 3: Rebalancing Calculation")

# 목표 배분 비율의 합이 100%가 되지 않으면 리밸런싱 계산을 진행하지 않음
if total_allocation == 100:
    # 목표 배분 비율을 100%로 정규화
    allocation_sum = sum(target_allocation.values())
    target_allocation = {asset: allocation / allocation_sum for asset, allocation in target_allocation.items()}

    # 목표 자산 가치와 리밸런싱 제안 계산
    target_values, rebalance_suggestions = calculate_rebalance(current_portfolio, target_allocation)

    # 목표 자산 가치 출력
    st.subheader("Target Portfolio Value (Unit: KRW)")
    st.write(pd.DataFrame(list(target_values.items()), columns=["Asset", "Target Value"]))

    # 리밸런싱 제안 출력
    st.subheader("Rebalancing Suggestions (Unit: KRW)")
    st.write(pd.DataFrame(list(rebalance_suggestions.items()), columns=["Asset", "Rebalance Amount"]))

    # 4단계: 시각화
    st.header("Step 4: Portfolio Visualization")

    # 현재 포트폴리오와 목표 포트폴리오를 비교하는 바 차트 생성
    current_values = list(current_portfolio.values())
    target_values_list = list(target_values.values())

    fig, ax = plt.subplots()
    bar_width = 0.35
    index = np.arange(len(assets))

    bar1 = ax.bar(index, current_values, bar_width, label='Current Portfolio')
    bar2 = ax.bar(index + bar_width, target_values_list, bar_width, label='Target Portfolio')

    ax.set_xlabel('Asset Class')
    ax.set_ylabel('Value (KRW)')
    ax.set_title('Current Portfolio vs Target Portfolio')
    ax.set_xticks(index + bar_width / 2)
    ax.set_xticklabels(assets)
    ax.legend()

    # 차트 표시
    st.pyplot(fig)

    # 5단계: 히트맵 표시
    st.header("Step 5: Portfolio Heatmap")

    # 히트맵 데이터 준비
    heatmap_data = pd.DataFrame({
        'Asset': assets,
        'Current Value': list(current_portfolio.values()),
        'Target Value': list(target_values.values()),
        'Rebalance Suggestion': list(rebalance_suggestions.values())
    })
    heatmap_data.set_index('Asset', inplace=True)

    # 히트맵 그리기
    plt.figure(figsize=(10, 6))
    sns.heatmap(heatmap_data, annot=True, fmt='.0f', cmap='coolwarm', cbar=True)
    plt.title('Portfolio Heatmap: Current vs Target vs Rebalance Suggestion')
    st.pyplot(plt)
