from django.db import models
from django.utils.translation import gettext_lazy as _
import uuid

# Create your models here.
class State(models.TextChoices):
    ACCEPTED = 'ACC', _('Accepted')
    CANCELLED = 'CAN', _('Cancelled')
    AWAITING_THEIR_ACCEPTANCE = 'ATA', _('AwaitingTheirAcceptance')
    AWAITING_YOUR_ACCEPTANCE = 'AYA', _('AwaitingYourAcceptance')
    WITHDRAWN_BY_ME = 'WBM', _('WithdrawnByMe')
    WITHDRAWN_BY_THEM = 'WBT', _('WithdrawnByThem')

class Offer(models.Model):

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user1_id = models.CharField(max_length=50)
    user2_id = models.CharField(max_length=50)
    user1_state = models.CharField(max_length=3, choices=State.choices, default=State.AWAITING_THEIR_ACCEPTANCE)
    user2_state = models.CharField(max_length=3, choices=State.choices, default=State.AWAITING_THEIR_ACCEPTANCE)
    product_name = models.CharField(max_length=50)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    version = models.IntegerField()
    # private_data = models.TextField()

class History(models.Model):
    offer_id = models.CharField(max_length=50)
    version = models.IntegerField()
    action = models.CharField(max_length=50)
    user_id = models.CharField(max_length=50)
    user1_state = models.CharField(max_length=3, choices=State.choices, default=State.AWAITING_THEIR_ACCEPTANCE)
    user2_state = models.CharField(max_length=3, choices=State.choices, default=State.AWAITING_THEIR_ACCEPTANCE)
    product_name = models.CharField(max_length=50)
    buyer = models.CharField(max_length=50)
    seller = models.CharField(max_length=50)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    # private_data = models.TextField()
