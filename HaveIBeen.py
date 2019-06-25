import smtplib, ssl, email
import json
import requests
import os.path
from os import path
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

gmail_user = 'projdeploy@gmail.com'
gmail_password = 'Password Goes Here'
usernames = ["Thrillechs@gmail.com","Cameron22123","Canderson8495@gmail.com","Erryial","anitaa0570@yahoo.com"]

# First, we will open the file/create it if it doesn't exist


port = 465  # For SSL


# Create a secure SSL context
context = ssl.create_default_context()


server = smtplib.SMTP_SSL("smtp.gmail.com", port, context=context)
server.login(gmail_user, gmail_password)

try:
    path.exists("lastCheck.json")
    #It exists, so we'll parse it here
    LastBreachCheckFile = open("lastCheck.json", "r")
    LastBreachCheckJson = json.loads(LastBreachCheckFile.read())
    print(LastBreachCheckJson)
    LastBreachCheckFile.close()
except IOError:
    LastBreachCheck = open("lastCheck.json", "w+")
    print("There was an issue opening the file. Please contact System Administrator")
    LastBreachCheck.close()

userBreachList = []
#Now we want to parse the json
for name in usernames:
    #We're constructing our own json list
    data = {}
    data['Name'] = name
    print(name)

    r = requests.get('https://haveibeenpwned.com/api/v2/breachedaccount/'+name+'?includeUnverified=true')


    print(r.status_code)
    if r.status_code == 404:
        print("No breach has been found")
    else:
        print(r.content)
        jsonParse = json.loads(r.content)
        breaches = []
        descriptions = []
        domains = []
        for breach in jsonParse:
            print(breach['Title'])
            print(breach['Description'])
            print(breach['Domain'])
            information = []
            information.append(breach['Title'])
            information.append(breach['Description'])
            information.append(breach['Domain'])
            breaches.append(information)

#Dumping all the information into a json object
    data['Breaches'] = breaches
    userBreachList.append(data)
    data = {}
    breaches = []
    print(" ")

print(userBreachList)


#We want to check for any differences in the Breaches
#And there is most likely a better way to comparse these json objects
for old in LastBreachCheckJson:
    for new in userBreachList:
        if old['Name'] == new['Name']:
            #Found a name match
            for x in new['Breaches']:
                #Going through the new breach list, checking against old for x
                if x not in old['Breaches']:
                    message = MIMEMultipart()

                    message["From"] = gmail_user
                    message["To"] = "Thrillechs@gmail.com"
                    message["Subject"] = "A New Breach has been found - " + x[0]
                    msgAlternative = MIMEMultipart('alternative')
                    msgText = MIMEText("<h2>A new data breach has been found at " + x[0] +". </h2> <p><br><b>It's recommended that you change the passwords shared with the account used at that website.</p></b><br>" + "<p>Please click <a href='https://www."+ x[2] + "'> here </a> to go to the website. </p><br><p>"+ x[1] +"</p> <br> <h4> All data has been provided by <a href='haveibeenpwned.com'>haveibeenpwned.com</a>.</h4> ", 'html', 'utf-8')
                    msgAlternative.attach(msgText)
                    message.attach(msgAlternative)
                    print("Send out an email here")
                    text = message.as_string()
                    print(text)
                    server.sendmail(gmail_user, "Thrillechs@gmail.com", text)
                    #A new breach has been found
                #else:
                    #x was found within both breaches, nothing new


#Writing newBreachList to file
print(json.dumps(userBreachList))
NewBreachCheckJson = json.dumps(userBreachList)

LastBreachCheckWriter = open("lastCheck.json", "w+")

LastBreachCheckWriter.write(NewBreachCheckJson)
