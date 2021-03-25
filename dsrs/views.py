from sqlite3 import IntegrityError

from rest_framework import viewsets
from os import listdir
from os.path import isfile, join
from . import models, serializers
import gzip
import gzinfo
import csv
import re
import ccy
from forex_python.converter import CurrencyCodes
import pandas as pd
from django.http import Http404
from rest_framework import viewsets, generics



def FillBD():
    filesgz = [f for f in listdir("./data/") if isfile(join("./data/", f))]
    for file in filesgz:
        is_first = 0
        with gzip.open(join("./data/", file), 'rt') as f:
            regex = re.search(r"(.*_.*)_([A-Z]{2})_([A-Z]{3})_(\d{8})-(\d{8})", file)
            period_start = pd.to_datetime(regex.group(4), format='%Y%m%d', errors='ignore')
            period_end = pd.to_datetime(regex.group(5), format='%Y%m%d', errors='ignore')
            territory_code_2 = regex.group(2)
            territory_name = ccy.country(territory_code_2)
            currency_code = regex.group(3)
            currency_name = ccy.currency(currency_code).name
            currency_symbol = CurrencyCodes().get_symbol(currency_code)
            try:
                cur, currency = models.Currency.objects.get_or_create(name=currency_name, symbol=currency_symbol, code=currency_code)
                ter, territory = models.Territory.objects.get_or_create(name=territory_name, code_2=territory_code_2,code_3=currency_code, local_currency = cur)
                d, dsr = models.DSR.objects.get_or_create(path= file, period_start=period_start, period_end=period_end,status="ingested", territory = ter, currency = cur)
                for row in csv.reader(f, delimiter='\t'):
                    if is_first==0:
                        is_first = 1
                    else:
                        art, artist = models.Artist.objects.get_or_create(name = row[2])
                        stat, ststistics = models.Statistics.objects.get_or_create(isrc = row[3], usages = row[4], revenue = row[5])
                        models.Recording.objects.get_or_create(dsp_id = row[0], title = row[1], artist = art, statistics = stat, dsr = d)
            except IntegrityError as e:
                print(e)



class DSRViewSet(viewsets.ModelViewSet):
    FillBD()
    queryset = models.DSR.objects.all()
    serializer_class = serializers.DSRSerializer



class DSR_IDViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.DSRSerializer

    def get_queryset(self):
        try:
            queryset = models.DSR.objects.get(id = int(self.request.id))
        except:
            raise Http404
        return queryset

class RecordingPercentileViewSet(generics.ListAPIView):
    serializer_class = serializers.RecordingListSerializer

    def get_queryset(self):
        queryset = []
        try:
            queryset_statistics = models.Statistics.objects.filter(revenue__lte = int(self.kwargs['number']))
            for item in queryset_statistics:
                queryset.append(models.Recording.objects.filter(statistics = item))
        except Exception as e:
            print(e)
        return queryset