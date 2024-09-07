import requests
from typing import List

from cloud_blocker.scripts.CloudProvider import CloudProviderBase
from cloud_blocker.model.Info import Info


class AWSProvider(CloudProviderBase):
    def get_url(self) -> str:
        return "https://ip-ranges.amazonaws.com/ip-ranges.json"

    def fetch_ip_ranges(self, url: str) -> dict:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def extract_info(self, data: dict) -> List[Info]:
        return [
            Info(cidr=prefix['ip_prefix'], cloud_provider="Amazon", cloud_region=prefix['region'])
            for prefix in data.get('prefixes', [])
        ]


def fetch() -> List[Info]:
    return AWSProvider().fetch()
