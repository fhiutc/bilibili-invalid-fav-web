# -*- coding:utf-8 -*-
import json
from sanic import Sanic
from sanic import response
from getInvalidVideos import get_fav_videos_from_user


app = Sanic()


@app.route("/id/<uid>")
async def processInvalid(request, uid):
    print('ok')
    data = json.dumps({'data': get_fav_videos_from_user(uid)}, ensure_ascii = False)
    return response.text(data, content_type="application/json")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
