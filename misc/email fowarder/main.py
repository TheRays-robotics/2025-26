import os
import smtplib
from time import sleep
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
f = ""
with open(str(os.path.relpath(__file__).replace("main.py","SIGNIN.TXT")), "r", encoding="utf-8") as file:
            password = file.readline().strip()
            to = file.readline().strip()
            direct = file.readline().strip()
i = False
tryagain = False
while True:
    sleep(0.1)
    pf = f
    f = next(os.walk(direct), (None, None, []))[2]
    f.sort(key=lambda x: os.path.getmtime(direct+"/"+x))
    f = f[-1]
    print([" ",""][i]+"FREAK!!!!")
    c = False
    if (pf != "" and f !=  pf):
        c = True
    i = not i
    if c or tryagain:
            print("sending")
            sleep(1)
            email = 'theraysbattlebot@gmail.com' # Your email
            
            subject = "Pitcuer"
            msg = MIMEMultipart()
            msg['From'] = email
            msg['To'] = to
            msg['Subject'] = subject
            
            # Attach the message to the MIMEMultipart object
            msg.attach(MIMEText("beep boop", 'plain'))    


            ImgFileName = direct+"/"+str(f)
            with open(ImgFileName, 'rb') as z:
                    img_data = z.read()
            image = MIMEImage(img_data, name=os.path.basename(ImgFileName),_subtype="png")

            msg.attach(image)


            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(email, password)
            text = msg.as_string() # You now need to convert the MIMEMultipart object to a string to send
            server.sendmail(email, to, text)
            server.close()

            tryagain = False
