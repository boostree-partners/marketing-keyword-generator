# 🔤 키워드 조합 생성기

엑셀 파일에서 키워드 데이터를 읽어와 조합 규칙에 따라 새로운 키워드 조합을 생성하는 도구입니다.

## ✨ 주요 기능

- 📊 **엑셀 파일 읽기**: 구조화된 키워드 데이터 로드
- 🔄 **조합 규칙 처리**: A열의 숫자 규칙에 따른 컬럼 조합
- 📈 **다양한 출력 형식**: 대시보드, 그룹별 시트, 상세 결과
- 🌐 **웹 인터페이스**: Streamlit 기반 사용자 친화적 UI
- 💻 **명령행 인터페이스**: CLI를 통한 배치 처리

## 🚀 빠른 시작

### 1. 환경 설정
```bash
# 저장소 클론
git clone <repository-url>
cd keyword-generator

# 가상환경 설정 및 패키지 설치
make setup
```

### 2. 웹앱 실행 (권장)
```bash
make web
```
브라우저에서 `http://localhost:8501`로 접속하여 사용하세요.

### 3. 명령행 실행
```bash
# 기본 파일로 실행
make run

# 특정 파일 지정
make file FILE=resources/my_data.xlsx

# 출력 디렉토리 지정
make output DIR=my_results
```

## 📁 프로젝트 구조

```
keyword-generator/
├── src/
│   ├── keyword_generator.py    # 핵심 로직
│   ├── streamlit_app.py        # 웹 인터페이스
│   ├── resources/              # 입력 파일들
│   │   └── sample_keywords.xlsx
│   └── output/                 # 결과 파일들
├── requirements.txt            # Python 패키지 의존성
├── Makefile                   # 빌드 및 실행 명령어
└── README.md                  # 이 파일
```

## 📊 입력 파일 형식

엑셀 파일은 다음과 같은 구조를 가져야 합니다:

| A열 (조합규칙) | B열 | C열 (1) | D열 (2) | E열 (3) | ... |
|---------------|-----|---------|---------|---------|-----|
| 2,3           | 그룹1 | 키워드1 | 키워드1 | 키워드1 | ... |
| 1,4           | 그룹2 | 키워드2 | 키워드2 | 키워드2 | ... |
| ...           | ...  | ...     | ...     | ...     | ... |

### 규칙 설명
- **1행**: 각 컬럼의 번호 (C=1, D=2, E=3, ...)
- **2행**: 카테고리 제목
- **3행부터**: 실제 키워드 데이터
- **A열**: 조합 규칙 (예: "2,3" = D열과 E열 조합)

## 🎯 사용법

### 웹 인터페이스 (권장)
1. `make web` 실행
2. 브라우저에서 파일 업로드
3. 설정 조정 및 결과 확인
4. 결과 파일 다운로드

### 명령행 사용법
```bash
# 기본 실행
make run

# 특정 파일 사용
make file FILE=path/to/your/file.xlsx

# 출력 디렉토리 지정
make output DIR=results

# 파일과 출력 모두 지정
make custom FILE=input.xlsx DIR=output_dir
```

## 📈 출력 형식

생성되는 엑셀 파일은 다음 시트들을 포함합니다:

1. **Dashboard**: 전체 통계 및 요약
2. **Group별 시트**: 각 그룹의 키워드 조합
3. **Detailed Results**: 모든 조합의 상세 정보

### 출력 컬럼
- **Rule**: 적용된 조합 규칙
- **Group**: 키워드 그룹명
- **Columns**: 사용된 컬럼 번호
- **Keyword**: 생성된 키워드 조합
- **Components**: 원본 키워드들

## 🛠️ 개발 환경

### 필수 요구사항
- Python 3.8 이상
- macOS, Windows, Linux 지원

### 설치된 패키지
- `pandas`: 데이터 처리
- `openpyxl`: 엑셀 파일 읽기/쓰기
- `xlrd`: 엑셀 파일 읽기
- `streamlit`: 웹 인터페이스
- `numpy`: 수치 계산

### 개발 명령어
```bash
# 개발 환경 초기화
make dev-setup

# 기능 테스트
make test

# 정리
make clean          # 출력 파일 정리
make clean-build    # 빌드 파일 정리
make clean-all      # 전체 정리
```

## 📋 Makefile 명령어

| 명령어 | 설명 |
|--------|------|
| `make web` | Streamlit 웹앱 실행 |
| `make run` | 기본 파일로 키워드 생성 |
| `make file FILE=파일명` | 특정 파일로 실행 |
| `make output DIR=디렉토리` | 출력 디렉토리 지정 |
| `make setup` | 가상환경 설정 |
| `make clean` | 출력 파일 정리 |
| `make help` | 도움말 표시 |

## 🔧 고급 사용법

### 환경 변수 설정
```bash
# 입력 파일 변경
make run INPUT_FILE=my_data.xlsx

# 출력 디렉토리 변경
make run OUTPUT_DIR=results
```

### 직접 Python 실행
```bash
# 가상환경 활성화
source venv/bin/activate

# 직접 실행
cd src && python keyword_generator.py --input file.xlsx --output results
```

## 🐛 문제 해결

### 일반적인 문제들

**Q: "File not found" 오류**
A: 입력 파일 경로를 확인하고 `resources/` 폴더에 파일이 있는지 확인하세요.

**Q: 웹앱이 시작되지 않음**
A: 포트 8501이 사용 중인지 확인하고, 다른 포트를 사용해보세요.

**Q: 메모리 부족 오류**
A: 큰 파일의 경우 웹 인터페이스보다 명령행 실행을 권장합니다.

### 로그 확인
```bash
# 상세 로그와 함께 실행
make run 2>&1 | tee log.txt
```

## 📝 라이선스

이 프로젝트는 MIT 라이선스 하에 배포됩니다.

## 🤝 기여하기

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📞 지원

문제가 발생하거나 질문이 있으시면 이슈를 생성해주세요.

---

**키워드 생성기로 더 나은 마케팅 콘텐츠를 만들어보세요!** 🚀
