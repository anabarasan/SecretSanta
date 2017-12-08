import json
import random
import ssl
import urllib2

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from smtplib import SMTP

from flask import Flask, request, render_template, url_for

SMTP_SERVER = "smtp.office365.com"
SMTP_SERVER_PORT = 587
USERNAME = ""
PASSWORD = ""
FROM_ADDR = ""
SUBJECT = "Your Mom has sent you a Task"

HOSTNAME = ""
MATTERMOST_HOST = ""
WEBHOOK = ""

def construct_mail_message(from_addr, to_addr, subject, text):
    """construct mail message"""
    msg = MIMEMultipart()
    msg['From'] = from_addr
    msg['To'] = to_addr
    msg['Subject'] = subject
    msg.attach(MIMEText(text, 'html'))
    return msg

def send_mail(smtp_server, smtp_server_port, username, password,
              from_addr, to_addr, subject, text):
    """ send email """
    message = construct_mail_message(from_addr, to_addr, subject, text)
    server = SMTP(smtp_server, smtp_server_port)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(from_addr, to_addr, message.as_string())
    server.quit()

def post_to_mattermost(channel, message):
    webhook = MATTERMOST_HOST + WEBHOOK
    logo = HOSTNAME + url_for('static', filename='santahat.jpg')
    payload = {
        "username": "SecretSanta",
        "icon": logo,
        "channel": channel,
        "text": message,
    }
    print payload
    mm_request = urllib2.Request(webhook, json.dumps(payload),
                                 {'Content-Type':'application/json'})
    context = ssl._create_unverified_context()
    response = urllib2.urlopen(mm_request, context=context)
    result = response.read()
    print result

WALLPAPERS = [
    'christmas_12.jpg',
    'Christmas-Cookies-Full.jpg',
    'Christmas-Cookies.jpg',
    'Christmas-Decoration-Patterb.jpg',
    'Christmas-Decorations.jpg',
    'Christmas-Lights.jpg',
    'Christmas-tree.jpg',
    'Firefox.png',
    'game-of-thrones.jpg',
    'golden-christmas-stars.jpg',
    'merry_christmas.jpg',
    'red-christmas.jpg',
    'santa-claus-flying.jpg',
    'small-christmas-house.jpg',
    'StarWars.jpg',
    'superheroes-christmas.jpg',
    'tangle-of-christmas-lights.jpg',
]

APP = Flask(__name__)


@APP.route('/', methods=['GET', 'POST'])
def home():
    flash_message = ""
    if request.method == 'POST':
        to_addr = request.form.get('sendto', None)
        message = request.form['content'].strip()
        private_message = (True
                           if request.form.get('private', '') == 'private'
                           else False)
        if to_addr and message:
            to_addr = to_addr.strip()
            message = """{0}
{1}
With Love, Mom""".format(to_addr, message)
            channel = to_addr if private_message else 'chrismom-chrischild'
            try:
                print "{0} messaging {1}to {2}".format(request.remote_addr,
                                                       'privately ' if private_message else '',
                                                       to_addr)
                post_to_mattermost(channel, message)
                flash_message = "message posted successfully"
            except Exception:
                flash_message = "something went wrong"
        else:
            flash_message = "Select a user and type a message"

    wallpaper = random.choice(WALLPAPERS)
    return render_template('index.html', message=flash_message,
                           logo=url_for('static', filename='secretsanta.jpg'),
                           wallpaper=url_for('static', filename=wallpaper))
