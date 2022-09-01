# import unittest
# import os
# from pyramid import testing
# from mock import Mock
# from sqlalchemy_utils import create_database, database_exists
# from .meta_module import Base
# from .base_models import get_engine, get_session_factory, get_tm_session
#
#
#
# from ..dc_module.category import category_domain
#
# from ..dc_module.product import product_domain
#
# from ..dc_module.account import account_domain
#
# from ..dc_module.image import image_domain
#
# from ..dc_module.group import group_domain
#
# from ..dc_module.tag import tag_domain
#
#
#
# def dummy_request(dbsession):
#     csrf = 'abc'
#     request = testing.DummyRequest(db_session=dbsession,
#                                    real_ip="127.0.0.1",
#                                    user_id="",
#                                    headers={'X-CSRF-Token': csrf})
#     request.session = Mock()
#     csrf_token = Mock()
#     csrf_token.return_value = csrf
#     request.session.get_csrf_token = csrf_token
#     return request
#
# class BaseTest(unittest.TestCase):
#     def setUp(self):
#         self.config = testing.setUp(settings={
#             'sqlalchemy.url': 'postgresql+psycopg2://postgres:password@localhost/test_DRgym',
#             'repository_path': os.path.join(os.getcwd(), 'tests_uploads')
#         })
#         self.config.include('.base_models')
#         settings = self.config.get_settings()
#
#         self.engine = get_engine(settings)
#         session_factory = get_session_factory(self.engine)
#         # 檢查DB是否存在
#         if not database_exists(settings.get('sqlalchemy.url')):
#             # 創建DB
#             create_database(settings.get('sqlalchemy.url'))
#
#         self.session = get_tm_session(session_factory, transaction.manager)
#
#     def init_database(self):
#         Base.metadata.create_all(self.engine)
#
#     def tearDown(self):
#         testing.tearDown()
#         transaction.abort()
#         Base.metadata.drop_all(self.engine)
#
#
#
# import transaction
# import webtest
# from .. import main
#
# class FunctionalTests(unittest.TestCase):
#     @classmethod
#     def setUpClass(cls):
#         settings = {
#             'sqlalchemy.url': 'postgresql+psycopg2://postgres:password@localhost/test_DRgym',
#             'auth.secret': 'seekrit',
#             'repository_path': os.path.join(os.getcwd(), 'tests_uploads')
#         }
#         cls.init_database()
#
#         app = main({}, **settings)
#         cls.testapp = webtest.TestApp(app)
#
#     @classmethod
#     def init_database(cls):
#         from DRgym.models import domain
#         config = testing.setUp(settings={
#             'sqlalchemy.url': 'sqlite:///DRgym.sqlite'
#         })
#         config.include('DRgym.models')
#         settings = config.get_settings()
#         cls.engine = get_engine(settings)
#
#         Base.metadata.create_all(cls.engine)
#
#     @classmethod
#     def tearDownClass(cls):
#         Base.metadata.drop_all(bind=cls.engine)
#         path = os.path.abspath(os.path.join(os.path.dirname("__file__")))
#         os.remove('{}/DRgym.sqlite'.format(path))