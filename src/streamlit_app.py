import streamlit as st
import pandas as pd
import itertools
import os
import io
from datetime import datetime
import sys

# keyword_generator.py의 함수들을 import하기 위해 현재 디렉토리를 sys.path에 추가
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 기존 함수들을 그대로 재사용하되, print를 streamlit UI로 변경
def load_source_data_streamlit(uploaded_file):
    """Load and preprocess source Excel file for Streamlit"""
    try:
        # header=None으로 읽어서 원본 데이터 그대로 가져오기
        df_raw = pd.read_excel(uploaded_file, header=None)
        st.info(f"원본 데이터 로드 완료: {df_raw.shape}")
        
        # 첫 번째 행 (엑셀의 1행): 컬럼 번호들
        column_numbers = df_raw.iloc[0].tolist()
        
        # 두 번째 행 (엑셀의 2행): 카테고리 제목들
        category_titles = df_raw.iloc[1].tolist()
        
        # 실제 데이터는 3행부터 (인덱스 2부터)
        df_data = df_raw.iloc[2:].reset_index(drop=True)
        
        # 컬럼명을 카테고리 제목으로 설정
        df_data.columns = category_titles
        
        st.success(f"실제 데이터 형태: {df_data.shape}")
        
        # 컬럼 정보 표시
        with st.expander("📊 데이터 구조 확인"):
            st.write("**컬럼 번호와 카테고리 매핑:**")
            col_info = []
            for i, (col_num, category) in enumerate(zip(column_numbers, category_titles)):
                if pd.notna(col_num) and pd.notna(category):
                    col_info.append({"컬럼 번호": str(col_num), "카테고리": str(category)})
            st.dataframe(pd.DataFrame(col_info))
        
        return df_data, column_numbers, category_titles
        
    except Exception as e:
        st.error(f"데이터 로드 오류: {e}")
        return None, None, None

def parse_combination_rule(rule_str):
    """조합 규칙 문자열을 파싱 (예: "2,3" -> [2, 3])"""
    try:
        if pd.isna(rule_str):
            return []
        # 숫자만 추출하여 리스트로 변환
        numbers = [int(x.strip()) for x in str(rule_str).split(',') if x.strip().isdigit()]
        return numbers
    except:
        return []

def get_column_values(df, col_index, category_titles):
    """특정 컬럼의 모든 고유값 반환 (NaN 제외)"""
    if col_index > len(category_titles) - 1:
        return []
    
    # 카테고리 제목을 통해 컬럼명 찾기
    col_name = category_titles[col_index]
    
    if col_name in df.columns:
        unique_values = df[col_name].dropna().unique().tolist()
        # 빈 문자열이나 공백만 있는 값 제외
        unique_values = [val for val in unique_values if str(val).strip()]
        return unique_values
    return []

def generate_keyword_combinations_streamlit(df_data, column_numbers, category_titles):
    """스트림릿용 모든 조합 규칙에 따라 키워드 조합 생성"""
    results = []
    rule_group_mapping = {}
    
    # 진행 상황 표시
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    status_text.text("조합 규칙-그룹 매핑 생성 중...")
    
    for idx, row in df_data.iterrows():
        rule = row.iloc[0]  # 조합 규칙 (A열)
        group = row.iloc[1]  # 그룹 (B열)
        
        # 조합 규칙이 있고, 그룹이 비어있으면 'ungrouped'으로 대체
        if pd.notna(rule):
            if pd.isna(group) or str(group).strip() == '':
                group = 'ungrouped'
            rule_group_mapping[str(rule)] = str(group)
    
    st.info(f"총 {len(rule_group_mapping)}개 매핑 완료")
    
    # 규칙 매핑 정보 표시
    with st.expander("🔗 조합 규칙-그룹 매핑"):
        mapping_data = [{"조합 규칙": str(rule), "그룹": str(group)} for rule, group in rule_group_mapping.items()]
        st.dataframe(pd.DataFrame(mapping_data))
    
    total_rules = len(rule_group_mapping)
    current_rule = 0
    
    for rule_str, group in rule_group_mapping.items():
        current_rule += 1
        progress = current_rule / total_rules
        progress_bar.progress(progress)
        status_text.text(f"조합 규칙 '{rule_str}' 처리 중... ({current_rule}/{total_rules})")
        
        # 조합 규칙 파싱
        rule_numbers = parse_combination_rule(rule_str)
        if not rule_numbers:
            continue
        
        # 각 규칙 번호에 해당하는 컬럼 값들 가져오기
        column_values_list = []
        column_names = []
        
        for rule_num in rule_numbers:
            # rule_num은 1부터 시작하는 컬럼 번호
            # category_titles에서 찾기 위해 인덱스 조정
            col_values = get_column_values(df_data, rule_num + 1, category_titles)  # +1은 조합/그룹 컬럼 때문
            if col_values:
                column_values_list.append(col_values)
                # 컬럼명 찾기
                if rule_num + 1 < len(category_titles):
                    col_name = category_titles[rule_num + 1]
                    column_names.append(col_name)
        
        if not column_values_list:
            continue
        
        # 카테시안 곱으로 모든 조합 생성
        combinations = list(itertools.product(*column_values_list))
        
        # 결과에 추가
        for combo in combinations:
            keyword = " ".join(str(item) for item in combo)
            components = " | ".join(str(item) for item in combo)
            
            results.append({
                'rule': rule_str,
                'group': group,
                'columns': ", ".join(column_names),
                'keyword': keyword,
                'components': components
            })
    
    progress_bar.progress(1.0)
    status_text.text("키워드 조합 생성 완료!")
    
    return pd.DataFrame(results)

def create_dashboard_data(results_df):
    """Dashboard용 통계 데이터 생성"""
    dashboard_data = []
    
    # 기본 통계
    total_keywords = len(results_df)
    total_rules = results_df['rule'].nunique()
    total_groups = results_df['group'].nunique()
    
    # 헤더 추가 (Numbers 호환성을 위해 === 제거)
    dashboard_data.append(['키워드 생성 통계', ''])
    dashboard_data.append(['생성 일시', datetime.now().strftime("%Y-%m-%d %H:%M:%S")])
    dashboard_data.append(['총 키워드 수', f"{total_keywords:,}"])
    dashboard_data.append(['총 조합 규칙 수', total_rules])
    dashboard_data.append(['총 그룹 수', total_groups])
    dashboard_data.append(['', ''])
    
    # 그룹별 통계
    dashboard_data.append(['그룹별 키워드 수', ''])
    dashboard_data.append(['그룹명', '키워드 수'])
    group_counts = results_df['group'].value_counts()
    for group, count in group_counts.items():
        dashboard_data.append([group, f"{count:,}"])
    
    dashboard_data.append(['', ''])
    
    # 규칙별 통계 (상위 15개)
    dashboard_data.append(['규칙별 키워드 수 (상위 15개)', ''])
    dashboard_data.append(['규칙', '키워드 수'])
    rule_counts = results_df['rule'].value_counts().head(15)
    for rule, count in rule_counts.items():
        dashboard_data.append([rule, f"{count:,}"])
    
    return dashboard_data

def create_excel_download(results_df, progress_bar=None, status_text=None):
    """엑셀 파일을 메모리에서 생성하여 다운로드 가능한 형태로 반환"""
    buffer = io.BytesIO()
    
    # ExcelWriter로 여러 시트 생성
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        # Dashboard 시트
        if status_text:
            status_text.text("📊 Dashboard 시트 생성 중...")
        dashboard_data = create_dashboard_data(results_df)
        dashboard_df = pd.DataFrame(dashboard_data, columns=['항목', '값'])
        dashboard_df.to_excel(writer, sheet_name='Dashboard', index=False)
        
        if progress_bar:
            progress_bar.progress(30)
        
        # 그룹별 시트 생성
        unique_groups = results_df['group'].unique()
        total_groups = len(unique_groups)
        
        for i, group in enumerate(unique_groups):
            if status_text:
                status_text.text(f"📋 {group} 그룹 시트 생성 중... ({i+1}/{total_groups})")
            
            group_data = results_df[results_df['group'] == group]
            group_data.to_excel(writer, sheet_name=group, index=False)
            
            if progress_bar:
                # 30%에서 90%까지 그룹별로 진행
                progress = 30 + (i + 1) / total_groups * 60
                progress_bar.progress(int(progress))
    
    if progress_bar:
        progress_bar.progress(100)
    
    buffer.seek(0)
    return buffer.getvalue()

# Streamlit 앱 메인 UI
def main():
    st.set_page_config(
        page_title="키워드 생성기",
        page_icon="🔤",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # 세션 상태 초기화
    if 'results_df' not in st.session_state:
        st.session_state.results_df = None
    if 'file_processed' not in st.session_state:
        st.session_state.file_processed = False
    if 'current_file_name' not in st.session_state:
        st.session_state.current_file_name = None
    if 'excel_data' not in st.session_state:
        st.session_state.excel_data = None
    if 'excel_filename' not in st.session_state:
        st.session_state.excel_filename = None
    if 'reset_uploader' not in st.session_state:
        st.session_state.reset_uploader = False
    
    # 메인 헤더
    st.title("🔤 키워드 조합 생성기")
    st.markdown("---")
    
    # 사이드바
    with st.sidebar:
        st.header("📋 사용 방법")
        st.markdown("""
        1. **엑셀 파일 업로드**
           - 조합 규칙이 포함된 엑셀 파일을 업로드하세요
        
        2. **키워드 생성**
           - '키워드 생성' 버튼을 클릭하세요
        
        3. **결과 확인**
           - 생성된 키워드를 미리보기로 확인하세요
        
        4. **다운로드**
           - 엑셀 파일로 결과를 다운로드하세요
        """)
        
        # 양식 다운로드 버튼 추가
        st.markdown("---")
        st.markdown("**📥 양식 다운로드**")
        # sample_template.xlsx 파일을 읽어서 다운로드 버튼 생성
        template_path = os.path.join(os.path.dirname(__file__), "resources", "sample_template.xlsx")
        if os.path.exists(template_path):
            with open(template_path, "rb") as f:
                template_data = f.read()
            st.download_button(
                label="📄 엑셀 양식 다운로드",
                data=template_data,
                file_name="sample_template.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                help="키워드 생성에 사용할 엑셀 양식을 다운로드합니다",
                use_container_width=True
            )
        
        st.markdown("---")
        
        # 현재 상태 표시
        if st.session_state.results_df is not None:
            st.success(f"✅ 생성된 키워드: {len(st.session_state.results_df):,}개")
            if st.button("🔄 새로운 파일로 시작", use_container_width=True):
                st.session_state.results_df = None
                st.session_state.file_processed = False
                st.session_state.current_file_name = None
                st.session_state.excel_data = None
                st.session_state.excel_filename = None
                # 파일 업로더 초기화를 위해 세션 상태에 플래그 추가
                st.session_state.reset_uploader = True
                st.rerun()
    
    # 메인 컨텐츠 영역
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("📁 파일 업로드")
        
        # reset_uploader 플래그가 True인 경우 파일 업로더 초기화
        if st.session_state.reset_uploader:
            st.session_state.reset_uploader = False
            uploaded_file = None
        else:
            uploaded_file = st.file_uploader(
                "엑셀 파일을 업로드하세요",
                type=['xlsx', 'xls'],
                help="조합 규칙이 포함된 엑셀 파일을 선택하세요",
                key="file_uploader"  # 키를 추가하여 초기화 가능하도록
            )
    
    with col2:
        if uploaded_file:
            st.success("✅ 파일 업로드 완료")
            st.info(f"파일명: {uploaded_file.name}")
            st.info(f"파일 크기: {uploaded_file.size:,} bytes")
            
            # 새로운 파일인 경우 상태 초기화
            if st.session_state.current_file_name != uploaded_file.name:
                st.session_state.results_df = None
                st.session_state.file_processed = False
                st.session_state.current_file_name = uploaded_file.name
                st.session_state.excel_data = None
                st.session_state.excel_filename = None
    
    # 메인 콘텐츠
    if uploaded_file is not None:
        st.markdown("---")
        
        # 파일 로드 및 데이터 분석
        st.header("📊 데이터 분석")
        
        with st.spinner("파일을 분석하는 중..."):
            df_data, column_numbers, category_titles = load_source_data_streamlit(uploaded_file)
        
        if df_data is not None:
            # 키워드 생성 섹션
            st.markdown("---")
            st.header("🚀 키워드 생성")
            
            # 아직 결과가 없는 경우에만 생성 버튼 표시
            if st.session_state.results_df is None:
                if st.button("🔥 키워드 조합 생성 시작", type="primary", use_container_width=True):
                    with st.spinner("키워드 조합을 생성하는 중... 잠시만 기다려주세요."):
                        results_df = generate_keyword_combinations_streamlit(df_data, column_numbers, category_titles)
                    
                    if not results_df.empty:
                        # 세션 상태에 결과 저장
                        st.session_state.results_df = results_df
                        st.session_state.file_processed = True
                        st.success(f"🎉 총 {len(results_df):,}개의 키워드 조합이 생성되었습니다!")
                        st.rerun()  # 페이지 새로고침하여 결과 표시
                    else:
                        st.error("❌ 키워드 조합 생성에 실패했습니다.")
            
            # 결과가 있는 경우 결과 표시
            if st.session_state.results_df is not None:
                results_df = st.session_state.results_df
                
                st.success(f"🎉 총 {len(results_df):,}개의 키워드 조합이 생성되었습니다!")
                
                # 결과 통계 표시
                st.markdown("---")
                st.header("📈 생성 결과 통계")
                
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("총 키워드 수", f"{len(results_df):,}")
                with col2:
                    st.metric("총 규칙 수", results_df['rule'].nunique())
                with col3:
                    st.metric("총 그룹 수", results_df['group'].nunique())
                with col4:
                    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    st.metric("현재 시간", timestamp.split()[1])
                
                # 그룹별 통계
                col1, col2 = st.columns(2)
                
                with col1:
                    st.subheader("📊 그룹별 키워드 수")
                    group_counts = results_df['group'].value_counts()
                    st.bar_chart(group_counts)
                
                with col2:
                    st.subheader("📋 그룹별 상세 정보")
                    group_stats = []
                    for group in results_df['group'].unique():
                        count = len(results_df[results_df['group'] == group])
                        percentage = (count / len(results_df)) * 100
                        group_stats.append({
                            "그룹": str(group),
                            "키워드 수": f"{count:,}",
                            "비율": f"{percentage:.1f}%"
                        })
                    st.dataframe(pd.DataFrame(group_stats), use_container_width=True)
                
                # 결과 미리보기
                st.markdown("---")
                st.header("🔍 생성된 키워드 미리보기")
                
                # 그룹 필터 (key를 사용하여 상태 유지)
                all_groups = sorted(results_df['group'].unique())
                default_groups = all_groups[:3] if len(all_groups) > 3 else all_groups
                
                selected_groups = st.multiselect(
                    "표시할 그룹 선택",
                    options=all_groups,
                    default=default_groups,
                    key="group_filter"
                )
                
                if selected_groups:
                    filtered_df = results_df[results_df['group'].isin(selected_groups)]
                    
                    # 표시할 행 수 선택
                    max_rows = min(1000, len(filtered_df))
                    num_rows = st.slider(
                        "표시할 행 수", 
                        10, 
                        max_rows, 
                        min(50, max_rows),
                        key="num_rows_slider"
                    )
                    
                    # 데이터프레임 표시 (모든 컬럼을 문자열로 변환)
                    display_df = filtered_df.head(num_rows).copy()
                    for col in display_df.columns:
                        display_df[col] = display_df[col].astype(str)
                    
                    st.dataframe(
                        display_df,
                        use_container_width=True,
                        hide_index=True
                    )
                    
                    st.info(f"선택된 그룹에서 {len(filtered_df):,}개 중 {min(num_rows, len(filtered_df))}개 표시")
                else:
                    st.warning("표시할 그룹을 선택해주세요.")
                
                # 다운로드 섹션
                st.markdown("---")
                st.header("📥 결과 다운로드")
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    st.markdown("""
                    **다운로드되는 엑셀 파일 구성:**
                    - **Dashboard 시트**: 전체 통계 및 요약 정보
                    - **그룹별 시트**: 각 그룹의 키워드 목록
                    """)
                    
                    # 이미 생성된 엑셀 파일이 있는지 확인
                    if st.session_state.excel_data is not None:
                        st.success("📁 엑셀 파일이 이미 준비되어 있습니다!")
                        st.download_button(
                            label="📥 엑셀 파일 다운로드",
                            data=st.session_state.excel_data,
                            file_name=st.session_state.excel_filename,
                            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                            type="primary",
                            use_container_width=True
                        )
                        
                        if st.button("🔄 엑셀 파일 재생성", use_container_width=True):
                            st.session_state.excel_data = None
                            st.session_state.excel_filename = None
                            st.rerun()
                    else:
                        # 엑셀 파일 생성 버튼
                        if st.button("🔧 엑셀 파일 생성", type="primary", use_container_width=True):
                            with st.spinner("📊 엑셀 파일을 생성하는 중... 잠시만 기다려주세요."):
                                # 진행 상황 표시
                                progress_bar = st.progress(0)
                                status_text = st.empty()
                                
                                # 타임스탬프 생성
                                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                                filename = f"generated_keywords_{timestamp}.xlsx"
                                
                                # 엑셀 파일 생성 (진행 상황 표시 포함)
                                excel_data = create_excel_download(results_df, progress_bar, status_text)
                                
                                # 세션 상태에 저장
                                st.session_state.excel_data = excel_data
                                st.session_state.excel_filename = filename
                                
                                # 완료 메시지
                                status_text.text("✅ 엑셀 파일 생성 완료!")
                                
                                # 다운로드 버튼 표시
                                st.success("📁 엑셀 파일이 준비되었습니다!")
                                st.download_button(
                                    label="📥 엑셀 파일 다운로드",
                                    data=excel_data,
                                    file_name=filename,
                                    mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                                    type="primary",
                                    use_container_width=True
                                )
                        else:
                            st.info("💡 위의 '엑셀 파일 생성' 버튼을 클릭하여 다운로드 파일을 준비하세요.")
                
                with col2:
                    # 파일 정보 표시
                    if st.session_state.excel_data is not None:
                        st.success(f"""
                        **📁 엑셀 파일 정보**
                        - 파일명: {st.session_state.excel_filename}
                        - 총 시트 수: {results_df['group'].nunique() + 1}
                        - 총 키워드 수: {len(results_df):,}
                        """)
                    else:
                        st.info(f"""
                        **📊 예상 파일 정보**
                        - 총 시트 수: {results_df['group'].nunique() + 1}
                        - 총 키워드 수: {len(results_df):,}
                        """)
                    
                    # 생성될 시트 목록
                    with st.expander("📋 생성될 시트 목록"):
                        st.write("1. **Dashboard** (통계 정보)")
                        for i, group in enumerate(sorted(results_df['group'].unique()), 2):
                            group_count = len(results_df[results_df['group'] == group])
                            st.write(f"{i}. **{group}** ({group_count:,}개 키워드)")
        else:
            st.error("❌ 파일 로드에 실패했습니다.")
    
    else:
        # 파일이 업로드되지 않은 경우 안내 메시지
        st.info("""
        🎯 **키워드 생성기에 오신 것을 환영합니다!**
        
        엑셀 파일에 정의된 조합 규칙에 따라 키워드를 자동으로 생성하는 도구입니다.
        
        왼쪽에서 엑셀 파일을 업로드하여 시작하세요.
        """)
        
        # 샘플 이미지나 설명 추가 가능
        with st.expander("💡 지원하는 엑셀 파일 형식"):
            st.markdown("""
            - **A열**: 조합 규칙 (예: "2,3,4")
            - **B열**: 그룹명 (예: "SEO", "메인")
            - **C열 이후**: 키워드 카테고리별 데이터
            - **1행**: 컬럼 번호
            - **2행**: 카테고리 제목
            - **3행 이후**: 실제 키워드 데이터
            """)

if __name__ == "__main__":
    main()