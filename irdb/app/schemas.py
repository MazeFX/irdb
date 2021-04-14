"""Schemas module"""
from marshmallow import Schema, fields, validate


class BaseSchema(Schema):
    class Meta:
        ordered = True


class BaseSuccessSchema(BaseSchema):
    success = fields.Boolean(
        metadata={
            "required": True,
            "metadata": {
                "description": 'This is always "True" when a request succeeds',
                "example": True
            }
        }
    )


class BaseErrorSchema(BaseSchema):
    success = fields.Boolean(
        metadata={
            "required": True,
            "metadata": {
                "description": 'This is always "False" when a request fails',
                "example": False
            }
        }
    )


class BadRequestSchema(BaseErrorSchema):
    errors = fields.Dict(
        metadata={
            "required": False,
            "metadata": {
                "description": "Attached request body validation errors",
                "example": {"name": ["Missing data for required field."]}
            }
        }
    )


class ArtistSchema(BaseSchema):
    """Complete Rock Artist schema"""

    Id = fields.Int(
        metadata={
            "required": True,
            "metadata": {
                "description": "Id of Artist",
                "example": "760"}
        }
    )

    Name = fields.Str(
        metadata={
            "required": True,
            "metadata": {
                "description": "Name of Artist",
                "example": "Def Leppard"}
        },
        validate=validate.Length(min=1, max=16),
    )


class ArtistCreateSchema(ArtistSchema):
    class Meta:
        ordered = True
        exclude = ("Id",)


class ArtistCreateSuccessSchema(BaseSuccessSchema):
    artist = fields.Nested(
        ArtistSchema,
        metadata={
            "required": True,
            "metadata": {
                "description": "Validated and newly created Rock Artist information"
            }
        }
    )


class SongSchema(BaseSchema):
    """Complete Rock Song schema"""

    Id = fields.Int(
        metadata={
            "required": True,
            "metadata": {
                "description": "Id of the Song",
                "example": "760"}
        }
    )

    Name = fields.Str(
        metadata={
            "required": True,
            "metadata": {
                "description": "Name of the Rock Song",
                "example": "(Don't Fear) The Reaper"}
        },
    )

    Year = fields.Int(
        metadata={
            "required": True,
            "metadata": {
                "description": "Year when the song was recorded",
                "example": 1975}
        },
    )

    Artist = fields.Str(
        metadata={
            "required": True,
            "metadata": {
                "description": "Artist of the Rock Song",
                "example": "Blue Öyster Cult"}
        },
    )

    Shortname = fields.Str(
        metadata={
            "required": True,
            "metadata": {
                "description": "Short name of the Rock Song",
                "example": "dontfearthereaper"}
        },
    )

    Bpm = fields.Int(
        metadata={
            "required": True,
            "metadata": {
                "description": "Beats per Minute of the song",
                "example": 141}
        },
    )

    Duration = fields.Int(
        metadata={
            "required": True,
            "metadata": {
                "description": "Duration of the song in miliseconds",
                "example": 322822}
        },
    )

    Genre = fields.Str(
        metadata={
            "required": True,
            "metadata": {
                "description": "Genre of the Rock Song",
                "example": "Classic Rock"}
        },
    )

    SpotifyId = fields.Str(
        metadata={
            "required": True,
            "metadata": {
                "description": "Spotify Id of the Rock Song",
                "example": "5QTxFnGygVM4jFQiBovmRo"}
        },
    )

    Album = fields.Str(
        metadata={
            "required": True,
            "metadata": {
                "description": "Album of the Rock Song",
                "example": "Agents of Fortune"}
        },
    )


class SongCreateSchema(SongSchema):
    class Meta:
        ordered = True
        exclude = ("Id",)


class SongCreateSuccessSchema(BaseSuccessSchema):
    artist = fields.Nested(
        SongSchema,
        metadata={
            "required": True,
            "metadata": {
                "description": "Validated and newly created Rock Song information"
            }
        }
    )