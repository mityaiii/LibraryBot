import smtplib
import typing
from Config import mail_for_extending, bot_mail, mail_password


def __send_mail(recipient_mails: typing.List[str], text_message: str):
    sender: str = bot_mail
    password: str = mail_password

    server = smtplib.SMTP("smtp.mail.ru", 587)
    server.starttls()

    try:
        message = text_message
        server.login(sender, password)

        for recipient in recipient_mails:
            server.sendmail(sender, recipient, message.encode("utf-8"))

        return True
    except Exception as _ex:
        print(f"{_ex}\n Check your login or password")

        return False


def send_message_for_extend(library_card_number) -> bool:
    return __send_mail(mail_for_extending,
                       f"Subject: От бота о продлении книги\n{library_card_number} хочет продлить свои книги")


# def send_message_for_excursion(form, time) -> bool:
#     return __send_mail(f"{mail_for_excursion}",
#                        f"Subject: От бота о записи на экскрсию\n {form} хочет записаться на {time}")
