# k9s field notes: the parts the cheat sheets get wrong

> **Short, illustrated version:** [`linkedin-article.md`](linkedin-article.md) —
> 556 words and four diagrams, written for LinkedIn's long-form editor.
> This file is the full reference behind it.

*Verified against k9s **v0.51.0** — source read at the release tag, binary run
against a live cluster. Every keybinding below cites the file and line it comes
from. Nothing here is quoted from another blog post.*

---

## Why I wrote this

Search for a k9s cheat sheet and you get the same twelve keys, copied between
posts for six years. Some of them are now wrong. One of the most-repeated tips —
`:popeye` — does not exist in the version I am running, and hasn't for a while.

That is the problem with keybinding content: it ages badly and nobody re-checks
it. A wrong shortcut costs you thirty seconds; a wrong shortcut in a cluster
incident costs more, and the correction lives in the comments forever.

So I did it differently. I cloned k9s at the `v0.51.0` tag, ran that exact
binary against a kind cluster, and read the key-binding tables in the source
rather than trusting anyone's summary. What follows is what the code actually
does, with citations. Where I could not verify something, I say so.

---

## 1. k9s has browser history, and almost nobody uses it

This is the finding that surprised me most. Three global keys:

| Key | Action |
|---|---|
| `[` | Go Back |
| `]` | Go Forward |
| `-` | Last View |

```go
ui.KeyLeftBracket:  ui.NewSharedKeyAction("Go Back", a.previousCommand, false),
ui.KeyRightBracket: ui.NewSharedKeyAction("Go Forward", a.nextCommand, false),
ui.KeyDash:         ui.NewSharedKeyAction("Last View", a.lastCommand, false),
```
> `internal/view/app.go:259-261`

`-` is the one worth building a habit around. It is the shell's `cd -`: bounce
between the last two views. Deployments → pod logs → `-` → back to deployments,
without retyping `:deploy`. `[` and `]` walk the full history stack, the way a
browser does.

Note the guard in the same file: these only fire when you are **not** in command
mode (`app.go:735, 749, 765`). Inside a `:` prompt, `[` is just a bracket.

## 2. Ctrl-Z shows you only what is broken

`Ctrl-Z` is bound to "Toggle Faults" (`internal/view/table.go:233`). It filters
the current table down to rows k9s considers faulty.

The mechanism is worth knowing, because it explains the failure mode:

```go
func (t *TableData) filterToast() *RowEvents {
	rr := NewRowEvents(10)
	idx, ok := t.header.IndexOf("VALID", true)
	if !ok {
		return rr
	}
	...
}
```
> `internal/model1/table_data.go:221-235`

k9s keeps a hidden `VALID` column. `Ctrl-Z` keeps every row where that column is
non-empty — i.e. where something is wrong.

**The gotcha:** if the current view has no `VALID` column, `IndexOf` fails and
the function returns an *empty* set. The table goes blank. That is not a hang
and not a lost connection — it is `Ctrl-Z` on a view that has no fault concept.
Press it again to come back. It reads exactly like a bug until you find those
four lines.

## 3. The filter language is four different languages

Press `/` to filter (`internal/view/table.go:232`). What you type next is parsed
into one of four modes:

| Type | Mode | Verified at |
|---|---|---|
| `nginx` | regular expression | `table_data.go:156` |
| `!nginx` | **inverse** — everything that does not match | `helpers.go:21-26` |
| `-l app=web` | **label selector** | `helpers.go:29-35` |
| `-f nginx` | **fuzzy** match | `helpers.go:38-45` |

The two prefix forms are real regexes in the source, not folklore:

```go
fuzzyRx = regexp.MustCompile(`\A-f\s?([\w-]+)\b`)
labelRx = regexp.MustCompile(`\A\-l`)
```
> `internal/helpers.go:14-15`

Two things fall out of reading that:

- The `\A` anchors mean the prefix must be at the **very start**. `/pods -l app=web`
  is a plain regex search, not a label filter.
- The space in `-f\s?` is optional — `-fnginx` works as well as `-f nginx`.
- `!` is the plainest win of the four: `/!kube-` hides system noise in every
  namespace-wide view.

## 4. Marking rows for bulk work

| Key | Action | Verified at |
|---|---|---|
| `Space` | Mark / unmark row | `table.go:228` |
| `Ctrl-Space` | Mark a **range** | `table.go:229` |
| `Ctrl-\` | Clear all marks | `table.go:230` |

`Ctrl-Space` is the one people miss: mark a row, move down, `Ctrl-Space`, and
everything between is marked. Then delete or describe the set in one action.

`Ctrl-\` matters because marks survive view changes. Clearing them deliberately
is safer than assuming they are gone — particularly before pressing `Ctrl-D`.

## 5. Sorting without reaching for the mouse

| Key | Sorts by |
|---|---|
| `Shift-N` | Name |
| `Shift-A` | Age |
| `Shift-S` | Status |
| `Shift-O` | **the column you have selected** |

> `internal/view/table.go:235-238`

`Shift-O` is the general case that makes the other three redundant — it sorts by
whatever column the cursor sits in, which covers CPU, memory, restarts and any
custom column you have configured.

## 6. The alias list, straight from the source

These are hard-coded, not from anyone's config file:

```go
a.declare(client.HlpGVR, "h", "?")
a.declare(client.QGVR,   "q", "q!", "qa", "Q")
a.declare(client.AliGVR, "alias", "a")
a.declare(client.HmGVR,  "charts", "chart", "hm")
a.declare(client.DirGVR, "dir", "d")
a.declare(client.CtGVR,  "context", "ctx")
a.declare(client.UsrGVR, "user", "usr")
a.declare(client.GrpGVR, "group", "grp")
a.declare(client.PfGVR,  "portforward", "pf")
a.declare(client.BeGVR,  "benchmark", "bench")
a.declare(client.SdGVR,  "screendump", "sd")
a.declare(client.PuGVR,  "pulse", "pu", "hz")
a.declare(client.XGVR,   "xray", "x")
a.declare(client.WkGVR,  "workload", "wk")
```
> `internal/config/alias.go:185-198`

Three of these deserve more attention than they get:

- **`:wk`** — the workload view, added in v0.30.0 and described in that release
  note as "similar to `kubectl get all`". One view, every workload kind.
- **`:x`** — xray, a tree view of a resource and everything hanging off it.
  The fastest way to see why a Service has no endpoints.
- **`:usr` / `:grp`** — RBAC from the other direction: pick a user or group and
  see what it can actually do.

And `Ctrl-A` opens the full alias list at any time (`app.go:262`), so you never
have to remember this table.

## 7. `:popeye` is gone

Every second k9s tutorial tells you to press `:popeye` for a cluster audit.

In v0.51.0 there is **no occurrence of the string "popeye" in any `.go` file in
the repository.** I checked the whole tree. The last release notes that mention
it are v0.31.9 and v0.32.2.

I could not determine the exact release that removed it — I worked from a shallow
clone with no history to bisect, so I am not going to guess a version number.
What I can state precisely: it is not in v0.51.0, and typing `:popeye` will get
you nothing. Popeye still exists as a separate CLI; it is the *integration* that
went away.

## 8. Custom jumps — the feature nobody writes about

This one is genuinely obscure and genuinely useful. You can redefine what
`Enter` does on a given resource type.

Two examples ship in the repo's `jumps/` directory:

```yaml
# jumps/certificates.yaml
jumps:
  "cert-manager.io/v1/certificates":
    targetGVR: "v1/secrets"
    fieldSelector: "metadata.name={{.metadata.name}}"
    targetNamespace: "{{.metadata.namespace}}"
```

```yaml
# jumps/karpenter.yaml
jumps:
  "karpenter.sh/v1/nodepools":
    targetGVR: "v1/nodes"
    labelSelector: "karpenter.sh/nodepool={{.metadata.name}}"
```

Press `Enter` on a cert-manager Certificate and you land on the Secret it
produced. Press `Enter` on a Karpenter NodePool and you get its Nodes.

The hook is explicit in the source — custom jumps are checked *before* the
default Enter behaviour:

```go
// Check for custom jump rules first
if rule, ok := b.App().CustomJumps().GetRule(b.GVR()); ok {
	if err := customJump(b.app, b.GVR(), path, rule); err != nil {
		b.app.Flash().Errf("Custom jump failed: %s", err)
	}
	return nil
}
// Fall back to default behavior
```
> `internal/view/browser.go:460-473` (v0.51.0; the same block sits at 464-473 on current `master`)

Those are Go templates over the selected object, so any CRD that references
another resource by name or label can become a one-keystroke jump. If you run
operators with CRDs, this is the highest-value hour you can spend on your k9s
config.

Config lives in `jumps.yaml` — path in section 10.

## 9. Custom hotkeys

The shipped template is one commented-out example, which is probably why this
feature stays invisible:

```yaml
hotKeys:
  # shift-0:
  #   shortCut: Shift-0
  #   description: View Workloads
  #   command: wk k8s-app=cilium
```
> `internal/config/templates/hotkeys.yaml`

`command` takes anything you would type at the `:` prompt, filter included. Bind
the three views you open twenty times a day and stop typing them.

## 10. Where the config actually lives

Straight from `k9s info` on v0.51.0:

```
Config:            ~/.config/k9s/config.yaml
Custom Views:      ~/.config/k9s/views.yaml
Custom Jumps:      ~/.config/k9s/jumps.yaml
Plugins:           ~/.config/k9s/plugins.yaml
Hotkeys:           ~/.config/k9s/hotkeys.yaml
Aliases:           ~/.config/k9s/aliases.yaml
Skins:             ~/.config/k9s/skins
```

If you are following an older guide that says `~/.k9s/`, that moved. Run
`k9s info` rather than trusting the path in any post, including this one — it
resolves XDG variables for your machine.

## 11. Two flags worth knowing before you open a production cluster

```
--readonly    Sets readOnly mode by overriding readOnly configuration setting
--write       Sets write mode by overriding the readOnly configuration setting
```
> `k9s --help`, v0.51.0

`--readonly` disables the destructive commands. On any cluster where you are
looking rather than changing, it is the flag to alias into your shell. `--write`
exists to override a config file that sets read-only globally — which is the
better default to set once in `config.yaml`.

Also useful, all verified from `--help` on this version: `-c` to pick the
opening view (`k9s -c pods`), `-A` for all namespaces, `--crumbsless`,
`--logoless`, `--splashless` to strip the chrome, and `-r` to change the refresh
rate.

---

## How this was verified, and what I could not check

**Method.** Source read at the `v0.51.0` tag (commit `558caaf`), then every
claim re-checked against the current `master` of the repository. Line numbers
are given for v0.51.0; the code is unchanged on `master` and the citations
resolve there too, with one exception noted inline where the line numbers have
shifted by four. The binary was v0.51.0, run against a local kind cluster
(Kubernetes v1.37.0); `--help` and `info` output are quoted from that run, not
from documentation.

**Limits, stated plainly:**

- Keybindings are quoted from the binding tables in source. I did not press all
  of them one by one in the TUI — a terminal UI does not automate cleanly, and I
  would rather cite the code than claim a test I did not run.
- The exact release that dropped popeye is unknown to me (shallow clone, no
  history). I state only that it is absent in v0.51.0.
- Everything is version-qualified because it needs to be. If you are on a
  different release, `Ctrl-A` and `?` are the two keys that tell you the truth
  for your build.

**If you find an error here, open an issue.** That is the point of publishing it
in a repository rather than as a screenshot.

---

*k9s is by Fernand Galiana and its contributors, Apache-2.0. This document is
independent field notes, not affiliated with the project.*
