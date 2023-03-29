import bpy
import numpy as np
import time
import math
from os import listdir, mkdir, getcwd
import random
import uuid
import argparse


# Получение имени изображения 
# и файлов разметки(должно быть одинаковым)
def get_name():
    return f"{str(uuid.uuid4()).replace('-','')}_frame_"

def set_basepath_to_output_file():
    # set own filename for each image file
    file_output_nodes = find_nodes_byname("File Output")
    for file_output_node in file_output_nodes:
        if file_output_node.label == "image":
            file_output_node.base_path = f"{getcwd()}/dataset/images"
        elif file_output_node.label == "car": 
            file_output_node.base_path = f"{getcwd()}/dataset/masks/car"
        elif file_output_node.label == "license_plate": 
            file_output_node.base_path = f"{getcwd()}/dataset/masks/license_plate"

# Выставление одинакового имени файлов для всех
# узлов File Output в Compositing
def set_name_to_output_file(filename):
    # set own filename for each image file
    file_output_nodes = find_nodes_byname("File Output")
    for file_output_node in file_output_nodes:
        file_output_node.file_slots[0].path = filename
        if file_output_node.label == "image":
            file_output_node.base_path = f"{getcwd()}/dataset/images"
        elif file_output_node.label == "car": 
            file_output_node.base_path = f"{getcwd()}/dataset/masks/car"
        elif file_output_node.label == "license_plate": 
            file_output_node.base_path = f"{getcwd()}/dataset/masks/license_plate"

# Поиск узла в Compositing по имени
def find_nodes_byname(node_name:str) -> list:
    result_nodes = []
    bpy.context.scene.use_nodes = True 
    tree = bpy.context.scene.node_tree.nodes
    image_node = None
    for node in tree:
        if node.bl_label == node_name:
            result_nodes.append(node)
    return result_nodes

# Функция рендеринга. Выставляет параметры рендеринга и
# производит рендеринг с прогонкой через граф Compositing
# и сохранением всех файлов изображений
def render(**kwargs):
    # Получение объектов сцены и рендера
    render = bpy.context.scene.render
    scene = bpy.context.scene
    # Параметры сглаживания шума создаваемого рендером
    scene.cycles.use_denoising = True
    scene.cycles.denoiser = 'OPTIX'
    scene.cycles.preview_denoising_input_passes = 'RGB_ALBEDO'
    # Качество рендеринга - чем выше тем дольше рендер одного изображений и выше качество
    scene.cycles.samples = kwargs['quality'] if 'quality' in kwargs else 32



    # Имя и путь к файлу изобраения генерируемого по умолчанию
    render.filepath = f'{getcwd()}/test_image'
    # Рендер CYCLES - более реалистичное качество чем Evee
    render.engine = 'CYCLES'
    # Параметры для работы с CUDA
    scene.cycles.device = 'GPU'
    # Разрешение изображений
    render.resolution_x = 1920
    render.resolution_y = 1080
    # Параметр прозрачности при рендере фона, для png формата и работой с альфа каналом в Compositing
    render.film_transparent = True
    # Создание нового имени файла 
    set_name_to_output_file(get_name())
    
    # Запуск рендеринга
    if 'layer' in kwargs:
        bpy.ops.render.render(write_still=True, layer=kwargs['layer'])
    else:
        bpy.ops.render.render(write_still=True)
    print('Rendering has completed')

# Перемещение и вращение камеры на случайное расстояние и угол
def move_camera():
    # Перемещение камеры по оси X
    bpy.data.objects["Camera"].location[0] = random.uniform(6.06, 8.82)
    # Перемещение камеры по оси Y
    bpy.data.objects["Camera"].location[1] = random.uniform(-12.0, 0.78)
    # Перемещение камеры по оси Z
    bpy.data.objects["Camera"].location[2] = random.uniform(8.54, 12.74)
    # Поворот камеры вокруг оси X
    bpy.data.objects["Camera"].rotation_euler[0] = math.radians(random.uniform(44.5, 72.2))
    # Поворот камеры вокруг оси Z
    bpy.data.objects["Camera"].rotation_euler[2] = math.radians(random.uniform(24, 43))

if __name__ == "__main__":
    # Количество синтезируемых изображений
    images_count = 3
    set_basepath_to_output_file()
    for index in range(images_count):
        print(f"====== Start synthesis image number {index + 1} =====")
        move_camera()
        render(**{'quality':10})

