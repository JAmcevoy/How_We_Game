import gspread
from google.oauth2.service_account import Credentials
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
        if not (1 <= rating <= 10):
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

def user_questions():
    """
    Collect user survey responses and validate inputs.
    """
    while True:
        print("Welcome How We Game Survey")
        questions = {}

        for key, prompt in QUESTION_PROMPTS.items():
            while True:
                if key == 'console_brand':
                    answer = get_user_choice(prompt, VALID_CONSOLE_CHOICES)
                elif key == 'satisfaction_rating':
                    answer = input(prompt)
                    try:
                        questions[key] = validate_satisfaction_rating(answer)
                        break
                    except ValueError as ve:
                        print(f"Error: {ve}")
                        continue
                else:
                    answer = get_user_choice(prompt, VALID_CONSOLE_CHOICES)
                    questions[key] = answer

                break

            if key == 'loyalty_choice':
                while True:
                    check_answers = input(f"Are you sure these are your final answers? "
                                          f"Q1){questions.get('console_brand', '')} Q2){questions.get('satisfaction_rating', '')} "
                                          f"Q3){questions.get('age_group', '')} Q4){questions.get('loyalty_choice', '')} : ")

                    if check_answers.lower() == "yes" or check_answers.lower() == "no":
                        break
                    else:
                        print("Invalid choice. Please enter yes or no.")

                if check_answers.lower() == "yes":
                    print("Thank you for completing the survey!")
                    return [LET_TO_CONSOLE.get(questions.get('console_brand', ''), ''),
                            questions.get('satisfaction_rating', ''),
                            LET_TO_AGE.get(questions.get('age_group', ''), ''),
                            LET_TO_LOYALTY.get(questions.get('loyalty_choice', ''), '')]
                elif check_answers.lower() == "no":
                    break  # Allow the user to retry if they say "no"
                else:
                    raise ValueError("Please select yes or no.")

        another_attempt = input("Do you want to retry the survey? (yes/no): ").lower()
        if another_attempt != 'yes':
            print("You have left the system.")
            break

    return None 

def admin_questions():
    """
    Admin panel to perform various actions based on user input.
    """
    try:
        options = {
            'console_count': ('What is the number of users for each console? (yes/no): ', console_count),
            'rating_count': ('How many users gave a rating greater than 5 or less than 5? (yes/no): ', get_rating),
            'loyalty_count': ('How many users are likely to stay with their current console brand? (yes/no): ', get_loyalty_count),
            'export_csv': ('Export survey data to CSV? (yes/no): ', export_to_csv)
        }

        for option, (promt, function) in options.items():
            while True:
                user_input = input(promt).lower()
                if user_input == 'yes' or user_input == 'no':
                    break
                else:
                    handle_invalid_choice()
            if user_input == 'yes':
                function()

    except Exception as e:
        print(f"Error: {e}")
        print("An error occurred. Please try again.\n")

def user_login():
    """
    User login to choose between regular user and admin.
    """
    while True:
        user_type = input("Which user type do you wish to continue with? User or Admin: ").lower()

        if user_type == "user":
            data = user_questions()
            if data is not None:
                update_worksheet(data, 'submissions')
                print("Survey Submitted Successfully!")

        elif user_type == "admin":
            admin_password = input("Enter the admin password: ")

            if admin_password == ADMIN_PASSWORD:
                admin_questions()
            else:
                print("Incorrect password. Access denied.")

        else:
            print("Invalid User. Please select User or Admin.")

        another_attempt = input("Do you want to continue? (yes/no): ").lower()
        if another_attempt != 'yes':
            print("You have left the system.")
            break

def update_worksheet(data, worksheet_name):
    """
    Update the Google Sheet with user responses.
    """
    try:
        console_brand, satisfaction_rating, age_group, loyalty_choice = data
        data_with_words = [console_brand, satisfaction_rating, age_group, loyalty_choice]

        print(f"Updating {worksheet_name} worksheet...\n")
        worksheet_to_update = SHEET.worksheet(worksheet_name)
        worksheet_to_update.append_row(data_with_words)
        print(f"{worksheet_name} Worksheet Updated Successfully\n")

    except Exception as e:
        print(f"Error: {e}")
        print("Failed to update worksheet. Please try again.\n")

def console_count():
    """
    Count the number of users for each console.
    """
    try:
        console_column = SHEET.worksheet("submissions").col_values(1)[1:]

        for console in set(console_column):
            count = console_column.count(console)
            print(f"{LET_TO_CONSOLE.get(console, console)}: {count}")
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to retrieve console count. Please try again.\n")

def get_rating():
    """
    Get the count of users with ratings higher or lower than a threshold.
    """
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

def get_loyalty_count():
    """
    Count the number of users likely to stay with their console choice next purchase (Likely, Neutral, Unlikely).
    """
    try:
        loyalty_column = SHEET.worksheet("submissions").col_values(4)[1:]

        for loyalty in set(loyalty_column):
            count = loyalty_column.count(loyalty)
            print(f"{LET_TO_LOYALTY.get(loyalty, loyalty)}: {count}")

    except Exception as e:
        print(f"Error: {e}")
        print("Failed to retrieve loyalty count. Please try again.\n")

def export_to_csv():
    """
    Export survey data to a CSV file.
    """
    try:
        data = SHEET.worksheet("submissions").get_all_values()
        headers = data[0]
        rows = data[1:]

        with open('survey_data.csv', 'w', newline='') as csvfile:
            csvwriter = csv.writer(csvfile)
            csvwriter.writerow(headers)
            csvwriter.writerows(rows)

        print("Survey data exported to 'survey_data.csv' successfully.")
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to export survey data to CSV. Please try again.\n")

if __name__ == "__main__":
    user_login()
