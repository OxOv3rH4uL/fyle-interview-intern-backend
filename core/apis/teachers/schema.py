from marshmallow import Schema, EXCLUDE, fields, post_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field
from core.libs.helpers import GeneralObject
from core.models.teachers import Teacher



class TeacherSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Teacher
        unknown = EXCLUDE

    created_at = auto_field(dump_only=True)
    id = fields.Integer(required=True, allow_none=False)
    updated_at = auto_field(dump_only=True) 
    user_id = fields.Integer(required=True, allow_none=False)

    @post_load
    def initiate_class(self,data_dict,many,partial):
        return GeneralObject(**data_dict)