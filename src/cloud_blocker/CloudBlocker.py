import os
import json
import time
from typing import Optional

from cloud_blocker.scripts import CloudProvider
from cloud_blocker.model.RadixTree import RadixTree
from cloud_blocker.model.Info import Info
from cloud_blocker.scripts.AWSProvider import AWSProvider
from cloud_blocker.scripts.GCPProvider import GCPProvider
from cloud_blocker.scripts.OracleProvider import OracleProvider

CACHE_FILE = "ip_ranges_cache.json"
CACHE_EXPIRY = 86400  # 24 hours in seconds


class CloudBlocker:
    def __init__(self, providers: list[CloudProvider]):
        self.tree = RadixTree()
        self.providers = providers

    def initialize_tree(self):
        cache_data = self._load_cache()
        if cache_data:
            self._build_tree_from_cache(cache_data)
        else:
            self._fetch_and_build_tree()

    def lookup(self, ip: str) -> Optional[Info]:
        return self.tree.lookup(ip)

    @staticmethod
    def _load_cache():
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, 'r') as f:
                cache_data = json.load(f)
            if time.time() - cache_data['timestamp'] < CACHE_EXPIRY:
                return cache_data['data']
        return None

    @staticmethod
    def _save_cache(data):
        cache_data = {
            'timestamp': time.time(),
            'data': [info.to_dict() for info in data]
        }
        with open(CACHE_FILE, 'w') as f:
            json.dump(cache_data, f)

    def _build_tree_from_cache(self, cache_data):
        for info_dict in cache_data:
            info = Info.from_dict(info_dict)
            self.tree.insert(info)

    def _fetch_and_build_tree(self):
        all_infos = []
        for provider in self.providers:
            infos = provider.fetch()
            all_infos.extend(infos)
            for info in infos:
                self.tree.insert(info)

        self._save_cache(all_infos)
