import utils
from flask import Flask, render_template, request, redirect, url_for

UPLOAD_PATH = "modelDB/uid=0"

app = Flask(__name__)
app.config["UPLOAD_PATH"] = UPLOAD_PATH


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/builder", methods=["GET", "POST"])
def upload_data():
    if request.method == "POST":
        meta_map = request.form.to_dict()
        model_type = meta_map.pop("type")
        if not all(meta_map.values()) or "model" not in request.files:
            return redirect(request.url)
        else:
            model_file = request.files["model"]
            if any([int(i) == 0 for i in meta_map.values()]) or not utils.allowed_file(model_file.filename):
                return redirect(request.url)
            else:
                dt = utils.timestamp_hash()
                utils.ensure_dir(f"{UPLOAD_PATH}/dt={dt}/")
                with open(f"{UPLOAD_PATH}/dt={dt}/ModelIO.hpp", "w", encoding="utf-8") as model_io:
                    model_io.write(utils.make_cpp_header(meta_map))
                model_file.save(f"{UPLOAD_PATH}/dt={dt}/trace_model.pth")
                utils.build_model_server(dt, model_type)
                return redirect(url_for("uploaded_data", dt=dt))
    else:
        return render_template("build_form.html")


@app.route("/builder/submit", methods=["GET", "POST"])
def uploaded_data():
    dt = request.args.get("dt")
    return f"submitted={dt}"
