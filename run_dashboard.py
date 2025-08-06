"""
대시보드 실행 스크립트
"""

import subprocess
import sys
import os

def run_dashboard():
    """대시보드 실행"""
    print("🚀 GPT Bitcoin 자동매매 대시보드 시작...")
    print("=" * 50)
    print("📊 웹 브라우저에서 http://localhost:8501 으로 접속하세요")
    print("🔄 대시보드를 종료하려면 Ctrl+C를 누르세요")
    print("=" * 50)
    
    try:
        # Streamlit 대시보드 실행
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", "dashboard.py",
            "--server.port", "8501",
            "--server.address", "localhost",
            "--server.headless", "true"
        ])
    except KeyboardInterrupt:
        print("\n🛑 대시보드가 종료되었습니다.")
    except Exception as e:
        print(f"❌ 대시보드 실행 오류: {e}")

if __name__ == "__main__":
    run_dashboard()
