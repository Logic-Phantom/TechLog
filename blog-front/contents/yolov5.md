---
date: '2025-05-15'
title: 'YOLOv5를 활용한 객체 탐지'
categories: ['AI', 'Computer Vision']
summary: 'YOLOv5를 사용한 이미지 객체 탐지와 데이터 변환 과정'
thumbnail: './images/AI/ai.jpg'
comments: true
---

# YOLOv5를 활용한 이미지 객체 탐지 및 데이터 변환

## YOLOv5 소개

YOLO(You Only Look Once)는 실시간 객체 탐지(Object Detection)를 위한 최첨단 딥러닝 모델입니다. YOLOv5는 Ultralytics에서 개발한 YOLO 시리즈의 5번째 버전으로, 이전 버전들의 장점을 계승하면서 성능과 사용성을 크게 개선했습니다.

### YOLOv5의 주요 특징

1. **빠른 처리 속도**
   - 실시간 객체 탐지가 가능한 빠른 추론 속도
   - GPU 및 CPU 환경 모두에서 효율적인 성능

2. **높은 정확도**
   - 다양한 객체 크기에 대한 우수한 탐지 성능
   - 복잡한 장면에서도 안정적인 객체 인식

3. **사용 편의성**
   - PyTorch 기반으로 구현되어 사용이 쉬움
   - 풍부한 문서와 커뮤니티 지원
   - 다양한 export 형식 지원 (ONNX, TensorRT 등)

4. **다양한 모델 크기**
   - YOLOv5n (nano): 가장 작은 모델
   - YOLOv5s (small): 작은 모델
   - YOLOv5m (medium): 중간 크기 모델
   - YOLOv5l (large): 큰 모델
   - YOLOv5x (xlarge): 가장 큰 모델

## 객체 탐지 워크플로우

### 1. 이미지 객체 탐지

```python
import torch

# YOLOv5 모델 로드
model = torch.hub.load('ultralytics/yolov5', 'yolov5s')

# 이미지에서 객체 탐지
results = model('image.jpg')

# 결과 추출
detections = results.pandas().xyxy[0]  # 바운딩 박스 좌표
```

### 2. JSON 데이터 생성

탐지된 객체 정보를 JSON 형식으로 변환하는 예시:

```python
import json

def create_detection_json(detections):
    json_data = {
        "objects": []
    }
    
    for _, detection in detections.iterrows():
        object_info = {
            "class": detection["name"],
            "confidence": float(detection["confidence"]),
            "bbox": {
                "xmin": float(detection["xmin"]),
                "ymin": float(detection["ymin"]),
                "xmax": float(detection["xmax"]),
                "ymax": float(detection["ymax"])
            }
        }
        json_data["objects"].append(object_info)
    
    return json_data
```

### 3. XML 변환

JSON 데이터를 XML 형식으로 변환하는 예시:

```python
import dicttoxml
from xml.dom.minidom import parseString

def json_to_xml(json_data):
    xml = dicttoxml.dicttoxml(json_data)
    dom = parseString(xml)
    return dom.toprettyxml()
```

## 프로젝트 구현 목표

1. **이미지 객체 탐지**
   - YOLOv5를 사용하여 이미지에서 객체 탐지
   - 객체의 위치(바운딩 박스)와 클래스 정보 추출

2. **데이터 구조화**
   - 탐지된 객체 정보를 JSON 형식으로 구조화
   - 객체별 클래스, 신뢰도, 위치 정보 포함

3. **데이터 형식 변환**
   - JSON 데이터를 XML 형식으로 변환
   - 표준 XML 형식 준수

4. **결과 활용**
   - 변환된 XML 데이터를 다른 시스템과 연동
   - 데이터 분석 및 시각화에 활용

## 기대 효과

1. **자동화된 객체 탐지**
   - 수동 라벨링 작업 최소화
   - 처리 시간 단축

2. **데이터 호환성**
   - JSON과 XML 형식 지원으로 다양한 시스템과 연동 가능
   - 표준화된 데이터 형식 사용

3. **확장성**
   - 다양한 객체 탐지 시나리오에 적용 가능
   - 새로운 객체 클래스 추가 용이

## 참고 자료

- [YOLOv5 GitHub Repository](https://github.com/ultralytics/yolov5)
- [YOLOv5 Documentation](https://docs.ultralytics.com/)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html) 