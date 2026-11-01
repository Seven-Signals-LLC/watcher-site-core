#!/usr/bin/env python3
"""Site build: fetches the shared Watcher site core, then builds this site with it.

Copy this file into a site repo as tools/build.py. The core version to use is
the single line in core.version at the site root: a release tag such as v0.1.0,
or a commit SHA. Change that line to move the site onto a newer core.

    python3 tools/build.py                          normal build (downloads the core)
    WATCHER_CORE_PATH=../watcher-site-core python3 tools/build.py
                                                    build against a local core checkout

No dependencies beyond the Python 3 standard library.
"""
import io, os, pathlib, runpy, shutil, sys, tarfile, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
REPO = "Seven-Signals-LLC/watcher-site-core"


def core_dir():
    local = os.environ.get("WATCHER_CORE_PATH")
    if local:
        return pathlib.Path(local).resolve()
    ref = (ROOT / "core.version").read_text().strip()
    cache = ROOT / ".core-cache" / ref
    if not (cache / "build.py").exists():
        url = f"https://codeload.github.com/{REPO}/tar.gz/{ref}"
        print(f"fetching watcher-site-core {ref}")
        data = urllib.request.urlopen(url, timeout=60).read()
        tmp = cache.with_name(ref + ".tmp")
        shutil.rmtree(tmp, ignore_errors=True)
        with tarfile.open(fileobj=io.BytesIO(data)) as tar:
            tar.extractall(tmp, filter="data") if sys.version_info >= (3, 12) else tar.extractall(tmp)
        (inner,) = list(tmp.iterdir())
        shutil.rmtree(cache, ignore_errors=True)
        inner.rename(cache)
        shutil.rmtree(tmp, ignore_errors=True)
    return cache


core = core_dir()
sys.argv = [str(core / "build.py"), "--site", str(ROOT)]
runtime_path = str(core / "build.py")
runpy.run_path(runtime_path, run_name="__main__")
