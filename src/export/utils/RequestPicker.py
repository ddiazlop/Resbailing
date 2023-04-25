import random

from src.export import RequestCreator
from src.export.RequestCreator import RequestType
from src.export.creator.BackGroundImageRequestCreator import BackGroundImageRequestCreator
from src.export.creator.SideImageSlideRequestCreator import  RightImageSlideRequestCreator, \
    LeftImageSlideRequestCreator
from src.export.creator.TitleAndTextRequestCreator import TitleAndTextRequestCreator


def get_request_creator(request_type: RequestType, page_id: int, **kwargs) -> RequestCreator:
    title = kwargs.get("title")
    body = kwargs.get("body")
    if title is not None and body is not None and len(title) > len(body):
        return BackGroundImageRequestCreator(page_id, title=body, body=title)

    if request_type == RequestType.TITLE_AND_TEXT:
        return TitleAndTextRequestCreator(page_id, **kwargs)
    elif request_type == RequestType.RIGHT_IMAGE:
        return RightImageSlideRequestCreator(page_id, **kwargs)
    elif request_type == RequestType.LEFT_IMAGE:
        return LeftImageSlideRequestCreator(page_id, **kwargs)
    else:
        raise ValueError("Invalid request type")

def get_random_request_type(page_id: int, **kwargs) -> RequestCreator:
    number = random.randint(2, 4)
    return get_request_creator(RequestType(number), page_id, **kwargs)