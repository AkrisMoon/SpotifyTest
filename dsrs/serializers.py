from rest_framework import serializers

from . import models


class TerritorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Territory
        fields = (
            "name",
            "code_2",
        )


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Currency
        fields = (
            "name",
            "code",
        )

class ArtistSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Artist
        fields = (
            "name",
        )
class StatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Statistics
        fields = (
            "isrc",
            "usages",
            "revenue",
        )



class DSRSerializer(serializers.ModelSerializer):
    territory = TerritorySerializer()
    currency = CurrencySerializer()

    class Meta:
        model = models.DSR
        fields = (
            "id",
            "path",
            "period_start",
            "period_end",
            "status",
            "territory",
            "currency",
        )

class RecordingSerializer(serializers.ModelSerializer):
    statistics = StatisticsSerializer()
    dsr = DSRSerializer
    class Meta:
        model = models.Recording
        fields = (
            "dsp_id",
            "title",
            "artist",
            "statistics",
            "dsr",
        )

class RecordingListSerializer(serializers.ListSerializer):
    child = RecordingSerializer()