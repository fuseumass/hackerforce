from whitenoise import storage 
class CompressedManifestStaticFilesStorage(storage.CompressedManifestStaticFilesStorage):
    manifest_strict = False