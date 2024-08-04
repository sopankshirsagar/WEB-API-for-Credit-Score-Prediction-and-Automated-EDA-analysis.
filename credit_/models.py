from django.db import models
import pandas as pd


class Credit_score(models.Model):
    
    file = models.FileField( max_length=150)
    record_id = models.AutoField(primary_key=True)
    
    def save(self, *args, **kwargs):
        self.file.name = self.file.name.split('/')[-1]
        super().save(*args, **kwargs)
        print(self.file.name)
        
        
class Auto_eda(models.Model):
    file = models.FileField(upload_to="auto_eda/")












# # model = pickle.load(open( 'credit_score.pkl', 'rb'))
# # Age                             38.000000
# # Gender                           0.000000
# # Income                       56000.000000
# # Credit History Length          414.000000
# # Number of Existing Loans         0.000000
# # Loan Amount                 138215.000000
# # Loan Tenure                     42.000000
# # LTV Ratio                       62.607963
# # Employment Profile               1.000000
# # Profile Score                   60.000000
# # credit history                   1.000000


