from django.core.management.base import BaseCommand
from django.utils import timezone
from Corrugation.models import PaperReels


class Command(BaseCommand):
    help = 'Deletes Paper Reels older than 30 days'

    def handle(self, *args, **kwargs):
        cutoff_date = timezone.now() - timezone.timedelta(days=30)
        old_reels = PaperReels.objects.filter(created_at__lt=cutoff_date, used=True)
        count, _ = old_reels.delete()
        self.stdout.write(f'Successfully deleted {count} old and used paper reels')
