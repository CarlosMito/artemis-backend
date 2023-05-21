from django.db import models


class User(models.Model):
    username = models.CharField(max_length=512)
    password = models.CharField(max_length=512)
    email = models.CharField(max_length=512)


class Input(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    prompt = models.TextField()
    negative_prompt = models.TextField()
    image_dimensions = models.CharField(max_length=32)
    num_outputs = models.IntegerField()
    num_inference_steps = models.PositiveIntegerField()
    guidance_scale = models.FloatField()
    scheduler = models.CharField(max_length=128)
    seed = models.BigIntegerField()
    style = models.CharField(max_length=64)
    saturation = models.CharField(max_length=64)
    value = models.CharField(max_length=64)
    color = models.CharField(max_length=64)


class Output(models.Model):

    def upload_to(instance, filename):
        return f"outputs/{filename}"

    input = models.ForeignKey(Input, on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to=upload_to)
    is_public = models.BooleanField(default=False)
    favorite_count = models.IntegerField(default=0)
