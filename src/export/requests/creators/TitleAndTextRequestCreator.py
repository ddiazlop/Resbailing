from src.export.requests.RequestCreator import RequestCreator


class TitleAndTextRequestCreator(RequestCreator):


    def __init__(self, page_id: int, **kwargs):
        self._request = ""
        self._image_request = ""
        self.page_id = page_id
        self.title = kwargs.get("title")
        self.body = kwargs.get("body")

    @property
    def request(self) -> str:
        request = self._request
        return request

    @property
    def image_request(self) -> str:
        return self._image_request

    def prepare_request(self) -> None:
        requests = [
            {
                'createSlide': {
                    'objectId': 'pageId' + str(self.page_id),
                    'insertionIndex': str(self.page_id),
                    'slideLayoutReference': {
                        'predefinedLayout': 'TITLE_AND_BODY'
                    },
                    "placeholderIdMappings": [
                        {
                            "layoutPlaceholder": {
                                "type": "TITLE",
                                "index": 0
                            },
                            "objectId": "titleId" + str(self.page_id)
                        },
                        {
                            "layoutPlaceholder": {
                                "type": "BODY",
                                "index": 0
                            },
                            "objectId": "bodyId" + str(self.page_id)
                        }
                    ]
                }
            },
            {
                'insertText': {
                    'objectId': 'titleId' + str(self.page_id),
                    'text': self.title
                },
            },
            {
                'insertText': {
                    'objectId': 'bodyId' + str(self.page_id),
                    'text': self.body
                },
            },
        ]
        self._request = requests

    def prepare_image_request(self, uploaded_image_url : str, image_index:int) -> None:
        requests = [
            {
                'createImage': {
                    'url': uploaded_image_url,
                    'elementProperties': {
                        'pageObjectId': 'pageId' + str(image_index),
                        'size': {
                            'height': {
                                'magnitude': 200,
                                'unit': 'PT'
                            },
                            'width': {
                                'magnitude': 200,
                                'unit': 'PT'
                            }
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': 35,
                            'translateY': 185,
                            'unit': 'PT'
                        }
                    }
                }
            }
        ]
        self._image_request = requests
