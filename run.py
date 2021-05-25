import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')

def get_sales_data():
    """
    Get sales figures input from the user.
    """

    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here: ")
        
        sales_data = data_str.split(",")
        
        if validate_data(sales_data):
            print("Data Valid")
            break
    
    return sales_data

def validate_data(values):
    """
    Parse all into integer.
    Raises VaalueError if can't conver or if not exactly 6 values
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True

def update_worksheet(data, worksheet):
    """
    Update sales worksheet, add new row with the list data provided
    Update surplus worksheet, add new row with the list data provided
    """
    print(f"Updating {worksheet} worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated!\n")


def calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate surplus
    positive stock - wasted
    minus stock - extra made
    """
    print("Calculate surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus_data.append(int(stock) - sales)
    
    return surplus_data

def get_las_5_entries_sales():
    """
    Retrievs last 5 rows from sales worksheet
    """
    sales = SHEET.worksheet("sales")
    columns = []
    for ind in range(1,7):
        column = sales.col_values(ind)
        columns.append(column[-5:])
    
    return columns

def calculate_stock_data(data):
    """
    Calculates stock data for recomendation
    """
    print(f"Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]
        average = sum(int_column)/5
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data



def main():
    """
    Run all program functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_worksheet(sales_data, "sales")
    surplus_result = calculate_surplus_data(sales_data)
    update_worksheet(surplus_result, "surplus")
    sales_columns = get_las_5_entries_sales()
    stock_data = calculate_stock_data(sales_columns)
    update_worksheet(stock_data, "stock")

print("Welcome to Love  Sandwiches data automation\n")
main()