import utils
from flask import Flask, render_template, request, redirect, url_for
from werkzeug.utils import secure_filename

UPLOAD_PATH = "/Users/alexkim/Downloads/modelDB/uid=0"

app = Flask(__name__)
app.config["UPLOAD_PATH"] = UPLOAD_PATH


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/builder", methods=["GET", "POST"])
def upload_data():
    if request.method == "POST":
        model_meta = request.form.keys()
        if "inputSize" not in model_meta or "outputSize" not in model_meta or "model" not in request.files:
            print("input error")
            return redirect(request.url)
        else:
            input_size = int(request.form.get("inputSize"))
            output_size = int(request.form.get("outputSize"))
            model = request.files["model"]
            if input_size == 0 or output_size == 0 or not utils.allowed_file(model.filename):
                print("non valid input")
                return redirect(request.url)
            else:
                dt = utils.timestamp_hash()
                utils.ensure_dir(f"{UPLOAD_PATH}/dt={dt}/")
                model_name = f"{secure_filename(model.filename)}"
                with open(f"{UPLOAD_PATH}/dt={dt}/{model_name}.meta", "w", encoding="utf-8") as meta:
                    meta.write(f"inputSize={input_size}\noutputSize={output_size}")
                model.save(f"{UPLOAD_PATH}/dt={dt}/{model_name}")
                return redirect(url_for("uploaded_data", dt=dt))
    else:
        return render_template("build_form.html")


@app.route("/builder/submit", methods=["GET", "POST"])
def uploaded_data():
    dt = request.args.get("dt")
    return f"submitted={dt}"
