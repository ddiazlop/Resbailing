import random

from src.export.requests import RequestCreator
from src.export.requests.RequestCreator import RequestType
from src.export.requests.creators.BackGroundImageRequestCreator import BackGroundImageRequestCreator
from src.export.requests.creators.SideImageSlideRequestCreator import RightImageSlideRequestCreator, \
    LeftImageSlideRequestCreator
from src.export.requests.creators.TitleAndTextRequestCreator import TitleAndTextRequestCreator
from src.export.requests.creators.TitleRequestCreator import TitleRequestCreator


def get_request_creator(request_type: RequestType, page_id: int, **kwargs) -> RequestCreator:
    title = kwargs.get("title")
    body = kwargs.get("body")
    if title is not None and body is not None and len(title) > len(body):
        return BackGroundImageRequestCreator(page_id, title=body, body=title)

    if request_type == RequestType.TITLE:
        return TitleRequestCreator(page_id, **kwargs)
    if request_type == RequestType.TITLE_AND_TEXT:
        return TitleAndTextRequestCreator(page_id, **kwargs)
    elif request_type == RequestType.RIGHT_IMAGE:
        return RightImageSlideRequestCreator(page_id, **kwargs)
    elif request_type == RequestType.LEFT_IMAGE:
        return LeftImageSlideRequestCreator(page_id, **kwargs)
    else:
        raise ValueError("Invalid request type")

def get_random_request_type(page_id: int, **kwargs) -> RequestCreator:
    number = random.randint(3, 4) # So far, 1 and 2 are not used since they are not as good as 3 and 4
    return get_request_creator(RequestType(number), page_id, **kwargs)