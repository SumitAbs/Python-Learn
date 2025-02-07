from django.urls import path
from . import views,matplotlib

urlpatterns = [
    path('', views.index, name='index'), # This is the root path
    path('about/', views.about, name='about'), # This is the about path
    path('contact/', views.contact, name='contact'), # This is the contact path
    path('login/', views.set_login, name='set_login'), # This is the login path
    path('signup/', views.signup, name='signup'), # This is the signup path
    path('logout/', views.logout, name='logout'), # This is the logout path
    path('profile/', views.profile, name='profile'), # This is the profile path
    path('forgot-password/', views.forgot_password, name='forgot-password'), # This is the forgot_password path
    path('reset-password/<uidb64>/<token>/', views.reset_password, name='reset-password'), # This is the reset_password path

    path('cdashboard/', views.cdashboard, name='cdashboard'), # This is the Home path
    
    path('numpy-example/', views.numpy_example, name='numpy-example'),
    path('matrix_multiplication/', views.matrix_multiplication, name='matrix_multiplication'),
    
    path('ArrayCreationFunctions/', views.ArrayCreationFunctions, name='ArrayCreationFunctions'),
    path('BooleanLogicalOperations/', views.BooleanLogicalOperations, name='BooleanLogicalOperations'),
    path('SortingSearching/', views.SortingSearching, name='SortingSearching'),
    path('RandomNumberGeneration/', views.RandomNumberGeneration, name='RandomNumberGeneration'),
    path('StatisticalFunctions/', views.StatisticalFunctions, name='StatisticalFunctions'),
    path('MathematicalFunctions/', views.MathematicalFunctions, name='MathematicalFunctions'),
    path('ArrayManipulationFunctions/', views.ArrayManipulationFunctions, name='ArrayManipulationFunctions'),
    
    path('PandasExamples/', views.PandasExamples, name='PandasExamples'),
    path('MatLab/', matplotlib.test, name='test'),
    
]