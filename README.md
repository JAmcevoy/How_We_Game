![Terminal](docs/images/terminal.JPG)

# Welcome to How We Game

[How We Game Survey](https://how-we-game-cf3ccf22f56d.herokuapp.com/)

- This Python script is designed to conduct a gaming survey and manage the administrative tasks associated with the collected data. Users can participate in the survey by providing their gaming preferences, and administrators can perform various actions such as counting users for each console, analyzing satisfaction ratings, and assessing user loyalty.

### User Survey and Data Collection Module
- Whats is this? 
    - This is a Survey setup around gamers.
- What is the aim of this software    
    - To find out what console people are currently playing.
    - To find out what is the most popular console based on age groups
    - Find out how loyal players are to their console of choice.

## User Hopes

- As a user I hope the software is easy to understand
- As a user I want to limit the amount errors unhandled
- As a user I would want constant information to ensure I am filling the survey out correctly.

## Features

- **User Survey** : Users can participate in the survey by answering questions about their preferred gaming console brand, satisfaction rating, age group, and loyalty choice.
- **Admin Panel** : Administrators have access to an admin panel where they can perform various actions based on user input. Actions include counting users for each console, analyzing satisfaction ratings, and assessing user loyalty.

## Wirframe Logic for Questions
![Wirframe Logic](docs/images/Wirframe.JPG)


## Prerequisites

- Google Sheets API Credentials
- Python 3
- Required Python libraries (install using pip install -r requirements.txt):
    - gspread
    - google-auth

## Python Script Overview/Pseudo Code

The provided code is a Python script that implements a simple survey system related to gaming preferences and console usage. The script utilizes Google Sheets for data storage and interaction. Here's a summary of the main components and functionalities:

### Google Sheets Integration

- The script uses the `gspread` library to interact with Google Sheets.
- Google Sheets API credentials are set up using a service account file (`creds.json`).
- The script opens a specific Google Sheets document named 'how_we_game' to store survey responses.

### Constants

- The script defines some constants such as the administrator password (`ADMIN_PASSWORD`) and valid console choices (`VALID_CONSOLE_CHOICES`).

### Mapping Dictionaries

- Dictionaries (`LET_TO_CONSOLE`, `LET_TO_AGE`, `LET_TO_LOYALTY`) are used to map user choices (e.g., 'A', 'B') to corresponding labels (e.g., 'Xbox', '25-34', 'Likely').

![Map Of Chocies](docs/images/map_choice.JPG)

### Question Prompts

- A dictionary named `QUESTION_PROMPTS` stores prompts for various survey questions. Each key in the dictionary corresponds to a question, and the associated value is the prompt.

![Question Prompts](docs/images/question_prom.JPG)

### User Input Validation

- Functions like `handle_invalid_choice` and `validate_satisfaction_rating` handle the validation of user inputs.

### User Login

- The `user_login` function allow the user to choose with panel they want to access admin or user. It also hanlde the exit from the system when user is complete.

### User Survey Functions

- The `user_questions` function collects survey responses from users, validates inputs, and updates the Google Sheets document accordingly.

### Admin Panel Functions

- The `admin_questions` function provides an admin panel to perform various actions based on user input, such as counting users for each console, getting the count of users with ratings above/below a threshold, and counting users likely to stay with their current console brand.

### Export to CSV

- The script includes a function (`export_results_to_csv`) to export survey results to a CSV file.

### Conditional Execution

- The script includes an `if __name__ == "__main__":` block to ensure that the main function is executed when the script is run.

## Usage

- **Google Sheets Setup:**
    - Create a Google Sheet named 'how_we_game.'
    - Share the sheet with the email address specified in    your Google Sheets API credentials.
- **Credentials:**
    - Obtain the creds.json file containing your Google Sheets API credentials.
    - Install Dependencies:
- **Survey Participation:**
    - Users can participate in the survey by selecting their preferences.
- **Admin Panel:**
    - Administrators can access the admin panel by providing the correct password.
    - Admins can choose from various actions to analyze survey data.
- **Error Handling:**
    - The script handles errors gracefully, providing informative messages to guide users and admins.
- **Data Persistence:**
    - User survey responses are appended to the Google Sheet for ongoing data analysis.

### Survey Questions:
- `console_brand`: Preferred gaming console brand (Xbox, PlayStation, Nintendo, PC).
- `satisfaction_rating`: Satisfaction rating on a scale of 1 to 10.
- `age_group`: Age group (18-24, 25-34, 35-44, 45+).
- `loyalty_choice`: Likelihood to stick with the current gaming console brand (Likely, Neutral, Unlikely).

## Survey Script Functions Overview

This section provides an overview of the functions used in the provided Python script for the How We Game survey system.

### 1. Google Sheets Integration

#### `update_worksheet(data, worksheet_name)`
- **Description:** Updates the specified Google Sheets worksheet with user responses.
- **Parameters:**
  - `data`: List containing user survey data.
  - `worksheet_name`: Name of the Google Sheets worksheet to update.

  ![Update Worksheet](docs/images/update_worksheet.JPG)

### 2. User Input and Validation

#### `handle_invalid_choice()`
- **Description:** Handles invalid choices entered by the user.

#### `validate_satisfaction_rating(answer)`
- **Description:** Validates user input for satisfaction rating.
- **Parameters:**
  - `answer`: User input for satisfaction rating.

  ![User Input Validation](docs/images/validation_user.JPG)

#### `get_user_choice(prompt, valid_choices)`
- **Description:** Gets and validates user input based on a prompt and valid choices.
- **Parameters:**
  - `prompt`: Prompt for the user.
  - `valid_choices`: Set of valid choices.

  ![Get User Choices](docs/images/get_user_choice.JPG)

### 3. User Survey Functions

#### `user_questions()`
- **Description:** Welcomes the user with a print and displays the user questions then returns the result

![User Survey Functions](docs/images/user.JPG)

#### `get_console_brand()`
- **Description:** Collects user survey responses for the console brand question.

![Console Brand](docs/images/console_fucntion.JPG)

#### `get_satisfaction_rating()`
- **Description:** Collects user survey responses for the Satisfaction rating question.

![Satisfaction Rating](docs/images/rating_fucntion.JPG)

#### `get_age_group()`
- **Description:** Collects user survey responses for the age group question.

![age group](docs/images/age_fucntion.JPG)

#### `get_loyalty_choice()`
- **Description:** Collects user survey responses for the loyalty choice question.

![Loyalty Choice](docs/images/loyalty_function.JPG)

#### `get_user_confirmation(data)`
- **Description:** Displays the users choices for each question then ask the user to confirm if they are happy with their answers. if selected no then the survey goes back to the first question.

![User Confirm](docs/images/user_confirm_fucntion.JPG)

### 4. Admin Panel Functions

#### `admin_questions()`
- **Description:** Provides an admin panel to perform various actions based on user input.

![Admin Panel Functions](docs/images/admin.JPG)

#### `console_count()`
- **Description:** Counts the number of users for each gaming console.

![Console Count](docs/images/console_count.JPG)

#### `get_rating()`
- **Description:** Gets the count of users with satisfaction ratings above or below a specified threshold.

![Count Rating](docs/images/get_rating.JPG)

#### `get_loyalty_count()`
- **Description:** Counts the number of users likely to stay with their current console brand for the next purchase.

![Loyalty Count](docs/images/get_loyalty.JPG)

#### `export_to_csv()`
- **Description:** Exports survey data to a CSV file.

![Export to CSV](docs/images/export.JPG)

### 5. User Login

#### `user_login()`
- **Description:** Manages user login, allowing users to choose between being a regular user or an admin.

![User Login](docs/images/user_login.JPG)

### 6. Conditional Execution

#### `__main__`
- **Description:** Ensures that the main function (`user_login()`) is executed when the script is run.


![Conditional Execution](docs/images/conditional.JPG)


## Constants and Configuration: 
- ADMIN_PASSWORD: Password to access the admin panel.
- VALID_CONSOLE_CHOICES: Set of valid choices for console preferences.

## Deployment

## Github
This section describes how to create a new repository.

- This repository was created using [GitHub](https://github.com/) The steps are as followed:
  - I went to the [Code Institute Template](https://github.com/Code-Institute-Org/ci-full-template)
  - I selected the green button labeled 'Use this template'
  - Then, Create a new repository.
  - Then I was brought to a new page to set the name and setting for my new repository.
  - I named my repository 'How_We_Game'

This section describes how I set up my workspace, Once my repository has been created.

## Codeanywhere
- The workspace I used for this project was [codeanywhere](https://app.codeanywhere.com/). The steps are as follows:
  - I opened [GitHub](https://github.com/) and went to the 'How_We_Game' repository.
  - To get the link for codeanywhere I clicked the green button '<>code'.
  - Here under local, I could copy the link needhttps://github.com/JAmcevoy/How_We_Game.gitS.git>
  - Then I went to code anywhere.
  - In workplaces, I selected new workspaces
  - Here I copied the link from the git hub and clicked to create to make my workspace.

## Setting Up APIs for Google Spreadsheet Access

### Step 1: Google Cloud Platform
Navigate to the [Google Cloud Platform](https://console.cloud.google.com/), the hub for developers using Google Cloud services, including Google Sheets. This is where we will configure the necessary APIs.

### Step 2: Create a New Project
Click on the "Select a project" button, then choose "new project." Provide a name for the project; for example, "loveSandwiches." Click "Select Project" to proceed.

### Step 3: Unique Projects
Create a new project for each distinct project requiring a Google Cloud API. This ensures unique access credentials for each project.

### Step 4: Enable APIs and Services
From the side menu, select "APIs and services" and then choose "Library." We need to enable two APIs: Google Drive and Google Sheets.

### Step 5: Enable Google Drive API
Use the search bar to find and select "Google Drive API." Click "Enable" to activate the API. This action will take you to the API overview page.

### Step 6: Generate Credentials for Google Drive API
To connect to the Google Drive API, generate credentials by clicking "Create credentials." Select "Google Drive API" in the dropdown, specify usage as "From a web server," and access application data. Choose "No" for the app or computer engine. Click "What credentials do I need?" and proceed to fill out the form with the necessary details:

- From the "Which API are you using?" dropdown menu, choose Google Drive API
- For the "What data will you be accessing?" question, select Application Data
- For the "Are you planning to use this API with Compute Engine, Kubernetes Engine, App Engine, or Cloud Functions?" question, select No, I'm not using them
- Click Next

### Step 7: Service Account and Role Configuration
Enter a Service Account name, for example, "How_we_game," and click "Create." In the Role Dropdown box, choose Basic > Editor, then press "Continue." You can leave other options blank. Click "Done."

### Step 8: Download Credentials File
On the next page, click on the Service Account that has been created. Then, click on the "Keys" tab. Click on the "Add Key" dropdown and select "Create New Key." Choose JSON and click "Create." This will trigger the JSON file with your API credentials to download to your machine.

### Step 9: Conclusion
Now, both APIs are enabled, and the credentials file is downloaded. In the next video, we will set up our development environment to proceed with Python code integration.



### 1. Create a Heroku App

- From the Heroku dashboard, click the "Create new app" button.
- Name your app (e.g., how-we-game) – ensure the name is unique.
- Choose your region (e.g., Europe) and click "Create app."

### 2. Configure App Settings

#### Config Vars

- Go to the "Settings" tab on your Heroku app dashboard.
- Locate the "Config Vars" section.
- Add a new config var:
  - Key: `CREDS` (all capital letters)
  - Value: Copy the entire content of the `creds.json` file from your Gitpod workspace.
  - Click "Add."

**Note:** The `creds.json` file is necessary for connecting to the API, and this config var ensures it's available during Heroku app deployment.

#### Buildpacks

- Go to the "Settings" tab and scroll down to the "Buildpacks" section.
- Add two buildpacks:
  1. Select "Python" and click "Save changes."
  2. Select "node.js" and click "Save."

Ensure the buildpacks are in the correct order: Python on top, and node.js underneath. Adjust the order if needed.

### 3. Deploy from GitHub

- Go to the "Deploy" tab on your Heroku app dashboard.
- Choose "Github" as the deployment method.
- Connect to your Github account and search for your repository name.
- Connect your Heroku app to your Github repository.

#### Deployment Method

Choose one of the following deployment methods:

- **Automatic Deploys:** Heroku will rebuild your app every time you push a new change to your Github repository.
- **Manual Deploy:** Manually deploy using the "Deploy Branch" option. This option allows you to show deployment logs as the app is built.

### 4. Monitor Deployment

- Watch the deployment logs to ensure a successful build.
- Verify the installation of Python, dependencies listed in `requirements.txt`, and node.js.

### 5. Test the Deployed App

- Once the deployment is successful, click the provided link to view your deployed app.
- Test the functionality of your app, ensuring that it operates as expected in the deployed environment.

Congratulations! You have successfully deployed the **How We Game Survey** project to Heroku. Verify that your app functions correctly in the live environment, and refer to the deployment logs for troubleshooting if needed.


## Constraints

The deployment terminal is set to 80 columns by 24 rows. That means that each line of text needs to be 80 characters or less otherwise it will be wrapped onto a second line.

### Features Left to Implement

- When I started this project I had an idea for one more admin function get most popular console by age group. This fucntion was suppose to pull and compare the two column from the spread sheet and display the most input console for each age group. However, I couldnt get the function to work each time it ran it display no data because of this I made a decision to remove it form the program. I would like this feature to be added if I had more time but at my current time and knowledge I didn't find it possible.

# Testing

- I tested that this page works in different browsers: Chrome, Firefox and Microsoft Edge.

![Chrome](docs/images/chrome.JPG)

![Firefox](docs/images/firfox.JPG)

![Microsoft Edge](docs/images/edge.JPG)

### Questions test

#### Aim - My aim in the choice test is to ensure no input besides the predefine choice could be input

### Testing

- Because of the limit of choice and most being answered A, B, C, D not much testing was required.

- There was some text and integer type questions further on so they will also be tested in this section.

    #### User Questions
    1. I started the survey and logged in as a user.
    2. I went through the first question a selected a random letter on my keyboard (L, K, H and anything that wasn't A, B, C or D)
            - **Input** = yes 
           - **Result** = Invalid choice. Please choose B, C, D, A..
        - **Input** = 43903645 
            - **Result** = Invalid choice. Please choose B, C, D, A.
        - **Input** = *Blank* 
            - **Result** = Invalid choice. Please choose B, C, D, A.
    3. Because of the error handling I set up for the fucntion the error was flagged and showed which chioce I has and printed the question again.
    4. The next question required a integer answer so I had to check that the console would not accept letters but also nothing lower that 1 or higher than 10.
        - **Input** = yes 
           - **Result** = Error: Invalid choice for rating. invalid literal for int() with base 10: 'yes'
        - **Input** = 11 and 0
            - **Result** = Error: Invalid choice for rating. invalid literal for int() with base 10: '11 and 0'
        - **Input** = *Blank* 
            - **Result** = Error: Invalid choice for rating. invalid literal for int() with base 10: ''
    5. Again, due my error handling the console display a message letting me know the correct values to choose.
    6. The last question were similar to the first two that they were multiple choice so the test method was the same as mentioned in (2.)

    #### Admin Questions
    1. The first admin question was to pull data from the spreadsheet so I had two factors to test.
        - Does the console allow me to input incorrect values
        - Is the data match my spreadsheet
    2. The answers for all of the admin questions were a simple Yes or No. So, once I got to the first question.
        - **Input** = Maybe 
           - **Result** = Invalid choice. Please enter yes or no.
        - **Input** = 8695 
            - **Result** = Invalid choice. Please enter yes or no.
        - **Input** = *Blank* 
            - **Result** = Invalid choice. Please enter yes or no.
    3. The error handling I set up for the yes and no questions handled the invalid input and then printed the question again.
    4. The next question had two part the first part was a ye4s or no answer so the output was the same as (2.) However there was a second part to this question which ask the admin if they wanted a count of submissions lower or higher than 5
        - **Input** = yes 
           - **Result** = Invalid Choice. Please choose higher or lower.
        - **Input** = 78 
            - **Result** = Invalid Choice. Please choose higher or lower.
        - **Input** = *Blank* 
            - **Result** = Invalid Choice. Please choose higher or lower.
    5. I noted down the number of submission for each questions then checked the spreadsheet and done a manual count. The numbers matched.
    6. Another feature of the admin is the option to export the spreadsheet with all submissions to that point. When I selected to export the spreadsheet it worked fine but I had to check all data was there so I compared the exported sheet with the one I am using to write back too.


### Conclusion

- My conlusion from this testing is that all the error handling I setup for the questions is working correct and will prevent any invalid date from submitting to the spreadsheet.
- From my testing I can also confirm that the data is in fact submitting to the spreadsheet correctly and is being pulled back correctly too.
- I can confirm the cvs is exported correctly and hold the correct data to the last submission.

### Validator Testing

- Python
  - No errors were returned when passing through the official [Python Code Chekcer](https://extendsclass.com/python-tester.html)
    ![python validator](docs/images/errors.JPG)

### Bugs I Faced Along The Way

- I had a lot of trouble finding the errors but more importanly knowing how to handle them. The invalid data was a hard issue to find my way around as most of my question we letter or number answers some of them required the user the type in something longer than a letter for example the higher or lower question. I just need to go through each question one by one and keep going till I  got it how I wanted.
- I struggled a little with some of the indentation in the script. Sometime I had to switch postion of the script or copy logic from one function to another when refactoring which cause the indentation to be a little off but I eventually got the hang of it.
- Another constant bug was whenever an invalid input was put in sometime it would exit the script or even just roll back to the first question in the section, weather it be admin or user. Using while loop I found a way to repeat the current question when a invalid option has been choosen.
- When I print the console count an extra count comes up that is not a console, not really sure why this is happening or where this extra variable is coming from. turns out my spreadsheet had some submission with a blank option for console brand. Left in from error testing.

![Unfix Bug](docs/images/unfix_bug.JPG)

### Bugs I did not get to fix

- For the export of the cvs, I noticed that in the app I cannot export the cvs to download in my browser. I am not sure if this is a requirement for the project but I found it worth mentioning when I test it in codeanywhere the csv file save to my file, this was the same when I tried it in replit.
- As mentioned above I had a feature to compare the age group and console to find the most popular per age group. I know this feature is no longer included but I found it necessary to bring up as it was a bug I could not fix even though it has been removed from the program.


## Credits

- I used these resources to research and develop my understanding of JavaScript, as well as get inspiration for my own code. During this research, I have borrowed some ideas and modified the code to suit my project. No code was used unedited

### Design

- All the design screenshots from above came from [Wirframe](https://wireframe.cc/)

### Code

- Python Documents was my main point of research for this project here I found all I need to complete this project along with example and explainations on how to use the code. [Python Documentation](https://docs.python.org/3/tutorial/errors.html)
