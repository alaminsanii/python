import smtplib

email = "[email protected]"
app_password = "abcdefghijklmnop"

server = smtplib.SMTP("smtp.gmail.com", 587)

server.starttls()

server.login(email, app_password)

server.sendmail(
    email,
    "[email protected]",
    "Subject: Test Mail\n\nHello World"
)

print("Email sent successfully!")

server.quit()