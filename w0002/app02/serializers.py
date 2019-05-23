from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.reverse import reverse
from .models import Restaurant
User = get_user_model()

class RestaurantSerializer(serializers.ModelSerializer):

    user = serializers.SlugRelatedField(
        slug_field = User.USERNAME_FIELD, required=False, allow_null=True, queryset = User.objects.all()
    )
    links = serializers.SerializerMethodField()

    class Meta:
        model = Restaurant
        fields = ('id', 'name','street', 'number', 'city', 'zipCode', 'stateOrProvince', 'country', 'telephone', 'url', 'user', 'date', 'links',)

    def get_links(self, obj):
        request = self.context['request']
        return {
            'self': reverse('restaurant-detail', kwargs={'pk': obj.pk}, request=request),
        }

