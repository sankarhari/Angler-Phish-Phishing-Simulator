from flask import Flask, render_template, url_for, redirect, request
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app = Flask(__name__)

templates = [{"id":1,"name":"DHL","subject":"Your package has arrived","content":'<html><head><title></title></head><body><p style="margin-left:13.5pt">Hi {{.FirstName}},<br><br>Your package arrived at the post office. Here is your Shipping Document/Invoice and copy of DHL receipt for your tracking which includes the bill of lading and DHL tracking number, the new Import/Export policy supplied by DHL Express. Please kindly check the attached to confirm accordingly if your address is correct, before we submit to our outlet office for dispatch to your destination.</p><p style="margin-left:13.5pt"><strong>Label Number: E727D5151D<br>Class: Package Services<br>Service(s): Delivery Confirmation<br>Status: eNotification sent</strong></p><p><a href="{{.URL}}">View or download here</a>for the full statement information and a full description of package.</p><p style="margin-left:13.5pt">Your item will arrive from 2-5 days time.<br>We would like to thank you for using the services of DHL Express.<br>&nbsp;</p></body></html>'},{"id":2,"name":"LinkedIn","subject":"Messages awaiting your reply","content":'<html><head><title></title><link href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css" rel="stylesheet"></head><body><p>&nbsp;</p><h1 style="color:#4472c4"><b>LinkedIn</b></h1><h2 style="color:#4472c4">REMINDER</h2><p>&nbsp;</p><h3><b>Invitation reminders/:&nbsp;&nbsp;&nbsp; From&nbsp; &nbsp;<a href="{{.URL}}">Steve Donaghy</a></b></h3><h3><b>There are a total of</b><strong><b>4</b><b></b></strong><b>other messages awaiting your reply.&nbsp;&nbsp;<a href="{{.URL}}">Go to INBOX now</a>.</b></h3><p><b>&nbsp;</b></p><p><b>Don&rsquo;t want to receive email notifications? Login to your LinkedIn account to<a href="{{.URL}}">unsubscribe.</a><br>LinkedIn values your privacy.&nbsp; At no time has LinkedIn made your email address available to any other LinkedIn users without your permission.&nbsp;&nbsp;<br>c2013, LinkedIn Corporation.</b></p></body></html>'},{"id":3,"name":"Microsoft","subject":"Account login alert","content":'<html><head><link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.7/css/bootstrap.min.css"></head><body><h1 style="color:#4472c4">Microsoft Account</h1><p>Dear {{.FirstName}},</p><p>Someone in Bogotá Colombia attempted to log into your account several times. If you believe this was fraudulent activity please report it<a href="{{.URL}}">here</a>.</p><p>If you do not believe this to be fraudulent activity you may ignore this message</p><br><p>Sincerely,</p><p>Office365 @ COMPANY.com</p></body></html>'}]
trackers = {}
form_response = None

## Email SMTP Credentials
host_email = "" #Your GMail ID Here
google_app_password = "" #Your Google App Password Here

@app.route("/", methods = ["GET"])
def home():
    global form_response
    response = None
    if form_response:
        response = form_response
    form_response = {}
    return render_template("home.html", templates = templates, trackers = trackers, form_response = response)

@app.route("/sendmail", methods = ["POST"])
def sendmail():
    global form_response
    try:
        emails_str = request.form['emails']
        emails = emails_str.split(";")
        emails = [email.strip() for email in emails]

        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(host_email, google_app_password)

        html = templates[int(request.form['template']) - 1]["content"]

        msg = MIMEMultipart('alternative')

        msg['Subject'] = templates[int(request.form['template']) - 1]["subject"]
        msg['From'] = host_email

        for email in emails:

            baseurl = f"http://{ request.host }/clicked?email={email}"

            split_email = email.split("@")

            html = html.replace("{{.URL}}", baseurl)
            html = html.replace("{{.FirstName}}", split_email[0])
            html_body = MIMEText(html, 'html')

            msg['To'] = email
            msg.attach(html_body)

            server.send_message(msg)

        server.quit()
        form_response = { "code": "success" }
    except Exception as e:
        form_response = { "code": "failed", "message": e }

    return redirect(url_for("home"))

@app.route("/clicked", methods = ["GET"])
def clicked():
    email = request.args.get("email")
    if email in trackers:
        trackers[email] += 1
    else:
        trackers[email] = 1
    return render_template("clicked.html")



if __name__ == "__main__":
    app.run(debug = True, port = 8000)
