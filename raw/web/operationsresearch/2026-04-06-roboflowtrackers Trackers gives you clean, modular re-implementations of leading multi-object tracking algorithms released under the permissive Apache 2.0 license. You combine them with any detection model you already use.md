---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: Trackers gives you clean, modular re-implementations of leading multi-object
  tracking algorithms released under the permissive Apache 2.0 license. You combine
  them with any detection model you already use. - roboflow/trackers
source_type: web
status: inbox
tags:
- null
- clippings
title: 'roboflow/trackers: Trackers gives you clean, modular re-implementations of
  leading multi-object tracking algorithms released under the permissive Apache 2.0
  license. You combine them with any detection model you already use.'
topics:
- 运筹优化
source_url: https://github.com/roboflow/trackers
published_at: null
related_concepts: []
---

trackers-2.0.0-promo.mp4<video src="https://private-user-images.githubusercontent.com/26109316/436954118-eef9b00a-cfe4-40f7-a495-954550e3ef1f.mp4?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzU0NjU0ODgsIm5iZiI6MTc3NTQ2NTE4OCwicGF0aCI6Ii8yNjEwOTMxNi80MzY5NTQxMTgtZWVmOWIwMGEtY2ZlNC00MGY3LWE0OTUtOTU0NTUwZTNlZjFmLm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA0MDYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNDA2VDA4NDYyOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWM5ODk1MjYwOTNmZTIyMDAxZmZjM2E2ODg0MDc0MWQ3MTY2YjM4YjRlNTlkMWQzODAyNDBlZDkxODc0MTE0YjcmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.w0gocscKxViwSni1eVlNiYPzNeHVarIbs_k9xflMrs0" controls="controls"></video>

## Install

```
pip install trackers
```
Install from source
```
pip install git+https://github.com/roboflow/trackers.git
```

For more options, see the [install guide](https://trackers.roboflow.com/develop/learn/install/).

[![[Image 29.png|Watch: Building Real-Time Multi-Object Tracking with RF-DETR and Trackers]]](https://www.youtube.com/watch?v=u0k2dTZ0vfs)

## Track from CLI

Point at a video, webcam, RTSP stream, or image directory. Get tracked output.

```
trackers track \
    --source video.mp4 \
    --output output.mp4 \
    --model rfdetr-medium \
    --tracker bytetrack \
    --show-labels \
    --show-trajectories
```

For all CLI options, see the [tracking guide](https://trackers.roboflow.com/develop/learn/track/).

## Track from Python

Plug trackers into your existing detection pipeline. Works with any detector.

```
import cv2
import supervision as sv
from inference import get_model
from trackers import ByteTrackTracker

model = get_model(model_id="rfdetr-medium")
tracker = ByteTrackTracker()

cap = cv2.VideoCapture("video.mp4")
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    result = model.infer(frame)[0]
    detections = sv.Detections.from_inference(result)
    tracked = tracker.update(detections)
```

For more examples, see the [tracking guide](https://trackers.roboflow.com/develop/learn/track/).

trackers-2.3.0-promo-1.mp4<video src="https://private-user-images.githubusercontent.com/26109316/564687439-d2347a25-469d-44cd-8049-d15274bd91ae.mp4?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzU0NjU0ODgsIm5iZiI6MTc3NTQ2NTE4OCwicGF0aCI6Ii8yNjEwOTMxNi81NjQ2ODc0MzktZDIzNDdhMjUtNDY5ZC00NGNkLTgwNDktZDE1Mjc0YmQ5MWFlLm1wND9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA0MDYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNDA2VDA4NDYyOFomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWVmODQ5YjY5NmI0NmI3ZmFkMmQzNjVjY2RjZDhiZDc1Y2NiMzJiMmQ4MmFlYjg0YmI1MzE5NWUxZWIwN2Y4ZDUmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.P6Q3PC9xssXftjeM2IJquhMDBLY8fDEeJf_43kzBMBM" controls="controls"></video>

## Algorithms

Clean, modular implementations of leading trackers. All HOTA scores use default parameters.

| Algorithm | Description | MOT17 HOTA | SportsMOT HOTA | SoccerNet HOTA | DanceTrack HOTA |
| --- | --- | --- | --- | --- | --- |
| [SORT](https://arxiv.org/abs/1602.00763) | Kalman filter + Hungarian matching baseline. | 58.4 | 70.9 | 81.6 | 45.0 |
| [ByteTrack](https://arxiv.org/abs/2110.06864) | Two-stage association using high and low confidence detections. | 60.1 | **73.0** | **84.0** | 50.2 |
| [OC-SORT](https://arxiv.org/abs/2203.14360) | Observation-centric recovery for lost tracks. | **61.9** | 71.7 | 78.4 | **51.8** |

For detailed benchmarks and tuned configurations, see the [tracker comparison](https://trackers.roboflow.com/develop/trackers/comparison/).

## Evaluate

Benchmark your tracker against ground truth with standard MOT metrics.

```
trackers eval \
    --gt-dir ./data/mot17/val \
    --tracker-dir results \
    --metrics CLEAR HOTA Identity \
    --columns MOTA HOTA IDF1
```

```
Sequence                        MOTA    HOTA    IDF1
----------------------------------------------------
MOT17-02-FRCNN                30.192  35.475  38.515
MOT17-04-FRCNN                48.912  55.096  61.854
MOT17-05-FRCNN                52.755  45.515  55.705
MOT17-09-FRCNN                51.441  50.108  57.038
MOT17-10-FRCNN                51.832  49.648  55.797
MOT17-11-FRCNN                55.501  49.401  55.061
MOT17-13-FRCNN                60.488  58.651  69.884
----------------------------------------------------
COMBINED                      47.406  50.355  56.600
```

For the full evaluation workflow, see the [evaluation guide](https://trackers.roboflow.com/develop/learn/evaluate/).

## Download Datasets

Pull benchmark datasets for evaluation with a single command.

```
trackers download mot17 \
    --split val \
    --asset annotations,detections
```

| Dataset | Description | Splits | Assets | License |
| --- | --- | --- | --- | --- |
| `mot17` | Pedestrian tracking with crowded scenes and frequent occlusions. | `train`, `val`, `test` | `frames`, `annotations`, `detections` | CC BY-NC-SA 3.0 |
| `sportsmot` | Sports broadcast tracking with fast motion and similar-looking targets. | `train`, `val`, `test` | `frames`, `annotations` | CC BY 4.0 |