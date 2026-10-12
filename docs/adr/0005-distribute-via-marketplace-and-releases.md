# Distribute via JetBrains Marketplace and GitHub Releases

The plugin is published to the [JetBrains Marketplace](https://plugins.jetbrains.com)
so anyone can install it from inside the IDE, and every version is also attached
to a GitHub Release so the signed zip is retrievable without the Marketplace.

Distribution is driven entirely by CI from a single manual trigger. A
`workflow_dispatch` **Release** workflow (`.github/workflows/release.yml`) reads
the version from `gradle.properties` (the single version of record), runs the
pre-land gate, verifies compatibility, signs the zip, creates the GitHub Release,
and publishes to the Marketplace.

Decisions:

- **Trigger is `workflow_dispatch`, not a tag push.** Landing is local (jj) and
  pushes belong to the owner; a manual "Run workflow" avoids requiring a local
  tag-and-push step. The workflow itself creates the bare `X.Y.Z` tag and the
  GitHub Release via `gh`.
- **Publish to the default channel automatically** on each release. No beta
  channel or approval gate.
- **Change notes come from `CHANGELOG.md`.** The build reads the section for the
  version being built into `<change-notes>` via `patchPluginXml`, so the
  Marketplace page shows what changed without manual editing.
- **Plugin Verifier runs before publish** (`verifyPlugin`) as a compatibility
  gate.
- **Signing uses the IntelliJ Platform Gradle Plugin's `signPlugin`** with an
  author RSA key and self-signed chain. Secrets (`CERTIFICATE_CHAIN`,
  `PRIVATE_KEY`, `PRIVATE_KEY_PASSWORD`, `PUBLISH_TOKEN`) live in GitHub Actions
  secrets; when they are absent, signing and publishing stay skipped so an
  ordinary `buildPlugin` needs no credentials.
- **The first publication is uploaded manually** through the Marketplace web UI,
  as JetBrains requires; only later versions are automated.

## Consequences

- Agents never push or release; the owner triggers releases and holds the
  signing key and Marketplace token.
- The first listing needs one manual upload before automation can publish.
- Re-running a release for an already-published version fails at the Marketplace
  upload (duplicate version); the GitHub Release is created first so the artifact
  is never lost.
- Version bumps follow the repo semver policy; the Marketplace rejects duplicate
  versions, so every release needs a fresh version in `gradle.properties`.

Status: accepted
