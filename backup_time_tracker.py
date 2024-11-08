import csv
import glob
import os
import smtplib
import time
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

dir_path = os.path.dirname(os.path.abspath(__file__)) + '\**\*.*'
excluded_files = {os.path.dirname(os.path.abspath(__file__)) + "\\file_creation.csv", os.path.dirname(os.path.abspath(__file__)) + "\\backup_time_tracker.py"}

file_dict = {}

for file in glob.glob(dir_path, recursive=True):
    if file not in excluded_files:
        creation_time = os.path.getctime(file)
        file_dict[file] = time.ctime(creation_time)

sorted_files = sorted(file_dict.items(), key=lambda x: x[1], reverse=True)

latest_file = sorted_files[0][0] if sorted_files else None
latest_file_creation_time = sorted_files[0][1] if sorted_files else None
if latest_file:
    print(f"Latest file: {latest_file} created on: {latest_file_creation_time}")

with open('file_creation.csv', 'w', newline='') as csvfile:
    csv_writer = csv.writer(csvfile, delimiter=',')
    csv_writer.writerow(['Folder', 'File', 'Last Backup'])
    for file, creation_time in sorted_files:
        folder = os.path.dirname(file)
        filename = os.path.basename(file)
        csv_writer.writerow([folder, filename, creation_time])

subject = "Files according to creation date"
body = "Email Body"
sender_email = os.getenv('sender_email')
recipient_email = os.getenv('recipient_email')
sender_password = os.getenv('sender_password')
smtp_server = "smtp.gmail.com"
smtp_port = 465
path_to_file = 'file_creation.csv'

message = MIMEMultipart()
message['Subject'] = subject
message['From'] = sender_email
message['To'] = recipient_email
body_part = MIMEText(body)
message.attach(body_part)

with open(path_to_file,'rb') as file:
    message.attach(MIMEApplication(file.read(), Name="file_creation.csv"))

with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
    server.login(sender_email, sender_password)
    server.sendmail(sender_email, recipient_email, message.as_string())