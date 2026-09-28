"""Exercise the release CLI against disposable Git repositories."""

import json
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
import zipfile


BUILDER = Path(__file__).resolve().parents[1] / 'dev-tools/buildScripts/build_release.py'
MODULE_ID = 'test-translation'
REPOSITORY = 'https://github.com/example/test-translation'


class BuildReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix='phb-release-test-')
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.name', 'Release Test')
        self.git('config', 'user.email', 'release-test@example.invalid')
        self.git('config', 'commit.gpgsign', 'false')
        self.git('config', 'core.autocrlf', 'false')
        self.meta = {
            'id': MODULE_ID, 'version': '1.0.0',
            'url': REPOSITORY,
            'manifest': f'{REPOSITORY}/releases/latest/download/module.json',
            'download': f'{REPOSITORY}/releases/download/v1.0.0/{MODULE_ID}.zip',
            'esmodules': ['scripts/main.js'],
            'languages': [{'lang': 'es', 'path': 'lang/es.json'}],
        }
        self.write_json('module.json', self.meta)
        self.write_json('compendium/items.json', {'entries': {'id': {'name': 'Original'}}})
        self.write_json('lang/es.json', {'test': 'Spanish'})
        self.write('scripts/main.js', '// committed runtime\n')
        for name in ['README.md', 'README.en.md', 'LICENSE.md']:
            self.write(name, '# Fixture\n')
        self.write('CHANGELOG.md', '# Changelog\n\n## [1.0.0] - 2026-09-28\n')
        self.write('.gitignore', 'dist/\n')
        self.write('.gitattributes', '.gitignore export-ignore\n.gitattributes export-ignore\ntests/ export-ignore\ndev-tools/ export-ignore\n')
        self.write('tests/private-fixture.txt', 'must not be distributed\n')
        self.initial = self.commit()

    def git(self, *args):
        return subprocess.check_output(['git', *args], cwd=self.root, stderr=subprocess.PIPE)

    def write(self, name, text):
        path = self.root / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(text.encode('utf-8'))

    def write_json(self, name, value):
        self.write(name, json.dumps(value, ensure_ascii=False, indent=2) + '\n')

    def commit(self):
        self.git('add', '--all')
        self.git('commit', '-qm', 'fixture')
        return self.git('rev-parse', 'HEAD').decode().strip()

    def invoke(self, *args):
        return subprocess.run(
            [sys.executable, '-B', str(BUILDER), *args], cwd=self.root,
            capture_output=True, text=True, encoding='utf-8',
        )

    def success(self, *args):
        result = self.invoke(*args)
        self.assertEqual(result.returncode, 0, result.stderr)

    def failure(self, message, *args):
        result = self.invoke(*args)
        self.assertNotEqual(result.returncode, 0, result.stdout)
        self.assertIn(message, result.stderr)

    def assert_payload(self, output='dist', base=MODULE_ID, alias=True):
        folder = self.root / output
        versioned = folder / f'{base}-1.0.0.zip'
        with zipfile.ZipFile(versioned) as archive:
            manifest = archive.read(f'{MODULE_ID}/module.json')
            self.assertEqual(manifest, self.git('show', f'{self.initial}:module.json'))
            self.assertEqual(manifest, (folder / 'module.json').read_bytes())
            self.assertEqual(archive.read(f'{MODULE_ID}/compendium/items.json'),
                             self.git('show', f'{self.initial}:compendium/items.json'))
            self.assertTrue(all(name.startswith(MODULE_ID + '/') for name in archive.namelist()))
            self.assertFalse(any('/tests/' in name for name in archive.namelist()))
            self.assertIn(f'{MODULE_ID}/README.en.md', archive.namelist())
            self.assertIn(f'{MODULE_ID}/LICENSE.md', archive.namelist())
        if alias:
            self.assertEqual(versioned.read_bytes(), (folder / f'{base}.zip').read_bytes())
        else:
            self.assertFalse((folder / f'{base}.zip').exists())

    def test_clean_checkout_of_another_version_uses_selected_commit(self):
        self.meta['version'] = '2.0.0'
        self.write_json('module.json', self.meta)
        self.write_json('compendium/items.json', {'entries': {}})
        self.commit()
        self.success('--ref', self.initial)
        self.assert_payload()
        self.assertFalse((self.root / 'dist' / f'{MODULE_ID}-2.0.0.zip').exists())

    def test_allow_dirty_ignores_staged_and_unstaged_changes(self):
        self.meta['version'] = '9.9.9'
        self.write_json('module.json', self.meta)
        self.git('add', 'module.json')
        self.write_json('compendium/items.json', {'local': 'not committed'})
        self.write('.gitattributes', '')
        self.write('untracked.txt', 'not committed\n')
        self.success('--allow-dirty')
        self.assert_payload()

    def test_dirty_checkout_requires_explicit_opt_in(self):
        self.write('README.md', '# Changed\n')
        self.failure('Working tree is not clean')
        self.assertFalse((self.root / 'dist').exists())

    def test_annotated_tag_short_full_and_explicit_with_sha(self):
        self.git('tag', '-a', 'v1.0.0', '-m', 'release')
        variants = [('--ref', 'v1.0.0'), ('--ref', 'refs/tags/v1.0.0'),
                    ('--ref', self.initial, '--release-tag', 'v1.0.0')]
        for number, args in enumerate(variants):
            with self.subTest(args=args):
                output = f'dist/case-{number}'
                self.success(*args, '--dist', output)
                self.assert_payload(output)

    def test_mismatched_tag_is_rejected_in_all_invocation_forms(self):
        self.git('tag', 'v9.0.0')
        variants = [('--ref', 'v9.0.0'), ('--ref', 'refs/tags/v9.0.0'),
                    ('--ref', self.initial, '--release-tag', 'v9.0.0')]
        for args in variants:
            with self.subTest(args=args):
                self.failure('does not match module.json version', *args)

    def test_matching_version_tag_must_point_to_selected_commit(self):
        self.git('tag', 'v1.0.0')
        self.write('README.md', '# Later commit, same version\n')
        self.commit()
        self.failure('does not point to the selected commit', '--release-tag', 'v1.0.0')

    def test_tagged_release_requires_changelog_entry(self):
        self.write('CHANGELOG.md', '# Changelog\n\n## [Unreleased]\n')
        self.commit()
        self.git('tag', 'v1.0.0')
        self.failure('missing from CHANGELOG.md', '--ref', 'v1.0.0')

    def test_invalid_pack_json_is_rejected(self):
        self.write('compendium/items.json', '{invalid json')
        self.commit()
        self.failure('Invalid JSON in archive: compendium/items.json')
        self.assertFalse((self.root / 'dist' / 'module.json').exists())

    def test_release_rejects_floating_wrong_version_and_wrong_asset_downloads(self):
        for download in [f'{REPOSITORY}/releases/latest/download/{MODULE_ID}.zip',
                         f'{REPOSITORY}/releases/download/v0.9.0/{MODULE_ID}.zip',
                         f'{REPOSITORY}/releases/download/v1.0.0/other.zip', None]:
            with self.subTest(download=download):
                self.write_json('module.json', dict(self.meta, download=download))
                commit = self.commit()
                self.git('tag', '-f', 'v1.0.0')
                self.failure('Release download must point', '--ref', commit, '--release-tag', 'v1.0.0')
                self.assertFalse((self.root / 'dist').exists())

    def test_release_rejects_branch_or_missing_manifest_url(self):
        for manifest in ['https://raw.githubusercontent.com/example/test-translation/main/module.json', None]:
            with self.subTest(manifest=manifest):
                self.write_json('module.json', dict(self.meta, manifest=manifest))
                self.commit()
                self.git('tag', '-f', 'v1.0.0')
                self.failure('Release manifest must point', '--ref', 'v1.0.0')

    def test_release_rejects_invalid_repository_url(self):
        for url in [None, 'https://example.invalid/repo', REPOSITORY + '/']:
            with self.subTest(url=url):
                self.write_json('module.json', dict(self.meta, url=url))
                self.commit()
                self.git('tag', '-f', 'v1.0.0')
                self.failure('Release url must be a GitHub repository URL', '--ref', 'v1.0.0')

    def test_release_cannot_omit_or_rename_download_asset(self):
        self.git('tag', 'v1.0.0')
        for args in [('--no-alias',), ('--name', 'custom-archive')]:
            with self.subTest(args=args):
                self.failure('Release requires the default module ZIP alias', '--ref', 'v1.0.0', *args)

    def test_historical_commit_can_still_build_without_release_url_contract(self):
        self.meta.pop('url')
        self.meta.pop('manifest')
        self.meta.pop('download')
        self.write_json('module.json', self.meta)
        self.initial = self.commit()
        self.success('--ref', self.initial)
        self.assert_payload()

    def test_failed_release_url_validation_preserves_existing_artifacts(self):
        self.success()
        output = self.root / 'dist'
        before = {path.name: path.read_bytes() for path in output.iterdir()}
        self.write_json('module.json', dict(self.meta, download=f'{REPOSITORY}/releases/latest/download/{MODULE_ID}.zip'))
        self.commit()
        self.git('tag', 'v1.0.0')
        self.failure('Release download must point', '--ref', 'v1.0.0')
        self.assertEqual(before, {path.name: path.read_bytes() for path in output.iterdir()})

    def test_profile_preserves_historical_alias(self):
        alias = MODULE_ID + '-es'
        self.write_json('dev-tools/buildScripts/release-profile.json', {'archive_name': alias})
        self.meta['download'] = f'{REPOSITORY}/releases/download/v1.0.0/{alias}.zip'
        self.write_json('module.json', self.meta)
        self.initial = self.commit()
        self.git('tag', 'v1.0.0')
        self.success('--ref', 'v1.0.0')
        self.assert_payload(base=alias)

    def test_main_channel_is_explicit_and_version_download_remains_required(self):
        self.write_json('dev-tools/buildScripts/release-profile.json', {'manifest_channel': 'main'})
        self.meta['manifest'] = 'https://raw.githubusercontent.com/example/test-translation/main/module.json'
        self.write_json('module.json', self.meta)
        self.initial = self.commit()
        self.git('tag', 'v1.0.0')
        self.success('--ref', 'v1.0.0')
        self.assert_payload()
        self.write_json('module.json', dict(self.meta, download=f'{REPOSITORY}/releases/latest/download/{MODULE_ID}.zip'))
        self.commit()
        self.git('tag', '-f', 'v1.0.0')
        self.failure('Release download must point', '--ref', 'v1.0.0')

    def test_profile_is_read_from_selected_commit(self):
        self.write_json('dev-tools/buildScripts/release-profile.json', {'archive_name': 'later-alias'})
        self.commit()
        self.success('--ref', self.initial)
        self.assert_payload()

    def test_checksums_cover_each_output_asset(self):
        self.success()
        output = self.root / 'dist'
        lines = (output / 'SHA256SUMS.txt').read_text().splitlines()
        self.assertEqual(len(lines), 3)
        for line in lines:
            digest, name = line.split('  ')
            self.assertEqual(digest, hashlib.sha256((output / name).read_bytes()).hexdigest())

    def test_unexpected_distribution_file_is_rejected(self):
        self.write('staged.txt', 'local diff accidentally tracked\n')
        self.commit()
        self.failure('Unexpected distribution file: staged.txt')

    def test_declared_entry_cannot_be_excluded(self):
        attributes = (self.root / '.gitattributes').read_text()
        self.write('.gitattributes', attributes + 'scripts/main.js export-ignore\n')
        self.commit()
        self.failure('Missing manifest entry: scripts/main.js')

    def test_license_cannot_be_excluded(self):
        attributes = (self.root / '.gitattributes').read_text()
        self.write('.gitattributes', attributes + 'LICENSE.md export-ignore\n')
        self.commit()
        self.failure('Missing distribution files: LICENSE.md')

    def test_invalid_archive_name_and_manifest_identity_are_rejected(self):
        self.failure('Invalid archive name', '--name', '../outside')
        for key, value in [('id', '../outside'), ('version', '../outside')]:
            with self.subTest(key=key):
                meta = dict(self.meta, **{key: value})
                self.write_json('module.json', meta)
                self.commit()
                self.failure('Invalid module ' + key)

    def test_name_override_keeps_module_folder_and_no_alias_is_respected(self):
        self.success('--name', 'custom-archive', '--no-alias')
        self.assert_payload(base='custom-archive', alias=False)

    def test_failed_validation_does_not_replace_existing_artifacts(self):
        self.success()
        output = self.root / 'dist'
        before = {p.name: p.read_bytes() for p in output.iterdir()}
        self.write('compendium/items.json', '{invalid json')
        self.commit()
        self.failure('Invalid JSON in archive')
        self.assertEqual(before, {p.name: p.read_bytes() for p in output.iterdir()})


if __name__ == '__main__':
    unittest.main()
