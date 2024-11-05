import os
import poplib
import smtplib
from email.parser import BytesParser
from email.policy import default
from email.message import EmailMessage
from classify_animal_image import *


def sender(subject, to_sender, from_receiver, r_password, generated_description):
    # Create the message
    msg = EmailMessage()
    msg['Subject'] = subject
    msg['From'] = from_receiver
    msg['To'] = to_sender
    msg.set_content(generated_description)

    # Send the description
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(from_receiver, r_password)
        smtp.send_message(msg)

    print("Image Description sent successfully.")





def receiver(r_username, r_password, save_dir):
    # Connect to the server
    pop_conn = poplib.POP3_SSL('pop.gmail.com')
    pop_conn.user(r_username)
    pop_conn.pass_(r_password)

    # Print Total number of messages
    message_count = len(pop_conn.list()[1])
    print(f"Total messages: {message_count}")

    if message_count > 0:
        for i in range(message_count):
            # Retrieve each message one by one
            response, lines, octets = pop_conn.retr(i + 1)

            # Join the lines and parse the message
            message_bytes = b'\r\n'.join(lines)
            message = BytesParser(policy=default).parsebytes(message_bytes)

            # Print message details for debugging
            print(f"Processing message") #{i + 1}
            print(f"Subject: {message['subject']}")
            print(f"From: {message['from']}")

            # Iterate over message parts
            found_image = False
            for part in message.iter_parts():
                if part.get_content_maintype() == 'multipart':
                    continue

                if part.get_content_disposition() == 'attachment' and part.get_content_maintype() == 'image':
                    found_image = True
                    # Get the image content
                    img_data = part.get_payload(decode=True)
                    filename = part.get_filename()
                    file_path = os.path.join(save_dir, filename)

                    # Ensure the directory exists
                    os.makedirs(save_dir, exist_ok=True)

                    # Save the image into the save_dir
                    with open(file_path, 'wb') as f:
                        f.write(img_data)
                    print(f'Image saved as {file_path}')
                    
            if found_image:
                print("Image found and saved.")
                
                # Process the received image and generate the description
                generated_description=classify_and_generate_image_description(file_path)
                print(generated_description)
                
                # Sending the generated description to the sender
                sender('Image Description','rpi2pc@gmail.com','sender2receiver24@gmail.com','lexu gfpk jcih xzww',str(generated_description))
                break  

        if not found_image:
            print("No attachment image is found.")

    # Quit the connection
    pop_conn.quit()



# Receiver Details
r_username = "sender2receiver24@gmail.com" 
r_password = "lexu gfpk jcih xzww"
save_dir = "./"

while True:
    receiver(r_username, r_password, save_dir)
