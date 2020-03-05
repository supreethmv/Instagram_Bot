# Instagram_Bot
Instagram bot for Marketing. Go to a specific hashtag, like their posts, randomly choose a comment to post.


Selenium Webdriver is used. Download the compatible version of the google chrome webdriver(from:https://chromedriver.chromium.org/downloads) for your machine and run 

python extract_links.py hashtag1 hashtag2 hashtag3 ...

Files will be created as
hashtag1.txt
hashtag2.txt
hashtag3.txt
...

Config the user account credentials using which you want to like and comment on posts in config_.ini

Now run 
python instagram_bot.py hashtag1

This will open chrome browser, login and go to the links of post with hashtag1, like and comment.

Comments are chosen randomly from the file comments.txt
Here each comment is one single line comment because instagram doesn't support multi line comments.
Add your different marketing comments in each line of this file. So, now the comments are chosen randomly from this list to comment on the post.
