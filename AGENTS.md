# AGENTS.md — Domain Prime

This folder is the Domain Prime product. It holds the seed, the empty registry template, and the pin list for an install. It is not an installed tree.

Kind: node. It is the installable product.

The constitution changes only with the principal's explicit approval.

Records of an install stay out of this repo: status, sittings, a composed protocol, and a roster. The empty registry in `template/nexus.md` is the template an install writes. It is not a roster.

Domain Prime is the hub of its product family: insitu, envoy, context-forge, and brain-forge. Naming and linking them is fine. Names from a real install that runs them are not.

`docs/family-copy.md` is the family's shared wording: the system paragraph, each member's first sentence and role sentence, and the fictional walkthrough characters. Member READMEs borrow from it. `tools/make_svgs.py` regenerates the diagrams in every member's `docs/`. Run it from this checkout with the folder that holds all five checkouts: `python tools/make_svgs.py ..`

This checkout is public. Stage paths by name. Enable the hygiene hook in each clone with `git config core.hooksPath .githooks`; name checks read an untracked `.git/hygiene-denylist`, one term per line. The README's first sentence is the GitHub description.
