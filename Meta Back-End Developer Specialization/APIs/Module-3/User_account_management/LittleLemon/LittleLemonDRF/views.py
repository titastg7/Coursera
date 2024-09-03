from rest_framework import generics, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Rating, MenuItem
from .serializers import RatingSerializer, MenuItemSerializer
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle

class MenuItemsViewSet(viewsets.ModelViewSet):
    # throttle_classes = [AnonRateThrottle, UserRateThrottle]
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemSerializer

    def get_throttles(self):
        if self.action == "create":
            throttle_classes = [UserRateThrottle]
        else:
            throttle_classes = []
        return [throttle() for throttle in throttle_classes]


class RatingsView(generics.ListCreateAPIView):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer

    def get_permission(self) :
        if(self.request.method=='GET') :
            return []
        return [IsAuthenticated]


        
