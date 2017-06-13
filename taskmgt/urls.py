# @Author: Tushar Agarwal(tusharcoder) <tushar>
# @Date:   2017-06-13T10:05:11+05:30
# @Email:  tamyworld@gmail.com
# @Filename: urls.py
# @Last modified by:   tushar
# @Last modified time: 2017-06-13T11:15:43+05:30



from django.conf.urls import include, url

from django.contrib import admin
from core import urls as coreurls
admin.autodiscover()

urlpatterns = [
    # Examples:
    # url(r'^$', 'taskmgt.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'', include(coreurls)),
]
