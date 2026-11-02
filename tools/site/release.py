"""What the site and the web builder publish: one release of one remix.

The generated manual, the remix overview table and `tools/web/publish.py` read
this, so a remix that is not listed here (octabam-bus, cxosc-core) has no
manual, no overview row and no builder entry. The remixes stay in the
repository.

On fork/ilia, BUILDER_REMIXES adds personal stacks to the web builder without
putting them in the official manual (gen_pages / gen_manual still use REMIXES).
"""

VERSION = "v0.4"          # the git tag the builder's patches are built from
REMIXES = ("octabam",)
# Web builder dropdown (fork tip). Official site keeps REMIXES only.
BUILDER_REMIXES = ("octabam", "latest", "vrcs-cx")
