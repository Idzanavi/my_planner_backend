from django.core.mail import send_mail

EMAIL = "myplannerobot@gmail.com"

def make_time(slot_no):
    return ("00" + str(slot_no+8))[-2:]+":00"


def make_email(user, items, date):
    title = "[MyPlanner] notification for {}".format(date)
    items = ["{}-{}: {}.\n".format(make_time(item.slot_no), make_time(item.slot_no+1), item.title) for item in items]
    html = """<!DOCTYPE html>\n<head>\n<meta charset="utf-8"/>\n<title>{title}</title>\n</head>\n<body><br><b>Dear {first_name} {last_name}</b><br/><br/>\nFor {date} you have the following plan items:<br/>\n{items}\n<br/><br/>Sincerely yours,<br/>My Planner<br/>\n</body>\n</html>""".format(
        title=title, first_name=user.first_name, last_name=user.last_name, date=date, items="<br/>".join(items))
    text = """Dear {first_name} {last_name}\r\n\r\nFor {date} you have the following plan items:\r\n{items}\r\n\r\nSincerely yours,\r\nMy Planner\r\n""".format(
        first_name=user.first_name, last_name=user.last_name, date=date, items="\r\n".join(items))
    return title, html, text


def send_email(email, title, text, html):
    emails = [email]
    send_mail(subject=title, message=text, html_message=html, fail_silently=False, from_email=EMAIL, recipient_list=emails)
