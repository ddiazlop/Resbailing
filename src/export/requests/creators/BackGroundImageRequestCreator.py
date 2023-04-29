from src.export.requests import CommonRequests
from src.export.requests.creators.super_creators.BlankRequestCreator import BlankRequestCreator
from src.export.requests.utils import UnitTranslator


class BackGroundImageRequestCreator(BlankRequestCreator):

    def add_body(self):
        """
        Returns empty since the body is not needed for this request.
        :return:
        """
        return []

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
                                'magnitude': UnitTranslator.cm_to_pt(3.43),
                                'unit': 'PT'
                            },
                            'width': {
                                'magnitude': UnitTranslator.cm_to_pt(18.73),
                                'unit': 'PT'
                            }
                        },
                        'transform': {
                            'scaleX': 1,
                            'scaleY': 1,
                            'translateX': UnitTranslator.cm_to_pt(3.33),
                            'translateY': UnitTranslator.cm_to_pt(4.97),
                            'unit': 'PT'
                        }
                    }
                }
            },
            {
                'insertText': {
                    'objectId': 'titleId' + str(self.page_id),
                    'text': self.title
                },
            }
        ]
        self._request.extend(request)
        self.style_text()
        self.style_textbox()


    def style_text(self):
        requests = [
            {
                'updateTextStyle': {
                    'objectId': 'titleId' + str(self.page_id),
                    'style': {
                        'bold': True,
                        'foregroundColor': {
                            'opaqueColor': {
                                'rgbColor': {
                                    'blue': UnitTranslator.rgb_to_range(255),
                                    'green': UnitTranslator.rgb_to_range(250),
                                    'red': UnitTranslator.rgb_to_range(250),
                                }
                            }
                        },
                        'fontFamily': 'Arial',
                        'fontSize': {
                            'magnitude': 29,
                            'unit': 'PT'
                        },
                    },
                    'fields': 'bold,fontFamily,fontSize,foregroundColor'
                }
            },
            {
                'updateParagraphStyle': {
                    "objectId": 'titleId' + str(self.page_id),
                    "style": {
                        "alignment": "CENTER"
                    },
                    "fields": 'alignment',
                }
            }
        ]
        self._request.extend(requests)

    def style_textbox(self):
        requests = [
            {
                'updateShapeProperties': {
                    'objectId': 'titleId' + str(self.page_id),
                    'shapeProperties': {
                        'shapeBackgroundFill': {
                            'solidFill': {
                                'color': {
                                    'rgbColor': {
                                        'blue': UnitTranslator.rgb_to_range(105),
                                        'green': UnitTranslator.rgb_to_range(105),
                                        'red': UnitTranslator.rgb_to_range(105),
                                    }
                                },
                                'alpha': 0.8
                            }
                        },
                        'outline': {
                            'dashStyle': 'SOLID',
                            'propertyState': 'RENDERED',
                            'weight': {
                                'magnitude': 1,
                                'unit': 'PT'
                            },
                            'outlineFill': {
                                'solidFill': {
                                    'color': {
                                        'rgbColor': {
                                            'blue': UnitTranslator.rgb_to_range(255),
                                            'green': UnitTranslator.rgb_to_range(250),
                                            'red': UnitTranslator.rgb_to_range(250),
                                        }
                                    }
                                }
                            }
                        },
                    },
                    'fields': 'shapeBackgroundFill.solidFill.color,shapeBackgroundFill.solidFill.alpha,outline'
                }
            }
        ]
        self._request.extend(requests)


    def prepare_image_request(self, uploaded_image_url: str, image_index: int) -> None:
        requests = CommonRequests.set_background_image(uploaded_image_url, image_index, image_index)
        self._image_request = requests



