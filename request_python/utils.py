import os
import time
import hashlib
import subprocess

BASE = 62
DEFAULT_CHARSET = "0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
ALLOWED_EXTENSIONS = {"pth"}
PARAMETER_MAP = {
    "inputFeatureSize": "INPUT_FEATURE_SIZE",
    "inputSequenceSize": "INPUT_SEQUENCE_SIZE",
    "outputFeatureSize": "OUTPUT_SIZE"
}


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def timestamp_hash():
    ts_trim = int(time.time() * 1000)
    ts_hash = int(hashlib.md5(str(ts_trim).encode("utf-8")).hexdigest(), 16)

    encode_str = []
    while ts_hash > 0:
        r = ts_hash % BASE
        ts_hash //= BASE

        encode_str.append(DEFAULT_CHARSET[r])

    if len(encode_str) > 0:
        encode_str.reverse()
    else:
        encode_str.append("0")

    return "".join(encode_str)


def ensure_dir(upload_path):
    upload_dir = os.path.dirname(upload_path)
    if not os.path.exists(upload_dir):
        os.makedirs(upload_dir, exist_ok=True)


def make_cpp_header(meta_map):
    header_string = ""
    meta_keys = meta_map.keys()
    for key in meta_keys:
        header_string += f"#define {PARAMETER_MAP.get(key)} {meta_map.get(key)}\n"
    return header_string


def build_model_server(build_id, model_type):
    print(build_id)
    if model_type == "dnn":
        subprocess.call("./build.sh")
    else:
        subprocess.call("./build.sh")
