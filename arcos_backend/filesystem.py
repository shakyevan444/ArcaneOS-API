import magic
import os
import shutil


class Filesystem:
    _root: str
    _template: str | None
    _userspace_size: int

    def __init__(self, root_path: str, template_path: str | None, userspace_size: int):
        self._root = root_path
        self._template = template_path
        self._userspace_size = userspace_size

        os.makedirs(self._root, exist_ok=True)

    def deploy_template(self, userspace: int, path: str):
        self._validate_path(userspace, path)
        if self._template is None:
            return

        for (parent, folders, files) in os.walk(self._template, followlinks=True):
            fullpath = parent[len(self._template) + 1:]
            for folder in folders:
                self.mkdir(userspace, os.path.join(path, fullpath, folder))
            for file in files:
                with open(os.path.join(parent, file), 'rb') as f:
                    self.write(userspace, os.path.join(path, fullpath, file), f.read())

    def get_userspace_size(self):
        return self._userspace_size

    def get_root(self):
        return self._root


class Userspace:
    _id: int
    _fs: Filesystem
    _root: str

    def __init__(self, fs: Filesystem, id: int):
        self._fs = fs
        self._id = id
        self._root = os.path.join(self._fs.get_root(), str(id))

        if not os.path.isdir(self._root):
            os.mkdir(os.path.join(self._root, str(id)))
            self._fs.deploy_template(self._id, '.')

    def get_root(self):
        return self._root

    def delete(self):
        shutil.rmtree(self._root)

    def mkdir(self, path: str):
        self._validate_path(path)
        os.mkdir(os.path.join(self._root, path))

    def listdir(self, path: str):
        self._validate_path(path)
        path = os.path.join(self._root, path)

        files, directories = [], []

        for felder in os.listdir(path):
            fullpath = os.path.join(path, felder)
            if os.path.isfile(fullpath):
                files.append(fullpath)
            else:
                directories.append(fullpath)

        return files, directories

    def write(self, path: str, data: bytes):
        self._validate_path(path)

        if self.get_size('.') + len(data) > self._fs.get_userspace_size():
            raise RuntimeError("data is too large (not enough space)")

        with open(os.path.join(self._root, path), 'wb') as f:
            f.write(data)

    def remove(self, path: str):
        self._validate_path(path)

        path = os.path.join(self._root, path)

        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.unlink(path)

    def move(self, source: str, destination: str):
        self._validate_path(source)
        self._validate_path(destination)
        shutil.move(os.path.join(self._root, source),
                    os.path.join(self._root, destination))

    def read(self, path: str) -> bytes:
        self._validate_path(path)
        with open(os.path.join(self._root, path), 'rb') as f:
            return f.read()

    def get_size(self, path: str) -> int:
        self._validate_path(path)
        # yes this is a oneliner, why? ngl idk, so... why not™
        # i am too lazy to redo the thing at this point
        return sum(sum(os.path.getsize(os.path.join(dirpath, file)) for file in files) for dirpath, files, _ in os.walk(walk_path)) if os.path.isdir(walk_path := os.path.join(self._root, path)) else os.path.getsize(os.path.join(walk_path))

    def get_mime(self, path: str) -> str:
        self._validate_path(path)
        return magic.from_file(os.path.join(self._root, path), mime=True)

    def get_tree(self, path: str):
        self._validate_path(path)
        base_path = self._root

        paths = []
        for dirpath, _, filepaths in os.walk(os.path.join(base_path, path)):
            paths.extend([os.path.join(dirpath[len(base_path) + 1:], filepath) for filepath in filepaths])

        return paths

    def _validate_path(self, path: str):
        userspace_root = os.path.abspath(self._root)
        requested_path = os.path.abspath(os.path.join(userspace_root, path))

        if not requested_path.startswith(userspace_root):
            raise ValueError("path breaks out of the filesystem")
