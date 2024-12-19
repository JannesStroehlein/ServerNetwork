"""
This represents a service that is running on a server
"""
class Service:
    def __init__(self, name : str, host : str, comment : str, urls: list[str], ports : list[int], proxy : str):
        """
        Initialize a new service
        :param name: The name of the service
        :param host: Server where the service is running
        :param comment: A comment about the service
        :param urls: List of URLs that the service is available at
        :param ports: List of ports that this service exposes
        :param proxy: A proxy service that is used to access this service
        """
        self.id = name.lower()
        self.name = name
        self.host = host
        self.comment = comment
        self.urls = urls
        self.ports = ports
        self.proxy = proxy

    def __str__(self):
        result = f'{self.name}'
        if self.host:
            result += f' ({self.host})'
        if self.comment:
            result += f' - {self.comment}'
