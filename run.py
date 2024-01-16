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
    while True:
        print("Welcome How We Game Survey")
        try:
            console_brand = input("What is your preferred gaming console brand? A)Xbox B)PlayStation C)Nintendo D)PC : ").upper()
            if console_brand not in {'A', 'B', 'C', 'D'}:
                raise ValueError("Invalid choice. Please choose A, B, C, or D.")
            
            satisfaction_rating = int(input("On a scale of 1 to 10, how satisfied are you with your current gaming console? (1-10): "))
            if not (1 <= satisfaction_rating <= 10):
                raise ValueError("Invalid choice. Please choose a number between 1 and 10.")
            
            age_group = input("What is your age group? A)18-24 B)25-34 C)35-44 D)45+ : ").upper()
            if age_group not in {'A', 'B', 'C', 'D'}:
                raise ValueError("Invalid choice. Please choose A, B, C, or D.")
            
            loyalty_choice = input("How likely are you to stick with your current gaming console brand for your next purchase? A)Likely B)Neutral C)Unlikely : ").upper()
            if loyalty_choice not in {'A', 'B', 'C'}:
                raise ValueError("Invalid choice. Please choose A, B, or C.")

            check_answers = input(f"Are you sure these are your final answers? Q1){console_brand} Q2){satisfaction_rating} Q3){age_group} Q4){loyalty_choice} : ")
            
            if check_answers.lower() == "yes":
                print("Thank you for completing the survey!")
                return [console_brand, satisfaction_rating, age_group, loyalty_choice]
            elif check_answers.lower() == "no":
                return None
            else:
                raise ValueError("Please select yes or no.")
        
        except ValueError as ve:
            print(f"Error: {ve}")
            print("Please provide valid input.\n")



def admin_questions():
    print("Welcome to How We Game Admin Panel!")
    print("Please confirm Yes/No to the following queries you wish to run:")

    try:
        console_count_input = input("1. What is the number of users for each console? (yes/no): ").lower()
        if console_count_input == "yes":
            console_count()
        
        rating_count_input = input("2. How many users gave a rating greater than 5 or less than 5? (yes/no): ").lower()
        if rating_count_input == "yes":
            get_rating()
        
        age_group_input = input("3. What is the most popular console for each age group? (yes/no): ").lower()
        if age_group_input == "yes":
            most_popular_console_by_age()

        loyalty_count_input = input("4. How many users are likely to stay with their current console brand? (yes/no): ").lower()
        if loyalty_count_input == "yes":
            get_loyalty_count()

    except Exception as e:
        print(f"Error: {e}")
        print("An error occurred. Please try again.\n")



def user_login():
    user_type = input("Which user type do you wish to continue with? User or Admin: ").lower()

    if user_type == "user":
        while not user_questions():
            print("Let's try again.")
    elif user_type == "admin":
        admin_password = input("Enter the admin password: ")
        
        if admin_password == 'Letsgame24!':
            admin_questions()
        else:
            print("Incorrect password. Access denied.")
    else:
        print("Invalid User. Please select User or Admin.")


def update_worksheet(data, worksheet_name):
    try:
        print(f"Updating {worksheet_name} worksheet...\n")
        worksheet_to_update = GSPREAD_CLIENT.open(SHEET_NAME).worksheet(worksheet_name)
        GSPREAD_CLIENT.insert_row(data, index=2, worksheet=worksheet_to_update)
        print(f"{worksheet_name} worksheet updated successfully\n")
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to update worksheet. Please try again.\n")

        


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


def get_rating():
    satisfaction_column = SHEET.sheet1.col_values(2)[1:]
    high_or_low = input("How many Higher than 5 or lower than 5? (Higher/Lower): ")

    if high_or_low.lower() == "higher":
        above_5_count = sum(1 for rating in satisfaction_column if int(rating) > 5)
        print(f"Number of users with a rating above 5: {above_5_count}")
    elif high_or_low.lower() == "lower":
        below_5_count = sum(1 for rating in satisfaction_column if int(rating) < 5)
        print(f"Number of users with a rating below 5: {below_5_count}")
    else:
        print("Invalid Choice. Please choose higher or lower than 5")

user_login()
data = user_questions()
ata = user_questions()
worksheet_name = "how_we_game"
update_worksheet(data, worksheet_name)