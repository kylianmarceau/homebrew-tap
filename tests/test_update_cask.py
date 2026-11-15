import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location("update_cask", Path(__file__).resolve().parents[1] / "scripts/update_cask.py")
updater = importlib.util.module_from_spec(spec)
spec.loader.exec_module(updater)


class UpdateCaskTest(unittest.TestCase):
    def release(self, tag="v0.2.0", **extra):
        name = f"Merlin-{tag[1:]}-arm64.dmg"
        base = f"https://github.com/kylianmarceau/merlin/releases/download/{tag}/"
        return dict(tag_name=tag, draft=False, prerelease=False,
                    assets=[dict(name=n, browser_download_url=base+n) for n in (name, name+".sha256")], **extra)

    def test_rejects_beta_draft_and_foreign_download(self):
        for tag in ("v0.2.0-beta.20", "v0.2.0\n", "arbitrary"):
            with self.assertRaises(ValueError):
                updater.release_asset(self.release(tag))
        for flag in ("draft", "prerelease"):
            release = self.release()
            release[flag] = True
            with self.assertRaises(ValueError):
                updater.release_asset(release)
        release = self.release()
        release["assets"][0]["browser_download_url"] = "https://example.com/merlin.dmg"
        with self.assertRaises(ValueError):
            updater.release_asset(release)

    def test_checksum_must_match_filename_and_github_digest(self):
        checksum = "a" * 64
        text = checksum + "  Merlin-0.2.0-arm64.dmg\n"
        self.assertEqual(updater.checksum_from(text, "Merlin-0.2.0-arm64.dmg", "sha256:"+checksum), checksum)
        for content, name, digest in ((text, "other.dmg", None), (text, "Merlin-0.2.0-arm64.dmg", "sha256:"+"b"*64),
                                     (text+"extra\n", "Merlin-0.2.0-arm64.dmg", None)):
            with self.assertRaises(ValueError):
                updater.checksum_from(content, name, digest)

    def test_version_upgrade_preserves_cask_and_prevents_replacement(self):
        old = 'cask "merlin" do\n  version "0.2.0"\n  sha256 "' + "a"*64 + '"\n  app "Merlin.app"\nend\n'
        new = updater.update_text(old, "0.2.1", "b"*64)
        self.assertIn('version "0.2.1"', new)
        self.assertIn('app "Merlin.app"', new)
        self.assertEqual(updater.update_text(old, "0.2.0", "a"*64), old)
        for version, checksum in (("0.1.9", "b"*64), ("0.2.0", "b"*64)):
            with self.assertRaises(ValueError):
                updater.update_text(old, version, checksum)
