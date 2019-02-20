# -*- coding:utf-8 -*-
from sanic import Sanic
from sanic.response import json
from getInvalidVideos import get_fav_videos_from_user


app = Sanic()


@app.route("/id/<uid>")
async def getInvalidVideos(request, uid):
    print('ok')
    data = get_fav_videos_from_user(uid)
    return json({"data": data})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
