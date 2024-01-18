import gspread
from google.oauth2.service_account import Credentials
import logging
import csv

ADMIN_PASSWORD = 'Letsgame24!'
VALID_CONSOLE_CHOICES = {'A', 'B', 'C', 'D'}

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('how_we_game')

QUESTION_PROMPTS = {
    'console_brand': "What is your preferred gaming console brand? A)Xbox B)PlayStation C)Nintendo D)PC : ",
    'satisfaction_rating': "On a scale of 1 to 10, how satisfied are you with your current gaming console? (1-10): ",
    'age_group': "What is your age group? A)18-24 B)25-34 C)35-44 D)45+ : ",
    'loyalty_choice': "How likely are you to stick with your current gaming console brand for your next purchase? A)Likely B)Neutral C)Unlikely : "
}

LET_TO_CONSOLE = {'A': 'Xbox', 'B': 'PlayStation', 'C': 'Nintendo', 'D': 'PC'}
LET_TO_AGE = {'A': '18-24', 'B': '25-34', 'C': '35-44', 'D': '45+'}
LET_TO_LOYALTY = {'A': 'Likely', 'B': 'Neutral', 'C': 'Unlikely'}

def handle_invalid_choice():
    """
    Function to handle invalid choices
    """
    print("Invalid choice. Please enter yes or no.")

def validate_satisfaction_rating(answer):
    """
    Validate the satisfaction rating input.
    """
    try:
        rating = int(answer)
        if not (1<= rating <= 10):
            raise ValueError("Invalid choice for rating. Please choose a number between 1 and 10.")
        return rating
    except ValueError:
        raise ValueError("Invalid choice for rating. Please choose a number between 1 and 10.")

def get_user_choice(prompt, valid_choices):
    """
    Get and validate user input based on a prompt and valid choices.
    """
    while True: 
        answer = input(prompt).upper()
        if answer in valid_choices:
            return answer
        else:
            print(f"Invalid choice. Please choose {', '.join(valid_choices)}.")

def user_questions(SHEET):
    """
    Collect user survey responses and validate inputs.
    """
    print("Welcome To How We Game Survey")
    questions = {}

    for key, prompt in QUESTION_PROMPTS.items():
        while True:
            if key == 'console_brand':
                answer == get_user_choice(prompt, VALID_CONSOLE_CHOICES)
            elif key == 'satisfaction_rating':
                answer = input(promt)
                try: 
                    questions[key] = validate_satisfaction_rating(answer)
                    break
                except ValueError as ve:
                    logging.error(f"ValueError: {ve}")
                    print(f"Error: {ve}")
                    print("Please provide valid input.\n")
                    continue
            else:
                answer = get_user_choice(prompt, VALID_CONSOLE_CHOICES)
                questions[key] = answer
                break

        check_answers = input(f"Are you sure these are your final answers? "
                         f"Q1){questions['console_brand']} Q2){questions['satisfaction_rating']} "
                         f"Q3){questions['age_group']} Q4){questions['loyalty_choice']} : ")

    if check_answers.lower() == "yes":
        print("Thank you for completing the survey!")
        return [LET_TO_CONSOLE[questions['console_brand']], questions['satisfaction_rating'],
                LET_TO_AGE[questions['age_group']], LET_TO_LOYALTY[questions['loyalty_choice']]]
    elif check_answers.lower() == "no":
        return None
    else:
        raise ValueError("Please select yes or no.")
            

def admin_questions(SHEET):
    """
    Admin panel to perform various actions based on user input.
    """
    try: 
        options = {
            'console_count': ('What is the number of users for each console? (yes/no): ', console_count),
            'rating_count': ('How many users gave a rating greater than 5 or less than 5? (yes/no): ', get_rating),
            'loyalty_count': ('How many users are likely to stay with their current console brand? (yes/no): ', get_loyalty_count)
        }

        for option, (promt, function) in options.items():
            while True:
                user_input = input(promt).lower()
                if user_input == 'yes' or user_input == 'no':
                    break
                else: 
                    handle_invalid_choice
            if user_input == 'yes':
                function(SHEET)
    except Exception as e:
        print(f"Error: {e}")
        print("An error occurred. Please try again.\n")

def user_login(SHEET):
    """
    User login to choose between regular user and admin.
    """
    while True: 
        user_type = input("Which user type do you wish to continue with? User or Admin: ").lower()

        if user_type == "user":
            data = user_questions(SHEET)
            if data is not None:
                update_worksheet(data, 'submissions', SHEET)
                print("Survey Submitted Successfully!")
                export_results_to_csv([data])
                break
            else:
                print("Lets try again.")
        elif user_type == "admin":
            if admin_password == ADMIN_PASSWORD:
                admin_questions(SHEET)
                break
            else ("Incorrect password. Access denied.")    
        else:print("Invalid User. Please select User or Admin.")


        

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
