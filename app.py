from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
import os
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

load_dotenv()  # Load .env

app = Flask(__name__)

# Load API key and email credentials
openai.api_key = os.getenv("OPENAI_API_KEY")
EMAIL_USER = os.getenv("EMAIL_USER")
EMAIL_PASS = os.getenv("EMAIL_PASS")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_email():
    prompt = request.form['prompt']

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an assistant that writes professional emails."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )
        email_text = response['choices'][0]['message']['content']
        return jsonify({'email': email_text})
    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/send', methods=['POST'])
def send_email():
    recipient = request.form['recipient']
    subject = request.form['subject']
    message_body = request.form['message']

    try:
        msg = MIMEMultipart()
        msg['From'] = EMAIL_USER
        msg['To'] = recipient
        msg['Subject'] = subject

        msg.attach(MIMEText(message_body, 'plain'))

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_USER, EMAIL_PASS)
        server.send_message(msg)
        server.quit()

        return jsonify({'success': 'Email sent successfully!'})
    except Exception as e:
        return jsonify({'error': str(e)})

if __name__ == '__main__':
    app.run(debug=True)
