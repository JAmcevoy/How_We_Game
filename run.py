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

import csv

def user_questions():
    
    print("Welcome How We Game Survey")
    print("first question is...")


    console_brand = input("What is your preferred gaming console brand? A)Xbox B)PlayStation C)Nintendo D)PC : ").upper()
    while console_brand not in {'A', 'B', 'C', 'D'}:
        print("Invalid choice. Please choose A, B, C, or D.")
        console_brand = input("What is your preferred gaming console brand? (A/B/C/D): ").upper()

        
    print("Second question...")


    satisfaction_rating = int(input("On a scale of 1 to 10, how satisfied are you with your current gaming console? (1-10): "))
    while satisfaction_rating <= 1 or satisfaction_rating > 10:
        print("Invalid choice. Please choose a number between 1 and 10.")
        satisfaction_rating = int(input("On a scale of 1 to 10, how satisfied are you with your current gaming console? (1-10): "))

    
user_questions()

