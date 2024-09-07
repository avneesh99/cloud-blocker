import ipaddress

from cloud_blocker.model.RadixNode import RadixNode


class RadixTree:
    def __init__(self):
        self.root = RadixNode()

    def insert(self, info):
        node = self.root
        cidr = info.cidr
        network = ipaddress.ip_network(cidr)
        bits = network.network_address.packed

        for i in range(network.prefixlen):
            bit = (bits[i // 8] >> (7 - (i % 8))) & 1
            if bit:
                if not node.right:
                    node.right = RadixNode()
                node = node.right
            else:
                if not node.left:
                    node.left = RadixNode()
                node = node.left

        node.is_leaf = True
        node.info = info

    def lookup(self, ip):
        node = self.root
        address = ipaddress.ip_address(ip).packed

        for i in range(len(address) * 8):
            if node.is_leaf:
                return node.info

            bit = (address[i // 8] >> (7 - (i % 8))) & 1
            if bit:
                if not node.right:
                    return None
                node = node.right
            else:
                if not node.left:
                    return None
                node = node.left

        return None if not node.is_leaf else node.info

