# Twig 0.2.0

Twig is a backend web framework for python utilizing the **socket** module to handle http requests and serve responses.

### Changelog

---

**0.2.0**

 - Added `set_all_routes` function

 - Fixed inconsistent request handling

 - Improved documentation



### REST API example

This example shows how to make a basic REST API with Twig that adds 2 numbers together.  It includes all the current functionalities of Twig.

Example *main.py*:

```py
import random
from typing import Dict
from Twig import Server, ContentType, Response as res

# SERVER CONSTRUCTOR EXAMPLE

app = Server("", verbose=False, open_root=False)

# ---PARAMETERS--- #
#
# verbose will show the full request each time when True
#
# open_root will open the index of the site in a web browser every time the server runs.
#
# ---------------- #


# SET ALL ROUTES EXAMPLE

app.set_all_routes({
    "about": lambda headers: res.Response("Im joe and this is my website.", ContentType.plain)
})

# ---ABOUT--- #
# this overwrites all routes in the app with new routes. This is so you can
#have all your routes in a separate file from their functions if you wanted.
# ----------- #


# ROUTE DECORATOR EXAMPLES

# ---ABOUT--- #
# Creates a path in the server for that function.  The path is whatever is
#supplied to the decorator as an argument
#
# Important!!!: every route function must include an argument for headers
#even if route function does not use any headers. 
# ----------- #

# json example
@app.route("apiexample/json")
def test_json(headers: Dict[str, str]):
    return res.Response(f"[{random.randint(0,100)},{random.randint(0,100)},{random.randint(0,100)}]", ContentType.json)

# plaintext example
@app.route("apiexample/plain")
def test_plain(headers: Dict[str, str]):
    return res.Response("Lorem ipsum dolor sit amet, consectetur adipiscing elit. Cras erat dui, finibus vel lectus ac, pharetra dictum odio. Etiam risus sapien, auctor eu volutpat sit amet, porta in nunc. Quisque vitae varius ex, eu volutpat orci. Cras vel elit sed mi placerat pharetra eget vel odio. Cras vel elit sed mi placerat pharetra eget vel odio. Proin ipsum purus, laoreet quis dictum a, laoreet sed ligula. Cras erat dui, finibus vel lectus ac, pharetra dictum odio. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Quisque vitae varius ex, eu volutpat orci. Quisque vitae varius ex, eu volutpat orci. Duis ac nulla varius diam ultrices rutrum. Nullam tempus scelerisque purus, sed mattis elit condimentum nec. Cras erat dui, finibus vel lectus ac, pharetra dictum odio. Etiam risus sapien, auctor eu volutpat sit amet, porta in nunc. Quisque vitae varius ex, eu volutpat orci. Integer ultricies malesuada quam. Etiam risus sapien, auctor eu volutpat sit amet, porta in nunc.", ContentType.plain)

# css example
@app.route("apiexample/css")
def test_css(headers: Dict[str, str]):
    return res.Response(res.read("index.css"), ContentType.css)

# wasm example
@app.route("apiexample/wasm")
def test_css(headers: Dict[str, str]):
    return res.Response(res.read("example.wasm"), ContentType.wasm)

# headers example
@app.route("apiexample")
def test_headers(headers: Dict[str, str]):
    sum = int(headers["num-1"]) + int(headers["num-2"])
    return res.Response(f'{{"result":{sum}}}', ContentType.json)

# html example
@app.route("")
def index(headers: Dict[str, str]):
    return res.Response(res.read("index.html"))


# MANUALLY SET ROUTE EXAMPLE

def manual_route(headers: Dict[str, str]):
    return res.Response('{"message":"Hello"}', ContentType.json)

app.set_route("manual", manual_route)

# ---ABOUT--- #
# this does the same thing as the @app.route() decorator and can be
#used to set routes for functions in external files.
# ----------- #

# Running the server
app.run()
```

Example *index.html*:

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Home</title>
</head>
<body>
    <input type="number" id="num1" value="0">
    +
    <input type="number" id="num2" value="0">
    =
    <span id="Content">
        
    </span>
    <div><button id="solve">solve</button></div>
    <script>
        const CONTENT_DIV = document.getElementById("Content")
        document.getElementById("solve").addEventListener("click", async_solve)
        async function async_solve(){
            let num1 = parseInt(document.getElementById("num1").value)
            let num2 = parseInt(document.getElementById("num2").value)
            const res = await fetch("/apiexample", {method:'POST', headers:{
                "num-1":num1,
                "num-2":num2
            }})
            const res_json = await res.json()
            CONTENT_DIV.innerText = res_json.result
        }
    </script>
</body>
</html>
```
