from src.export.RequestCreator import RequestCreator



class TitleRequestCreator(RequestCreator):
    def prepare_image_request(self, uploaded_image_url : str, image_index:int) -> None:
        raise ValueError("TitleRequestCreator does not support image requests")

    def __init__(self, page_id: int, **kwargs):
        self._request = []
        self.page_id = page_id
        self.title = kwargs.get("title")

    @property
    def request(self) -> list:
        request = self._request
        return request

    @property
    def image_request(self) -> str:
        raise ValueError("TitleRequestCreator does not support image requests")

    def prepare_request(self) -> None:
        requests = [
            {
                'createSlide': {
                    'objectId': 'pageId' + str(self.page_id),
                    'insertionIndex': str(self.page_id),
                    'slideLayoutReference': {
                        'predefinedLayout': 'TITLE_ONLY'
                    },
                    "placeholderIdMappings": [
                        {
                            "layoutPlaceholder": {
                                "type": "TITLE",
                                "index": 0
                            },
                            "objectId": "titleId" + str(self.page_id)
                        },
                    ]
                }
            },
            {
                'insertText': {
                    'objectId': 'titleId' + str(self.page_id),
                    'text': self.title
                },
            },
        ]
        self._request = requests
