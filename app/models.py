from django.db import models
from django.contrib.auth.models import User 
from easy_thumbnails.fields import ThumbnailerImageField

class Rubric(models.Model):
    name = models.CharField(max_length=255, verbose_name='Раздел')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subrubric')

    def __str__(self):
        return self.name

"""
    Ниже модель на объявления, которая через Foreign key отражает рубрики.
"""

class Post(models.Model):
    rubric = models.ForeignKey(Rubric, on_delete=models.PROTECT, verbose_name='Раздел')
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Описание')
    price = models.IntegerField(verbose_name='Цена')   
    contact = models.TextField(verbose_name='Контакты')
    image = ThumbnailerImageField(verbose_name='Картинка', upload_to='posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    
    def __str__(self):
        return f'{self.title} опубликовано {self.created_at} | {self.author}' 

"""
    Ниже модель на комментарии
"""

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='Объявления', related_name='comment')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор')
    content = models.TextField(verbose_name='Комментарий')