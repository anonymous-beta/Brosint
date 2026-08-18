"""
File metadata extraction: pulls EXIF data from an image file the user
provides locally. Purely local file parsing — no network calls.
target.value is expected to be a filesystem path.
"""
from core.module_base import BaseModule
from core.models import Target, Finding, TargetType, Confidence


class FileMetadataModule(BaseModule):
    name = "file_metadata"
    description = "Extracts EXIF/metadata from a local image file"
    accepts = (TargetType.FILE,)

    async def run(self, target: Target) -> list[Finding]:
        from PIL import Image
        from PIL.ExifTags import TAGS

        try:
            img = Image.open(target.value)
        except Exception as e:
            return [Finding(
                module=self.name, target_id=target.id, label="Could not open file",
                data={"error": str(e)}, confidence=Confidence.LOW,
            )]

        findings = [Finding(
            module=self.name, target_id=target.id, label="Image properties",
            data={"format": img.format, "size": img.size, "mode": img.mode},
            confidence=Confidence.HIGH,
        )]

        exif = img.getexif()
        if exif:
            tags = {}
            gps = {}
            for tag_id, value in exif.items():
                tag = TAGS.get(tag_id, tag_id)
                if tag == "GPSInfo":
                    gps = {k: str(v) for k, v in value.items()} if isinstance(value, dict) else {}
                else:
                    tags[str(tag)] = str(value)
            if tags:
                findings.append(Finding(
                    module=self.name, target_id=target.id, label="EXIF tags",
                    data=tags, confidence=Confidence.HIGH,
                ))
            if gps:
                findings.append(Finding(
                    module=self.name, target_id=target.id, label="GPS EXIF data (sensitive)",
                    data=gps, confidence=Confidence.HIGH,
                ))
        return findings
