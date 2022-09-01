# # coding=utf8
# from __future__ import unicode_literals
# from pyramid.security import Allow, Deny, Everyone, ALL_PERMISSIONS
#
#
# class AdminContext(object):
#
#     @staticmethod
#     def __acl__():
#         return [
#             # ACE( 1, 2, 3)
#             # 1. pyramid.security.Allow, or pyramid.security.Deny
#             # 2. principal. A principal is usually a user id， it also may be a group id
#             # 3. permission or sequence of permission names
#             # (Allow, 'sa', 'ALL_PERMISSIONS'),
#
#             (Allow, 'account', 'login'),
#
#
#             (Allow, 'per:index', 'index'),
#             (Allow, 'per:account', 'account'),
#
#             # (Allow, 'per:group_list', 'group'),
#
#
#
#             (Allow, 'per:category', 'category'),
#
#
#             (Allow, 'per:tag', 'tag'),
#
#
#
#             (Allow, 'per:product', 'product'),
#
#
#
#
#
#             # 拒絕全部
#             (Deny, Everyone, ALL_PERMISSIONS),
#         ]
#
#     def __init__(self, request):
#         pass