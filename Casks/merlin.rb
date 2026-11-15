cask "merlin" do
  version "0.3.0"
  sha256 "dd7214b478da5331b9bce7905a4fc3dd7ed8d1811f5e0fb6ed2d29ec6fedb0a2"

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

  caveats <<~EOS
    Merlin is ad-hoc signed and is not notarized by Apple.
    After the first launch attempt, open System Settings > Privacy & Security
    and click Open Anyway for Merlin, then confirm Open.

    Quit Merlin before upgrading. Your browser profile and settings are kept.
  EOS
end
