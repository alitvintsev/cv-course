import random
import cv2
########## Constants ##################
annotations_path = '../data/dataset/annotations' # Путь к файлам разметки
images_path = '../data/dataset/images' # Путь к изображениям
BOX_COLOR = (255, 0, 255) # фиолетовый цвет - boundingboxes не аугментированного изображения
TEXT_COLOR = (255, 255, 255) # белый цвет -  текст
classnames = {'0':'car', '1':'plate'}
AUG_BOX_COLOR = (0, 0, 255) # синий цвет - boundingboxes аугментированного изображения
debug = True # флаг отладки
#######################################

#######################################
# Добавляем случайное зерно для воспроизврдимости
# генерации при использовании albumentations
random.seed(42) 

# Функция преобразования координат из формата YOLO в формат PASCAL VOC (для простоты отображения boundingboxes)
def convert_from_yolo(xcenter_normalized, ycenter_normalized, width_normalized, height_normalized, frame_width, frame_height):
    xmin = int((float(xcenter_normalized) - (float(width_normalized)/2))*frame_width)
    ymin = int((float(ycenter_normalized) - (float(height_normalized)/2))*frame_height)
    xmax = int((float(xcenter_normalized) + (float(width_normalized)/2))*frame_width)
    ymax = int((float(ycenter_normalized) + (float(height_normalized)/2))*frame_height)
    return (xmin, ymin, xmax, ymax)

# Функция визуализации одного boundingbox
def visualize_bbox(image, bbox, class_name, color=BOX_COLOR, thickness=2):
    # Получаем координаты boundingbox
    xmin, ymin, xmax, ymax = list(map(int, bbox))
   
    # Нанесение прямоугольника на изображение
    cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color=color, thickness=thickness)
    
    # Нанесение имени класса
    ((text_width, text_height), _) = cv2.getTextSize(class_name, cv2.FONT_HERSHEY_SIMPLEX, 0.35, 1)    
    cv2.rectangle(image, (xmin, ymin - int(1.3 * text_height)), (xmin + text_width, ymin), color, -1)
    cv2.putText(
        image,
        text=class_name,
        org=(xmin, ymin - int(0.3 * text_height)),
        fontFace=cv2.FONT_HERSHEY_SIMPLEX,
        fontScale=0.35, 
        color=TEXT_COLOR, 
        lineType=cv2.LINE_AA,
    )
    return image