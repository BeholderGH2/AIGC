import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/")
def index():
    return app.send_static_file("index.html")

@app.route("/chat-with-ai", methods=["POST"])
def chat_with_ai():
    message = request.json["message"]
    if message == "请进行对话来对我进行肖像":
        ai_reply = "你好！请问有什么可以帮您的吗？"
    else:
        api_url = "https://api.openai.com/v1/engines/davinci/completions"
        prompt = "对话：" + message
        input_data = {"prompt": prompt, "max_tokens": 50}
        headers = {"Authorization": "vSjJ8sj3h45H3uHAaj3"}
        response = requests.post(api_url, json=input_data, headers=headers)
        ai_reply = response.json()["choices"][0]["text"].strip()

    return jsonify({"reply": ai_reply})

@app.route("/generate-image", methods=["POST"])
def generate_image():
    prompt = request.json["prompt"]
    access_token = get_access_token()
    api_url = "https://aip.baidubce.com/rest/2.0/image-process/v1/generate_product"
    headers = {"Content-Type": "application/x-www-form-urlencoded"}
    params = {"access_token": access_token, "image": prompt}
    response = requests.post(api_url, data=params, headers=headers)
    task_id = response.json()["data"]["task_id"]

    return jsonify({"task_id": task_id})

@app.route("/get-image-link/<task_id>")
def get_image_link(task_id):
    access_token = get_access_token()
    api_url = f"https://aip.baidubce.com/rest/2.0/image-process/v1/get_result?access_token={access_token}&task_id={task_id}"
    response = requests.get(api_url)
    image_link = response.json()["data"]["image"]

    return jsonify({"image_link": image_link})

os.environ['STABILITY_HOST'] = 'grpc.stability.ai:443'

os.environ['STABILITY_KEY'] = 'sk-rbhsWXlm8UsbHoE1lCVtDWTddaP4Bf4s5ART8DOySB8cAEXI'

stability_api = client.StabilityInference(
    key=os.environ['STABILITY_KEY'],
    verbose=True,
    engine="stable-diffusion-xl-1024-v1-0"
)

seed = random.randint(0 ,2147483647)
answers = stability_api.generate(
    prompt="A Starcraft II Archbishop character portrait",
    seed=seed,
    steps=50,
    cfg_scale=8.0,
    width=1024,
    height=1024,
    samples=1,

    sampler=generation.SAMPLER_K_DPMPP_2M
)
for resp in answers:
    for artifact in resp.artifacts:
        if artifact.finish_reason == generation.FILTER:
            warnings.warn(
                "Your request activated the API's safety filters and could not be processed."
                "Please modify the prompt and try again.")
        if artifact.type == generation.ARTIFACT_IMAGE:
            img = Image.open(io.BytesIO(artifact.binary))
            img.save(str(artifact.seed)+ ".png")

def get_access_token():
    api_url = "https://aip.baidubce.com/oauth/2.0/token"
    api_key = "No3IG2nmnGBQU81OSTAEg8Tf"
    secret_key = "CUiP1w28KXIpgLc6bEjXEFaOr6ZFR8xc"
    params = {
        "grant_type": "client_credentials",
        "client_id": api_key,
        "client_secret": secret_key
    }
    response = requests.get(api_url, params=params)
    return response.json()["access_token"]

if __name__ == "__main__":
    app.run(debug=True)