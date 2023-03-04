import smtplib


def send_email(msg):
    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()
    server.login("meetingsandcoursesprinters@gmail.com", "")

    msg = msg
    server.sendmail("meetingsandcoursesprinters@gmail.com", "happel@cshl.edu", msg)
    server.quit()
