from src.export.requests.utils import UnitTranslator


def set_background_image(image_url: str, image_index: int, page_index:int) -> list:
    requests = [
        {
            'createImage': {
                'objectId': 'imageId' + str(image_index),
                'url': image_url,
                'elementProperties': {
                    'pageObjectId': 'pageId' + str(page_index),
                    'size': {
                        'height': {
                            'magnitude': UnitTranslator.cm_to_pt(26.86),
                            'unit': 'PT'
                        },
                        'width': {
                            'magnitude': UnitTranslator.cm_to_pt(26.86),
                            'unit': 'PT'
                        }
                    },
                    'transform': {
                        'scaleX': 1,
                        'scaleY': 1,
                        'translateX': UnitTranslator.cm_to_pt(-1.46),
                        'translateY': UnitTranslator.cm_to_pt(-7.24),
                        'unit': 'PT'
                    }
                }
            }
        },
        # Image overlaps with elements, so the image needs to be brought to back
        {
            'updatePageElementsZOrder': {
                'pageElementObjectIds': ['imageId' + str(image_index)],
                'operation': 'SEND_TO_BACK'
            }
        }
    ]
    return requests

def set_image_as_background(image_url:str, page_index:int) -> list:
    requests = [
        {
            'updatePageProperties': {
                'objectId': 'pageId' + str(page_index),
                'pageProperties': {
                    'pageBackgroundFill': {
                        'stretchedPictureFill': {
                            'contentUrl': image_url,
                            'size': {
                                'height': {
                                    'magnitude': 1,
                                    'unit': 'PT'
                                },
                                'width': {
                                    'magnitude': 1,
                                    'unit': 'PT'
                                }
                            }
                        }
                    }
                },
                'fields': 'pageBackgroundFill'
            }
        }
    ]
    return requests