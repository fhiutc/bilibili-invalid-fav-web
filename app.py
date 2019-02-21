# -*- coding:utf-8 -*-
import json
from sanic import Sanic
from sanic import response
from sanic_jinja2 import SanicJinja2
from getInvalidVideos import get_fav_videos_from_user


app = Sanic()
jinja = SanicJinja2(app)


@app.route("/id/<uid>")
async def processInvalid(request, uid):
    print('ok')
    # data = json.dumps({'data': get_fav_videos_from_user(uid)}, ensure_ascii = False)
    # return response.text(data, content_type="application/json")
    data = get_fav_videos_from_user(uid)
    return jinja.render('index.html', request, video_datas = data)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)
