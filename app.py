from flask import Flask, render_template, request
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

load_dotenv(f"{os.getcwd()}/{'.env'}")

SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')
SENDER_EMAIL = os.environ.get('SENDER_EMAIL')
PASSWORD = os.environ.get('SENDGRID_API_KEY')
RECEIVER_EMAIL = os.environ.get('RECEIVER_EMAIL')

# USE YOUR OWN npoint LINK! ADD AN IMAGE URL FOR YOUR POST. 👇
blog_url = ("https://gist.githubusercontent.com/gellowg/389b1e4d6ff8effac71badff67e4d388/raw"
            "/fc31e41f8e1a6b713eafb9859f3f7e335939d518/data.json")

posts = requests.get(blog_url).json()

app = Flask(__name__)


@app.route('/')
def get_all_posts():
    return render_template("index.html", all_posts=posts)


@app.route("/about")
def about():
    return render_template("about.html")


@app.route("/contact", methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        data = request.form
        # print(data["name"])
        # print(data["email"])
        # print(data["phone"])
        # print(data["message"])
        send_email(data["name"], data["email"], data["phone"], data["message"])
        return render_template("contact.html", msg_sent=True)
    return render_template("contact.html", msg_sent=False)


# message = MIMEMultipart("alternative")
# part2 = MIMEText(html2, "html")
# message.attach(part2)

#
def send_email(name, email, phone, message):
    message_out = Mail(
        from_email=SENDER_EMAIL,
        to_emails=RECEIVER_EMAIL,
        subject="Alexandr's Blog",
        html_content="<h1>Subject: <strong>New Message<strong></h1>"
                     f"<p>Name:  {name}</p>"
                     f"<p>Email: <a href='mailto:{email}' target='_blank'>{email}</a></link></p>"
                     f"<p>Phone:  {phone}</p>"
                     "<br/>"
                     f"<p>{message}</p>"
                    )

    try:
        sg = SendGridAPIClient(SENDGRID_API_KEY)
        response = sg.client.mail.send.post(request_body=message_out.get())
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)


@app.route("/post/<int:index>")
def show_post(index):
    requested_post = None
    for blog_post in posts:
        if blog_post["id"] == index:
            requested_post = blog_post
    return render_template("post.html", post=requested_post)


if __name__ == "__main__":
    app.run(debug=True, port=5001)
