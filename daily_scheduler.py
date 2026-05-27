"""
=============================================================
AUTOMATIC DAILY DATA UPDATER
=============================================================
This script automatically fetches new stock data every day
and regenerates all analysis at a scheduled time.

Setup:
  1. pip install schedule
  2. Run: python daily_scheduler.py
  3. Script will fetch data every day at 6:00 PM
  4. Keep this script running in the background

Or use Windows Task Scheduler (see DAILY_UPDATE_SETUP.md)
=============================================================
"""

import os
import sys
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
import subprocess
import schedule
import time
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def fetch_data():
    """Fetch latest stock data from API"""
    print(f"\n{'='*60}")
    print(f"📡 FETCHING DATA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            [sys.executable, 'fetch_live_data.py'],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            print("✓ Data fetched successfully")
            return True
        else:
            print(f"✗ Error fetching data: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ Data fetch timeout (exceeded 10 minutes)")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def regenerate_analysis():
    """Regenerate all charts and analysis"""
    print(f"\n📊 REGENERATING ANALYSIS - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        result = subprocess.run(
            [sys.executable, 'stock_analysis.py', '--offline'],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            print("✓ Analysis charts regenerated")
            return True
        else:
            print(f"✗ Error generating analysis: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ Analysis timeout (exceeded 10 minutes)")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def build_excel_report():
    """Build Excel report with latest data"""
    print(f"\n📑 BUILDING EXCEL REPORT - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        result = subprocess.run(
            [sys.executable, 'build_excel.py'],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            print("✓ Excel report updated")
            return True
        else:
            print(f"✗ Error building Excel: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ Excel build timeout (exceeded 10 minutes)")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def update_dashboard_data():
    """Build dashboard live data script"""
    print(f"\n💻 UPDATING DASHBOARD DATA - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    try:
        result = subprocess.run(
            [sys.executable, 'generate_dashboard_data.py', '--provider', 'yahoo'],
            cwd=BASE_DIR,
            capture_output=True,
            text=True,
            timeout=600
        )
        
        if result.returncode == 0:
            print("✓ Dashboard live data updated")
            return True
        else:
            print(f"✗ Error updating dashboard: {result.stderr}")
            return False
    except subprocess.TimeoutExpired:
        print("✗ Dashboard update timeout (exceeded 10 minutes)")
        return False
    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return False

def daily_update():
    """Complete daily update pipeline"""
    print(f"\n{'#'*60}")
    print(f"# 🔄 DAILY UPDATE PIPELINE STARTED")
    print(f"# {datetime.now().strftime('%A, %B %d, %Y at %H:%M:%S')}")
    print(f"{'#'*60}")
    
    # Step 1: Fetch data
    if not fetch_data():
        print("\n⚠️  Skipping analysis - data fetch failed")
        return
    
    time.sleep(2)  # Brief pause between operations
    
    # Step 2: Regenerate analysis
    if not regenerate_analysis():
        print("\n⚠️  Skipping Excel - analysis generation failed")
        return
    
    time.sleep(2)
    
    # Step 3: Build Excel report
    if not build_excel_report():
        print("\n⚠️  Excel report failed")
        return
        
    time.sleep(2)
    
    # Step 4: Update Dashboard data
    if not update_dashboard_data():
        print("\n⚠️  Dashboard update failed")
        return
    
    print(f"\n{'#'*60}")
    print(f"# ✅ DAILY UPDATE COMPLETED SUCCESSFULLY")
    print(f"# {datetime.now().strftime('%A, %B %d, %Y at %H:%M:%S')}")
    print(f"{'#'*60}\n")

def schedule_updates():
    """Schedule daily updates at 6:00 PM"""
    print(f"\n{'='*60}")
    print(f"📅 DAILY SCHEDULER INITIALIZED")
    print(f"{'='*60}")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Updates scheduled for: 6:00 PM daily")
    print(f"(Stock market closes at 4:00 PM, allowing time for data)")
    print(f"\nScheduler running... Press Ctrl+C to stop\n")
    
    try:
        # Schedule daily update at 6:00 PM
        schedule.every().day.at("18:00").do(daily_update)
        
        # Keep scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    except KeyboardInterrupt:
        print("\n\n⏹️  Scheduler stopped by user")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Scheduler error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    # Check if schedule library is installed
    try:
        import schedule
    except ImportError:
        print("Installing 'schedule' library...")
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'schedule'])
        import schedule
    
    schedule_updates()
