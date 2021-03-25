from django.db import models


class Territory(models.Model):
    name = models.CharField(max_length=48)
    code_2 = models.CharField(max_length=2)
    code_3 = models.CharField(max_length=3)
    local_currency = models.ForeignKey(
        "Currency", related_name="territories", on_delete=models.CASCADE
    )

    class Meta:
        db_table = "territory"
        verbose_name = "territory"
        verbose_name_plural = "territories"
        ordering = ("name",)


class Currency(models.Model):
    name = models.CharField(max_length=48)
    symbol = models.CharField(max_length=4)
    code = models.CharField(max_length=3)

    class Meta:
        db_table = "currency"
        verbose_name = "currency"
        verbose_name_plural = "currencies"


class Artist(models.Model):
    name = models.CharField(max_length=256)


class Statistics(models.Model):
    isrc = models.CharField(max_length=256)
    usages = models.CharField(max_length=256)
    revenue = models.CharField(max_length=256)


class DSR(models.Model):
    class Meta:
        db_table = "dsr"

    STATUS_ALL = (
        ("failed", "FAILED"),
        ("ingested", "INGESTED"),
    )

    path = models.CharField(max_length=256)
    period_start = models.DateField(null=False)
    period_end = models.DateField(null=False)

    status = models.CharField(
        choices=STATUS_ALL, default=STATUS_ALL[0][0], max_length=48
    )

    territory = models.ForeignKey(
        Territory, related_name="dsrs", on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        Currency, related_name="dsrs", on_delete=models.CASCADE
    )

class Recording(models.Model):
    dsp_id = models.CharField(max_length=30)
    title = models.CharField(max_length=256)
    artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
    statistics = models.ForeignKey(Statistics, on_delete=models.CASCADE)
    dsr = models.ForeignKey(
        DSR, related_name="dsr", on_delete=models.CASCADE
    )

