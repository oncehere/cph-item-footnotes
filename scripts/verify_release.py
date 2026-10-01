#!/usr/bin/env python3
"""Verify public artifact bytes and paths; also enforce checks under python -O."""
import hashlib
import json
from pathlib import Path
import re
import stat
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MOD_ID = 'cph_item_footnotes'
REQUIRED_PATCHES = {'cph-item-footnotes-hooks-a43a8f2-to-candidate.patch',
                    'cph-item-footnotes-fixes-32a2a03-to-candidate.patch'}


def require(condition, message):
    if not condition:
        raise ValueError(message)


def safe_path(name, base=ROOT, *, directory=False):
    require(isinstance(name, str) and bool(name), 'Nonempty relative path required')
    relative = Path(name)
    require(not relative.is_absolute() and '..' not in relative.parts, 'Unsafe artifact path: '+name)
    path = base / relative
    require(path.resolve().is_relative_to(ROOT.resolve()), 'Artifact escapes release root: '+name)
    current = path
    while current != ROOT:
        require(not current.is_symlink(), 'Symlink in artifact path: '+name)
        require(current.is_relative_to(ROOT), 'Artifact escapes release root: '+name)
        current = current.parent
    require(path.is_dir() if directory else path.is_file(), 'Missing artifact: '+name)
    return path


def sha256(path):
    digest = hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def checked_file(name, record, base=ROOT):
    path = safe_path(name, base)
    require(isinstance(record, dict) and type(record.get('bytes')) is int and record['bytes'] >= 0,
            'Invalid file size record: '+name)
    expected = record.get('sha256')
    require(isinstance(expected, str) and re.fullmatch('[0-9a-f]{64}', expected) is not None,
            'Invalid SHA256 record: '+name)
    require(path.stat().st_size == record['bytes'] and sha256(path) == expected, 'Changed file: '+name)
    return path


def verify():
    manifest = json.loads(safe_path('manifest.json').read_text(encoding='utf-8'))
    require(manifest.get('schema_version') == 1 and manifest.get('mod_id') == MOD_ID, 'Invalid release identity')
    version = manifest.get('version')
    require(isinstance(version, str) and re.fullmatch(r'[0-9]+\.[0-9]+\.[0-9]+', version) is not None,
            'Invalid release semantic version')
    package = safe_path('mod/'+MOD_ID, directory=True)
    actual = {}
    for path in sorted(package.rglob('*')):
        require(not path.is_symlink(), 'Symlink in MOD package')
        require(path.resolve().is_relative_to(ROOT), 'MOD path escapes release root')
        if path.is_file():
            actual[path.relative_to(package).as_posix()] = sha256(path)
    require(actual and actual == manifest.get('package_file_hashes'), 'MOD files differ from the frozen manifest')
    require(isinstance(manifest.get('files'), dict) and manifest['files'], 'Missing release file records')
    for name, record in manifest['files'].items():
        checked_file(name, record)
    metadata = json.loads(safe_path('mod/'+MOD_ID+'/modinfo.json').read_text(encoding='utf-8'))
    require(isinstance(metadata, list) and len(metadata) == 1 and metadata[0].get('type') == 'MOD_INFO', 'Invalid native MOD metadata')
    require(metadata[0].get('id') == MOD_ID and metadata[0].get('dependencies') == ['ccb'], 'Invalid MOD dependencies')
    artworks = json.loads(safe_path('mod/'+MOD_ID+'/data/ascii_art.json').read_text(encoding='utf-8'))
    for artwork in artworks:
        require(artwork.get('type') == 'ascii_art' and isinstance(artwork.get('picture'), list)
                and 1 <= len(artwork['picture']) <= 12, 'Invalid native artwork')
        for line in artwork['picture']:
            require(isinstance(line, str) and len(line) <= 41 and all(32 <= ord(char) <= 126 for char in line),
                    'Invalid printable ASCII artwork')
    archive_name = MOD_ID+'-v'+version+'.zip'
    require(archive_name in manifest['files'], 'Archive is not bound by release manifest')
    archive = safe_path(archive_name)
    with zipfile.ZipFile(archive) as zipped:
        members = zipped.infolist()
        names = [member.filename for member in members]
        require(len(names) == len(set(names)), 'Duplicate ZIP member')
        require(set(names) == {MOD_ID+'/'+name for name in actual}, 'ZIP paths differ from the MOD package')
        for member in members:
            mode = stat.S_IFMT(member.external_attr >> 16)
            require(not member.is_dir() and mode in (0, stat.S_IFREG), 'ZIP member is not a regular file: '+member.filename)
            name = member.filename[len(MOD_ID)+1:]
            require(hashlib.sha256(zipped.read(member)).hexdigest() == actual[name], 'ZIP bytes differ: '+name)
    patches = safe_path('engine-patches', directory=True)
    sums = safe_path('SHA256SUMS', patches)
    recorded = set()
    for line in sums.read_text(encoding='utf-8').splitlines():
        require('  ' in line, 'Malformed engine SHA256SUMS line')
        expected, name = line.split('  ', 1)
        require(re.fullmatch('[0-9a-f]{64}', expected) is not None and name not in recorded,
                'Invalid or duplicate engine checksum')
        recorded.add(name)
        require(sha256(safe_path(name, patches)) == expected, 'Changed engine artifact: '+name)
    actual_engine_files = {path.relative_to(patches).as_posix() for path in patches.rglob('*') if path.is_file()}
    require(recorded == actual_engine_files - {'SHA256SUMS'}, 'Engine checksum inventory differs')
    actual_patches = {path.name for path in patches.glob('*.patch')}
    require(actual_patches == REQUIRED_PATCHES, 'Required engine patch inventory differs')
    patch_manifest = json.loads(safe_path('source-hashes/manifest.json', patches).read_text(encoding='utf-8'))
    records = patch_manifest.get('patches')
    require(isinstance(records, list) and len(records) == len(REQUIRED_PATCHES), 'Missing engine patch records')
    require({record.get('path') for record in records} == REQUIRED_PATCHES, 'Engine patch manifest inventory differs')
    for record in records:
        path = checked_file(record['path'], record, patches)
        data = path.read_bytes()
        require(b'/home/' not in data and b'/tmp/' not in data, 'Private path in patch: '+path.name)
    print(json.dumps({'status': 'PASS', 'version': version, 'counts': manifest['content']['counts'],
                      'archive_sha256': sha256(archive)}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    verify()
