from django.test import Client
from django.test import TestCase, RequestFactory
from stranke4.views import Produkt, Stranka, Obisk, User



# # #---------------------------------------------------------------- Set up djang
# #----------------------------- project_dir = abspath(dirname(dirname(__file__)))
# #----------------------------------------------- sys.path.insert(0, project_dir)
# #-------------------- os.environ['DJANGO_SETTINGS_MODULE'] = 'stranke4.settings'
# #------------------------------------------------------------------- print('dd')
# #------------------------------------------------------------------------------
# #------------------------------------------------------------ print('dddfdfffd')
#---------------------------------------------------------- print(User.username)






class Test_1(TestCase):
    def setUp(self):
        User.objects.create_user('user1', 'ads@dsa.as', 'user')
        self.c=Client()
        self.c.login(username='user1', password='user')
        self.respo=self.c.get('/stranke/')
        print(self.respo.templates)
        
        
    def test_11(self):
        pass
        #self.assertContains(self.respo,'div')
        
class Test_2(TestCase):
    print('ssss')
    fixtures = ['initial.json']

    def setUp(self):
        self.factory = RequestFactory()
        self.c=Client()
        self.c.login(username='robertb', password='miren54321')
        self.a=self.c.get('/stranka/50/')
        print(self.a.content)   
        
    #===========================================================================
    #     
    #     #self.c=Client()
    #     #self.c.login(username='robertb', password='miren54321')
    #     print('oooo')
    #     #TestCase.setUp(self)
        self.user = User.objects.get(username='robertb')
        self.skupina_strank=Stranka.objects.filter(kraj='Postojna', uporabnik=self.user)
        self.stranka=self.skupina_strank.filter(podjetje__icontains='vitraj')[0]
        print(self.stranka)
        
    def test_22(self):
        print(self.stranka.kraj)
    #    request=self.factory.get('/stranke/')
    #     request.user=self.user
        self.assertIn(self.stranka, self.skupina_strank)
    #===========================================================================
    def test__33(self):
        
        self.assertIn('Letrika', str(self.a.content))
        
from django.test import LiveServerTestCase
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from selenium.webdriver.firefox.webdriver import WebDriver

class MySeleniumTests(StaticLiveServerTestCase):
    fixtures = ['initial.json']
    @classmethod
    def setUpClass(cls):
        cls.selenium = WebDriver()
        super(MySeleniumTests, cls).setUpClass()
        
    @classmethod
    def tearDownClass(cls):
        cls.selenium.quit()
        super(MySeleniumTests, cls).tearDownClass()
        
    def test_login(self):
        self.selenium.get('%s%s' % (self.live_server_url, '/'))
        #username_input = self.selenium.find_element_by_name("username")
        #username_input.send_keys('robertb')
        #password_input = self.selenium.find_element_by_name("password")
        #password_input.send_keys('miren54321')
        #self.selenium.find_element_by_xpath('//button[@type="submit"]').click()