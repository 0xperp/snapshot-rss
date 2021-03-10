from flask import request, jsonify
from rss import app
from rss.settings import SNAPSHOT_API_ENDPOINT, SNAPSHOT_BASE_URL, RSS_FEED_BASE_URL
from rfeed import Feed, Item, Guid
import requests
from datetime import datetime

@app.route('/api/v1/spaces/<space>/proposals', methods=['GET'])
def proposals(space):
    # Get the proposal from the space
    r = requests.get('%s/api/%s/proposals' % (SNAPSHOT_API_ENDPOINT, space))

    # Success response
    if r.ok:
        # Build list of items
        items = []
        for k, v in r.json().items():
            items.append(Item(
                title=v['msg']['payload']['name'],
                link='%s/#/%s/proposal/%s' % (SNAPSHOT_BASE_URL, space, k),
                description=v['msg']['payload']['body'],
                author=v['address'],
                guid=Guid(k, False),
                pubDate=datetime.fromtimestamp(int(v['msg']['timestamp'])),
            ))

        feed = Feed(
            title='%s Proposals' % space,
            link='%s/api/v1/spaces/%s/proposals' % (RSS_FEED_BASE_URL, space),
            description = "Proposals for %s" % space,
            language='en-US',
            lastBuildDate=datetime.now(),
	        items=items
        )

    return feed.rss()