from django.db import models

#jango 2.0 에서는 따로 python 2 decorator 설정 안해도 되는듯.... 
#from django.utils.encoding import python_2_unicode_compatible

#글로벌 models과 동일한 이름이지만, user app 안에 있는 models 을 호출해야하 하기때문에 임시 이름을 변경함 (as user_models)
from codegram.users import models as user_models
# Create your models here.


#좋아요나 이미지 생성 등 타임에 대한 베이스는 아래 클래스 사용 
class TimeStampedModel(models.Model):
    #create_at 은 생성 될때 신규 시간 생성
    created_at = models.DateTimeField(auto_now_add=True)
    #updated_at 은 새로 고침
    updated_at = models.DateTimeField(auto_now=True)

# META : 데이터 베이스와 연결되지 않는 필드  
# timestampModel 클래스안에 Meta 클래스를 넣음으로써 해당 클래스를 일일이 DB에 포함하지 않고, Meta Field로만 사용함 (추상 속성의 클래스 상속)
    class Meta:
        #추상적 모델
        abstract = True


#이미지 관련 클래스 (이미지 필드, 주소, 내용)
class Image (TimeStampedModel):
    file = models.ImageField()
    location = models.CharField(max_length=140)
    caption = models.TextField()
    #on_delete 를 사용하는 이유는 foreignkey 사용 시, 연결된 foreginkey 가 삭제되거나 했을때의 행위를 정할수 있음) 
    #protect 는 삭제 되는 행위를 막는거고, 여러 옵션들이 있음
    creator = models.ForeignKey(user_models.User, null=True, on_delete=models.PROTECT, related_name='images')
    
    #@prperty 는 모델의 필드, 데이터로 가지 않지만, 모델 안에 존재  (펑션개념)
    @property  
    def like_count(self):
        return self.likes.all().count()








    #Magic Method : __?? 사용해서 원하는 데이터를 출력 할수 있음
    def __str__(self):
        return '{}-{}'.format(self.location, self.caption)

        #DB에서 얻는 리스트를 생성된 날짜로 정렬
        class Meta:
            ordering = ['-created_at']

#댓글 관련 클래스 (메시지)
#   @python_2_unicode_compatible
class Comment (TimeStampedModel):
    message = models.TextField()
    creator = models.ForeignKey(user_models.User, null=True, on_delete=models.PROTECT)

    #related_name을 지정함으로써 comments_set의 이름을 변경 할수 있음
    image = models.ForeignKey(Image ,null=True, on_delete=models.PROTECT,related_name='comments')

    #message 를 출력함으로써 작성한 message TextField 가 보여짐
    def __str__(self):
        return self.message


#좋아요 클래스 (foreign 키 지정)
#@python_2_unicode_compatible
class Like (TimeStampedModel):  
    creator = models.ForeignKey(user_models.User, null=True, on_delete=models.PROTECT)
    image = models.ForeignKey(Image, null=True, on_delete=models.PROTECT,related_name='likes')

    #like 의 경우 message field 가 없음으로 foregin key 를 가지고 message 를 불러옴  (user이름, Image 이름) 
    def __str__(self):
        return 'User:{} - Image Caption{}'.format(self.creator.username, self.image.caption)




    