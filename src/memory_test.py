#!/usr/bin/env python3
"""
Streamlit 메모리 사용량 테스트 스크립트
"""

import streamlit as st
import psutil
import os
import gc
import sys
from datetime import datetime

def get_memory_usage():
    """현재 프로세스의 메모리 사용량 반환 (MB)"""
    process = psutil.Process(os.getpid())
    return process.memory_info().rss / 1024 / 1024  # MB 단위

def format_bytes(bytes_size):
    """바이트를 읽기 쉬운 형태로 변환"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if bytes_size < 1024.0:
            return f"{bytes_size:.2f} {unit}"
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} TB"

def main():
    st.set_page_config(
        page_title="메모리 사용량 테스트",
        page_icon="🧠",
        layout="wide"
    )
    
    st.title("🧠 Streamlit 메모리 사용량 분석")
    st.markdown("---")
    
    # 실시간 메모리 모니터링
    col1, col2, col3 = st.columns(3)
    
    with col1:
        current_memory = get_memory_usage()
        st.metric("현재 메모리 사용량", f"{current_memory:.2f} MB")
    
    with col2:
        if 'initial_memory' not in st.session_state:
            st.session_state.initial_memory = current_memory
        memory_increase = current_memory - st.session_state.initial_memory
        st.metric("시작 대비 증가량", f"{memory_increase:.2f} MB", delta=f"{memory_increase:.2f} MB")
    
    with col3:
        if 'uploaded_files_count' not in st.session_state:
            st.session_state.uploaded_files_count = 0
        st.metric("업로드된 파일 수", st.session_state.uploaded_files_count)
    
    # 세션 상태 정보
    st.markdown("---")
    st.header("📊 세션 상태 정보")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🔍 현재 세션 상태")
        st.write(f"**세션 키 개수:** {len(st.session_state)}")
        if st.session_state:
            for key, value in st.session_state.items():
                if hasattr(value, '__len__') and not isinstance(value, str):
                    try:
                        size = len(value)
                        st.write(f"- `{key}`: {type(value).__name__} (크기: {size})")
                    except:
                        st.write(f"- `{key}`: {type(value).__name__}")
                else:
                    st.write(f"- `{key}`: {type(value).__name__}")
    
    with col2:
        st.subheader("🧹 메모리 관리")
        if st.button("🗑️ 가비지 컬렉션 실행", use_container_width=True):
            before_gc = get_memory_usage()
            collected = gc.collect()
            after_gc = get_memory_usage()
            freed = before_gc - after_gc
            st.success(f"GC 완료! {collected}개 객체 정리, {freed:.2f} MB 해제")
        
        if st.button("🔄 세션 상태 초기화", use_container_width=True):
            before_clear = get_memory_usage()
            for key in list(st.session_state.keys()):
                if key not in ['initial_memory']:  # 초기 메모리는 유지
                    del st.session_state[key]
            st.session_state.uploaded_files_count = 0
            after_clear = get_memory_usage()
            freed = before_clear - after_clear
            st.success(f"세션 상태 초기화 완료! {freed:.2f} MB 해제")
            st.rerun()
    
    # 파일 업로드 테스트
    st.markdown("---")
    st.header("📁 파일 업로드 메모리 테스트")
    
    uploaded_file = st.file_uploader(
        "테스트용 파일 업로드",
        type=['xlsx', 'xls', 'txt', 'csv'],
        help="파일을 업로드하여 메모리 사용량 변화를 확인하세요"
    )
    
    if uploaded_file is not None:
        # 업로드 전 메모리
        if 'memory_before_upload' not in st.session_state:
            st.session_state.memory_before_upload = get_memory_usage()
        
        # 파일 정보
        file_size_bytes = uploaded_file.size
        file_size_readable = format_bytes(file_size_bytes)
        
        st.success(f"✅ 파일 업로드 완료: {uploaded_file.name}")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.info(f"**파일 크기:** {file_size_readable}")
        with col2:
            memory_after_upload = get_memory_usage()
            memory_diff = memory_after_upload - st.session_state.memory_before_upload
            st.info(f"**메모리 증가:** {memory_diff:.2f} MB")
        with col3:
            ratio = (memory_diff * 1024 * 1024) / file_size_bytes if file_size_bytes > 0 else 0
            st.info(f"**메모리 배율:** {ratio:.2f}x")
        
        # 파일 카운트 증가
        st.session_state.uploaded_files_count += 1
        
        # 파일을 세션에 저장하여 누적 테스트
        if 'uploaded_files_data' not in st.session_state:
            st.session_state.uploaded_files_data = []
        
        # 파일 내용을 세션에 저장 (누적 테스트용)
        file_data = {
            'name': uploaded_file.name,
            'size': file_size_bytes,
            'content': uploaded_file.read(),  # 메모리에 저장
            'upload_time': datetime.now().strftime("%H:%M:%S")
        }
        st.session_state.uploaded_files_data.append(file_data)
        
        # 업로드된 파일 목록
        if st.session_state.uploaded_files_data:
            st.subheader("📋 세션에 저장된 파일 목록")
            for i, file_info in enumerate(st.session_state.uploaded_files_data):
                st.write(f"{i+1}. **{file_info['name']}** ({format_bytes(file_info['size'])}) - {file_info['upload_time']}")
            
            total_stored = sum(len(f['content']) for f in st.session_state.uploaded_files_data)
            st.write(f"**총 저장된 데이터:** {format_bytes(total_stored)}")
    
    # 메모리 정보 요약
    st.markdown("---")
    st.header("📈 메모리 사용 패턴 분석")
    
    # 시스템 메모리 정보
    memory_info = psutil.virtual_memory()
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💻 시스템 메모리")
        st.write(f"**전체 메모리:** {format_bytes(memory_info.total)}")
        st.write(f"**사용 중:** {format_bytes(memory_info.used)} ({memory_info.percent:.1f}%)")
        st.write(f"**사용 가능:** {format_bytes(memory_info.available)}")
    
    with col2:
        st.subheader("⚡ 프로세스 정보")
        process = psutil.Process(os.getpid())
        st.write(f"**PID:** {process.pid}")
        st.write(f"**RSS 메모리:** {format_bytes(process.memory_info().rss)}")
        st.write(f"**VMS 메모리:** {format_bytes(process.memory_info().vms)}")
    
    # 자동 새로고침 (옵션)
    st.markdown("---")
    auto_refresh = st.checkbox("🔄 자동 새로고침 (5초)", value=False)
    if auto_refresh:
        import time
        time.sleep(5)
        st.rerun()

if __name__ == "__main__":
    main()