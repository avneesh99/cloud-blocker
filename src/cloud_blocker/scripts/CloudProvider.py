from abc import ABC, abstractmethod
from typing import List
from cloud_blocker.model.Info import Info


class CloudProviderBase(ABC):
    @abstractmethod
    def fetch_ip_ranges(self, url: str) -> dict:
        pass

    @abstractmethod
    def extract_info(self, data: dict) -> List[Info]:
        pass

    def fetch(self) -> List[Info]:
        url = self.get_url()
        data = self.fetch_ip_ranges(url)
        return self.extract_info(data)

    @abstractmethod
    def get_url(self) -> str:
        pass
