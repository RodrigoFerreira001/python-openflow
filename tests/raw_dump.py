"""Help reading raw dump files."""
from pyof.foundation.utils import unpack_message


class RawDump:
    """A helper to deal with paths and reading raw files.

    Attributes:
        content (bytes): Raw file's content.
    """

    _HEADER_BYTES = 8  # According to OF Protocol specification

    def __init__(self, version, basename):
        """Information to locate the dump file.

        Args:
            version (str): OpenFlow protocol version, e.g. ``v0x01``.
            basename (str): Only the filename without extension.
                E.g. ``ofpt_echo_reply``.
        """
        self._path = 'raw/{}/{}.dat'.format(version, basename)

    def read(self):
        """Read the raw file.

        Returns:
            bytes: Raw file's content.
        """
        with open(self._path, 'rb') as file:
            return file.read()

    def unpack(self):
        """Unpack header and message from a byte sequence.

        Returns:
            The object type specified in the header with the coresponding
                header.
        """
        content = self.read()
        return unpack_message(content)
