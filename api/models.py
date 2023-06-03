from django.db import models


class User(models.Model):
    username = models.CharField(max_length=512)
    password = models.CharField(max_length=512)
    email = models.CharField(max_length=512)


class Input(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    prompt = models.TextField()
    negative_prompt = models.TextField(null=True, blank=True)
    image_dimensions = models.CharField(max_length=32)
    num_outputs = models.IntegerField()
    num_inference_steps = models.PositiveIntegerField()
    guidance_scale = models.FloatField()
    scheduler = models.CharField(max_length=128)
    seed = models.BigIntegerField()
    style = models.CharField(max_length=64, null=True, blank=True)
    saturation = models.CharField(max_length=64, null=True, blank=True)
    value = models.CharField(max_length=64, null=True, blank=True)
    color = models.CharField(max_length=64, null=True, blank=True)
    version = models.CharField(max_length=128)
    replicate_id = models.TextField(null=True, blank=True)


class Output(models.Model):

    def upload_to(instance, filename):
        return f"outputs/{filename}"

    input = models.ForeignKey(Input, related_name='outputs', on_delete=models.DO_NOTHING)
    image = models.ImageField(upload_to=upload_to)
    is_public = models.BooleanField(default=False)
    favorite_count = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.id}: {self.image.url}"