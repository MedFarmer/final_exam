from django.urls import path, reverse_lazy
from .views import SignUpView, Home, VerifyEmailView, VerificationSuccess, VerificationError, Login, Logout, AddPost, PostsView, PostView, DeleteComment, DeletePost, UpdatePost
from django.contrib.auth.views import PasswordResetConfirmView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetView

urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('verify/<int:user_id>/<str:token>/', VerifyEmailView.as_view(), name='verify'),
    path('verify/success/', VerificationSuccess.as_view(), name='verify_success'),
    path('verify/error/', VerificationError.as_view(), name='verify_error'),
    path('login/', Login.as_view(), name='login'),
    path('reset/', PasswordResetView.as_view(template_name='password_reset.html'), name='reset'),
    path('reset/<uidb64>/<str:token>/', PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'),  name='password_reset_confirm'),
    path('reset/done/', PasswordResetDoneView.as_view(template_name='reset_done.html'), name='password_reset_done'),
    path('reset/complete/', PasswordResetCompleteView.as_view(template_name='reset_complete.html'), name='password_reset_complete'),
    path('logout/', Logout.as_view(), name='logout'),
    path('add_post/', AddPost.as_view(), name='add_post'),
    path('rubric/<int:subrubric_pk>/', PostsView.as_view(), name='posts'),
    path('rubric/<int:subrubric_pk>/post/<int:post_pk>/', PostView.as_view(), name='post'),
    path('rubric/<int:subrubric_pk>/post/<int:post_pk>/delete_comment/<int:comment_pk>/', DeleteComment.as_view(), name='delete_comment'),
    path('rubric/<int:subrubric_pk>/delete_post/<int:post_pk>/', DeletePost.as_view(), name='delete_post'),
    path('rubric/<int:subrubric_pk>/update_post/<int:post_pk>/', UpdatePost.as_view(), name='update_post'),
]
