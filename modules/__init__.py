from .domain_recon import DomainReconModule
from .username_enum import UsernameEnumModule
from .email_analysis import EmailAnalysisModule
from .ip_geolocation import IPGeolocationModule
from .file_metadata import FileMetadataModule

# Add new modules here after subclassing BaseModule in modules/your_module.py
MODULE_REGISTRY = {
    "domain_recon": DomainReconModule(),
    "username_enum": UsernameEnumModule(),
    "email_analysis": EmailAnalysisModule(),
    "ip_geolocation": IPGeolocationModule(),
    "file_metadata": FileMetadataModule(),
}
