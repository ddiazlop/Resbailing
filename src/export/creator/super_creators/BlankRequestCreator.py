from abc import abstractmethod

from src.export.RequestCreator import RequestCreator


class BlankRequestCreator(RequestCreator):
    def __init__(self, page_id: int, **kwargs):
        self._request = []
        self._image_request = []
        self.page_id = page_id

        self.title = kwargs.get("title")
        self.body = kwargs.get("body")

    @property
    def request(self) -> list:
        return self._request

    @property
    def image_request(self) -> list:
        return self._image_request

    def prepare_request(self) -> None:
        requests = [
            {
                'createSlide': {
                    'objectId': 'pageId' + str(self.page_id),
                    'insertionIndex': str(self.page_id),
                    'slideLayoutReference': {
                        'predefinedLayout': 'BLANK'
                    },
                }
            },

        ]
        self._request = requests
        self.add_title()
        self.add_body()

    @abstractmethod
    def add_title(self) -> list:
        pass

    @abstractmethod
    def add_body(self)-> list:
        pass

    @abstractmethod
    def prepare_image_request(self, uploaded_image_url: str, image_index: int) -> None:
        pass
