# Snapshot RSS

Convert Snapshot space proposals into RSS feeds

## Usage

To create an RSS feed, just identify the name of the `space` on the [Snapshot Page](https://snapshot.page) (it is the name that appears in the URL bar of your browser), and then register the feed `https://snapshot-rss.vercel.app/api/v1/spaces/<SPACE>/proposals`in your RSS reader application.

## Local Development

The project used Python 3 and Flask.

```shell
python3 -m venv env 
source env/bin/activate
pip install -r requirements.txt
flask run
```
