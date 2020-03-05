from selenium import webdriver
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
from utility_methods.utility_methods import *
import urllib.request
import os
import sys
from random import randrange

class InstaBot:
    def __init__(self, username=None, password=None):
        """"
        Creates an instance of InstaBot class.

        Args:
            username:str: The username of the user, if not specified, read from configuration.
            password:str: The password of the user, if not specified, read from configuration.

        Attributes:
            driver_path:str: Path to the chromedriver.exe
            driver:str: Instance of the Selenium Webdriver (chrome 72) 
            login_url:str: Url for logging into IG.
            nav_user_url:str: Url to go to a users homepage on IG.
            get_tag_url:str: Url to go to search for posts with a tag on IG.
            logged_in:bool: Boolean whether current user is logged in or not.
        """
        self.username = config['IG_AUTH']['USERNAME']
        self.password = config['IG_AUTH']['PASSWORD']
        self.login_url = config['IG_URLS']['LOGIN']
        self.nav_user_url = config['IG_URLS']['NAV_USER']
        self.get_tag_url = config['IG_URLS']['SEARCH_TAGS']
        self.driver = webdriver.Chrome(config['ENVIRONMENT']['CHROMEDRIVER_PATH'])
        self.logged_in = False


    @insta_method
    def login(self):
        """
        Logs a user into Instagram via the web portal
        """
        self.driver.get(self.login_url)

        time.sleep(1)
        #login_btn = self.driver.find_element_by_xpath('//*[@id="react-root"]/section/main/div/article/div/div[1]/div/form/div[3]') # login button xpath changes after text is entered, find first
        login_btn = self.find_buttons('Log In')[0]

        #WebDriverWait(self.driver, 20).until(EC.frame_to_be_available_and_switch_to_it((By.XPATH,'/html/body/div[1]/section/main/div/article/div/div[1]/div/form/div[2]/div/label/input')))
        #username_input = self.driver.find_element_by_xpath()
        username_input = self.driver.find_element_by_name('username')
        password_input = self.driver.find_element_by_name('password')
        username_input.send_keys(self.username)
        password_input.send_keys(self.password)
        login_btn.click()

    @insta_method
    def search_tag(self, tag):
        """
        Naviagtes to a search for posts with a specific tag on IG.
        Args:
            tag:str: Tag to search for
        """
        self.driver.get(self.get_tag_url.format(tag))


    @insta_method
    def nav_user(self, user):
        """
        Navigates to a users profile page

        Args:
            user:str: Username of the user to navigate to the profile page of
        """
        self.driver.get(self.nav_user_url.format(user))


    @insta_method
    def follow_user(self, user):
        """
        Follows user(s)
        Args:
            user:str: 
                    Username of the user to follow
                    or
                    Link of any pic of the user
        """
        if "www.instagram.com" not in user:
            self.nav_user(user)
            follow_buttons = self.find_buttons('Follow')
            for btn in follow_buttons:
                btn.click()
        else:
            self.driver.get(user)
            follow_buttons = self.find_buttons('Follow')
            for btn in follow_buttons:
                btn.click()
    @insta_method
    def unfollow_user(self, user):
        """
        Unfollows user(s)
        Args:
            user:str: Username of user to unfollow
        """
        self.nav_user(user)
        unfollow_btns = self.find_buttons('Following')
        if unfollow_btns:
            for btn in unfollow_btns:
                btn.click()
                unfollow_confirmation = self.find_buttons('Unfollow')[0]
                unfollow_confirmation.click()
        else:
            print('No {} buttons were found.'.format('Following'))

    @insta_method
    def like_latest_posts(self, user, n_posts, like=True):
        """
        Likes a number of a users latest posts, specified by n_posts.

        Args:
            user:str: User whose posts to like or unlike
            n_posts:int: Number of most recent posts to like or unlike
            like:bool: If True, likes recent posts, else if False, unlikes recent posts

        TODO: Currently maxes out around 15.
        """
        action = 'Like' if like else 'Unlike'
        self.nav_user(user)
        imgs = []
        imgs.extend(self.driver.find_elements_by_class_name('_9AhH0'))
        for img in imgs[:n_posts]:
            img.click() 
            time.sleep(1) 
            try:
                self.driver.find_element_by_xpath("//*[@aria-label='{}']".format(action)).click()
            except Exception as e:
                print(e)
            #self.comment_post('beep boop testing bot')
            self.driver.find_elements_by_class_name('ckWGn')[0].click()



    @insta_method
    def like_comment(self, link, comments):
        done = open("Done.txt","a+")
        if (link in done.readlines()):
            done.close()
            return 0
        self.driver.get(link)
        time.sleep(2)
        
        if len(self.driver.find_elements_by_class_name('Ypffh'))==0:
            return 1
        comment_input = self.driver.find_elements_by_class_name('Ypffh')[0]
        comment_input.click()
        #print("before",comment_input)
        comment_input = self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div[2]/section[3]/div/form/textarea')
        comment_input.click()
        #print("after",comment_input)
        comment_input.send_keys(comments[randrange(len(comments))])
        comment_input.send_keys(Keys.RETURN)
        self.driver.find_elements_by_class_name('_8-yf5 ')[0].click()
        #self.driver.find_element_by_xpath('/html/body/div[1]/section/main/div/div/article/div[2]/section[1]/span[1]/button/svg').click()
        done.write(link)
        done.close()
        return 1


    #@insta_method
    #def comment_post(self, text):
        #"""
        #Comments on a post that is in modal form
        #"""

        #comment_input = self.driver.find_elements_by_class_name('Ypffh')[0]
        #comment_input.click()
        #comment_input.send_keys(text)
        #comment_input.send_keys(Keys.Return)

        #print('Commentd.')

    def infinite_scroll(self):
        """
        Scrolls to the bottom of a users page to load all of their media

        Returns:
            bool: True if the bottom of the page has been reached, else false

        """
        SCROLL_PAUSE_TIME = 1
        self.last_height = self.driver.execute_script("return document.body.scrollHeight")
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SCROLL_PAUSE_TIME)
        self.new_height = self.driver.execute_script("return document.body.scrollHeight")
        if self.new_height == self.last_height:
            return True
        self.last_height = self.new_height
        return False

    def find_buttons(self, button_text):
        """
        Finds buttons for following and unfollowing users by filtering follow elements for buttons. Defaults to finding follow buttons.
        Args:
            button_text: Text that the desired button(s) has
        """
        buttons = self.driver.find_elements_by_xpath("//*[text()='{}']".format(button_text))
        return buttons


if __name__ == '__main__':

    config_file_path = 'config_.ini' 
    logger_file_path = './bot.log'
    config = init_config(config_file_path)
    logger = get_logger(logger_file_path)

    comment_file = open("comments.txt","r+")
    comments=comment_file.readlines()
    comment_file.close()

    bot = InstaBot()
    bot.login()
    f=open(sys.argv[1]+'.txt','r+')
    links = f.readlines()
    f.close()
    count=5
    for line in links:
        #bot.follow_user(line)
        success = bot.like_comment(line,comments)
        if success:
            with open(sys.argv[1]+'.txt', 'r') as fin:
                data = fin.read().splitlines(True)
            with open(sys.argv[1]+'.txt', 'w') as fout:
                fout.writelines(data[1:])
            count-=1
        if not count:
            break
    ##bot.follow_user('psyshiva319')
    #bot.like_latest_posts('s_v4pe', 1, like=True)