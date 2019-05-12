from django.contrib import admin
from .models import Post
from .models import Userprofile
from .models import BookData
from .models import BookRated

admin.site.register(Post)
admin.site.register(Userprofile)
admin.site.register(BookData)
admin.site.register(BookRated)
