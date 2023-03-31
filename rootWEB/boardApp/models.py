from django.db import models

from django.utils import timezone
# Create your models here.
# Create table user_tbl()

class user_tbl(models.Model) :
    user_id    = models.CharField(primary_key=True , max_length=50)
    user_pwd   = models.CharField(max_length=50)
    user_name  = models.CharField(max_length=50)
    user_point = models.IntegerField(default=0)
    user_img   = models.CharField(max_length=50)

    def __str__(self):
        return self.user_id+'\t'+self.user_name



class board_tbl(models.Model) :
    # id (primary)
    title       = models.CharField(max_length=500)
    writer      = models.ForeignKey(user_tbl,
                                    on_delete=models.CASCADE ,
                                    db_column='writer',
                                    null=False)
    content   = models.TextField()
    regdate   = models.DateTimeField(default=timezone.now)
    viewcnt   = models.IntegerField(default=0)