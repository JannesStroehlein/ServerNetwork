"""
Represents a connection between two services in the network
"""
class Connection:
    def __init__(self, protocol : str, origin : str, remote : str, comment : str = None):
        """
        Initialize a new connection
        :param protocol: The protocol used to connect
        :param origin: The origin service
        :param remote: The remote service
        :param comment: A comment about the connection
        """
        self.protocol = protocol
        self.origin = origin
        self.remote = remote
        self.comment = comment

    def __str__(self):
        result = f'{self.origin} -- {self.protocol} --> {self.remote}'
        if self.comment:
            result += f' - {self.comment}'
        return result