# This doesn't reflect backrefs in the user graph
select sum(followers_count)
from users
where users.twitter_id IN (
  select followers.twitter_follower_id from users
  JOIN followers on users.twitter_id = followers.twitter_id
  where screen_name = 'nellykfm');


# Fetched finally a hole set - this gives
select count(distinct twitter_follower_id) from followers where twitter_id in
(
	select twitter_follower_id from followers where twitter_id = 237347211
)




-- followers_of_follower
select count(distinct twitter_follower_id) from followers where twitter_id in
(
	select twitter_follower_id from followers where twitter_id = 237347211
)

select cast(created_at as date) as foo, favorite_count, is_retweet, retweet_count
from tweets
where user_id = 279
group by foo, favorite_count, is_retweet, retweet_count
order by foo






select twitter_follower_id from followers where twitter_id = 48399689


select * from users where id = 245;

select * from followers where user_id = 244;

select * from users where twitter_id = 4584605573;

select * from users where screen_name = 'rlsux';

select * from users where screen_name = 'nellykfm';


select * from tweets where user_id = 279;

select avg(is_retweet::int) from tweets where user_id = 279

select coalesce(count(case when in_reply_to_user_id = null then 1 end)/count(*), 0) * 100 Percentage from tweets where user_id = 279
