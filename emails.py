from flask_mail import Mail, Message


# from app import mail

def send_email(subject, sender, recipients, text_body, ):
    msg = Message(subject, sender=sender, recipients=recipients)
    msg.body = text_body
    # msg.html = html_body
    return msg
