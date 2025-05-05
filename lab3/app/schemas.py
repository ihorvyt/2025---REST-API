from marshmallow import Schema, fields, validate

class BookSchema(Schema):
    id = fields.Int(dump_only=True)
    title = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    author = fields.Str(required=True, validate=validate.Length(min=1, max=100))
    created_at = fields.DateTime(dump_only=True)

class PaginationSchema(Schema):
    items = fields.Nested(BookSchema, many=True)
    total = fields.Int()
    limit = fields.Int()
    offset = fields.Int()