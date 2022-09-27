from django.urls import path
from .views import WordList, WordAdd, WordEdit, WordDelete

app_name = 'word'

urlpatterns = [
    path('', WordList.as_view(), name='home'),
    path('new/', WordAdd.as_view(), name='add'),
    path('edit/<int:pk>', WordEdit.as_view(), name='edit'),
    path('delete/<int:pk>', WordDelete.as_view(), name='delete'),
]