class Info:
    __slots__ = ['cidr', 'cloud_provider', 'cloud_region']

    def __init__(self, cidr=None, cloud_provider=None, cloud_region=None):
        self.cidr = cidr
        self.cloud_provider = cloud_provider
        self.cloud_region = cloud_region

    def __repr__(self):
        return f"Info(cidr={self.cidr}, cloud_provider={self.cloud_provider}, cloud_region={self.cloud_region})"

    def to_dict(self):
        return {
            'cidr': self.cidr,
            'cloud_provider': self.cloud_provider,
            'cloud_region': self.cloud_region
        }

    @classmethod
    def from_dict(cls, data):
        return cls(**data)
