from PIL import ImageDraw

def draw_yolo_boxes(img, results, class_map):
    draw = ImageDraw.Draw(img)

    for box in results[0].boxes:
        x1,y1,x2,y2 = box.xyxy[0]
        cls = int(box.cls)
        conf = float(box.conf)

        label = f"{class_map.get(cls,'Class_'+str(cls))} {conf:.2f}"

        draw.rectangle([x1,y1,x2,y2], outline="lime", width=4)
        draw.text((x1, y1), label, fill="white")

    return img
