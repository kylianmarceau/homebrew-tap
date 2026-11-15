# Merlin for Homebrew

Install [Merlin](https://github.com/kylianmarceau/merlin), a Chromium-based
browser with Vim-style keyboard navigation. Requires an Apple Silicon Mac
and macOS 14 Sonoma or later.

```sh
brew install --cask kylianmarceau/tap/merlin
```

After the first launch attempt, open **System Settings > Privacy & Security**
and click **Open Anyway** for Merlin, then confirm **Open**. Merlin is ad-hoc
signed and is not notarized by Apple. Homebrew uses the normal macOS
quarantine protections.

Quit Merlin, then update it with:

```sh
brew update
brew upgrade --cask kylianmarceau/tap/merlin
```

Your browser profile and settings are kept. Homebrew does not upgrade it in
the background; run the commands above when you want to update.

If Merlin was installed by dragging it into Applications, quit it and use
`brew install --cask --adopt kylianmarceau/tap/merlin` to let Homebrew manage
the existing app. If Homebrew reports that its files differ, move the old
`Merlin.app` to the Trash and run the normal install command. Keep your
profile and configuration folders.

This is Merlin's own tap, separate from Homebrew's central cask repository.
Always use the full `kylianmarceau/tap/merlin` name to avoid other packages
called Merlin.

## Maintaining releases

The updater checks Merlin's latest stable GitHub Release hourly and on
manual workflow runs. GitHub schedules can be delayed. Beta releases and
drafts are ignored. Each published stable release must include:

- `Merlin-<version>-arm64.dmg`
- `Merlin-<version>-arm64.dmg.sha256`, containing the SHA-256 and exact filename

The updater checks the filename, release URL, version and GitHub asset digest
before committing the new version and checksum. It refuses downgrades and
changed checksums for an existing version. No extra access token or secret
is needed: the workflow's token only writes to this tap.

To update immediately after publishing a stable release:

```sh
gh workflow run update-merlin.yml --repo kylianmarceau/homebrew-tap
```

For a local check:

```sh
python3 -m unittest discover -s tests -v
python3 scripts/update_cask.py
brew style Casks/merlin.rb
```
