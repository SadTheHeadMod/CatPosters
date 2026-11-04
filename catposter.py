"""Display a random cat poster.

Fetches a random cat image from The Cat API and opens it in the default
browser. No API key is required for basic use.
"""

import json
import urllib.request
import webbrowser

CAT_API_URL = "https://api.thecatapi.com/v1/images/search"


def fetch_random_cat_poster():
    """Return the URL of a random cat image from The Cat API."""
    with urllib.request.urlopen(CAT_API_URL) as response:
        data = json.loads(response.read().decode("utf-8"))
    return data[0]["url"]


def main():
    poster_url = fetch_random_cat_poster()
    print("Random cat poster:", poster_url)
    webbrowser.open(poster_url)


if __name__ == "__main__":
    main()
