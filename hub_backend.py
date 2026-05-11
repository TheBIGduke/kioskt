# Created by Kaléin Tamaríz
import os
import hashlib
import subprocess
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

app = FastAPI()

def get_dynamic_apps():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    apps_dir = os.path.join(base_dir, "apps")
    if not os.path.exists(apps_dir):
        return {}
    
    apps = {}
    for item in sorted(os.listdir(apps_dir)):
        item_path = os.path.join(apps_dir, item)
        if os.path.isdir(item_path):
            hash_val = int(hashlib.md5(item.encode()).hexdigest(), 16)
            port = 3000 + (hash_val % 5000)
            
            # Support for fixed port overrides via port.txt
            port_file = os.path.join(item_path, "port.txt")
            if os.path.exists(port_file):
                try:
                    with open(port_file, "r") as f:
                        port = int(f.read().strip())
                except:
                    pass

            app_config = {
                "id": item,
                "name": item.replace("_", " ").title(),
                "type": "web",
                "port": port,
                "pm2_name": f"app-{item}",
                "script": "python3", 
                "cwd": item_path,
                "args": ["--", "-m", "http.server", str(port)]
            }

            deploy_dir = os.path.join(item_path, "deploy")
            if os.path.exists(deploy_dir) and os.path.isdir(deploy_dir):
                sh_files = [f for f in os.listdir(deploy_dir) if f.endswith('.sh')]
                if sh_files:
                    app_config["script"] = os.path.join("deploy", sh_files[0])
                    app_config["args"] = []

            url_file = os.path.join(item_path, "url.txt")
            if os.path.exists(url_file):
                with open(url_file, "r") as f:
                    app_config["type"] = "url"
                    app_config["url"] = f.read().strip()

            type_file = os.path.join(item_path, "type.txt")
            if os.path.exists(type_file):
                with open(type_file, "r") as f:
                    app_config["type"] = f.read().strip()

            apps[item] = app_config
    return apps

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_hub():
    return FileResponse("static/index.html")

@app.get("/api/apps")
async def list_apps():
    return JSONResponse(get_dynamic_apps())

@app.post("/api/start/{app_id}")
async def start_app(app_id: str):
    apps = get_dynamic_apps()
    if app_id not in apps:
        raise HTTPException(status_code=404, detail="App not found")

    app_data = apps[app_id]

    if app_data.get("type") == "url":
        return {"status": "success", "app_info": app_data}

    check_cmd = ["pm2", "describe", app_data["pm2_name"]]
    check_result = subprocess.run(check_cmd, capture_output=True)

    if check_result.returncode == 0:
        cmd = ["pm2", "restart", app_data["pm2_name"]]
    else:
        cmd = [
            "pm2", "start", app_data["script"],
            "--name", app_data["pm2_name"],
            "--cwd", app_data["cwd"]
        ]
        if app_data["script"].endswith(".sh"):
            cmd += ["--interpreter", "bash"]
        if app_data.get("args"):
            cmd.extend(app_data["args"])
            
    subprocess.run(cmd, capture_output=True)
    return {"status": "success", "app_info": app_data}

@app.post("/api/stop/{app_id}")
async def stop_app(app_id: str):
    apps = get_dynamic_apps()
    if app_id not in apps:
        raise HTTPException(status_code=404, detail="App not found")

    app_data = apps[app_id]
    if app_data.get("type") != "url":
        subprocess.run(["pm2", "stop", app_data["pm2_name"]], check=True)
    return {"status": "success"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=9019)