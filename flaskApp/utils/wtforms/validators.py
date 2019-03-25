from wtforms.validators import ValidationError
import datetime

class Date_gte(object):
    def __init__(self, compare_with=None, message=None):
        self.compare_with = compare_with
        if not message:
            message = u'Il campo deve corrispondere a %i' % (compare_with)
        self.message = message

    def __call__(self, form, field):
        if (not form[self.compare_with].data):
            raise ValidationError(self.message)
        if field.data < form[self.compare_with].data:
            raise ValidationError(self.message)