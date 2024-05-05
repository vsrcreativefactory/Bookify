from django.conf import settings
from twilio.rest import Client

class MessageHandler:
    mobile=None
    otp=None

    def __init__(self,mobile,otp) -> None:
        self.mobile=mobile
        self.otp=otp
    def send_otp_via_message(self):
        try:
            client= Client(settings.ACCOUNT_SID,settings.AUTH_TOKEN)
            message=client.messages.create(
                body=f'your otp is:{self.otp}',
                from_=f'{settings.TWILIO_PHONE_NUMBER}',
                to=f'{settings.COUNTRY_CODE}{self.mobile}'
                )
            print(f'Message sent successfully: {message.sid}')
        except Exception as e:
            print(f'Error sending message: {e}')
        