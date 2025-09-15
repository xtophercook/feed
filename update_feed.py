import feedparser
import time
import json

def generate_feed_data():
    """
    Fetches data from FT and Bluesky RSS feeds, combines them, sorts by date,
    and returns the data as a list of dictionaries.
    """
    ft_url = "https://www.ft.com/chris-cook?format=rss"
    bsky_url = "https://bsky.app/profile/did:plc:bgmujpqmzqtx4p3wafhq4t6c/rss"

    ft_feed = feedparser.parse(ft_url)
    bsky_feed = feedparser.parse(bsky_url)
    all_items = []

    # Process FT feed
    if ft_feed.entries:
        for entry in ft_feed.entries:
            if hasattr(entry, 'published_parsed'):
                all_items.append({
                    "source": "FT.com",
                    "title": entry.get('title', 'No Title Available'),
                    "link": entry.get('link'),
                    "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", entry.published_parsed) # ISO 8601 format
                })

    # Process Bluesky feed
    if bsky_feed.entries:
        for entry in bsky_feed.entries:
            if hasattr(entry, 'published_parsed'):
                post_content = entry.get('description', '')
                if "contains quote post or other embedded content" in post_content:
                    continue
                
                all_items.append({
                    "source": "Bluesky",
                    "title": post_content,
                    "link": entry.get('link'),
                    "date": time.strftime("%Y-%m-%dT%H:%M:%SZ", entry.published_parsed) # ISO 8601 format
                })

    # Sort all items by date, newest first
    all_items.sort(key=lambda x: x["date"], reverse=True)
    
    return all_items

if __name__ == "__main__":
    feed_data = generate_feed_data()
    # Save the data to a JSON file
    with open("feed.json", "w") as f:
        json.dump(feed_data, f, indent=4)
    
    print(f"Successfully generated feed.json with {len(feed_data)} items.")
