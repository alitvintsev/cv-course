def convert_to_pascal_voc(xmin: int, ymin: int, width: int, height: int)-> tuple:
    xmax = xmin + width
    ymax = ymin + height
    return (xmin, ymin, xmax, ymax)

def convert_to_albumentation(xmin: int, ymin: int, width: int, height: int, frame_width: int, frame_height: int)-> tuple:
    xmin_normalized = xmin/frame_width
    ymin_normalized = ymin/frame_height
    xmax_normalized = (xmin + width)/frame_width
    ymax_normalized = (ymin + height)/frame_height
    return (xmin_normalized, ymin_normalized, xmax_normalized, ymax_normalized)

def convert_to_yolo(xmin: int, ymin: int, width: int, height: int, frame_width: int, frame_height: int)-> tuple:
    xcenter_normalized = (xmin + width/2)/frame_width
    ycenter_normalized = (ymin + height/2)/frame_height
    width_normalized = width/frame_width
    height_normalized = height/frame_height
    return (xcenter_normalized, ycenter_normalized, width_normalized, height_normalized)