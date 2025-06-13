from django.db import models

class LedgerEntry(models.Model):
    client_name = models.CharField(max_length=200)
    client_address = models.TextField()
    credit = models.FloatField(default=0)
    debit = models.FloatField(default=0)
    remark = models.TextField(blank=True)
    date = models.DateField(auto_now_add=True)

    def remaining(self):
        return self.credit - self.debit

    def __str__(self):
        return self.client_name
