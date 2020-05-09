"""
Implementation of the schemas to validate analysis input before sending it to SONG

TODO: The more generic validators should be moved to the Python Overture SDK
"""

from marshmallow import Schema, fields, validate

NonEmptyString = fields.Str(required=True, validate=validate.Length(min=1))
ReqPosInt = fields.Int(required=True, validate=validate.Range(min=1))

class AnalysisType(Schema):
    """
    Validation schema for the type entry of the analysis in the analysis payload
    """
    name = fields.Str(required=True, validate=validate.OneOf(["clinReadAlignment"]))
    version = ReqPosInt

class FileMetadata(Schema):
    """
    Validation schema for the metadata entries of files in the analysis payload
    """
    fileName = fields.Str(required=True)
    studyId = fields.Str(required=True)
    fileSize = fields.Int(required=True)
    fileType = fields.Str(required=True)
    fileMd5sum = fields.Str(required=True)
    fileAccess = fields.Str(required=True)
    dataType = fields.Str(required=True)

class Sample(Schema):
    """
    Validation schema for the sample entries in the analysis payload
    The rest of the sample metadata SONG needs is added server-side so the client doesn't need to
    manage it.
    """
    submitterSampleId = fields.Str(required=True)

class SubmittedAnalysis(Schema):
    """
    Validation for the analysis when it is first read from the metadata file submitted by the user.

    This is before any processing is done on the data.

    The customizable 'experiment' field is missing to keep this class generic, so it should be
    subclassed with a validator that implements that field.
    """
    studyId = NonEmptyString
    analysisType = fields.Nested(AnalysisType(), required=True)
    files = fields.List(fields.Nested(
        FileMetadata(only=("fileName", "dataType"))
    ), required=True)
    samples = fields.List(fields.Nested(
        Sample(only=("submitterSampleId",))
    ), required=True)

class UploadAnalysis(Schema):
    """
    Validation for the analysis after it has been processed and is ready to be submitted to SONG.

    The customizable 'experiment' field is missing to keep this class generic, so it should be
    subclassed with a validator that implements that field.
    """
    studyId = NonEmptyString
    analysisType = fields.Nested(AnalysisType(), required=True)
    files = fields.List(fields.Nested(
        FileMetadata()
    ), required=True)
    samples = fields.List(fields.Nested(
        Sample()
    ), required=True)

class ClinReadAlignment(Schema):
    """
    Validator for the 'experiment' field for the ClinReadAlignment analysis type which is
    specific to the Clin project
    """
    libraryStrategy = NonEmptyString
    libraryName = NonEmptyString
    libraryType = NonEmptyString
    aligned = fields.Boolean(required=True)
    alignmentTool = NonEmptyString
    referenceGenome = NonEmptyString
    pairedEnd = fields.Boolean(required=True)
    insertSize = ReqPosInt
    sequencingStrategy = NonEmptyString
    sequencingId = NonEmptyString
    runId = NonEmptyString
    runDate = fields.Date(required=True)
    totalReadsCount = ReqPosInt
    readSupplementary = ReqPosInt
    readDuplicates = ReqPosInt
    readMapped = ReqPosInt
    readProperlyPaired = ReqPosInt

class SubmittedClinReadAlignmentAnalysis(SubmittedAnalysis):
    """
    Subclassing of the generic SubmittedAnalysis validator with the experiment field being
    validated by the ClinReadAlignment validator
    """
    experiment = fields.Nested(ClinReadAlignment(), required=True)

class UploadClinReadAlignmentAnalysis(UploadAnalysis):
    """
    Subclassing of the generic UploadAnalysis validator with the experiment field being
    validated by the ClinReadAlignment validator
    """
    experiment = fields.Nested(ClinReadAlignment(), required=True)
