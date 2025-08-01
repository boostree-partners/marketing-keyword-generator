#!/usr/bin/env python3
"""
키워드 생성기 실행 파일 런처
비개발자도 쉽게 사용할 수 있도록 자동화된 실행기
"""

import os
import sys
import time
import socket
import subprocess
import webbrowser
import threading
from datetime import datetime

def find_free_port(start_port=8501):
    """사용 가능한 포트를 찾는 함수"""
    for port in range(start_port, start_port + 100):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def wait_for_server(port, timeout=30):
    """서버가 시작될 때까지 대기"""
    start_time = time.time()
    while time.time() - start_time < timeout:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                result = s.connect_ex(('localhost', port))
                if result == 0:
                    return True
        except:
            pass
        time.sleep(0.5)
    return False

def open_browser(url, delay=2):
    """지정된 시간 후 브라우저 열기"""
    def _open():
        time.sleep(delay)
        try:
            webbrowser.open(url)
            print(f"🌐 브라우저에서 {url} 이 열렸습니다")
        except Exception as e:
            print(f"⚠️  브라우저 자동 열기 실패: {e}")
            print(f"   수동으로 {url} 에 접속해주세요")
    
    thread = threading.Thread(target=_open)
    thread.daemon = True
    thread.start()

def get_script_dir():
    """스크립트가 위치한 디렉토리 반환 (PyInstaller 호환)"""
    if getattr(sys, 'frozen', False):
        # PyInstaller로 패키징된 경우
        return os.path.dirname(sys.executable)
    else:
        # 개발 환경
        return os.path.dirname(os.path.abspath(__file__))

def main():
    print("=" * 60)
    print("🔤 키워드 조합 생성기")
    print("=" * 60)
    print(f"⏰ 시작 시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 실행 경로 설정
    script_dir = get_script_dir()
    
    # streamlit_app.py 경로 찾기
    app_paths = [
        os.path.join(script_dir, 'streamlit_app.py'),  # PyInstaller에서 복사된 위치 (루트)
        os.path.join(script_dir, 'src', 'streamlit_app.py'),  # src 서브디렉토리
        os.path.join(script_dir, '..', 'src', 'streamlit_app.py'),  # 상위/src
    ]
    
    streamlit_app = None
    for path in app_paths:
        if os.path.exists(path):
            streamlit_app = path
            break
    
    if not streamlit_app:
        print("❌ 오류: streamlit_app.py 파일을 찾을 수 없습니다")
        print("   다음 위치를 확인했습니다:")
        for path in app_paths:
            exists = "✅ 존재" if os.path.exists(path) else "❌ 없음"
            print(f"   - {path} ({exists})")
        
        # 디버깅 정보 추가
        print(f"\n🔍 디버깅 정보:")
        print(f"   실행 파일 위치: {sys.executable}")
        print(f"   스크립트 디렉토리: {script_dir}")
        print(f"   현재 작업 디렉토리: {os.getcwd()}")
        
        input("\n엔터를 눌러 종료...")
        return 1
    
    print(f"📁 앱 파일 위치: {streamlit_app}")
    
    # 사용 가능한 포트 찾기
    port = find_free_port()
    if not port:
        print("❌ 오류: 사용 가능한 포트를 찾을 수 없습니다")
        input("\n엔터를 눌러 종료...")
        return 1
    
    print(f"🔌 사용 포트: {port}")
    
    # Streamlit 실행 명령어 구성
    cmd = [
        sys.executable, '-m', 'streamlit', 'run',
        streamlit_app,
        '--server.port', str(port),
        '--server.headless', 'true',
        '--browser.gatherUsageStats', 'false',
        '--server.enableXsrfProtection', 'false',
        '--server.enableCORS', 'false'
    ]
    
    print("🚀 웹 서버 시작 중...")
    print("   잠시만 기다려주세요...")
    
    try:
        # Streamlit 프로세스 시작
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )
        
        # 서버 시작 대기
        url = f"http://localhost:{port}"
        print(f"⏳ 서버 시작 대기 중... ({url})")
        
        if wait_for_server(port, timeout=30):
            print("✅ 서버 시작 완료!")
            print(f"🌐 웹 주소: {url}")
            
            # 브라우저 자동 열기
            open_browser(url, delay=1)
            
            print("\n" + "=" * 60)
            print("🎉 키워드 생성기가 실행되었습니다!")
            print("=" * 60)
            print("📌 사용법:")
            print("   1. 브라우저에서 엑셀 파일을 업로드하세요")
            print("   2. '키워드 조합 생성 시작' 버튼을 클릭하세요")
            print("   3. 결과를 확인하고 엑셀 파일로 다운로드하세요")
            print()
            print("⚠️  주의사항:")
            print("   - 이 창을 닫으면 웹앱이 종료됩니다")
            print("   - 종료하려면 Ctrl+C를 누르거나 이 창을 닫으세요")
            print("=" * 60)
            
            # 프로세스 대기
            try:
                process.wait()
            except KeyboardInterrupt:
                print("\n\n🛑 사용자가 종료를 요청했습니다")
                process.terminate()
                process.wait()
        else:
            print("❌ 오류: 서버 시작에 실패했습니다")
            process.terminate()
            
            # 에러 출력
            stdout, stderr = process.communicate()
            if stderr:
                print(f"오류 메시지: {stderr}")
            
            input("\n엔터를 눌러 종료...")
            return 1
            
    except Exception as e:
        print(f"❌ 실행 중 오류 발생: {e}")
        input("\n엔터를 눌러 종료...")
        return 1
    
    print("\n🔚 키워드 생성기가 종료되었습니다")
    print("   감사합니다!")
    
    # macOS에서는 자동 종료, Windows에서는 잠시 대기
    if sys.platform == 'darwin':
        time.sleep(2)
    else:
        input("\n엔터를 눌러 종료...")
    
    return 0

if __name__ == "__main__":
    sys.exit(main())