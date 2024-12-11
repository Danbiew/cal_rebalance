import matplotlib.pyplot as plt
from matplotlib import font_manager, rcParams

# 시스템에서 사용 가능한 한글 폰트를 자동으로 찾기
font_path = None
for font in font_manager.findSystemFonts(fontpaths=None, fontext='ttf'):
    if 'NanumGothic' in font:
        font_path = font
        break

# 폰트가 찾으면 설정
if font_path:
    font_prop = font_manager.FontProperties(fname=font_path)
    rcParams['font.family'] = font_prop.get_name()
    rcParams['axes.unicode_minus'] = False
else:
    print("한글 폰트를 찾을 수 없습니다. 폰트를 설치한 후 다시 시도해주세요.")


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import rcParams

# 한글 폰트 설정 (여기서는 'NanumGothic' 폰트를 사용합니다)
rcParams['font.family'] = 'NanumGothic'
rcParams['axes.unicode_minus'] = False  # 마이너스 기호 깨지는 문제 해결

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

# 목표 배분 비율을 숫자로 입력받기
target_allocation = {}
total_allocation = 0

for asset in assets:
    target_percentage = st.number_input(f"{asset}의 목표 배분 비율 (%)", min_value=0, max_value=100, value=25)
    target_allocation[asset] = target_percentage
    total_allocation += target_percentage

# 목표 배분 비율 합이 100%가 되도록 조정
if total_allocation != 100:
    st.warning("목표 배분 비율의 합이 100%가 되지 않았습니다. 현재 합계는 {}%입니다.".format(total_allocation))

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
