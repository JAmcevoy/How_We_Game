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

console_mapping = {'A': 'Xbox', 'B': 'PlayStation', 'C': 'Nintendo', 'D': 'PC'}
age_mapping = {'A': '18-24', 'B': '25-34', 'C': '35-44', 'D': '45+'}
loyalty_mapping = {'A': 'Likely', 'B': 'Neutral', 'C': 'Unlikely'}


def user_questions():
    """
    User survey questions
    """
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
    """
    admin control questions
    """
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
    """
    Prompts the user to pick a user type and directs them to the correct questions base on the user type.
    Asks the admin user for a defined password
    """
    while True:
        user_type = input("Which user type do you wish to continue with? User or Admin: ").lower()

        if user_type == "user":
            data = user_questions()
            if data is not None:
                update_worksheet(data, 'submissions')
                print("Survey submitted successfully!")
                break
            else:
                print("Let's try again.")
        elif user_type == "admin":
            admin_password = input("Enter the admin password: ")

            if admin_password == 'Letsgame24!':
                admin_questions()
                break
            else:
                print("Incorrect password. Access denied.")
        else:
            print("Invalid User. Please select User or Admin.")



def update_worksheet(data, worksheet_name):
    """
    Updates the worksheets with the answers from the user questions function.
    """
    try:
        print(f"Updating {worksheet_name} worksheet...\n")
        sheet = GSPREAD_CLIENT.open('how_we_game')
        worksheet_to_update = sheet.worksheet(worksheet_name)
        worksheet_to_update.append_row(data)
        print(f"{worksheet_name} worksheet updated successfully\n")
    except Exception as e:
        print(f"Error: {e}")
        print("Failed to update worksheet. Please try again.\n")


        
def console_count():
    """
    Counts the number of enteries by console type (Xbox, PlayStation, Nintendo, Pc)
    """
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


def most_popular_console_by_age():
    """
    Gets the the most popular console by ages group
    """
    try:
        age_column = SHEET.worksheet("submissions").col_values(3)[1:]
        console_column = SHEET.worksheet("submissions").col_values(1)[1:]

        age_groups = {'A': '18-24', 'B': '25-34', 'C': '35-44', 'D': '45+'}

        most_popular_console_by_age_group = {}

        for age_group_code, age_group in age_groups.items():
            age_indices = [i for i, age in enumerate(age_column) if age == age_group_code]
            consoles_for_age_group = [console_column[i] for i in age_indices]

            most_common_console = max(set(consoles_for_age_group), key=consoles_for_age_group.count)
            most_popular_console_by_age_group[age_group] = most_common_console

        print("Most popular console for each age group:")
        for age_group, console in most_popular_console_by_age_group.items():
            print(f"{age_group}: {console}")

    except Exception as e:
        print(f"Error: {e}")
        print("Failed to retrieve most popular console by age group. Please try again.\n")


def get_loyalty_count():
    """
    Count the how many user wish to stick with their console choice next purchase (Likely, Netural, Unlikely)
    """
    try:
        loyalty_column = SHEET.worksheet("submissions").col_values(4)[1:]

        likely_count = loyalty_column.count('A')
        neutral_count = loyalty_column.count('B')
        unlikely_count = loyalty_column.count('C')

        print("Number of users likely to stay with their current console brand:")
        print(f"Likely: {likely_count}")
        print(f"Neutral: {neutral_count}")
        print(f"Unlikely: {unlikely_count}")

    except Exception as e:
        print(f"Error: {e}")
        print("Failed to retrieve loyalty count. Please try again.\n")


user_login()
data = user_questions()
update_worksheet(data, 'submissions')