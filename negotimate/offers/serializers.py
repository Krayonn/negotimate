from rest_framework import serializers
from .models import History


class HistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = History
        fields = ('offer_id', 'version', 'action', 'user_id', 'user1_state', 'user2_state', 'product_name', 'buyer', 'seller', 'price', 'private_data')