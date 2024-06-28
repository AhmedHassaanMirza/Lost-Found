from .models import ImageData

obj=ImageData.objects.only('id')
print(len(obj))