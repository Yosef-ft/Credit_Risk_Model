from django.db import models


class Feature(models.Model):
    Product_Choices = [
        ('financial_services', 'Financial Services'),
        ('airtime', 'Airtime'),
        ('utility_bill', 'Utility Bill'),
        ('data_bundles', 'Data Bundles'),
        ('tv', 'TV'),
        ('ticket', 'Ticket'),
        ('movies', 'Movies'),
        ('transport', 'Transport'),
        ('other', 'Other')
    ]

    ProviderId = models.IntegerField()
    ProductId = models.IntegerField()
    ProductCategory = models.CharField(max_length=100, choices=Product_Choices)
    ChannelId = models.IntegerField()
    Amount = models.FloatField()
    Transaction_Hour = models.IntegerField()
    Transaction_Day = models.IntegerField()
    Average_transaction_amount = models.FloatField()
    STD_Transaction_Amount = models.FloatField()
    Transaction_Month = models.IntegerField()



    def __str__(self):
        return f"The Product category {self.ProductCategory}. The total amount {self.Amount}"
