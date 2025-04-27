from django.db.models.signals import post_delete
from django.dispatch import receiver

from .models import Loan

@receiver(post_delete, sender=Loan)
def loanReduction(sender, instance, using, **kwargs):
    borrower = instance.borrower
    book = instance.book
    
    borrower.loaned -= 1
    borrower.save()

    book.available = True
    book.save()

    