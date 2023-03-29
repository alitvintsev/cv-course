import ipywidgets as widgets
import albumentations as A
from matplotlib import pyplot as plt
import ipyplot
import numpy as np


class AugmentatorOption():
    def __init__(self, option_name: str, option_description: str, step:[int, float], min_val: [int, float], max_val: [int, float], default: [int, float], 
                 readout_format: str='.2f', image_path=""):
        self.__label = widgets.Label(value=option_description)
        self.__type = type(min_val)
        self.__name = option_name
        if self.__type==float:
            self.__slider = widgets.FloatSlider(
                                                    value=default,
                                                    min=min_val,
                                                    max=max_val,
                                                    step=step,
                                                    description='',
                                                    disabled=False,
                                                    continuous_update=True,
                                                    orientation='horizontal',
                                                    readout=True,
                                                    readout_format=readout_format,
                                                    layout=widgets.Layout(width="170px"),
                                                    style={'handle_color': 'lightblue'}
                                                )
            
        else:
            self.__slider = widgets.IntSlider(
                                                value=default,
                                                min=min_val,
                                                max=max_val,
                                                step=step,
                                                description='',
                                                disabled=False,
                                                continuous_update=True,
                                                orientation='horizontal',
                                                readout=True,
                                                readout_format='d',
                                                layout=widgets.Layout(width="170px"),
                                                style={'handle_color': 'lightblue'}
                                            )
        self.__slider.name = option_name
        self.__label.name = ""
    
    
    def __call__(self):
        return [self.__label, self.__slider]
    
    @property
    def name(self):
        return self.__name
    

class Augmentator():
    def __init__(self, name: str, options: dict, augmentation):
        self.__checkbox = widgets.Checkbox(
                                                value=False,
                                                description=name,
                                                disabled=False,
                                                indent=False,
                                                layout=widgets.Layout(width="130px")
                                          )
        self.__checkbox.name = ""
        self.__options = options
        self.__augmentation = augmentation
        self.__widget = None
        self.__check_digits = "0123456789"
    
    def __call__(self):
        hbox=[self.__checkbox]
        for option_name, option in self.__options.items():
            hbox.extend(option())
        self.__widget = widgets.HBox(hbox)
        return self.__widget
    
    def check(self):
        return self.__checkbox.value
    
    def augmentate_operator(self):
        named_options = {}
        ordered_options = []
        augmentation_operator = None
        if self.__widget is not None:
            for option in self.__widget.children:
                if option.name!="":
                    if option.name[0] in self.__check_digits:
                        ordered_options.append([int(option.name[0]), option.value])
                    else:
                        named_options[option.name] = option.value
            if len(ordered_options)>0:
                ordered_options.sort(key= lambda x: x[0])
                ordered_options = [option_value[1] for option_value in ordered_options]
                augmentation_operator = self.__augmentation(*ordered_options, **named_options)
            else:
                augmentation_operator = self.__augmentation(**named_options)
            # options= {option.name: option.value for option in self.__widget.children if option.name!=""}
        return augmentation_operator

def augmentate_image(image: np.ndarray=..., transform: A.Compose=..., images_count: int=2, image_width: int=300)->None:
    if transform is ...:
        # Построение pipeline albumentations для 
        # задачи классификации (без учета разметки)
        transform = A.Compose([
            A.HorizontalFlip(p=0.5),
            A.ShiftScaleRotate(p=0.8),
            A.ShiftScaleRotate(shift_limit=0.0625, scale_limit=0.2, rotate_limit=45, p=0.2),
            A.Blur(blur_limit=3),
            A.MedianBlur(blur_limit=3, p=0.9),
            A.RandomBrightnessContrast(p=0.6),
            A.OpticalDistortion(p=0.5)
        ])
        
    
    transformed_images = list()

    # Получение аугментированных изображений
    for index in range(images_count):
        transformed_images.append(transform(image=image)["image"])

    # Отображение полученных изображений
    return ipyplot.plot_images(transformed_images, max_images=images_count, img_width=image_width)
        
class AlbumentationWidget():
    def __init__(self, debug=True, image=None):
        self.debug = debug
        self.image = image
        #ShiftScaleRotate аугментатор
        shiftscalerotate_p = AugmentatorOption("p", "Probability(p): ", 0.05, 0.0, 1.0, 0.5)
        shiftscalerotate_shift_limit = AugmentatorOption("shift_limit", "Shift(shift_limit): ", 0.0005, 0.0, 1.0, 0.0625, '.4f')
        shiftscalerotate_scale_limit = AugmentatorOption("scale_limit", "Scale(scale_limit): ", 0.05, 0.0001, 0.9999, 0.3, '.2f')
        shiftscalerotate_rotate_limit = AugmentatorOption("rotate_limit", "Rotate(rotate_limit): ", 1, 0, 360, 60)
        shiftscalerotate_options = {
                                    shiftscalerotate_p.name: shiftscalerotate_p,
                                    shiftscalerotate_shift_limit.name: shiftscalerotate_shift_limit,
                                    shiftscalerotate_scale_limit.name: shiftscalerotate_scale_limit,
                                    shiftscalerotate_rotate_limit.name: shiftscalerotate_rotate_limit
                                    }

        #ColorJitter аугментатор
        colorjitter_p = AugmentatorOption("p", "Probability(p): ", 0.05, 0.0, 1.0, 0.5)
        colorjitter_brightness = AugmentatorOption("brightness", "Brightness(brightness): ", 0.025, 0.0, 1.0, 0.75, '.2f')
        colorjitter_contrast = AugmentatorOption("contrast", "Contrast(contrast): ", 0.025, 0.0, 1.0, 0.25, '.2f')
        colorjitter_saturation = AugmentatorOption("saturation", "Saturation(saturation): ", 0.025, 0.0, 1.0, 0.5, '.2f')

        colorjitter_options = {
                                colorjitter_p.name: colorjitter_p,
                                colorjitter_brightness.name: colorjitter_brightness,
                                colorjitter_contrast.name: colorjitter_contrast,
                                colorjitter_saturation.name: colorjitter_saturation
                            }

        #Blur аугментатор
        blur_p = AugmentatorOption("p", "Probability(p): ", 0.05, 0.0, 1.0, 0.7)
        blur_limit = AugmentatorOption("blur_limit", "Blur(blur_limit): ", 1, 1, 12, 3)

        blur_options = {
                            blur_p.name: blur_p,
                            blur_limit.name: blur_limit,
                        }

        #RandomRain аугментатор
        randomrain_p = AugmentatorOption("p", "Probability(p): ", 0.05, 0.0, 1.0, 0.4)
        randomrain_drop_length = AugmentatorOption("drop_length", "Length(drop_length): ", 1, 0, 100, 5)
        randomrain_drop_width = AugmentatorOption("drop_width", "Width(drop_width): ", 1, 1, 5, 2)
        randomrain_blur_value = AugmentatorOption("blur_value", "Blurry(blur_value): ", 1, 1, 12, 3)

        randomrain_options = {
                            randomrain_p.name: randomrain_p,
                            randomrain_drop_length.name: randomrain_drop_length,
                            randomrain_drop_width.name: randomrain_drop_width,
                            randomrain_blur_value.name: randomrain_blur_value,
                        }
        #Augmentators
        self.shiftscalerotate = Augmentator("ShiftScaleRotate: ", shiftscalerotate_options, A.ShiftScaleRotate)
        self.colorjitter = Augmentator("ColorJitter: ", colorjitter_options, A.ColorJitter)
        self.blur = Augmentator("Blur: ", blur_options, A.Blur)
        self.randomrain = Augmentator("RandomRain: ", randomrain_options, A.RandomRain)
        
        # Widgets
        self.shiftscalerotate_widget = self.shiftscalerotate()
        self.colorjitter_widget = self.colorjitter()
        self.blur_widget = self.blur()
        self.randomrain_widget = self.randomrain()
        
        label_image_count_widget = widgets.Label(value='Количество изображений: ')
        images_count_widget = widgets.IntText(value=7, description='', disabled=False, layout=widgets.Layout(width="50px"))
        self.himage_count_widget = widgets.HBox([label_image_count_widget, images_count_widget])
        self.vbox_augmentators = [self.shiftscalerotate, self.colorjitter, self.blur, self.randomrain, self.himage_count_widget]
        
        self.create_button_widget = widgets.Button(description='Аугментировать', disabled=False, button_style='success', tooltip='Аугментировать', icon='check')
        
        # Output
        self.output = widgets.Output()
        
        # Add callback for button click
        self.create_button_widget.on_click(self.on_button_click)

    def on_button_click(self, event):
        image_count = int(self.vbox_augmentators[-1].children[-1].value)
        augmentation = []
        self.output.clear_output()
        with self.output:
            for augmentator in self.vbox_augmentators[:-1]:
                if augmentator.check():
                    augmentation.append(augmentator.augmentate_operator())
            augmentation = A.Compose(augmentation)
            if self.debug:
                print(augmentation)
            augmentate_image(self.image, images_count=image_count, transform=augmentation)
    
    def __call__(self):
        vbox = widgets.VBox([self.shiftscalerotate_widget, self.colorjitter_widget, self.blur_widget, self.randomrain_widget, self.himage_count_widget])
        return (vbox, self.create_button_widget, self.output)

class AlbumentationPipelineWidget():
    def __init__(self, debug=True, image=None):
        self.debug = debug
        
        #ShiftScaleRotate аугментатор
        shiftscalerotate_p = AugmentatorOption("p", "Probability(p): ", 0.05, 0.0, 1.0, 0.5)
        shiftscalerotate_shift_limit = AugmentatorOption("shift_limit", "Shift(shift_limit): ", 0.0005, 0.0, 1.0, 0.0625, '.4f')
        shiftscalerotate_scale_limit = AugmentatorOption("scale_limit", "Scale(scale_limit): ", 0.05, 0.0001, 0.9999, 0.3, '.2f')
        shiftscalerotate_rotate_limit = AugmentatorOption("rotate_limit", "Rotate(rotate_limit): ", 1, 0, 360, 60)
        shiftscalerotate_options = {
                                    shiftscalerotate_p.name: shiftscalerotate_p,
                                    shiftscalerotate_shift_limit.name: shiftscalerotate_shift_limit,
                                    shiftscalerotate_scale_limit.name: shiftscalerotate_scale_limit,
                                    shiftscalerotate_rotate_limit.name: shiftscalerotate_rotate_limit
                                    }

        #ColorJitter аугментатор
        colorjitter_p = AugmentatorOption("p", "Probability(p): ", 0.05, 0.0, 1.0, 0.5)
        colorjitter_brightness = AugmentatorOption("brightness", "Brightness(brightness): ", 0.025, 0.0, 1.0, 0.75, '.2f')
        colorjitter_contrast = AugmentatorOption("contrast", "Contrast(contrast): ", 0.025, 0.0, 1.0, 0.25, '.2f')
        colorjitter_saturation = AugmentatorOption("saturation", "Saturation(saturation): ", 0.025, 0.0, 1.0, 0.5, '.2f')

        colorjitter_options = {
                                colorjitter_p.name: colorjitter_p,
                                colorjitter_brightness.name: colorjitter_brightness,
                                colorjitter_contrast.name: colorjitter_contrast,
                                colorjitter_saturation.name: colorjitter_saturation
                            }

        #RandomCrop аугментатор
        randomcrop_p = AugmentatorOption("p", "Probability(p): ", 0.05, 0.0, 1.0, 0.85)
        randomcrop_width = AugmentatorOption("2width", "Width(width): ", 1, 300, 600, 350)
        randomcrop_height = AugmentatorOption("1height", "Height(height): ", 1, 200, 400, 250)

        randomcrop_options = {
                                randomcrop_p.name: randomcrop_p,
                                randomcrop_height.name: randomcrop_height,
                                randomcrop_width.name: randomcrop_width,
                             }

        #RandomRain аугментатор
        randomrain_p = AugmentatorOption("p", "Probability(p): ", 0.05, 0.0, 1.0, 0.4)
        randomrain_drop_length = AugmentatorOption("drop_length", "Length(drop_length): ", 1, 0, 100, 5)
        randomrain_drop_width = AugmentatorOption("drop_width", "Width(drop_width): ", 1, 1, 5, 2)
        randomrain_blur_value = AugmentatorOption("blur_value", "Blurry(blur_value): ", 1, 1, 12, 3)

        randomrain_options = {
                            randomrain_p.name: randomrain_p,
                            randomrain_drop_length.name: randomrain_drop_length,
                            randomrain_drop_width.name: randomrain_drop_width,
                            randomrain_blur_value.name: randomrain_blur_value,
                        }
        #Augmentators
        self.shiftscalerotate = Augmentator("ShiftScaleRotate: ", shiftscalerotate_options, A.ShiftScaleRotate)
        self.colorjitter = Augmentator("ColorJitter: ", colorjitter_options, A.ColorJitter)
        self.randomcrop = Augmentator("RandomCrop: ", randomcrop_options, A.RandomCrop)
        self.randomrain = Augmentator("RandomRain: ", randomrain_options, A.RandomRain)
        
        # Widgets
        self.shiftscalerotate_widget = self.shiftscalerotate()
        self.colorjitter_widget = self.colorjitter()
        self.randomcrop_widget = self.randomcrop()
        self.randomrain_widget = self.randomrain()
        
        self.vbox_augmentators = [self.shiftscalerotate, self.colorjitter, self.randomcrop, self.randomrain]
    
    def __call__(self):
        vbox_widget = widgets.VBox([self.shiftscalerotate_widget, self.colorjitter_widget, self.randomcrop_widget, self.randomrain_widget])
        return vbox_widget
    
    def get_transform(self):
        augmentation = []
        for augmentator in self.vbox_augmentators:
            if augmentator.check():
                augmentation.append(augmentator.augmentate_operator())
        return A.Compose(augmentation, bbox_params=A.BboxParams(format='pascal_voc'))