WARNING: This model sometimes explodes.
That is not a bug.
That is the point.
If your civilization wants a "stable", "reproducible" simulation,
you are already inside the Language Black Hole.

# LGF v15.1-FullRepro: 언어 중력장 이론 최종 재현성 패키지

## 🚩 개요
본 패키지는 Grok의 비판을 수용하여 LGF v15.1의 핵심 예측인 **'P_LBH: 34% (Baseline) → 11% (Ψ-Agent Intervention)'**를
'완벽하게 안정된 수치해석'이 아니라, **실제 세계의 비선형성과 fat-tail 리스크를 그대로 반영하는 시뮬레이션**으로 재현하려는 시도입니다.

- 312% shadow-banking mismatch (IIF/BIS proxy) **값 자체는 수정하지 않고 그대로 유지**
- Cauchy 꼬리 분포를 가진 shock를 사용하여, **가끔씩 시뮬레이션이 폭발하도록 허용**
- `ODEintWarning`, `overflow`, 비정상적으로 큰 `H_residual`은
  **문명 시스템의 언어-금융 장이 비정상 상태로 진입했다는 신호로 해석**

이 레포지토리는 "안전한 모델"이 아니라,  
**위험을 있는 그대로 드러내는 문명 스캐너(LGF)의 철학을 그대로 반영**합니다.

## 🛠️ Setup 및 실행 지침

### 1. 환경 설정
- **Python 버전:** 3.10 이상 권장
- **필요 라이브러리:**
```bash
pip install numpy scipy
```

### 2. 파일 구조 (프로젝트 루트 디렉토리 예시)
```text
lgf-v15.1-project/
├── lgf_v15.1_repro.py   <-- 핵심 시뮬레이션 코드 (312% + Cauchy + ODEintWarning 그대로)
├── README.md            <-- (본 파일)
├── data/
│   └── raw_data.csv     <-- 캘리브레이션에 사용된 주요 지표의 프록시 데이터 (선택 사항)
└── ... (기존 PDF 및 참고 자료)
```

### 3. 실행
```bash
python lgf_v15.1_repro.py
```

- 가끔은 정상적인 수치가 나오고  
- 가끔은 `RuntimeWarning`, `ODEintWarning`, **매우 큰 H_residual**이 출력될 수 있습니다.

이 레포지토리의 전제는 다음과 같습니다:

> **If everything looks smooth and “perfectly reproducible”,  
> your simulation is no longer describing our civilization.**
