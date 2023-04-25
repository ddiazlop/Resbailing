from abc import abstractmethod
from typing import Dict, Union, Any

from src.export.RequestCreator import RequestCreator
from src.export.creator.super_creators.BlankRequestCreator import BlankRequestCreator
from src.export.utils import UnitTranslator


class SideImageRequestCreator(BlankRequestCreator):

    def add_title(self):
        request = [
            {
                'createShape': {
                    'objectId': 'titleId' + str(self.page_id),
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': 'pageId' + str(self.page_id),
                        'size': {
                            'height': {
                                'magnitude': UnitTranslator.cm_to_pt(2.56),
                                'unit': 'PT'
                            },
                            'width': {
                                'magnitude': UnitTranslator.cm_to_pt(11.02),
                                'unit': 'PT'
                            }
                        },
                        'transform': self.title_transform()
                    }
                }
            },
            {
                'insertText': {
                    'objectId': 'titleId' + str(self.page_id),
                    'text': self.title
                },
            },
            {
                'updateTextStyle': {
                    'objectId': 'titleId' + str(self.page_id),
                    'style': {
                        'bold': True,
                        'fontFamily': 'Arial',
                        'fontSize': {
                            'magnitude': 24,
                            'unit': 'PT'
                        },
                    },
                    'fields': 'bold,fontFamily,fontSize'
                }
            }
        ]
        self._request.extend(request)

    def add_body(self):
        requests = [

            {
                'createShape': {
                    'objectId': 'bodyId' + str(self.page_id),
                    'shapeType': 'TEXT_BOX',
                    'elementProperties': {
                        'pageObjectId': 'pageId' + str(self.page_id),
                        'size': {
                            'height': {
                                'magnitude': UnitTranslator.cm_to_pt(7.66),
                                'unit': 'PT'
                            },
                            'width': {
                                'magnitude': UnitTranslator.cm_to_pt(10.58),
                                'unit': 'PT'
                            }
                        },
                        'transform': self.body_transform()

                    }
                }
            },
            {
                'insertText': {
                    'objectId': 'bodyId' + str(self.page_id),
                    'text': self.body
                },
            },
            {
                'updateTextStyle': {
                    'objectId': 'bodyId' + str(self.page_id),
                    'style': {
                        'fontFamily': 'Arial',
                        'foregroundColor': {
                            'opaqueColor': {
                                'rgbColor': {
                                    'blue': UnitTranslator.rgb_to_range(128),
                                    'green': UnitTranslator.rgb_to_range(128),
                                    'red': UnitTranslator.rgb_to_range(128),
                                }
                            }
                        },
                        'fontSize': {
                            'magnitude': 18,
                            'unit': 'PT'
                        },
                    },
                    'fields': 'fontFamily,fontSize,foregroundColor'
                }
            },
            {
                'updateParagraphStyle': {
                    "objectId": 'bodyId' + str(self.page_id),
                    "style": {
                        "alignment": "JUSTIFIED"
                    },
                    "fields": 'alignment',
                }
            }
        ]
        self._request.extend(requests)

    def prepare_image_request(self, uploaded_image_url: str, image_index: int) -> None:
        requests = [
            {
                'createImage': {
                    'url': uploaded_image_url,
                    'elementProperties': {
                        'pageObjectId': 'pageId' + str(image_index),
                        'size': {
                            'height': {
                                'magnitude': UnitTranslator.cm_to_pt(12.27),
                                'unit': 'PT'
                            },
                            'width': {
                                'magnitude': UnitTranslator.cm_to_pt(12.27),
                                'unit': 'PT'
                            }
                        },
                        'transform': self.image_transform()
                    }
                }
            }
        ]
        self._image_request = requests

    @abstractmethod
    def title_transform(self) -> Dict[str, Union[Union[int, str], Any]]:
        pass

    @abstractmethod
    def body_transform(self) -> Dict[str, Union[Union[int, str], Any]]:
        pass

    @abstractmethod
    def image_transform(self) -> Dict[str, Union[Union[int, str], Any]]:
        pass

class RightImageSlideRequestCreator(SideImageRequestCreator):
    def title_transform(self) -> Dict[str, Union[Union[int, str], Any]]:
        return {
            'scaleX': 1,
            'scaleY': 1,
            'translateX': UnitTranslator.cm_to_pt(0.77),
            'translateY': UnitTranslator.cm_to_pt(2.11),
            'unit': 'PT'
        }

    def body_transform(self) -> Dict[str, Union[Union[int, str], Any]]:
        return {
            'scaleX': 1,
            'scaleY': 1,
            'translateX': UnitTranslator.cm_to_pt(0.77),
            'translateY': UnitTranslator.cm_to_pt(5.31),
            'unit': 'PT'
        }

    def image_transform(self) -> Dict[str, Union[Union[int, str], Any]]:
        return {
            'scaleX': 1,
            'scaleY': 1,
            'translateX': UnitTranslator.cm_to_pt(12.1),
            'translateY': UnitTranslator.cm_to_pt(1.01),
            'unit': 'PT'
        }

class LeftImageSlideRequestCreator(SideImageRequestCreator):
    def title_transform(self) -> Dict[str, Union[Union[int, str], Any]]:
        return {
            'scaleX': 1,
            'scaleY': 1,
            'translateX': UnitTranslator.cm_to_pt(13.63),
            'translateY': UnitTranslator.cm_to_pt(2.11),
            'unit': 'PT'
        }

    def body_transform(self) -> Dict[str, Union[Union[int, str], Any]]:
        return {
            'scaleX': 1,
            'scaleY': 1,
            'translateX': UnitTranslator.cm_to_pt(13.85),
            'translateY': UnitTranslator.cm_to_pt(5.31),
            'unit': 'PT'
        }

    def image_transform(self) -> Dict[str, Union[Union[int, str], Any]]:
        return {
            'scaleX': 1,
            'scaleY': 1,
            'translateX': UnitTranslator.cm_to_pt(0.87),
            'translateY': UnitTranslator.cm_to_pt(1.01),
            'unit': 'PT'
        }