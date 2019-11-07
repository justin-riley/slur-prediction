<center><h1>slur-prediction</h1></center><br>
Analysis of reddit comments to determine whether someone can be identified as someone who uses bigoted language based on comments that don't use explicit slurs.

<h3>Data collection:</h3><br>
I identified a small collection of subreddits where one would be more likely to
encounter users who would be more likely to use racist or homophobic language,
then scraped those subreddits until I was able to find a good collection of
accounts who used words of interest.  I then went through the comment histories
of those accounts and scraped as many of their past comments as the Reddit API
allowed, changing the sorting method on each user to get around the limit of
1000 comments.<br>


