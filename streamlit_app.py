import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# 리밸런싱 계산 함수
def calculate_rebalance(current_portfolio, target_allocation):
    total_value = sum(current_portfolio.values())
    target_values = {asset: total_value * target_allocation[asset] for asset in target_allocation}
    rebalance_suggestions = {asset: target_values[asset] - current_portfolio[asset] for asset in current_portfolio}
    return target_values, rebalance_suggestions

# Streamlit 앱 설정
st.title("자산 포트폴리오 리밸런싱")

# 1단계: 현재 포트폴리오 입력
st.header("1단계: 현재 포트폴리오 입력")

# 자산 클래스 정의
assets = ['주식', '채권', 'ETF', '현금']

# 각 자산의 현재 가치를 입력받기 위한 입력창 생성
current_portfolio = {}
for asset in assets:
    current_portfolio[asset] = st.number_input(f"{asset}의 현재 가치를 입력하세요 (단위: KRW)", min_value=0, value=1000000, step=100000)

# 2단계: 목표 배분 입력
st.header("2단계: 목표 배분 설정")

# 목표 배분 비율을 설정하기 위한 슬라이더 생성
target_allocation = {}
for asset in assets:
    target_allocation[asset] = st.slider(f"{asset}의 목표 배분 비율 (%)", min_value=0, max_value=100, value=25)

# 3단계: 리밸런싱 계산
st.header("3단계: 리밸런싱 계산")

# 목표 배분 비율의 합이 100%가 되도록 정규화
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

bar1 = ax.bar(index, current_values, bar_width, label='현재 포트폴리오')
bar2 = ax.bar(index + bar_width, target_values_list, bar_width, label='목표 포트폴리오')

ax.set_xlabel('자산 클래스')
ax.set_ylabel('가치 (KRW)')
ax.set_title('현재 포트폴리오 vs 목표 포트폴리오')
ax.set_xticks(index + bar_width / 2)
ax.set_xticklabels(assets)
ax.legend()

# 차트 표시
st.pyplot(fig)
