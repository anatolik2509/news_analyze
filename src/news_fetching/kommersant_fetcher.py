from rss_parser import RSSParser
from requests import get

rss_url = "https://www.kommersant.ru/RSS/section-economics.xml"
response = get(rss_url)

rss = RSSParser.parse(response.text)

# Print out rss meta data
print("Language", rss.channel.language.content)
print("RSS", rss.version.content)
# print(rss.channel)

for item in rss.channel.items:
    print(item.title.content)