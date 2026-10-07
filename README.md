# Reddit Engagement Analysis
Data analysis of 20+ Reddit posts on 20+ subreddits

## Overview 

This project examines patterns of engagement across Reddit posts using publicly observable measures including views, upvotes, and comments. The dataset was collected over approximately ten months and contains observations from 20+ subreddit communities. This includes the number of views, upvotes and comments at different time intervals, i.e., when the post is 1 hour old, 10 minutes old, 1 day old, etc.

## Research Questions

This study investigates:

1. How does view count relate to upvotes?
2. How does view count relate to comments?
3. How does comment engagement vary across subreddit categories?
4. Do different types of Reddit communities show different engagement patterns?
5. When do the most views/upvotes come in?

## Data

The dataset contains observations of Reddit posts including:

- Post
- Subreddit
- Views (at various time intervals)
- Upvotes (at various time intervals)
- Comments (at various time intervals)
- Time since posting

Derived metrics include:

- Upvotes per 1,000 views
- Comments per 1,000 views

## Methodology

Data were collected manually over approximately ten months. I would look at the number of views, upvotes, comments and how old the post was and note it down on a Google Docs folder. The study is observational and uses a small, non-random sample of Reddit posts.

## Results

The subreddit matters more than the content. The same posts perform differently on different subreddits. This fact is consistent with previous research done on similar matter about Reddit. The growth of a post is the highest in the beginning and plateaus. One should not expect the second day to be like the first.

## Limitations

The dataset is relatively small and is not a random sample of Reddit. Subreddit audiences differ substantially, and observations were collected at different time intervals. I also did not include the data of posts that did get more than 5 upvotes, so this has selection bais.

Therefore, the findings should be interpreted as exploratory rather than as representative of Reddit as a whole.

## Reproducibility

The analysis code and dataset are provided in this repository.
