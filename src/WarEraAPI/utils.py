from datetime import datetime
from typing import get_args


def is_type_dict_based(
    _class: type
) -> bool:
    
    return (
        isinstance(_class, type) and
        issubclass(_class, dict) and
        hasattr(_class, "__annotations__")
    )


# gl refactoring ts
def edit_types(
    obj: object,
    class_overwrite: type | None = None
) -> None:
    
    for attr_name,attr_type in (
        obj.__annotations__.items() if class_overwrite==None else
        class_overwrite.__annotations__.items()
    ):
        
        if not isinstance(obj, dict):
            cur_value = getattr(obj, attr_name, None)
            attr_type = (attr_type,) if not get_args(attr_type) else get_args(attr_type)

            # fix dates from api response
            if datetime in attr_type and isinstance(cur_value, str):
                setattr(obj, attr_name,datetime.fromisoformat(cur_value))
            

        
        elif isinstance(obj, dict):
            cur_value = obj.get(attr_name)
            attr_type = (attr_type,) if not get_args(attr_type) else get_args(attr_type)


            # fix dates from api response
            if datetime in attr_type and isinstance(cur_value, str):
                obj[attr_name] = datetime.fromisoformat(cur_value)
        

        # fix nested TypedDict based types inside an object
        if any(
            [
                is_type_dict_based(_type) for _type in attr_type
            ]
        ):

            if isinstance(cur_value, dict):
                edit_types(cur_value, class_overwrite=attr_type[0])

            elif isinstance(cur_value, list):
                for item in cur_value:
                    edit_types(item, class_overwrite=attr_type[0])