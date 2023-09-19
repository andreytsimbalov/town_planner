from datetime import datetime

from constants import Ext


class Files:
    data_dir = './data'

    @classmethod
    def filename(cls, prefix: str = 'file', ext: str = Ext.txt):
        """Return: 'data_dir/file_1695130955.txt' """
        return f'{cls.data_dir}/{prefix}_{int(datetime.now().timestamp())}{ext}'
