from django.contrib import admin
from . import models
from django.utils.encoding import python_2_unicode_compatible
# Register your models here.



# @ <- decorator

@admin.register(models.Image)
class ImageAdmin(admin.ModelAdmin):
#emty class   = pass

    #글자에 하이퍼 링크 연결 (클릭시 이동)
    list_display_links= (    
        'location',
        'caption',
    )

    # 검색 장에 해당 field 내용으로 검색
    search_fields = (
        'location',
        'caption',
    )

    #사용자가 필터 할수 있는 인터페이스
    list_filter = (
        'location',
        'creator',
    )

    
    list_display= (    
    'creator',    
    'created_at',
    'updated_at',
    'file',
    'location',
    'caption',
    )
    

@admin.register(models.Like)
class LikeAdmin(admin.ModelAdmin):
    list_display= (    
    'creator',
    'image',
    'created_at',
    'updated_at',
    )


@admin.register(models.Comment)
class CommentAdmin(admin.ModelAdmin):    
#메시지 내용 이미지 생성일 등등 화면 표시 (string representation)
    list_display= (
    'message',
    'creator',
    'image',
    'created_at',
    'updated_at',
    )

