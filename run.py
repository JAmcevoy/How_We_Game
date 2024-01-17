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

let_to_console = {'A': 'Xbox', 'B': 'PlayStation', 'C': 'Nintendo', 'D': 'PC'}
let_to_age = {'A': '18-24', 'B': '25-34', 'C': '35-44', 'D': '45+'}
let_to_loyalty = {'A': 'Likely', 'B': 'Neutral', 'C': 'Unlikely'}

def handle_invalid_choice():
    print("Invalid choice. Please enter yes or no.")

def user_questions(SHEET):
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
            handle_invalid_choice()

def admin_questions(SHEET):
    print("Welcome to How We Game Admin Panel!")

    try:
        while True:
            console_count_input = input("1. What is the number of users for each console? (yes/no): ").lower()
            if console_count_input == "yes" or console_count_input == "no":
                break
            else:
                handle_invalid_choice()

        if console_count_input == "yes":
            console_count(SHEET)

        while True:
            rating_count_input = input("2. How many users gave a rating greater than 5 or less than 5? (yes/no): ").lower()
            if rating_count_input == "yes" or rating_count_input == "no":
                break
            else:
                handle_invalid_choice()

        if rating_count_input == "yes":
            get_rating(SHEET)

        while True:
            loyalty_count_input = input("3. How many users are likely to stay with their current console brand? (yes/no): ").lower()
            if loyalty_count_input == "yes" or loyalty_count_input == "no":
                break
            else:
                handle_invalid_choice()

        if loyalty_count_input == "yes":
            get_loyalty_count(SHEET)

    except Exception as e:
        print(f"Error: {e}")
        print("An error occurred. Please try again.\n")

def user_login(SHEET):
    while True:
        user_type = input("Which user type do you wish to continue with? User or Admin: ").lower()

        if user_type == "user":
            data = user_questions(SHEET)
            if data is not None:
                update_worksheet(data, 'submissions', SHEET)
                print("Survey submitted successfully!")
                break
            else:
                print("Let's try again.")
        elif user_type == "admin":
            admin_password = input("Enter the admin password: ")

            if admin_password == 'Letsgame24!':
                admin_questions(SHEET)
                break
            else:
                print("Incorrect password. Access denied.")
        else:
            print("Invalid User. Please select User or Admin.")

def update_worksheet(data, worksheet_name, SHEET):
    try:
        console_brand, satisfaction_rating, age_group, loyalty_choice = data
        console_brand = let_to_console.get(console_brand, console_brand)
        age_group = let_to_age.get(age_group, age_group)
        loyalty_choice = let_to_loyalty.get(loyalty_choice, loyalty_choice)

        data_with_words = [console_brand, satisfaction_rating, age_group, loyalty_choice]

        print(f"Updating {worksheet_name} worksheet...\n")
        sheet = SHEET
        worksheet_to_update = sheet.worksheet(worksheet_name)
        worksheet_to_update.append_row(data_with_words)
        print(f"{worksheet_name} worksheet updated successfully\n")
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to update worksheet. Please try again.\n")

def console_count(SHEET):
    try:
        console_column = SHEET.worksheet("submissions").col_values(1)[1:]

        xbox_count = console_column.count('Xbox')
        playstation_count = console_column.count('PlayStation')
        nintendo_count = console_column.count('Nintendo')
        pc_count = console_column.count('PC')

        print("Number of users for each console")
        print(f"Xbox: {xbox_count}")
        print(f"Playstation: {playstation_count}")
        print(f"Nintendo: {nintendo_count}")
        print(f"PC: {pc_count}")
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to retrieve console count. Please try again.\n")

def get_rating(SHEET):
    try:
        satisfaction_column = SHEET.worksheet("submissions").col_values(2)[1:]
        valid_ratings = all(value.isdigit() for value in satisfaction_column)

        if not valid_ratings:
            raise ValueError("No valid numeric ratings found in the column.")

        satisfaction_column = [int(rating) for rating in satisfaction_column]

        high_or_low = input("How many Higher than 5 or lower than 5? (Higher/Lower): ").lower()

        if high_or_low == "higher":
            above_5_count = sum(1 for rating in satisfaction_column if rating > 5)
            print(f"Number of users with a rating above 5: {above_5_count}")
        elif high_or_low == "lower":
            below_5_count = sum(1 for rating in satisfaction_column if rating < 5)
            print(f"Number of users with a rating below 5: {below_5_count}")
        else:
            raise ValueError("Invalid Choice. Please choose higher or lower than 5")
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to retrieve rating count. Please try again.\n")


def get_loyalty_count(SHEET):
  """
  Count the number of users likely to stay with their console choice next purchase (Likely, Neutral, Unlikely)
  """
  try:
      loyalty_column = SHEET.worksheet("submissions").col_values(4)[1:]

      likely_count = loyalty_column.count('Likely')
      neutral_count = loyalty_column.count('Neutral')
      unlikely_count = loyalty_column.count('Unlikely')

      print("Number of users likely to stay with their current console brand:")
      print(f"Likely: {likely_count}")
      print(f"Neutral: {neutral_count}")
      print(f"Unlikely: {unlikely_count}")

  except Exception as e:
      print(f"Error: {e}")
      print("Failed to retrieve loyalty count. Please try again.\n")


def main():
    user_login(SHEET)
    data = user_questions(SHEET)
    update_worksheet(data, 'submissions', SHEET)

if __name__ == "__main__":
    main()
