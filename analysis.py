import pandas as pd

# 1. Load the dataset
df = pd.read_csv('dataset.csv')

print("=== REDDIT ENGAGEMENT DATA ANALYSIS ===")
print(f"Total posts analyzed: {len(df)}")
print(f"Subreddits tracked: {df['subreddit'].nunique()}\n")

# 2. Analyze Upvotes per 1,000 views range by community type
print("--- Upvotes per 1,000 Views Range by Community Type ---")
for cat, group in df.groupby('community_type'):
    min_val = group['upvotes_per_1k'].min()
    max_val = group['upvotes_per_1k'].max()
    print(f"{cat}: Min = {min_val}, Max = {max_val} (across {len(group)} posts)")

print("\n--- Comments per 1,000 Views Range by Community Type ---")
# 3. Analyze Comments per 1,000 views range by community type
for cat, group in df.groupby('community_type'):
    min_val = group['comments_per_1k'].min()
    max_val = group['comments_per_1k'].max()
    print(f"{cat}: Min = {min_val}, Max = {max_val} (across {len(group)} posts)")

# 4. Filter for top performing post
top_post = df.loc[df['upvotes_per_1k'].idxmax()]
print("\n--- Highest Upvote Conversion Post ---")
print(f"Title: {top_post['post_title']}")
print(f"Subreddit: {top_post['subreddit']}")
print(f"Upvotes per 1k views: {top_post['upvotes_per_1k']}")
