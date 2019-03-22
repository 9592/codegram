#장고 템플릿 사용 안함
#from django.shortcuts import render

#APIView: 엘리멘트를 가져오고 보여주고 method 관리
#reponse : http response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers

# Create your views here.

"""
requeset 에 대하여
    httpRequest 의 속성으로는 다음과 같이 사용할수 있음
        
        request.scheme, body, path, path_info, method 등
        print (request.'attb') 로 확인가능

        request.user 는 현재 사용자의 대한 정보를 확인 할수 있음 
        print (request.user.website)

    Post 는 업로드 및 데이터 수정


테스트 했던 코드는 다 주석 처리!

class ListAllImages(APIView):
    #get http method  (self : 이미 정의된 variable, reqeust : Object 요청, format : json,xml 등 None(기본)= json
    def get(self, request, format=None):

        #httpRequest 속성
        #print (request.scheme)
        #print (request.path)


        #objects 는 많은 Objects 을 가지고 있음  (all, set, get 등등) 
        #전체 이미지 오브젝트를 넣음  (단 이건 파이썬 Object)
        all_images = models.Image.objects.all()

        #위 파이썬 오브젝트를 serializer 해서 json 으로 변경
        #시리얼 라이저는 단수(1개 값만 받음) 라서 여러개의 경우 따로 옵션을 정해줘야함 (many=True)
        serializer = serializers.imageSerializer (all_images, many=True)
        
        #response(data 는 불러올 데이터 )
        return Response(data=serializer.data)



# 시리얼 라이즈에 맞는 URL 을 맞춰서 입력 해야함
class ListAllComments(APIView):
    def get(self,request,format=None):
        #전부 다 확인하고 싶을때 all()
        #all_comment = models.Comment.objects.all()

        #조건을 통해 확인 하고 싶을때 filter ()
        #id
        #all_comment = models.Comment.objects.filter(id=2)
        #creator
        #all_comment = models.Comment.objects.filter(creator=1)
        #아래 출력으로 User ID 확인 가능 (현재 사용중인)
        #print (request.user.id)  

        #유저 변수로 작업
        user_id = request.user.id 
        all_comment = models.Comment.objects.filter(creator=user_id)

        serializer = serializers.CommentSerializer(all_comment, many=True)
        return Response(data=serializer.data)



class ListAllLikes(APIView):
    def get(self, request, format=None):
        all_likes = models.Like.objects.all()
        serializer = serializers.LikeSerializer(all_likes, many=True)
        return Response(data=serializer.data)

"""


class Feed(APIView):

    def get(self,request,format=None):

        user = request.user

        following_users = user.following.all()

        image_list = []     

        for following_user in following_users :
                
            #print(following_user.images.all()[:2])
            user_images = following_user.images.all()[:10]
            
            for image in user_images:
                #image_list 안에 가져온 user image 정보를 넣어라
                image_list.append(image)

        #sorted 메소드 사용 (1. 어떤 리스트 정렬, 2. key(function 불러옴) = 기준점(key,길이,이름 등등), 3. 역으로 정렬? )
        #lamda 사용 해서 아래 get_key 펑션 만들지 않고 바로 사용이 가능함
        #sorted_list = sorted(image_list,key=get_key,reverse =True)
        sorted_list = sorted(image_list,key=lambda image: image.created_at,reverse =True)


        #print(image_list)
        print (sorted_list)

        serializer  = serializers.imageSerializer(sorted_list, many=True)

        return Response(serializer.data)

"""
#image 불러와서 image 안에 생성 날짜 리턴 .. lamda 사용해서 펑션 만들지 않고 바로 사용 가능
def get_key(image):
    return image.created_at
"""



# 이미지에 대한 좋아요 처리 (한번 좋아요 두번 다시 해제)
class LikeImage(APIView):
    def get(self,request,image_id,format=None):
        
        user = request.user

        try:
            #Image_id 있다면?
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExists:
            #return Response(status=404)
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        try:
            preexisting_like = models.Like.objects.get(
                creator=user,
                image=found_image
            )
            preexisting_like.delete()

            return Response(status=status.HTTP_204_NO_CONTENT)

        except models.Like.DoesNotExist:
        #model 에서 user + image id 가져와서 
            new_like = models.Like.objects.create(
            creator = user,
            image = found_image
        )
        #저장
        new_like.save()

        #print(image_id)
        return Response(status=status.HTTP_201_CREATED)

#이미지에 댓글 단거 확인
class CommentOnImage(APIView):
    def post(self,request,image_id,format=None):
        
        user = request.user

        try : 
            #image ID 가져옴
            found_image = models.Image.objects.get(id=image_id)
            #존재하지 않으면 404
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        
        #POST 로 날린 데이터 받아오기 (Serializer)
        serializer = serializers.CommentSerializer (data=request.data)

        #Serializer 유효값 체크
        if serializer.is_valid():
            #유효하면 Save for 사용자와 사용자 프로필 사진
            serializer.save(creator=user, image=found_image)

            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        
        #print (request.data)

# 코멘트 (댓글 삭제하기)
class Comment(APIView):
    def delete(self,request,comment_id,format=None):
        
        #사용자 정보 받아오기
        user = request.user
        
        try:
            #Comment_id와 생성자 정보 받아옴
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            #삭제 처리
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)





