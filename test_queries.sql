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
