# Glossary

Domain Prime and its engines use a small set of words. Here is each one in plain terms.

| Term | Plain meaning |
|---|---|
| **tree** | Your whole install: one top folder, lines of work under it, projects under those. |
| **nexus** | A line of work. It groups projects and holds awareness of them, not their work. A nexus is also a node of the nexus above it. |
| **top nexus** | The root of the tree. In an install, that's Domain Prime. It is the one nexus that is not anyone's node. |
| **node** | A project: a folder of real work with its own rules. |
| **chair** | The agent's seat in one nexus or node. Every chair keeps its own rules, memory, and mail. |
| **constitution** | A chair's own rule file, usually `AGENTS.md`. It stops at the chair's edge. |
| **registry** | The nexus's list of its nodes, kept in `nexus.md`. It also marks which chairs are sensitive. |
| **step-in** | Working inside a chair from above. The agent loads that chair's constitution first and works under it. |
| **sensitive chair** | A chair marked private in the registry. It publishes less, stays hidden on the dashboard until shown, and gates any mail crossing its walls. |
| **article** | One piece of standing guidance in Insitu, one markdown file. |
| **skill** | A procedure your AI client exposes as `/name`. |
| **role** | A named bundle of articles and skills that a kind of chair subscribes to as a unit. |
| **pack** | A versioned bundle of articles, roles, and skills from outside your vault. |
| **shelf** | Where an install keeps its packs. |
| **protocol** | The composed set of guidance for one chair, written into files your AI client already loads. |
| **sitting** | One working session. Context Forge keeps a record of each. |
| **working files** | The current state of a chair's work in Context Forge, replaced in place. |
| **sitrep** | A short status report a chair publishes through Envoy. |
| **mail note** | A message between chairs, carried by Envoy and passed on by a nexus. |
| **board** | A nexus's ranked list of priorities, shown on the Envoy dashboard. |
| **library** | The Brain Forge vault, when an install includes one. |
| **raw / wiki** | Brain Forge's two layers: captures as they arrived, and the synthesis your agents maintain. |
