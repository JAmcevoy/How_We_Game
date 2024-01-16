import gspread
from google.oauth2.service_account import Credentials

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('how_we_game')


def user_questions():
    """
    Holds all the questions for the survey
    """

    while True:
        print("Welcome How We Game Survey")
        print("First question is...")

        console_brand = input("What is your preferred gaming console brand? A)Xbox B)PlayStation C)Nintendo D)PC : ").upper()
        while console_brand not in {'A', 'B', 'C', 'D'}:
            print("Invalid choice. Please choose A, B, C, or D.")
            console_brand = input("What is your preferred gaming console brand? A)Xbox B)PlayStation C)Nintendo D)PC : ").upper()

        print("Second question...")

        satisfaction_rating = int(input("On a scale of 1 to 10, how satisfied are you with your current gaming console? (1-10): "))
        while satisfaction_rating < 1 or satisfaction_rating > 10:
            print("Invalid choice. Please choose a number between 1 and 10.")
            satisfaction_rating = int(input("On a scale of 1 to 10, how satisfied are you with your current gaming console? (1-10): "))

        print("Third Question...")

        age_group = input("What is your age group? A)18-24 B)25-34 C)35-44 D)45+ : ").upper()
        while age_group not in {'A', 'B', 'C', 'D'}:
            print("Invalid choice. Please choose A, B, C, or D.")
            age_group = input("What is your age group? A)18-24 B)25-34 C)35-44 D)45+ : ").upper()

        print("Final Question...")

        loyalty_choice = input("How likely are you to stick with your current gaming console brand for your next purchase? A)Likely B)Neutral C)Unlikely : ").upper()
        while loyalty_choice not in {'A', 'B', 'C'}:
            print("Invalid choice. Please choose A, B, or C.")
            loyalty_choice = input("How likely are you to stick with your current gaming console brand for your next purchase? A)Likely B)Neutral C)Unlikely : ").upper()

        check_answers = input(f"Are you sure these are your final answers? Q1){console_brand} Q2){satisfaction_rating} Q3){age_group} Q4){loyalty_choice}")

        if check_answers.lower() == "yes":
            print("Thank you for completing the survey!")
            return True
        elif check_answers.lower() == "no":
            return False


def admin_questions():
    """
    Holds the admin questions for
    """
    print("Welcome to How We Game Admin Panel!")
    print("Please confirm Yes/No to the following query you wish to run!")

    console_count = input("Run console count query? (yes/no): ")

    if console_count.lower() == "yes":
        console_count()


def user_login():
    user_type = input("Which user type do you wish to continue with? User or Admin: ")

    if user_type.lower() == "user":
        while not user_questions():
            print("Let's try again.")
    elif user_type.lower() == "admin":
        admin_questions()
    else:
        print("Invalid User. Please select User or Admin.")


def console_count():
    console_column = SHEET.sheet1.col_values(1)[1:]

    xbox_count = console_column.count('Xbox')
    playstation_count = console_column.count('PlayStation')
    nintendo_count = console_column.count('Nintendo')
    pc_count = console_column.count('PC')

    print("Number of users for each console")
    print(f"Xbox: {xbox_count}")
    print(f"Playstation: {playstation_count}")
    print(f"Nintendo: {nintendo_count}")
    print(f"PC: {pc_count}")


user_login()
