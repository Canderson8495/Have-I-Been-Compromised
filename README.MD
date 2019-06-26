## Why did I create this
This script was created in an effort to help my close friends and me stay proactive about seemingly common data breaches occuring every few weeks.
## How does it work
Well the basic structure of the program is that it queries the HaveIbeenpwned.com API for different usernames. Then it compares the results with the results generated from the last time the script was run. If it finds any discrepancies, which indicates a new breach, it will notify the breached account using it's contact information. 

## Data storage

The script's results are saved to a .JSON file in the same directory, I chose this route because I didn't want to this project to be dependent on the fact that there is a database running in the background at all times. Due to this decision, any user can download the program, change some basic information at the top of the file, and their program will be functional.

## Crontab
This program should be run on a schedule with programs like crontab because it's funtionality depends on the fact that it has previous dataset to compare to.

## Plans for the future
A feature is currently being developed into my personal website Canderson.xyz that allows a user to fill out a form with their account that should be checked and their contact information. This information would then be used in the script, and hopefully, this would allow the common person to stay proactive about their data security.
