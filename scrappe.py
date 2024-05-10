import os

from scrapegraphai.graphs import SmartScraperGraph
from dotenv import load_dotenv
import json

load_dotenv()
graph_config = {
    "llm": {
        # "api_key": os.getenv("OPENAI_API_KEY"),
        "model": "gpt-3.5-turbo",
    },
}
# Crear un objeto SmartScraperGraph
smart_scraper = SmartScraperGraph(
    "List me all the repositories.",
    "https://github.com/alonsoir",
    config=graph_config,
)

results = smart_scraper.run()

print(json.dumps(results, indent=4))

print("Done!")
