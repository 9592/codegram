from rest_framework import serializers
from . import models
from codegram.users import models as user_models



#Following Feed class
class FeedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = user_models.User
        fields = (
            'username',
            'profile_image',
        )



#댓글
class CommentSerializer(serializers.ModelSerializer):
    creator = FeedUserSerializer(read_only=True)
    
    class Meta:
        model = models.Comment
        #fields = '__all__'
        fields = (
            'id',
            'message',
            'creator',
        )


#좋아요
class LikeSerializer(serializers.ModelSerializer):            
    #netsted Serializer  (다른 시리얼 라이즈의 데이터를 호출)
    #image = imageSerializer()
    class Meta:
        model = models.Like
        fields = '__all__'


class imageSerializer(serializers.ModelSerializer):
    #netsted Serializer
    #comment_set 을 Models> related_name 을 지정할 경우 아래 처럼 원하는 이름으로 변경 할수 있음
    #즉,set 은 그룹핑 할수 있음   A 가 B를 가릴킬때 B의 SET 은  B의 모든걸 가지고 있음.
    #imageSerializer 에서는 image 정보 뿐만 아니라 comment 와 like 가 그룹화되어 데이터를 가지고 올수 있음

    comments = CommentSerializer(many=True)
    #좋아요는 아래 카운팅 정보만 필요함으로 모델에서 selfcount 로 체크   
#    likes = LikeSerializer(many=True)    

    creator = FeedUserSerializer()

    class Meta:              
        model = models.Image
        #fields = '__all__'

        # serializer의 경우 comment_set 등이 사용할수 없음. 따라서 보고싶은 필드를 수동으로 넣어줘야함
        fields = (            
        'id',                
        'file',
        'location',
        'caption',
        'comments',
        'likes',
        'like_count',
        'creator',
        )
