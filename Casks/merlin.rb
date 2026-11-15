cask "merlin" do
  version "0.2.0"
  sha256 "a5d3b6715ebfb869a6187d649acc5186b9ea42f60e678f57e1143df1e42a96f6"

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
