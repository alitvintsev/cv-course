import random
import albumentations as A

__all__ = ["tpascal", "talbum", "tyolo", "talbumc"]

def pascal_solver(x, y, w, h):
    return (x, y, x + w, y + h)

def album_solver(x, y, w, h, fw, fh):
    xn = x/fw
    yn = y/fh
    xmn = (x + w)/fw
    ymn = (y + h)/fh
    return (xn, yn, xmn, ymn)

def yolo_solver(x, y, w, h, fw, fh):
    xcn = (x + w/2)/fw
    ycn = (y + h/2)/fh
    wn = w/fw
    hn = h/fh
    return (xcn, ycn, wn, hn)
    
def tpascal(func, **kwargs):
    fw = random.randint(0, 1280)
    fh = random.randint(0, 720)
    x = random.randint(0, fw-2)
    y = random.randint(0, fh-2)
    w = random.randint(0, fw - x) 
    h = random.randint(0, fh - y)
    
    try:
        xmin, ymin, xmax, ymax = func(x, y, w, h)
    except Exception as e:
        print(f"Ошибка выполнения convert_to_pascal_voc: {e}")

    xrmin, yrmin, xrmax, yrmax = pascal_solver(x, y, w, h)
    assert xmin == xrmin, "convert_to_pascal_voc: Неправильный возврат xmin"
    assert ymin == yrmin, "convert_to_pascal_voc: Неправильный возврат ymin"
    assert xmax == xrmax, "convert_to_pascal_voc: Неправильный возврат xmax"
    assert ymax == yrmax, "convert_to_pascal_voc: Неправильный возврат ymax"
    return func

def talbum(func, **kwargs):
    fw = random.randint(0, 1280)
    fh = random.randint(0, 720)
    x = random.randint(0, fw-2)
    y = random.randint(0, fh-2)
    w = random.randint(0, fw - x) 
    h = random.randint(0, fh - y)
    
    try:
        xmin, ymin, xmax, ymax = func(x, y, w, h, fw, fh)
    except Exception as e:
        print(f"Ошибка выполнения convert_to_albumentation: {e}")

    xrmin, yrmin, xrmax, yrmax = album_solver(x, y, w, h, fw, fh)
    assert xmin <= 1, "Xmin не отнормировано к 1"
    assert ymin <= 1, "Ymin не отнормировано к 1"
    assert xmax <= 1, "Xmax не отнормировано к 1"
    assert ymax <= 1, "Ymax не отнормировано к 1"
    assert xmin == xrmin, "Неправильный возврат xmin"
    assert ymin == yrmin, "Неправильный возврат ymin"
    assert xmax == xrmax, "Неправильный возврат xmax"
    assert ymax == yrmax, "Неправильный возврат ymax"
    return func

def tyolo(func, **kwargs):
    fw = random.randint(0, 1280)
    fh = random.randint(0, 720)
    x = random.randint(0, fw-2)
    y = random.randint(0, fh-2)
    w = random.randint(0, fw - x) 
    h = random.randint(0, fh - y)
    
    try:
        xcenter, ycenter, width, height = func(x, y, w, h, fw, fh)
    except Exception as e:
        print(f"Ошибка выполнения convert_to_yolo: {e}")

    xrcenter, yrcenter, rwidth, rheight = yolo_solver(x, y, w, h, fw, fh)
    assert xcenter <= 1, "Xcenter не отнормировано к 1"
    assert ycenter <= 1, "Ycenter не отнормировано к 1"
    assert width <= 1, "Width не отнормировано к 1"
    assert height <= 1, "Height не отнормировано к 1"
    assert xcenter == xrcenter, "Неправильный возврат xcenter"
    assert ycenter == yrcenter, "Неправильный возврат ycenter"
    assert width == rwidth, "Неправильный возврат width"
    assert height == rheight, "Неправильный возврат height"
    return func

def talbumc(func, **kwargs):
    try:
        transform = func()
    except Exception as e:
        print(f"Ошибка выполнения get_album_pipeline: {e}")
        
    assert type(transform) == A.Compose, "Ответ функции get_album_pipeline не соответствует типу albumentations.Compose"
    return func