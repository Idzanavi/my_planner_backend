from datetime import datetime

from celery import shared_task, Task
from my_planner.models import PlannerItem
from chat.event_logger import send_task_result
from my_planner.models import User, PlannerItem

from tasks.utils import fix_text
from tasks.mail_utils import make_email, send_email


class PrettifyTask(Task):
    def run(self, *args, **kwargs):
        pass

    def on_success(self, retval, task_id, args, kwargs):
        username, user_id, counter, total = retval
        name = self.name
        input = "{} [{}]".format(username, user_id)
        output = "{} of {}".format(counter, total)
        finished = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        send_task_result(name, input, output, finished)

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


@shared_task(name="Prettify", base=PrettifyTask)
def prettify(user_pk, username):
    items = list(PlannerItem.objects.filter(user__pk=user_pk).all())
    counter = 0
    total = len(items)
    for item in items:
        initial_text = item.text
        new_text = fix_text(initial_text)
        if new_text != initial_text:
            counter += 1
            item.text = new_text
            item.save()
    return username, user_pk, counter, total


class SendEmailTask(Task):
    def run(self, *args, **kwargs):
        pass

    def on_success(self, retval, task_id, args, kwargs):
        pass

    def on_failure(self, exc, task_id, args, kwargs, einfo):
        pass


@shared_task(name="SendMails", base=SendEmailTask)
def send_mails(date = datetime.now().date()):
    base_date_str = "1999-12-27"
    base_date = datetime.strptime(base_date_str, "%Y-%m-%d").date()
    days_delta = (date - base_date).days
    week_no = days_delta // 7
    day_no = days_delta % 7
    items = PlannerItem.objects.filter(week_no=week_no, day_no=day_no).order_by('slot_no').all()
    items_users_dict = {}
    for item in items:
        user_id = item.user.pk
        if user_id in items_users_dict:
            user, items_list = items_users_dict[user_id]
            items_list.append(item)
            items_users_dict[user_id] = user, items_list
        else:
            items_users_dict[user_id] = (item.user, [item])

        count = 0
        for id, (user, items) in items_users_dict.items():
            title, text, html = make_email(user, items, date)
            try:
                send_email(user.email, title, text, html)
                count += 1
            except Exception as ex:
                print(ex)

    return count