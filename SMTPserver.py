import email, smtplib, ssl, json, re, email, email.mime.base, email.mime.multipart,email.mime.text

# function to open file json and return data
def loadFileJSON (file): 
    with open(file, mode='r', encoding='utf-8') as json_file:
        data = json.load(json_file)
        return data

# function to resolve every tag in the message and return a list of tags eventually unresolved and the message with resolved tags (if only they can be resolved)
def resolvePersonalTag(message, recipient):
    copyMessage = message;
    matches = re.findall("\/\*<(\w+)>\*\/", copyMessage, re.MULTILINE) # find all tags in message
    matches = list(dict.fromkeys(matches)) # removing duplicates
    for tag in matches:
        if tag in recipient:
            copyMessage = re.sub('\/\*<'+ tag +'>\*\/', recipient[tag], copyMessage) # resolve tags
    tagsUnresolved = re.findall("\/\*<(\w+)>\*\/", copyMessage, re.MULTILINE) #research eventually tags unresolved
    return tagsUnresolved, copyMessage

# function to load File in the message, if File is not in ·/Attached directory it returns -1 else it returns message with attachment
def loadFile(recipient, message):
    # Open File file in binary mode
    try:
        with open("./Attached/"+recipient["Attached"], "rb") as attachment:
            # Add file as application/octet-stream
            part2 = email.mime.base.MIMEBase("application", "octet-stream")
            part2.set_payload(attachment.read())
        # Encode file in ASCII characters to send by email    
        email.encoders.encode_base64(part2)
        # Add header for the attachment
        part2.add_header("Content-Disposition", f"attachment; filename= "+recipient["Attached"])
        message.attach(part2)
    except FileNotFoundError:
        message = None
    return message

# function to formatting email and prepare that to send it        
def settingFormatMail(formatMail, recipient):
    # mail needs headers which are usefull to store information like sender, recipient and body (attachments and so on)
    # **Setting headers, body and attachment for the email**
    message = None
    tagsUnresolved, messageBody = resolvePersonalTag(formatMail["Message"], recipient)
    if tagsUnresolved == []:
        message = email.mime.multipart.MIMEMultipart()
        message["From"] = formatMail["From"]
        message["To"] = recipient["Mail"]
        message["Subject"] = formatMail["Subject"]
        message.attach(email.mime.text.MIMEText(messageBody, "plain")) # adding text into the body
        if "Attached" in recipient:
            message = loadFile(recipient, message) # adding file into the body
    return message

formatMail = loadFileJSON("format.json")
contacs = loadFileJSON("contats.json")
# go here to create a password: https://myaccount.google.com/security?rapt=AEjHL4MbGEoWlakBM55Kv8XTcOfZgPpiF0sn6LbXOMjRPYj9pFnk5933vhH9gJGVxa0BcDmwzu1WkRwGq5kwX7oUVX-KqCwEbg
# external app password is required to access to the sender account
password = 'password da genereare https://myaccount.google.com/security?rapt=AEjHL4MbGEoWlakBM55Kv8XTcOfZgPpiF0sn6LbXOMjRPYj9pFnk5933vhH9gJGVxa0BcDmwzu1WkRwGq5kwX7oUVX-KqCwEbg' 
context = ssl.create_default_context() # creation of ssl certificate whithout this we can't connect to google
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as SMTPserver:
    SMTPserver.login(formatMail["From"], password) # connection to google
    for contact in contacs:
        message = settingFormatMail(formatMail, contact) # getting the format of mail and all contacts and prepare the mail to send
        if message is None:
            print("**Error** To " + contact["Mail"] + " is not sent")
        else :
            SMTPserver.sendmail(formatMail["From"] , contact["Mail"], message.as_string()) # send email 
            print("To " + contact["Mail"] + " is sent successfuly") 