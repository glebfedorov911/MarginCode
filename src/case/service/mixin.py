from fastapi import UploadFile

from src.case.repository.case_repository import CaseRepository
from src.config.core.settings import settings

from typing import List
import os
import shutil


class CaseServiceMixin:


    def __init__(
            self,
            repo: CaseRepository,
    ):
        self.repo = repo
        self.image_path_dir = settings.file_settings.UPLOAD_IMAGE_DIR

    def _work_with_images(self, **kwargs) -> dict:
        images = kwargs.pop("images")
        saved_paths = self._save_images(images)
        kwargs['images'] = saved_paths if saved_paths else None
        return kwargs

    def _save_images(self, images: List[UploadFile]):
        saved_paths = []
        for image in images:
            image_path = os.path.join(self.image_path_dir, image.filename)
            with open(image_path, "wb") as image_file:
                shutil.copyfileobj(image.file, image_file)
            saved_paths.append(image_path)

        return saved_paths