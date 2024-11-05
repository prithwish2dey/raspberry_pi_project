import os
import smtplib
from email.message import EmailMessage
from datetime import datetime
from picamera import PiCamera
from time import sleep

def capture_image_using_picamera(image_path):

    camera = PiCamera()
    camera.start_preview()
    sleep(2) 
    camera.capture(image_path)
    camera.stop_preview()
    camera.close()
    print("Image captured successfully.")

def send_image(subject, body, to_receiver, from_sender, password, image_path=None):
    # Create the email message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_sender
    msg['To'] = to_receiver
    msg.set_content(body)

    # Attach the image
    if image_path:
        with open(image_path, 'rb') as img_file:
            img_data = img_file.read()
            img_name = os.path.basename(image_path)
            msg.add_attachment(img_data, maintype='image', subtype='jpeg', filename=img_name)

    # Send the image
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(from_sender, password)
        smtp.send_message(msg)
    print("Image sent successfully.")

# Sender Details
s_username = "rpi2pc@gmail.com"
r_username = "sender2receiver24@gmail.com"
s_password = "eiyu ulww ysxx mkzv"

while True:
    input("Press Enter to capture and send a new image...")
    
    # Capture the image using Pi Camera
    image_path = "./picamera_image.jpg"
    capture_image_using_picamera(image_path)

    # Send the image
    send_image(
        subject=f"Message Content - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
        body="Please find the attached image.",
        to_receiver=r_username,
        from_sender=s_username,
        password=s_password,
        image_path=image_path
    )
