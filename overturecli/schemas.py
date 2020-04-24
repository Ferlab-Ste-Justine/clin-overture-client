from marshmallow import Schema, fields, validate

NonEmptyString = fields.Str(required=True, validate=validate.Length(min=1))
ReqPosInt = fields.Int(required=True, validate=validate.Range(min=1))

class AnalysisType(Schema):
    name = fields.Str(required=True, validate=validate.OneOf(["clinReadAlignment"]))
    version = ReqPosInt

class FileMetadata(Schema):
    fileName = fields.Str(required=True)
    studyId = fields.Str(required=True)
    fileSize = fields.Int(required=True)
    fileType = fields.Str(required=True)
    fileMd5sum = fields.Str(required=True)
    fileAccess = fields.Str(required=True)
    dataType = fields.Str(required=True)

class Sample(Schema):
    submitterSampleId = fields.Str(required=True)

class SubmittedAnalysis(Schema):
    studyId = NonEmptyString
    analysisType = fields.Nested(AnalysisType(), required=True)
    files = fields.List(fields.Nested(
        FileMetadata(only=("fileName", "dataType"))
    ), required=True)
    samples = fields.List(fields.Nested(
        Sample(only=("submitterSampleId",))
    ), required=True)

class UploadAnalysis(Schema):
    studyId = NonEmptyString
    analysisType = fields.Nested(AnalysisType(), required=True)
    files = fields.List(fields.Nested(
        FileMetadata()
    ), required=True)
    samples = fields.List(fields.Nested(
        Sample()
    ), required=True)

class ClinReadAlignment(Schema):
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
    experiment = fields.Nested(ClinReadAlignment(), required=True)

class UploadClinReadAlignmentAnalysis(UploadAnalysis):
    experiment = fields.Nested(ClinReadAlignment(), required=True)