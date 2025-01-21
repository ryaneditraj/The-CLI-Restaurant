from flask import Flask, render_template, request
import smtplib


server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
sender_email = "senderemail@gmail.com"
sender_pass = "senderpass"
recipients_email = "reciever@gmail.com"
server.login(sender_email, sender_pass)


app = Flask(__name__)
app.config['SECRET_KEY'] = 'our very hard to guess secretfir'
@app.route('/email')
def email():
    sendmail()
    return render_template('index.html')

    

@app.route('/',  methods=['GET', 'POST'])
def index():
        if request.method == 'POST':
        
        
            name = request.form['name']
            mobilenumber = request.form['mobilenumber']
            numberpers = request.form['numberpers']
            print(name+ " " + mobilenumber +" " + numberpers)
            
            

            server.sendmail(str(sender_email),
                            recipients_email,
                            f"""
                            Name:{name}
                            Mobile Number:{mobilenumber}
                            Number of people:{numberpers}
                            """)
            return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Submitted</title>
</head>
<body>
    <H1> Dear {name}, Please expect a call from us shortly.</H1>
    <style>
        h1{{
            font-size:5vw;
            font-family:'Times New Roman', Times, serif;
            text-align:center;
        }}
    </style>
</body>
</html>"""
        
        
        
        return render_template('index.html', message="error")

# Simple form handling using raw HTML forms
@app.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    return "not available"


app.run(debug=True)
