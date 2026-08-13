import json
import urllib.request


def post(path, data):
    raw = json.dumps(data).encode("utf-8")
    req = urllib.request.Request(
        "http://127.0.0.1:8000" + path,
        data=raw,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    with urllib.request.urlopen(req) as response:
        return json.loads(response.read().decode("utf-8"))


def get(path):
    with urllib.request.urlopen("http://127.0.0.1:8000" + path) as response:
        return json.loads(response.read().decode("utf-8"))


def main():
    lesson = get("/api/lessons/3")
    print("title", lesson["title"])
    first = lesson["exercises"][0]
    print("mcq options", [item["text"] for item in first["options"]])
    print("start", post("/api/lessons/3/start", {}))
    print(
        "wrong mcq",
        post(
            "/api/lessons/3/answer",
            {"exercise_id": first["id"], "answer": "I am sorry"},
        ),
    )
    pairs = lesson["exercises"][2]
    print(
        "wrong pairs",
        post(
            "/api/lessons/3/answer",
            {
                "exercise_id": pairs["id"],
                "answer": "Por favor=I am sorry;De nada=Please;Lo siento=You are welcome",
            },
        ),
    )
    translate = lesson["exercises"][1]
    print(
        "wrong translate",
        post(
            "/api/lessons/3/answer",
            {"exercise_id": translate["id"], "answer": "Hola Casa"},
        ),
    )


if __name__ == "__main__":
    main()
