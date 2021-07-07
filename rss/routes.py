from flask import request, jsonify
from rss import app
from rss.settings import SNAPSHOT_API_ENDPOINT, SNAPSHOT_BASE_URL, RSS_FEED_BASE_URL
from rfeed import Feed, Item, Guid
import requests
from datetime import datetime

@app.route('/api/v1/spaces/<space>/proposals', methods=['GET'])
def proposals(space):
    # Get the proposal from the space
    graphql_query = """
        {
            proposals(
                orderBy: "created",
                orderDirection: desc,
                where:{space:"%s", state:"active"}
            ) {
                id
                title
                body
                created
                author
                state
            }
        }
    """ % space
    r = requests.post('%s/graphql' % SNAPSHOT_API_ENDPOINT, json={'query': graphql_query})

    # Success response
    if r.ok:
        # Build list of items
        items = []
        for proposal in r.json()['data']['proposals']:
            items.append(Item(
                title=proposal['title'],
                link='%s/#/%s/proposal/%s' % (SNAPSHOT_BASE_URL, space, proposal['id']),
                description=proposal['body'],
                author=proposal['author'],
                guid=Guid(proposal['id'], False),
                pubDate=datetime.fromtimestamp(int(proposal['created'])),
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
    else:
        return jsonify({'code': r.status_code, 'text': r.text})