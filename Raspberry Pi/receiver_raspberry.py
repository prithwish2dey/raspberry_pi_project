import poplib
from email.parser import Parser
import os

def receive_image(r_username, r_password, save_dir, subject_filter=None):
    # Connect to the server
    pop_conn = poplib.POP3_SSL('pop.gmail.com')
    pop_conn.user(r_username)
    pop_conn.pass_(r_password)

    # Get message numbers
    message_count = len(pop_conn.list()[1])

    if message_count > 0:
        for i in range(message_count):
            # Retrieve each message
            response, lines, octets = pop_conn.retr(i + 1)

            # Join the lines and parse the message
            message_bytes = b'\r\n'.join(lines)
            message = Parser().parsestr(message_bytes.decode('utf-8'))

            # Print message details for debugging
            print("Processing message")
            print("Subject: " + str(message['subject']))
            print("From: " + str(message['from']))


            if message.is_multipart():
                # Iterate over message parts to find the text content
                for part in message.get_payload():
                    # Check if the part is text and not an attachment
                    if part.get_content_type() == 'text/plain' and not part.get_content_disposition():
                        # Decode and print the text content
                        text_content = part.get_payload(decode=True).decode(part.get_content_charset())
                        print("Text content of the email:")
                        print(text_content)
                        break
            else:
                if message.get_content_type() == 'text/plain':
                    text_content = message.get_payload(decode=True).decode(message.get_content_charset())
                    print("Text content of the email:")
                    print(text_content)

    else:
        print("No messages found.")

    # Quit the connection
    pop_conn.quit()


#Receiver Details
r_username = "rpi2pc@gmail.com"  
r_password = "eiyu ulww ysxx mkzv"     
save_dir = "./"

while True:
    receive_image(r_username, r_password, save_dir)