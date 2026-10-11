# Cacophony's site

The public pages of [Cacophony](https://zelosleone.itch.io/cacophony), a native Apple Music player
for Windows, served at https://zelosleone.github.io/cacophony-site/:

- `privacy.html`: what the app sends, and to whom.
- `THIRD-PARTY-NOTICES.txt`: the licenses of what the app is made with.
- `token.json`: a MusicKit developer token, signed again every month by `.github/workflows/publish.yml`
  (`tools/mint.py`, with the key in the repository's secrets). Apple Music needs one with every
  request; the app builds one in and fetches this one when its own nears its expiry. The app
  accepts it only if it carries the signature of Cacophony's key.

Cacophony isn't made, endorsed or sponsored by Apple. Apple Music is a trademark of Apple Inc.