import email, smtplib, ssl, json

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def getContacs(file):
    with open(file, mode='r', encoding='utf-8') as contacts_file:
        contacts = json.load(contacts_file)
        return contacts
def getMailFormat(file):
    with open(file, mode='r', encoding='utf-8') as mailFormat_file:
        formatMail = json.load(mailFormat_file)
        return formatMail
def loadPdf(reciver, message):
    # Open PDF file in binary mode
    filename = reciver["Attached"]
    with open(pdfDir+filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part2 = MIMEBase("application", "octet-stream")
        part2.set_payload(attachment.read())
    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part2)
    # Add header as key/value pair to attachment part
    part2.add_header(
        "Content-Disposition",
        f"attachment; filename= {filename}",
    )
    message.attach(part2)
    return message
def settingFormatMail(formatMail, reciver):
    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = formatMail["From"]
    message["To"] = reciver["Mail"]
    message["Subject"] = formatMail["Subject"]
    # Add body to email
    message.attach(MIMEText(formatMail["Message"], "plain"))
    message = loadPdf(reciver, message)
    return message

formatMail = getMailFormat("format.json")
contacs = getContacs("contats.json")
password = 'password generate from google'
pdfDir= "./Attached/"

context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(formatMail["From"], password)

    for contact in contacs:
        message = settingFormatMail(formatMail, contact)
        server.sendmail(formatMail["From"] , contact["Mail"], message.as_string())
