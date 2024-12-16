import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class FinancialDataProcessor:
    def __init__(self):
        # Initialize with your data sources
        self.profit_loss_data = None
        self.cash_flow_data = None
        self.working_capital_data = None
        
    def load_data(self):
        """Load financial data from CSV files"""
        try:
            self.profit_loss_data = {
                'Sales': 1000000,
                'Material Cost': -400000,
                'Manufacturing Cost': -150000,
                'Employee Cost': -200000,
                'Other Cost': -50000,
                'Operating Profit': 200000,
                'Other Income': 30000,
                'Interest': -20000,
                'Depreciation': -30000,
                'Profit Before Tax': 180000,
                'Tax': -45000,
                'Net Profit': 135000
            }
            
            self.cash_flow_data = {
                'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
                'operating': [100000, 120000, 90000, 110000, 130000, 125000],
                'investing': [-50000, -30000, -40000, -45000, -35000, -42000],
                'financing': [-20000, -25000, -22000, -18000, -28000, -30000]
            }
            
            # Load working capital data from CSV
            self.working_capital_data = pd.read_csv('data/working_capital.csv')

        except Exception as e:
            print(f"Error loading data: {e}")

    def process_profit_loss(self):
        return self.profit_loss_data

    def process_cash_flow(self):
        return {
            'labels': self.cash_flow_data['months'],
            'operating': self.cash_flow_data['operating'],
            'investing': self.cash_flow_data['investing'],
            'financing': self.cash_flow_data['financing']
        }

    def process_working_capital(self):
        """Process Working Capital metrics"""
        try:
            latest_data = self.working_capital_data.iloc[-1]
            return {
                "labels": ["DSO", "DPO", "DIO", "CCC"],
                "values": [
                    float(latest_data['Debtor Days']),      # DSO
                    float(latest_data['Days Payable']),     # DPO
                    float(latest_data['Inventory Days']),   # DIO
                    float(latest_data['Cash Conversion Cycle'])  # CCC
                ]
            }
        except Exception as e:
            print(f"Error processing working capital data: {e}")
            return None

    def get_monthly_trends(self):
        return {
            'labels': self.cash_flow_data['months'],
            'datasets': [
                {
                    'name': 'Operating Cash Flow',
                    'values': self.cash_flow_data['operating']
                },
                {
                    'name': 'Investing Cash Flow',
                    'values': self.cash_flow_data['investing']
                },
                {
                    'name': 'Financing Cash Flow',
                    'values': self.cash_flow_data['financing']
                }
            ]
            
        }