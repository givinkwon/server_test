from django.urls import include, path
from rest_framework import routers
from django.conf.urls import url
from api.account import viewsets as view_account
from api.board import viewsets as view_board
from api.category import viewsets as view_category
from api.payment import viewsets as view_payment
from api.project import viewsets as view_project
from api.kakaotalk import viewsets as view_kakaotalk
from typing import TYPE_CHECKING
app_name = 'api'

router = routers.DefaultRouter()
#account
router.register('users', view_account.UserViewSet)
router.register('client', view_account.ClientViewSet)
router.register('partner', view_account.PartnerViewSet)
router.register('portfolio', view_account.PortfolioViewSet)
router.register('structure', view_account.StructureViewSet)
router.register('machine', view_account.MachineViewSet)
router.register('certification', view_account.CertificationViewSet)
router.register('process', view_account.ProcessViewSet)
#board
router.register('notice', view_board.NoticeViewSet)
router.register('magazine', view_board.MagazineViewSet)

#category
router.register('maincategory', view_category.MaincategoryViewSet)
router.register('category', view_category.CategoryViewSet)
router.register('subclass', view_category.SubclassViewSet)
router.register('region', view_category.RegionViewSet)
router.register('city', view_category.CityViewSet)
router.register('develop', view_category.DevelopViewSet)
router.register('developbig', view_category.DevelopbigViewSet)

#payment
router.register('paylist', view_payment.PaylistViewSet)

#project
router.register('project', view_project.ProjectViewSet)
router.register('requests', view_project.RequestViewSet)
router.register('select', view_project.SelectViewSet)
router.register('select_save', view_project.Select_saveViewSet)
router.register('common', view_project.CommonViewSet)
router.register('answer', view_project.AnswerViewSet)
router.register('review', view_project.ReviewViewSet)

#kakaotalk
router.register('kakaotalk', view_kakaotalk.KakaoViewSet, basename='kakao')

urlpatterns = [
    path('', include(router.urls))
]