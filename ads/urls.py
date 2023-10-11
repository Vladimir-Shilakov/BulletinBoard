from django.urls import path, include
from .views import AdsList, AdsDetail, AdsCreate, AdsUpdate, CategoryList, Replies, ReplyCreate, subscribe, \
    unsubscribe, ReplyDelete, reply_confirmed


urlpatterns = [
    path('', AdsList.as_view(), name='ads_list'),
    path('ads/create', AdsCreate.as_view(), name='ads_create'),
    path('ads/<int:pk>', AdsDetail.as_view(), name='ads_detail'),
    path('ads/<int:pk>/edit', AdsUpdate.as_view(), name='ads_edit'),
    path('categories/<int:pk>', CategoryList.as_view(), name='category_list'),
    path('replies/', Replies.as_view(), name='my_replies'),
    path('ads/<int:pk>/reply/create', ReplyCreate.as_view(), name='reply_create'),
    path('categories/<int:pk>/subscribe', subscribe, name='subscribe'),
    path('categories/<int:pk>/unsubscribe', unsubscribe, name='unsubscribe'),
    path('reply/<int:pk>/delete/', ReplyDelete.as_view(), name='reply_delete'),
    path('reply/<int:pk>/confirmed/', reply_confirmed, name='reply_confirmed'),
]