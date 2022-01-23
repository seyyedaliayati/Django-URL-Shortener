import random
from django.utils.timezone import datetime, timedelta
from django.core.management.base import BaseCommand

from app_urls.models import Click, Link, User

class Command(BaseCommand):
    help = "Fills database with fake data."

    def handle(self, *args, **kwargs):
        user = User.objects.create_superuser(
            email="admin@admin.com",
            password="admin"
        )
        today = datetime.today()
        for i in range(10):
            link, _ = Link.objects.get_or_create(
                user=user,
                url="https://github.com/seyyedaliayati",
                alias=f"link{i}"
            )
            self.stdout.write(str(link))
            for j in range(random.randint(0, 100)):
                click, _ = Click.objects.get_or_create(
                    link=link,
                    ip_address=f"{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}.{random.randint(0, 255)}"
                )
                click.clicked_date = today - timedelta(days=random.randint(0, 30))
                click.clicks_count += random.randint(1, 10)
                click.save()
                self.stdout.write("----  " + str(click))
        self.stdout.write("Admin Email: admin@admin.com, Password: admin")
