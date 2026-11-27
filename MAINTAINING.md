# Profile artwork

The header is an original pixel scene based on the ASCII monogram from this
repository's original README. `assets/monogram.txt` preserves its silhouette.
The tiny player is a fictional sprite. The game labels are decorative.

The artwork uses a built-in bitmap alphabet. It requires no external fonts,
image services, credentials, scheduled workflows, or tracking widgets.

To regenerate the GIF and still image from the repository root:

```sh
python -m venv .venv
# Activate the virtual environment for your shell.
python -m pip install -r scripts/requirements.txt
python scripts/build_profile.py
```

The README requests the PNG when the browser prefers reduced motion and links
to it explicitly as a fallback. Key identity details also appear as real text.
The GIF is 960 by 416 pixels with a 9.6-second loop.

Bio and project descriptions are adapted from the owner's public portfolio:

- [Portfolio](https://jancidlina.cz/)
- [Roadshow pro školy](https://jancidlina.cz/projekty/roadshow-pro-skoly)
- [HC Legio Prima](https://jancidlina.cz/projekty/hc-legio-prima)
- [Doučebnice](https://jancidlina.cz/projekty/doucebnice)

No private repository contents or course material are used in the profile.
