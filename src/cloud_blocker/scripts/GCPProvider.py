import requests
from typing import List

from cloud_blocker.scripts.CloudProvider import CloudProviderBase
from cloud_blocker.model.Info import Info


class GCPProvider(CloudProviderBase):
    def get_url(self) -> str:
        return "https://www.gstatic.com/ipranges/cloud.json"

    def fetch_ip_ranges(self, url: str) -> dict:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def extract_info(self, data: dict) -> List[Info]:
        return [
            Info(cidr=prefix.get('ipv4Prefix') or prefix.get('ipv6Prefix'),
                 cloud_provider="Google Cloud",
                 cloud_region=prefix.get('scope'))
            for prefix in data.get('prefixes', [])
        ]


def fetch() -> List[Info]:
    return GCPProvider().fetch()
