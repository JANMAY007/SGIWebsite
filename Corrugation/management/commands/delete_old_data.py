from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db.models import Q
from Corrugation.models import PaperReels, Program, Production


class Command(BaseCommand):
    help = 'Deletes Paper Reels older than 15 days, Programs older than 10 days and Productions older than 10 days.'

    def handle(self, *args, **kwargs):
        reels_cutoff_date = timezone.now() - timezone.timedelta(days=15)
        old_reels = PaperReels.objects.filter(Q(created_at__lt=reels_cutoff_date) & Q(used=True))
        count_reels, _ = old_reels.delete()
        programs_cutoff_date = timezone.now() - timezone.timedelta(days=10)
        old_programs = Program.objects.filter(Q(program_date__lt=programs_cutoff_date) & Q(active=False))
        count_programs, _ = old_programs.delete()
        productions_cutoff_date = timezone.now() - timezone.timedelta(days=10)
        old_productions = Production.objects.filter(Q(production_date__lt=productions_cutoff_date) & Q(active=False))
        count_productions, _ = old_productions.delete()
        self.stdout.write(f'Successfully deleted {count_reels} old and used paper reels')
        self.stdout.write(f'Successfully deleted {count_programs} old and archive programs')
        self.stdout.write(f'Successfully deleted {count_productions} old and archive productions')
