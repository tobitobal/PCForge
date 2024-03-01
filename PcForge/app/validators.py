from django import forms
from django.core.exceptions import ValidationError

class MaxSizeFileValidator:
    
    def __init__(self, max_file_size=5):
        self.max_file_size = max_file_size

    def __call__(self, value):
        size = value.size
        max_size = self.max_file_size * 1048576

        if size > max_size:
            raise ValidationError(f"El tamaño máximo del archivo debe ser de {self.max_file_size} MB")

        return value



from django.core.exceptions import ValidationError
from django.core.files.images import get_image_dimensions

def validate_square_image(value):
    """
    Validador que asegura que la imagen sea cuadrada y tenga dimensiones de 350x350.
    """
    width, height = get_image_dimensions(value)

    if width != height:
        raise ValidationError("La imagen debe ser cuadrada.")

