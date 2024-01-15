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
SHEET = GSPREAD_CLIENT.open('how_we_game')

def ask_preferred_console():
    print("What is your preferred gaming console brand?")
    print("A. Xbox")
    print("B. PlayStation")
    print("C. Nintendo")
    print("D. Other")

    user_choice = input("Enter the letter corresponding to your choice: ").upper()

    if user_choice == 'A':
        return "Xbox"
    elif user_choice == 'B':
        return "PlayStation"
    elif user_choice == 'C':
        return "Nintendo"
    elif user_choice == 'D':
        other_specify = input("Please specify the other gaming console brand: ")
        return f"Other: {other_specify}"
    else:
        print("Invalid choice. Please enter a valid letter.")
        return ask_preferred_console()
    
ask_preferred_console()

