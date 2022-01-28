import requests
import urllib.parse
import json


def getUrl(keyword):

    encoded_search = urllib.parse.quote_plus(keyword)
    url = f"https://www.youtube.com/results?search_query={encoded_search}&sp=EgIQAQ%253D%253D"
    response = requests.get(url).text
    while "ytInitialData" not in response:
        response = requests.get(url).text
    
    start = (
        response.index("ytInitialData")
        + len("ytInitialData")
        + 3
    )
    end = response.index("};", start) + 1
    
    json_str = response[start:end]
    data = json.loads(json_str)

    videos = data["contents"]["twoColumnSearchResultsRenderer"]["primaryContents"][
        "sectionListRenderer"]["contents"][0]["itemSectionRenderer"]["contents"]
        
    for row in videos:
        video_data = row.get("videoRenderer", {})
        duration = str(video_data.get("lengthText", {}).get("simpleText", 0))
        return "https://www.youtube.com/" +video_data.get("navigationEndpoint", {}).get("commandMetadata", {}).get("webCommandMetadata", {}).get("url", None)
