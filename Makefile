.PHONY: run setup clean clean-build clean-all help generate test examples web webapp

# 기본 변수 설정
INPUT_FILE ?= resources/미소구글SA구조개편_07.30.xlsx
OUTPUT_DIR ?= output
PYTHON_CMD = python3

# 기본 타겟 (make 명령어만 실행했을 때)
run: setup
	@echo "🚀 키워드 생성기 실행 중..."
	@. venv/bin/activate && cd src && python keyword_generator.py --input "$(INPUT_FILE)" --output "$(OUTPUT_DIR)"
	@echo "✅ 키워드 생성 완료!"

# 가상환경 설정 및 활성화
setup:
	@echo "🔧 가상환경 설정 중..."
	@if [ ! -d "venv" ]; then $(PYTHON_CMD) -m venv venv; fi
	@. venv/bin/activate && pip install -r requirements.txt > /dev/null 2>&1

# 키워드 생성기 실행 (별칭)
generate: run

# 웹앱 실행 (Streamlit)
web: setup
	@echo "🌐 Streamlit 웹앱 실행 중..."
	@echo "   브라우저가 자동으로 열립니다: http://localhost:8501"
	@echo "   종료하려면 Ctrl+C를 누르세요"
	@. venv/bin/activate && cd src && streamlit run streamlit_app.py --server.headless true --browser.gatherUsageStats false

# 웹앱 실행 (별칭)
webapp: web

# 특정 파일로 실행
file:
	@if [ -z "$(FILE)" ]; then \
		echo "❌ 오류: FILE 변수를 지정해야 합니다."; \
		echo "사용법: make file FILE=path/to/your/file.xlsx"; \
		exit 1; \
	fi
	@echo "📂 사용자 지정 파일로 실행: $(FILE)"
	@. venv/bin/activate && cd src && python keyword_generator.py --input "$(FILE)" --output "$(OUTPUT_DIR)"

# 출력 디렉토리 지정
output:
	@if [ -z "$(DIR)" ]; then \
		echo "❌ 오류: DIR 변수를 지정해야 합니다."; \
		echo "사용법: make output DIR=path/to/output/dir"; \
		exit 1; \
	fi
	@echo "📁 사용자 지정 출력 디렉토리: $(DIR)"
	@. venv/bin/activate && cd src && python keyword_generator.py --input "$(INPUT_FILE)" --output "$(DIR)"

# 파일과 출력 디렉토리 모두 지정
custom:
	@if [ -z "$(FILE)" ] || [ -z "$(DIR)" ]; then \
		echo "❌ 오류: FILE과 DIR 변수를 모두 지정해야 합니다."; \
		echo "사용법: make custom FILE=input.xlsx DIR=output_dir"; \
		exit 1; \
	fi
	@echo "🎯 사용자 지정 파일 및 출력 디렉토리"
	@echo "   입력: $(FILE)"
	@echo "   출력: $(DIR)"
	@. venv/bin/activate && cd src && python keyword_generator.py --input "$(FILE)" --output "$(DIR)"

# 출력 폴더 정리
clean:
	@echo "🧹 출력 파일 정리 중..."
	@rm -rf src/output/*.xlsx 2>/dev/null || true
	@if [ -n "$(DIR)" ]; then \
		rm -rf "$(DIR)"/*.xlsx 2>/dev/null || true; \
		echo "   $(DIR) 디렉토리 정리 완료"; \
	fi
	@echo "✅ 정리 완료!"

# 빌드 파일 정리
clean-build:
	@echo "🧹 빌드 파일 정리 중..."
	@rm -rf build dist package 2>/dev/null || true
	@rm -rf *.spec 2>/dev/null || true
	@rm -rf __pycache__ src/__pycache__ 2>/dev/null || true
	@echo "✅ 빌드 파일 정리 완료!"

# 전체 정리
clean-all: clean clean-build
	@echo "🧹 전체 정리 완료!"



# 개발 환경 초기화
dev-setup:
	@echo "💻 개발 환경 초기화 중..."
	@$(PYTHON_CMD) -m venv venv
	@. venv/bin/activate && pip install -r requirements.txt
	@echo "✅ 개발 환경 설정 완료!"

# 테스트 실행 (도움말 및 버전 확인)
test: setup
	@echo "🧪 기능 테스트 실행 중..."
	@. venv/bin/activate && cd src && python keyword_generator.py --help
	@echo ""
	@. venv/bin/activate && cd src && python keyword_generator.py --version



# 사용 예시 보기
examples:
	@echo "📚 키워드 생성기 사용 예시:"
	@echo ""
	@echo "🔹 기본 실행 (명령행):"
	@echo "   make run"
	@echo "   make generate"
	@echo ""
	@echo "🔹 웹앱 실행 (브라우저):"
	@echo "   make web"
	@echo "   make webapp"
	@echo ""

	@echo "🔹 특정 파일 사용:"
	@echo "   make file FILE=data/my_keywords.xlsx"
	@echo "   make file FILE=/absolute/path/to/file.xlsx"
	@echo ""
	@echo "🔹 출력 디렉토리 지정:"
	@echo "   make output DIR=results"
	@echo "   make output DIR=/path/to/output"
	@echo ""
	@echo "🔹 파일과 출력 디렉토리 모두 지정:"
	@echo "   make custom FILE=data.xlsx DIR=my_results"
	@echo ""
	@echo "🔹 직접 Python 명령어 사용:"
	@echo "   make setup  # 가상환경 설정"
	@echo "   . venv/bin/activate && cd src && python keyword_generator.py -i file.xlsx -o output"
	@echo ""
	@echo "🔹 정리 명령어:"
	@echo "   make clean              # 기본 출력 폴더 정리"
	@echo "   make clean DIR=my_dir   # 특정 디렉토리 정리"



# 도움말
help:
	@echo "🔧 키워드 생성기 - Makefile 명령어 도움말"
	@echo ""
	@echo "📌 기본 명령어:"
	@echo "   make run        - 키워드 생성기 실행 (기본 파일 사용)"
	@echo "   make generate   - 키워드 생성기 실행 (별칭)"
	@echo "   make web        - Streamlit 웹앱 실행"
	@echo "   make webapp     - Streamlit 웹앱 실행 (별칭)"
	@echo "   make setup      - 가상환경 설정"
	@echo "   make clean      - 출력 파일 정리"
	@echo "   make dev-setup  - 개발 환경 초기화"
	@echo ""

	@echo "🧹 정리 명령어:"
	@echo "   make clean      - 출력 파일 정리"
	@echo "   make clean-build - 빌드 파일 정리"
	@echo "   make clean-all  - 전체 정리"
	@echo ""
	@echo "🎯 고급 명령어:"
	@echo "   make file FILE=파일명           - 특정 파일로 실행"
	@echo "   make output DIR=디렉토리명       - 출력 디렉토리 지정"
	@echo "   make custom FILE=파일 DIR=디렉토리 - 파일과 출력 모두 지정"
	@echo ""
	@echo "🔍 정보 명령어:"
	@echo "   make test       - 기능 테스트 (도움말, 버전 확인)"
	@echo "   make examples   - 사용 예시 보기"
	@echo "   make help       - 이 도움말 표시"
	@echo ""
	@echo "📂 기본 설정:"
	@echo "   입력 파일: $(INPUT_FILE)"
	@echo "   출력 디렉토리: $(OUTPUT_DIR)"
	@echo ""
	@echo "💡 변수 오버라이드 예시:"
	@echo "   make run INPUT_FILE=my_data.xlsx OUTPUT_DIR=results" 