from sanic import Sanic
from sanic.response import json

app = Sanic()

@app.route("/id/<uid>")
async def test(request, uid):
    return json({"hello": "world"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000)