from app.cloudinary.config import cloudinary
import cloudinary.uploader


def upload_video(file):
    result = cloudinary.uploader.upload(
        file,
        resource_type="video"
    )

    return result
