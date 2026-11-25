cask "merlin" do
  version "0.5.16"
  sha256 "383ae349fc0f4d5fbfce22d5c95eb66c909bcbc6e12d19f8be2d21ff2e1ac79b"

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
