import socket
from django.core.mail.backends.smtp import EmailBackend

class IPv4EmailBackend(EmailBackend):
    """
    Custom SMTP backend that forces IPv4 resolution to bypass IPv6 routing 
    issues common on cloud platforms like Railway.
    """
    def _get_connection(self):
        # Force IPv4 for the socket
        orig_getaddrinfo = socket.getaddrinfo

        def forced_getaddrinfo(*args, **kwargs):
            args = list(args)
            if len(args) > 0 and args[0] == self.host:
                return orig_getaddrinfo(args[0], args[1], socket.AF_INET, *args[3:])
            return orig_getaddrinfo(*args, **kwargs)

        socket.getaddrinfo = forced_getaddrinfo
        try:
            return super()._get_connection()
        finally:
            # Restore original getaddrinfo to avoid side effects
            socket.getaddrinfo = orig_getaddrinfo
