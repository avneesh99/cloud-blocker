import requests
from typing import List

from cloud_blocker.scripts.CloudProvider import CloudProviderBase
from cloud_blocker.model.Info import Info


class OracleProvider(CloudProviderBase):
    def get_url(self) -> str:
        return "https://docs.oracle.com/en-us/iaas/tools/public_ip_ranges.json"

    def fetch_ip_ranges(self, url: str) -> dict:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def extract_info(self, data: dict) -> List[Info]:
        infos = []
        for region in data.get('regions', []):
            cloud_region = region.get('region')
            for cidr_info in region.get('cidrs', []):
                infos.append(Info(cidr=cidr_info.get('cidr'),
                                  cloud_provider="Oracle Cloud",
                                  cloud_region=cloud_region))
        return infos


def fetch() -> List[Info]:
    return OracleProvider().fetch()
