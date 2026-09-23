"""SporeRecon: реальная разведка сети системными утилитами.
Точки входа: full_recon(), dns_servers(), route_trace(), identify_isp(), neighbors_estimate().
Точки выхода: dict findings (JSON), CLI stdout, REST JSON."""
from .recon import NetworkRecon, full_recon, dns_servers, route_trace, identify_isp, neighbors_estimate, classify, __version__
__all__ = ["NetworkRecon", "full_recon", "dns_servers", "route_trace",
           "identify_isp", "neighbors_estimate", "classify", "__version__"]
