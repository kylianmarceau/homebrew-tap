cask "merlin" do
  version "0.5.13"
  sha256 "a0c876a997ac6e920e3202f7b15c74dd422a36cfe59ac288db8e7972b2bedb90"

  url "https://github.com/kylianmarceau/merlin/releases/download/v#{version}/Merlin-#{version}-arm64.dmg"
  name "Merlin"
  desc "Chromium-based browser with Vim-style keyboard navigation"
  homepage "https://github.com/kylianmarceau/merlin"

  livecheck do
    url :url
    strategy :github_latest
  end

  depends_on arch: :arm64
  depends_on macos: :sonoma

  app "Merlin.app"

  # Quits a running Merlin before an upgrade or uninstall replaces the app.
  uninstall quit: "io.github.kylianmarceau.merlin"

  # `brew uninstall --zap` also removes Merlin's data: the paths in Merlin's
  # README, "Uninstalling".
  zap trash: [
    "~/.config/modal_browser",
    "~/.local/share/modal_browser",
    "~/Library/Application Support/Merlin",
    "~/Library/Caches/Merlin",
    "~/Library/HTTPStorages/io.github.kylianmarceau.merlin",
    "~/Library/Preferences/io.github.kylianmarceau.merlin.plist",
    "~/Library/WebKit/io.github.kylianmarceau.merlin",
  ]

  caveats <<~EOS
    Merlin is not notarized by Apple.
    After the first launch attempt, open System Settings > Privacy & Security
    and click Open Anyway for Merlin, then confirm Open.

    Upgrading quits Merlin first. Your browser profile and settings are kept.
  EOS
end
