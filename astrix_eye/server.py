from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from concurrent.futures import ThreadPoolExecutor
from ultralytics import YOLO
import numpy as np
import cv2
import base64
import os

# --------------------------------------------------------------------
# MODEL SETUP
# --------------------------------------------------------------------
HERE = os.path.dirname(os.path.abspath(__file__))
WEIGHTS = os.path.join(os.path.dirname(HERE), "weights")
# First existing file wins. The last name in each list is an Ultralytics
# filename that downloads itself when the local weights are missing.
MODEL_CANDIDATES = {
    "general": ["yolov8m.pt", "yolov8n.pt"],
    "visdrone": ["visdrone.pt", "yolov8n_visdrone.pt"],
    "drone": ["drone.pt"],
    "weapon": ["weapon.pt", "best3.pt"],
}
_models = {}


def resolve_model_path(key):
    names = MODEL_CANDIDATES[key]
    for folder in (WEIGHTS, HERE):
        for name in names:
            path = os.path.join(folder, name)
            if os.path.isfile(path):
                return path
    return names[-1]


def get_model(key):
    if key not in _models:
        _models[key] = YOLO(resolve_model_path(key))
    return _models[key]


# --------------------------------------------------------------------
# FASTAPI APP
# --------------------------------------------------------------------
app = FastAPI(title="ASTRIX EYE - Multi-Model + Source Selection")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

executor = ThreadPoolExecutor(max_workers=4)

# --------------------------------------------------------------------
# FRONTEND INTERFACE
# --------------------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
@app.get("/ui", response_class=HTMLResponse)
def home_ui():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>ASTRIX EYE - Detection</title>
        <style>
            body { background:#0a0e14; color:#e6edf3; text-align:center; font-family:Segoe UI, Arial, sans-serif; }
            h1 { color:#22d3ee; letter-spacing:0.06em; margin-bottom:0.25em; }
            h3 { color:#8b98a9; font-weight:normal; }
            select,button,input { padding:10px; border-radius:8px; margin:5px; font-weight:bold; background:#161f2e; color:#e6edf3; border:1px solid #1f2a3c; }
            video,canvas,img { border:2px solid #22d3ee; border-radius:10px; width:80%; margin-top:10px; background:#000; }
            button.start { background:#10b981; border:none; color:white; }
            button.stop { background:#ef4444; border:none; color:white; }
        </style>
    </head>
    <body>
        <h1>◉ ASTRIX EYE</h1>
        <h3>Multi-Model Real-time Detection Control Panel</h3>

        <label>Select Model:</label>
        <select id="model">
            <option value="general">General (YOLOv8)</option>
            <option value="visdrone">Human & Vehicle (VisDrone)</option>
            <option value="drone">Drone Detection</option>
            <option value="weapon">Weapon Detection</option>
        </select><br>

        <label>Select Source:</label>
        <select id="source">
            <option value="camera">Device Camera</option>
            <option value="upload">Upload Video/Image</option>
        </select><br>

        <input type="file" id="fileInput" accept="video/*,image/*" style="display:none"><br>

        <video id="video" autoplay playsinline style="display:none"></video>
        <canvas id="canvas"></canvas><br>

        <button id="startBtn" class="start">Start Detection</button>
        <button id="stopBtn" class="stop">Stop Detection</button>

        <script>
            const video=document.getElementById('video');
            const canvas=document.getElementById('canvas');
            const startBtn=document.getElementById('startBtn');
            const stopBtn=document.getElementById('stopBtn');
            const modelSelect=document.getElementById('model');
            const sourceSelect=document.getElementById('source');
            const fileInput=document.getElementById('fileInput');
            let stream,interval;

            sourceSelect.onchange=()=>{
                if(sourceSelect.value==="camera"){
                    fileInput.style.display="none";
                    video.style.display="block";
                }else{
                    fileInput.style.display="block";
                    video.style.display="none";
                }
            };

            startBtn.onclick=async()=>{
                if(sourceSelect.value==="camera"){
                    try{
                        stream=await navigator.mediaDevices.getUserMedia({video:true});
                        video.srcObject=stream;
                        const ctx=canvas.getContext('2d');
                        interval=setInterval(async()=>{
                            ctx.drawImage(video,0,0,canvas.width=video.videoWidth,canvas.height=video.videoHeight);
                            canvas.toBlob(async(blob)=>{
                                const formData=new FormData();
                                formData.append("file",blob,"frame.jpg");
                                formData.append("model_type",modelSelect.value);
                                const res=await fetch("/detect_frame",{method:"POST",body:formData});
                                const data=await res.json();
                                const img=new Image();
                                img.src="data:image/jpeg;base64,"+data.processed_frame;
                                img.onload=()=>ctx.drawImage(img,0,0,canvas.width,canvas.height);
                            },"image/jpeg");
                        },700);
                    }catch(e){alert("Camera error: "+e);}
                }else{
                    const file=fileInput.files[0];
                    if(!file){alert("Select a file first!");return;}
                    const formData=new FormData();
                    formData.append("file",file);
                    formData.append("model_type",modelSelect.value);
                    const res=await fetch("/detect_file",{method:"POST",body:formData});
                    const data=await res.json();
                    const img=new Image();
                    img.src="data:image/jpeg;base64,"+data.processed_frame;
                    img.onload=()=>canvas.getContext('2d').drawImage(img,0,0,canvas.width,img.height*canvas.width/img.width);
                }
            };

            stopBtn.onclick=()=>{
                if(stream){stream.getTracks().forEach(t=>t.stop());clearInterval(interval);}
            };
        </script>
    </body>
    </html>
    """
    return HTMLResponse(html)

# --------------------------------------------------------------------
# DETECTION - CAMERA FRAME
# --------------------------------------------------------------------
@app.post("/detect")
@app.post("/detect_frame")
async def detect_frame(file: UploadFile = File(...), model_type: str = Form("general")):
    content = await file.read()
    img = cv2.imdecode(np.frombuffer(content, np.uint8), cv2.IMREAD_COLOR)
    result = executor.submit(run_detection, img, model_type).result()
    return JSONResponse({"processed_frame": result})

# --------------------------------------------------------------------
# DETECTION - IMAGE/VIDEO FILE
# --------------------------------------------------------------------
@app.post("/detect_file")
async def detect_file(file: UploadFile = File(...), model_type: str = Form("general")):
    filename = file.filename
    ext = os.path.splitext(filename)[1].lower()
    content = await file.read()

    if not content or len(content) < 10:
        return JSONResponse({"error": f"File {filename} is empty or corrupted"})

    np_data = np.frombuffer(content, np.uint8)
    print(f"[INFO] Received file: {filename} ({len(content)/1024:.2f} KB), Model: {model_type}")

    # 🔹 Handle image files
    if ext in [".jpg", ".jpeg", ".png"]:
        img = cv2.imdecode(np_data, cv2.IMREAD_COLOR)
        if img is None:
            return JSONResponse({"error": "Invalid image data"})
        result = executor.submit(run_detection, img, model_type).result()
        return JSONResponse({"processed_frame": result})

    # 🔹 Handle video files
    elif ext in [".mp4", ".mov", ".avi", ".mkv"]:
        tmp_path = "temp_video.mp4"
        with open(tmp_path, "wb") as f:
            f.write(content)

        cap = cv2.VideoCapture(tmp_path)
        ret, frame = cap.read()
        cap.release()

        if not ret or frame is None:
            os.remove(tmp_path)
            return JSONResponse({"error": "Video read error — invalid or unsupported file"})

        result = executor.submit(run_detection, frame, model_type).result()
        os.remove(tmp_path)
        return JSONResponse({"processed_frame": result})

    # 🔹 Unsupported file type
    else:
        return JSONResponse({"error": f"Unsupported file type: {ext}"})
# --------------------------------------------------------------------
# DETECTION CORE
# --------------------------------------------------------------------
def run_detection(frame, model_type):
    if model_type not in MODEL_FILES:
        print(f"[WARN] Unknown model type received: {model_type}, using default 'general'")
        model_type = "general"
    model = get_model(model_type)
    results = model(frame, verbose=False)
    annotated = results[0].plot()
    _, buffer = cv2.imencode(".jpg", annotated)
    return base64.b64encode(buffer).decode("utf-8")




# --------------------------------------------------------------------
# HEALTH CHECK
# --------------------------------------------------------------------
@app.get("/status")
def status():
    return {
        "name": "ASTRIX EYE",
        "status": "running",
        "models": list(MODEL_FILES.keys()),
        "sources": ["camera", "upload"],
    }
