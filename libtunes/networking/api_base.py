import watch
import vk


class APICaller(watch.WatchMe):
    api = watch.builtins.InstanceOf(vk.API)
    domain = "nondomain"
    method = "nonmethod"

    @classmethod
    def get_validated_fields(cls):
        return {
            field_name: field_value for field_name, field_value
            in cls.__dict__.items() if
            isinstance(
               field_value, watch.PredicateController
            )
        }

    @property
    def to_call_with(self):
        call_dict = dict()
        for field_name in self.get_validated_fields():
            field_value = getattr(self, field_name, None)
            if field_value is not None:
                call_dict[field_name] = field_value
        return call_dict

    def __setattr__(self, name, value):
        desctiptor = getattr(type(self), name, None)
        if not isinstance(desctiptor, watch.PredicateController):
            self.complain(name, value)

        super().__setattr__(name, value)

    def __init__(self, api_object):
        self.api = api_object

    def call_api(self):
        return getattr(getattr(self.api, self.domain), self.method)(
            **self.to_call_with
        )
