import enum
from abc import ABC, abstractmethod

from src.export.requests import CommonRequests


class RequestType(enum.Enum):
    TITLE = 1
    TITLE_AND_TEXT = 2
    RIGHT_IMAGE = 3
    LEFT_IMAGE = 4

class RequestCreator(ABC):
    @property
    @abstractmethod
    def request(self) -> list:
        pass

    @property
    @abstractmethod
    def image_request(self) -> list:
        pass

    @abstractmethod
    def prepare_request(self) -> None:
        pass

    @abstractmethod
    def prepare_image_request(self, uploaded_image_url : str, image_index:int) -> None:
        pass


    def create_request (self) -> list:
        self.prepare_request()
        return self.request

    def create_image_request(self, uploaded_image_url : str, image_index:int) -> list:
        self.prepare_image_request(uploaded_image_url, image_index)
        return self.image_request

    def create_image_and_background_request(self, uploaded_image_url : str,background_image_url:str, image_index:int) -> list:
        self.prepare_image_request(uploaded_image_url, image_index)
        request = CommonRequests.set_image_as_background(background_image_url, image_index)
        self.image_request.append(request)
        return self.image_request