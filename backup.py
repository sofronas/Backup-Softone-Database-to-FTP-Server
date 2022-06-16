import datetime
import os
from tkinter import messagebox
import pyodbc
import ftplib
import email
import smtplib
import ssl
import datetime
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

global name_of_server
global name_of_database
global name_of_path
name_of_server ='SERVER'
name_of_database='database name'
name_of_path=r'folder where to store the backup file'


def file_upload():
    session = ftplib.FTP('ftp..gr','ftp user','password of ftp)')
    session.cwd('mpove forward to specific folder')
    file = open('sql_backup.bak','rb')                  
    session.storbinary('STOR sql_backup.bak', file)     
    file.close()                                
    session.quit()

def send_email():
    now = datetime.datetime.now()
    d = now.strftime("%d_%m_%Y")
    subject = "Backup softone" + "-" + d + " - name of client"
    body = "Backup "
    sender_email = "sender email"
    receiver_email = "reveiver email"
    password = "password email"

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails

    # Add body to email
    message.attach(MIMEText(body, "plain"))
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("mail.gr", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)

def backupSQL():
    global name_of_server
    global name_of_database
    global name_of_path
    file_name = "sql_backup.bak"
    connection = pyodbc.connect(driver='{SQL Server Native Client 10.0}',server=name_of_server,database=name_of_database,uid="",pwd="",trusted_connection='no',autocommit=True)
    backup = name_of_path + "\\" + file_name
    sql = "BACKUP DATABASE [datbase name] TO  DISK = N'C:\backupsoftone\sql_backup.bak'"
    cursor = connection.cursor().execute(sql)
    while cursor.nextset():
        pass
    connection.close()    
    
def main():
    backupSQL()
    file_upload()
    send_email()

if __name__ == "__main__":
    main()
