# twitter-stats
A small python module to get twitter statistics and display them


### Steps to Install

`git clone`

Create your python virtual environment  
`mkvirtualenv smarttask`  
`workon smarttask`

`pip install -r requirements.txt`

Create a fresh User, and DB in postgres
The script asks for DB Name, DB user and password which you want to create  
`./setup.sh`

Add in the first three lines the credentials which you have typed in before  
`mv config_example.py config.py`
`edit config.py`

Now you have a empty DB which the "smarttask db_manage can access"
```
python db_manage.py db init
python db_manage.py db migrate
python db_manage.py db upgrade
python run.py
```





How often is a retweet retweted - can you measure it?
Short answer: No, since a retweet always refers directly to the original tweet
https://twittercommunity.com/t/is-the-retweet-count-for-a-tweet-object-correct-when-it-is-a-retweet/8751
