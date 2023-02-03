# Twig

Twig is a backend web framework for python utilizing the *socket* module to handle http requests and serve responses.

Example *main.py*:

```py
import random
from typing import Dict
from Twig import Server, ContentType, Response as res

# create the server instance
app = Server("", verbose=False)

# json example
@app.route("apiexample/json")
def test_json(headers: Dict[str, str]):
    return res.Response(f"[{random.randint(0,100)},{random.randint(0,100)},{random.randint(0,100)}]", ContentType.json)

# plaintext example
@app.route("apiexample/plain")
def test_plain(headers: Dict[str, str]):
    return res.Response("Lorem ipsum dolor sit amet, consectetur adipiscing elit.", ContentType.plain)

# css example
@app.route("apiexample/css")
def test_css(headers: Dict[str, str]):
    return res.Response(res.read("index.css"), ContentType.css)

# headers example
@app.route("apiexample")
def test_headers(headers: Dict[str, str]):
    sum = int(headers["num-1"]) + int(headers["num-2"])
    return res.Response(f'{{"result":{sum}}}', ContentType.json)

# html example
@app.route("")
def index(headers: Dict[str, str]):
    return res.Response(res.read("index.html"))

# run the server
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
    <input type="text" id="num1">
    +
    <input type="text" id="num2">
    =
    <span id="Content">
        
    </span>
    <div><button id="solve">solve</button></div>
    <script>
        const CONTENT_DIV = document.getElementById("Content")
        document.getElementById("solve").addEventListener("click", solve)
        function solve(){
            let num1 = parseInt(document.getElementById("num1").value)
            let num2 = parseInt(document.getElementById("num2").value)
            fetch("/apiexample", {method:'POST', headers:{
                "num-1":num1,
                "num-2":num2
            }}).then(res => res.json()).then(res => {
                CONTENT_DIV.innerHTML = res.result
            })
        }
    </script>
</body>
</html>
```
