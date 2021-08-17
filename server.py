from flask import Flask, render_template, url_for, request, redirect, make_response
import csv
import smtplib, ssl
from email.message import EmailMessage

app = Flask(__name__)
print(__name__)

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<path:subpath>')
def sub_paths(subpath='index'):
    return render_template(subpath+'.html')

# def write_to_file(data):
#     with open('venv/database.txt', mode='a') as database:
#         name = data["name"]
#         email = data["email"]
#         message = data["message"]
#         file = database.write(f'\n{name},{email},{message}')

def write_to_csv(data):
    with open('venv/database.csv', newline='', mode='a') as database2:
        name = data["name"]
        email = data["email"]
        subject = data["subject"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name,email,subject,message])

def emailer(data):
    email = EmailMessage() #instantiate emailmessage object
    email['from'] = data['email']
    email['to'] = 'natemead99@gmail.com'
    email['subject'] = data['subject']+' Priority-'+data['demo-priority'] #define email to, from, and subject
    
    email.set_content(data['message']) #set the message to be sent to me from the user

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo() 
        smtp.starttls()
        smtp.login('natemead99@gmail.com', '@2019gmail.com')
        smtp.send_message(email)
        print('message sent')

    if 'demo-copy' in data:     #This checks for the key, because the key will only exist if the box is checked. 
                                #therefore it will work to check and see if the user wants a confirmation
        confirmation_email(data)
   

def confirmation_email(data):   #this is the function for confirmation emails 
                                #it's pretty much the same as above but sends to the user instead of me.
    email = EmailMessage()
    email['from'] = 'natemead99@gmail.com'
    email['to'] = data['email']
    email['subject'] = 'Confirmation'

    email.set_content('Your email has been recieved.')

    with smtplib.SMTP(host='smtp.gmail.com', port=587) as smtp:
        smtp.ehlo()
        smtp.starttls()
        smtp.login('natemead99@gmail.com', '@2019gmail.com')
        smtp.send_message(email)
        print('message sent')

@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    
    if request.method == 'POST':
    
            data = request.form.to_dict() #turning the data from the form to a dictionary
            print(data)
            write_to_csv(data)
            emailer(data)
            return redirect('/thankyou')
        


# @app.route('/generic')
# def generic():
#     return render_template('generic.html')

# @app.route('/elements')
# def elements():
#     return render_template('elements.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')