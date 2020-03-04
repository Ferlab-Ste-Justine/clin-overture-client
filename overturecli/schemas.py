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

class Specimen(Schema):
    specimenId = fields.Str(default=None)
    donorId = fields.Str(default=None)
    submitterSpecimenId = NonEmptyString
    specimenType = NonEmptyString
    specimenTissueSource = NonEmptyString
    tumourNormalDesignation = NonEmptyString

class Donor(Schema):
    donorId = fields.Str(default=None)
    submitterDonorId = fields.Str(required=True)
    studyId = fields.Str(required=True)
    gender = fields.Str(
        required=True, 
        validate=validate.OneOf(["Male", "Female", "Other"])
    )

class Sample(Schema):
    sampleId = fields.Str(default=None)
    specimenId = fields.Str(default=None)
    submitterSampleId = fields.Str(required=True)
    matchedNormalSubmitterSampleId = fields.Str(default=None),
    sampleType = fields.Str(required=True)
    specimen = fields.Nested(Specimen(), required=True)
    donor = fields.Nested(Donor(), required=True)

class SubmittedAnalysis(Schema):
    studyId = NonEmptyString
    analysisType = fields.Nested(AnalysisType(), required=True)
    files = fields.List(fields.Nested(
        FileMetadata(only=("fileName", "dataType"))
    ), required=True)
    samples = fields.List(fields.Nested(
        Sample(only=("submitterSampleId",))
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