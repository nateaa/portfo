from flask import Flask, render_template, url_for, request, redirect, make_response
import csv

app = Flask(__name__)
print(__name__)

@app.route('/')
def my_home():
    return render_template('index.html')

@app.route('/<path:subpath>')
def sub_paths(subpath='index'):
    return render_template(subpath+'.html')

def write_to_file(data):
    with open('venv/database.txt', mode='a') as database:
        name = data["name"]
        email = data["email"]
        message = data["message"]
        file = database.write(f'\n{name},{email},{message}')

def write_to_csv(data):
    with open('venv/database.csv', newline='', mode='a') as database2:
        name = data["name"]
        email = data["email"]
        message = data["message"]
        csv_writer = csv.writer(database2, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        csv_writer.writerow([name,email,message])


@app.route('/submit_form', methods=['POST', 'GET'])
def submit_form():
    
    if request.method == 'POST':
        try:
            data = request.form.to_dict()
            print(data)
            write_to_csv(data)
            return redirect('/thankyou')
        except:
            return 'did not save to database'
    else:
        return 'something went wrong, try again'

# @app.route('/generic')
# def generic():
#     return render_template('generic.html')

# @app.route('/elements')
# def elements():
#     return render_template('elements.html')

# @app.route('/contact')
# def contact():
#     return render_template('contact.html')