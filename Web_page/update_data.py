import schedule
import time
from financial_data import FinancialDataProcessor

def update_financial_data():
    try:
        processor = FinancialDataProcessor()
        processor.load_data()
        print("Financial data updated successfully")
        # Add any additional processing or database updates here
    except Exception as e:
        print(f"Error updating financial data: {e}")

def main():
    try:
        # Run initial update
        update_financial_data()
        
        # Schedule data updates
        schedule.every().day.at("00:00").do(update_financial_data)
        
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        print("Update service stopped")
    except Exception as e:
        print(f"Error in main loop: {e}")

if __name__ == "__main__":
    main()