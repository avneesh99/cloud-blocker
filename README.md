# cloud-blocker

CloudBlocker is a Python library designed to efficiently determine whether a given IP address originates from one of the major public cloud providers, including AWS, GCP, or Oracle Cloud. It's fast, efficient, and easy to use in your projects.

## Features
**Cloud Detection:** Identify if an IP address belongs to AWS, GCP, Oracle Cloud, or other supported cloud providers.

**High Efficiency:** Utilizes a Radix Tree for rapid IP lookups, ensuring minimal latency even with large datasets.

**Caching:** Implements a caching mechanism to store IP ranges, reducing the need for frequent external requests and improving performance.

**Extensible Architecture:** Easily add support for additional cloud providers by extending the CloudProviderBase class.

**Automatic Cache Management:** Automatically refreshes cached IP ranges based on a configurable expiry time.


## Installation

```
git clone https://github.com/avneesh99/cloud-blocker
cd cloudblocker
pip install -e .
```

## Using it as a middleware
Here's a simple example of how to use CloudBlocker in a sample flask app:


```
providers = [AWSProvider(), GCPProvider(), OracleProvider()]
cloud_blocker = CloudBlocker(providers=providers)
cloud_blocker.initialize_tree()

@app.before_request
def before_request_func():
    ip = request.headers.get("x-forwarded-for")
    if ip:
        ip = ip.split(',')[0]
        cloud_blocker_info = cloud_blocker.lookup(ip)
        if cloud_blocker_info:
            print(f"Intercepted request from : {cloud_blocker_info.cloud_provider}")
```

## How It Works

### Getting the CIDR List
All cloud providers publish the list of CIDR ranges that they have. For example: AWS publishes it's CIDR on https://ip-ranges.amazonaws.com/ip-ranges.json. So once you have this list, you can check if the ip of incoming request falls under one of these CIDRs.

### Storing it efficiently and Querying it super fast
When dealing with large IP address datasets, such as AWS's 7,000+ CIDRs encompassing over a million IP addresses, we need to consider both storage efficiency and query performance. Let's explore two approaches and their trade-offs:

**Hashtable Approach:**

- **Pros:** Extremely fast lookups (O(1) time complexity)
- **Cons:** Memory-intensive, especially for large datasets

**CIDR List Approach:**

- **Pros:** Memory-efficient
- **Cons:** Slow lookups (O(n) time complexity)

A more balanced solution leverages the hierarchical nature of CIDRs. CIDRs are essentially IP prefixes. For example, 172.30.30.0/24 indicates that the first 24 bits of the IP are fixed, while the rest are variable (except for the broadcast IP).

**Optimal Solution:** Radix Tree
We can use a trie-like data structure called a Radix tree to store CIDR ranges efficiently. Here's why it's effective:

**Memory Efficiency:** Stores only the CIDR ranges, not individual IP addresses
**Fast Lookups:** Time complexity of O(M), where M is the maximum depth of the tree (typically 32 for IPv4)
Prefix Matching: Naturally suits the hierarchical structure of IP addresses

By using a Radix tree, we achieve a balance between storage efficiency and query performance, making it an ideal choice for managing large IP address datasets.


## Caching Mechanism
To enhance performance and reduce the need for frequent external API calls, CloudBlocker implements a robust caching system:

- Cache Storage: IP ranges are cached in a JSON file (ip_ranges_cache.json) after the initial fetch.
- Cache Expiry: Cached data is considered valid for 24 hours (CACHE_EXPIRY = 86400 seconds). After this period, the cache is refreshed.
- Automatic Management: The library automatically handles loading from cache, validating expiry, and updating the cache as needed.
- This caching strategy ensures that CloudBlocker remains both efficient and up-to-date with the latest IP ranges from supported cloud providers


## Extensibility
CloudBlocker is designed with extensibility in mind, allowing developers to add support for additional cloud providers with ease. To extend CloudBlocker to other clouds:

**Create a New Provider Class:** Extend the CloudProviderBase abstract class.

```
from cloud_blocker.scripts.CloudProvider import CloudProviderBase
from cloud_blocker.model.Info import Info
from typing import List
import requests

class NewCloudProvider(CloudProviderBase):
    def get_url(self) -> str:
        return "https://newcloudprovider.com/ip-ranges.json"

    def fetch_ip_ranges(self, url: str) -> dict:
        response = requests.get(url)
        response.raise_for_status()
        return response.json()

    def extract_info(self, data: dict) -> List[Info]:
        return [
            Info(cidr=prefix['ip_prefix'], cloud_provider="NewCloud", cloud_region=prefix['region'])
            for prefix in data.get('prefixes', [])
        ]
```

**Integrate the New Provider:** Add the new provider to the list of providers when initializing CloudBlocker.

```
from cloud_blocker.scripts.NewCloudProvider import NewCloudProvider

providers = [AWSProvider(), GCPProvider(), OracleProvider(), NewCloudProvider()]
cloud_blocker = CloudBlocker(providers)
cloud_blocker.initialize_tree()
```


## License
This project is licensed under the MIT License.

