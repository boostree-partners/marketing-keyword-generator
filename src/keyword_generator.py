import pandas as pd
import itertools
import os
import argparse
from datetime import datetime

def load_source_data(file_path):
    """Load and preprocess source Excel file"""
    try:
        if not os.path.exists(file_path):
            print(f"File not found: {file_path}")
            return None, None, None
            
        # Read with header=None to get raw data
        df_raw = pd.read_excel(file_path, header=None)
        print(f"Raw data loaded: {df_raw.shape}")
        
        # First row (Excel row 1): Column numbers
        column_numbers = df_raw.iloc[0].tolist()
        print(f"Column numbers: {column_numbers}")
        
        # Second row (Excel row 2): Category titles
        category_titles = df_raw.iloc[1].tolist()
        print(f"Category titles: {category_titles}")
        
        # Actual data starts from row 3 (index 2)
        df_data = df_raw.iloc[2:].reset_index(drop=True)
        
        # Set column names to category titles
        df_data.columns = category_titles
        
        print(f"Data shape: {df_data.shape}")
        print(f"Column names: {df_data.columns.tolist()}")
        
        return df_data, column_numbers, category_titles
        
    except Exception as e:
        print(f"Data loading error: {e}")
        return None, None, None

def parse_combination_rule(rule_str):
    """Parse combination rule string (e.g., "2,3" -> [2, 3])"""
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

def generate_keyword_combinations(df_data, column_numbers, category_titles):
    """모든 조합 규칙에 따라 키워드 조합 생성"""
    results = []
    rule_group_mapping = {}
    
    print("\n=== 조합 규칙-그룹 매핑 ===")
    for idx, row in df_data.iterrows():
        rule = row.iloc[0]  # 조합 규칙 (A열)
        group = row.iloc[1]  # 그룹 (B열)
        if pd.notna(rule) and pd.notna(group):
            rule_group_mapping[str(rule)] = str(group)
            print(f"  {rule} -> {group}")
    
    print(f"총 {len(rule_group_mapping)}개 매핑")
    
    print("\n=== 데이터 구조 확인 ===")
    print("컬럼 번호와 카테고리 매핑:")
    for i, (col_num, category) in enumerate(zip(column_numbers, category_titles)):
        if pd.notna(col_num) and pd.notna(category):
            print(f"  {col_num} -> {category}")
    
    print(f"\n총 {len(rule_group_mapping)}개의 조합 규칙 처리 시작...")
    
    for rule_str, group in rule_group_mapping.items():
        print(f"\n조합 규칙 '{rule_str}' 처리 중...")
        print(f"  그룹: {group}")
        
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
                    print(f"  컬럼 번호 {rule_num} ({col_name}): {len(col_values)}개 값")
        
        if not column_values_list:
            continue
        
        # 카테시안 곱으로 모든 조합 생성
        combinations = list(itertools.product(*column_values_list))
        print(f"  생성된 조합: {len(combinations)}개")
        
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
    
    return pd.DataFrame(results)

def create_dashboard_data(results_df):
    """Dashboard 시트용 통계 데이터 생성"""
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

def save_to_excel(results_df, output_dir):
    """Dashboard와 그룹별 시트로 분리하여 엑셀 파일 저장"""
    # 출력 디렉토리 확인/생성
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
        print(f"출력 디렉토리 생성: {output_dir}")
    
    # 파일명 생성 (타임스탬프 포함)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"generated_keywords_{timestamp}.xlsx"
    filepath = os.path.join(output_dir, filename)
    
    # ExcelWriter로 여러 시트 생성
    with pd.ExcelWriter(filepath, engine='openpyxl') as writer:
        print("Dashboard 시트 생성 중...")
        # Dashboard 시트
        dashboard_data = create_dashboard_data(results_df)
        dashboard_df = pd.DataFrame(dashboard_data, columns=['항목', '값'])
        dashboard_df.to_excel(writer, sheet_name='Dashboard', index=False)
        
        print("그룹별 시트 생성 중...")
        # 그룹별 시트 생성
        for group in results_df['group'].unique():
            group_data = results_df[results_df['group'] == group]
            print(f"  '{group}' 시트 생성...")
            group_data.to_excel(writer, sheet_name=group, index=False)
    
    print(f"결과 저장 완료: {filepath}")
    return filepath, len(results_df)

def parse_arguments():
    """명령행 인자 파싱"""
    parser = argparse.ArgumentParser(
        description='키워드 조합 생성기',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
사용 예시:
  %(prog)s                                           # 기본 파일 사용
  %(prog)s -i data.xlsx                              # 특정 파일 사용
  %(prog)s -i data.xlsx -o results                   # 출력 디렉토리 지정
  %(prog)s --input path/to/file.xlsx --output ./out  # 전체 경로 지정
        """
    )
    
    parser.add_argument(
        '-i', '--input',
        default=os.path.join("resources", "미소구글SA구조개편_07.30.xlsx"),
        help='입력 엑셀 파일 경로 (기본값: resources/미소구글SA구조개편_07.30.xlsx)'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='output',
        help='출력 디렉토리 경로 (기본값: output)'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version='키워드 생성기 v1.0'
    )
    
    return parser.parse_args()

def main():
    """메인 함수"""
    # 명령행 인자 파싱
    args = parse_arguments()
    
    print("=== 키워드 생성기 시작 ===")
    print(f"소스 파일: {args.input}")
    print(f"출력 디렉토리: {args.output}")
    
    # 입력 파일 존재 확인
    if not os.path.exists(args.input):
        print(f"❌ 오류: 입력 파일을 찾을 수 없습니다: {args.input}")
        print("다음을 확인해 주세요:")
        print(f"  1. 파일 경로가 올바른지 확인")
        print(f"  2. 파일이 존재하는지 확인")
        print(f"  3. 파일 접근 권한이 있는지 확인")
        return 1
    
    # 1. 소스 데이터 로드
    df_data, column_numbers, category_titles = load_source_data(args.input)
    if df_data is None:
        print("❌ 데이터 로드 실패")
        return 1
    
    # 2. 키워드 조합 생성
    results_df = generate_keyword_combinations(df_data, column_numbers, category_titles)
    if results_df.empty:
        print("❌ 키워드 조합 생성 실패")
        return 1
    
    # 3. 엑셀 파일로 저장
    try:
        filepath, total_count = save_to_excel(results_df, args.output)
        print(f"총 {total_count:,}개의 키워드 조합이 저장되었습니다.")
        
        # 통계 출력
        print("\n=== 생성 결과 통계 ===")
        print("규칙별 키워드 개수 (상위 10개):")
        print(results_df['rule'].value_counts().head(10))
        
        print("\n그룹별 키워드 개수:")
        print(results_df['group'].value_counts())
        
        print(f"\n생성된 시트:")
        print(f"  1. Dashboard (통계 정보)")
        for i, group in enumerate(results_df['group'].unique(), 2):
            group_count = len(results_df[results_df['group'] == group])
            print(f"  {i}. {group} ({group_count:,}개 키워드)")
        
        print(f"\n=== 생성된 키워드 샘플 (처음 10개) ===")
        for i, row in results_df.head(10).iterrows():
            print(f"{i+1}. [{row['rule']}] [{row['group']}] {row['keyword']}")
        
        print("\n=== 키워드 생성기 완료 ===")
        return 0
        
    except Exception as e:
        print(f"❌ 저장 중 오류 발생: {e}")
        return 1

if __name__ == "__main__":
    exit(main()) 