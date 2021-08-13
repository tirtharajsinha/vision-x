from django.db import models
from .utils import get_filtered_image
from PIL import Image
import numpy as np
from io import BytesIO
from django.core.files.base import ContentFile
import cv2
# Create your models here.
ACTION_CHOICES = (
    ('NO_FILTER', 'NO_FILTER'),
    ('COLORIZED', 'colorized'),
    ('GRAYSCALE', 'grayscale'),
    ('BLURRED', "blurred"),
    ('BINARY', 'binary'),
    ('INVERT', 'invert'),
    ('FACE_DETECTION', 'face_detection'),
    ('CLASSIFICATION', 'classification'),
    ('SKETCHED', 'sketched'),
    ('SHAPE', 'shape'),
    ('DOCUMENT', 'document'),
)


class Upload(models.Model):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=255, default="")
    image = models.ImageField(upload_to="finalimages")
    orgimage = models.ImageField(upload_to="orgimages", default="")
    action = ""
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.username)

    def save(self, *args, **kwargs):

        # open image
        pil_img = Image.open(self.image)
        print(self.image)

        # convert the image for processing

        cv_img = np.array(pil_img)
        try:
            img = get_filtered_image(cv_img, self.action)
        except:
            img = np.zeros((512, 512, 3), np.uint8)
            cv2.putText(img, "No Action", (100, 200),
                        cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 100), 10)

        # convert back to pil image
        im_pil = Image.fromarray(img)
        print(im_pil)

        # save

        buffer = BytesIO()
        im_pil.save(buffer, format='png')
        image_png = buffer.getvalue()
        self.image.save(str(self.image), ContentFile(image_png), save=False)

        super().save(*args, **kwargs)
        print()
