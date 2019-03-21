#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import subprocess
import json
import time
import requests


def download_github_code(path):
    filename = path.rsplit("/")[-1]
    os.system("shred -u {}".format(filename))
    os.system("wget https://raw.githubusercontent.com/ZEMUSHKA/skillfactory-dl/master/{} -O {}".format(path, filename))


def setup_common():
    os.system("pip install --force https://github.com/ZEMUSHKA/skillfactory-dl/releases/download/TqdmColab/tqdm-colab.zip")


def download_flowers():
    print("Downloading 102flowers.tgz...")
    os.system("wget https://github.com/ZEMUSHKA/skillfactory-dl/releases/download/Flowers/102flowers.tgz")
    print("Downloading imagelabels.mat...")
    os.system("wget https://github.com/ZEMUSHKA/skillfactory-dl/releases/download/Flowers/imagelabels.mat")


def _get_ngrok_tunnel():
    while True:
        try:
            tunnels_json = requests.get("http://localhost:4040/api/tunnels").content
            public_url = json.loads(tunnels_json)['tunnels'][0]['public_url']
            return public_url
        except Exception:
            print("Can't get public url, retrying...")
            time.sleep(2)


def _warmup_ngrok_tunnel(public_url):
    while requests.get(public_url).status_code >= 500:
        print("Tunnel is not ready, retrying...")
        time.sleep(2)


def expose_port_on_colab(port):
    os.system("apt-get install net-tools")
    # check that port is open
    while not (":{} ".format(port) in str(subprocess.check_output("netstat -vatn", shell=True))):
        print("Port {} is closed, retrying...".format(port))
        time.sleep(2)

    # run ngrok
    os.system("wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip")
    os.system("unzip ngrok-stable-linux-amd64.zip")
    os.system("./ngrok http {0} &".format(port))
    public_url = _get_ngrok_tunnel()
    _warmup_ngrok_tunnel(public_url)

    print("Open {0} to access your {1} port".format(public_url, port))
