from rest_framework import serializers

from .models import Event, EventWindow, Bookings
from users.serializers import UserSerializer


class EventWindowSerializer(serializers.ModelSerializer):
    time_format = '%H:%M'
    event_id = serializers.IntegerField(required=False)

    class Meta:
        model = EventWindow
        fields = ('id', 'event_id', 'start_time', 'end_time', 'available_seats', 'total_seats')
        depth = 1

        extra_kwargs = {
            'available_seats': {'required': False},
            'event': {'required': False}
        }

    def validate(self, attrs):

        if attrs['end_time'] <= attrs['start_time']:
            raise serializers.ValidationError({
                "error": f"start time {attrs['start_time']} should be less than end time {attrs['end_time']}"
            })

        return attrs

    def create(self, validated_data):

        if not validated_data.get('event_id'):
            raise serializers.ValidationError({
                "error": 'event_id is required while creating window'
            })

        window = EventWindow.objects.create(
            event=Event.objects.get(pk=validated_data['event_id']),
            start_time=validated_data['start_time'],
            end_time=validated_data['end_time'],
            available_seats=validated_data['total_seats'],
            total_seats=validated_data['total_seats']
        )

        return window

    def bulk_create(self, event, windows):
        data = [
            EventWindow(
                event=event,
                available_seats=window['total_seats'],
                **window
            )
            for window in windows
        ]
        EventWindow.objects.bulk_create(data)


class EventSerializer(serializers.ModelSerializer):
    event_windows = EventWindowSerializer(many=True)
    user = UserSerializer(many=False, read_only=True)

    class Meta:
        model = Event
        fields = ('id', 'name', 'description', 'user', 'event_windows')
        depth = 1

    def create(self, validated_data):
        event = Event.objects.create(
            name=validated_data['name'],
            description=validated_data['description'],
            user=self.context['request'].user
        )

        EventWindowSerializer().bulk_create(event, validated_data['event_windows'])

        return event
    
    def update(self, instance, validated_data):
        validated_data.pop('event_windows')
        return super(EventSerializer, self).update(instance, validated_data)


class BookingsSerializer(serializers.ModelSerializer):
    window = EventWindowSerializer(read_only=True)
    user = UserSerializer(many=False, read_only=True)
    event = EventSerializer(read_only=True)

    event_id = serializers.IntegerField(write_only=True)
    window_id = serializers.IntegerField(write_only=True)
    booking_id = serializers.IntegerField(source='id', read_only=True)

    class Meta:
        model = Bookings
        fields = ('booking_id', 'event', 'user', 'window', 'no_tickets', 'is_cancelled', 'event_id', 'window_id')
        extra_kwargs = {
            'window_id': {'required': True},
            'event_id': {'required': True},
        }

    def get_extra_kwargs(self):
        extra_kwargs = super(BookingsSerializer, self).get_extra_kwargs()
        if self.context['request'].method in ['PUT', 'PATCH']:
            kwargs = extra_kwargs.get('is_cancelled', {})
            kwargs['read_only'] = True
            extra_kwargs['is_cancelled'] = kwargs

        return extra_kwargs

    def create(self, validated_data):

        window_obj = EventWindow.objects.get(pk=validated_data['window_id'])

        if 0 <= window_obj.available_seats < validated_data['no_tickets']:
            message1 = f"All tickets are filled for this window. Try another window"
            message2 = f"Only {window_obj.available_seats} tickets are available. But requested for {validated_data['no_tickets']} tickets"
            raise serializers.ValidationError({
                "error": message1 if window_obj.available_seats <= 0 else message2
            })

        obj = Bookings.objects.create(
            event=Event.objects.get(pk=validated_data['event_id']),
            user=self.context['request'].user,
            window=window_obj,
            no_tickets=validated_data['no_tickets'],
            is_cancelled=False
        )

        window_obj.available_seats -= validated_data['no_tickets']
        window_obj.save()

        return obj
