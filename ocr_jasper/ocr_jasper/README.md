# Jasper_OCR 验证码识别

## PART 1: OCR 识别


```python
import ocr_jasper

ocr = ocr_jasper.OCR()

with open("test.jpg", 'rb') as f:
    image = f.read()

res = ocr.classification(image)
print(res)
``` 
由于事实上确实在一些图片上老版本的模型识别效果比新模型好，老模型也在其中，通过在初始化 ocr_jasper 的时候使用 old 参数即可快速切换老模型

```python
import ocr_jasper

ocr = ocr_jasper.OCR(old=True)

with open("test.jpg", 'rb') as f:
    image = f.read()

res = ocr.classification(image)
print(res)
``` 


## PART 2: 目标检测
  

```python
import ocr_jasper
import cv2

det = ocr_jasper.OCR(det=True)

with open("test.jpg", 'rb') as f:
    image = f.read()

poses = det.detection(image)
print(poses)

im = cv2.imread("test.jpg")

for box in poses:
    x1, y1, x2, y2 = box
    im = cv2.rectangle(im, (x1, y1), (x2, y2), color=(0, 0, 255), thickness=2)

cv2.imwrite("result.jpg", im)

```

# 安装

## 环境支持

`python <= 3.9`

`Windows/Linux/Macos..`

暂时不支持Macbook M1(X)，M1(X)用户需要自己编译 onnxruntime 才可以使用

## 安装命令

`pip install {oocr_jasper 文件夹路径}`


