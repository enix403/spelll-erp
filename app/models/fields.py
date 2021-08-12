from django.db import models

class TinyIntegerField(models.SmallIntegerField):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint"
        else:
            return super().db_type(connection)


class PositiveTinyIntegerField(models.SmallIntegerField, models.fields.PositiveIntegerRelDbTypeMixin):
    def db_type(self, connection):
        if connection.settings_dict['ENGINE'] == 'django.db.backends.mysql':
            return "tinyint unsigned"
        else:
            return super().db_type(connection)

def make_foreign_key(model_kclass, column_name: str, related_name: str = None, null: bool = False):
    return models.ForeignKey(
        model_kclass,
        db_column=column_name,
        related_name="+" if related_name is None else related_name,
        on_delete=models.CASCADE,
        null=null,
        blank=null
    )