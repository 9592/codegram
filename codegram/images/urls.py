

#jango function
#from django.conf.urls import url
from django.urls import path 
from . import views


"""
테스트 했던 것 다 주석 처리
#패턴 : path("~redirect/", view=user_redirect_view, name="redirect"),
urlpatterns = [
    path (
        "all/",
        view=views.ListAllImages.as_view(),
        name= "all_images"
    ),
     path (
        "comments/",
        view=views.ListAllComments.as_view(),
        name= "all_images"
    ),
     path (
        "likes/",
        view=views.ListAllLikes.as_view(),
        name= "all_images"
    )
]
"""


urlpatterns = [
    path (
        "",
        view=views.Feed.as_view(),
        name = "feed"
    ),
    path (
        "<image_id>/likes/",
        view = views.LikeImage.as_view(),
        name = "like_image"
    ),
    path (
        "<image_id>/comments/",
        view = views.CommentOnImage.as_view(),
        name = "comment_image"
    ),
    path ("comments/<comment_id>",
    view = views.Comment.as_view(),
    name ="comment"
    ),
]

