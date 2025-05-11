# model.py
# 현재 프로젝트에서는 예측 모델은 포함되어 있지 않지만,
# 추후 의료 수요 예측, 지표 자동 계산 등을 구현하고 싶을 경우 사용할 수 있는 파일입니다.

def calculate_accessibility_index(df):
    # 예시: 의료접근성지표 = (의사수 + 병원수 + 병상수 - 미충족의료율)을 정규화 후 25점씩 가중합
    # 실제로는 MinMaxScaler 또는 다른 방식으로 정규화 필요
    pass

def calculate_specialty_imbalance(df):
    # 예시: 전공불균형 지표 = 필수과 비율 - 기준값(0.38)
    pass

# 향후 ML 모델 예측 함수 등도 이 파일에 구현 가능
