# Releasing

Releases are cut by the **Release** GitHub Actions workflow
(`workflow_dispatch`). It reads the version from `gradle.properties`, runs
`mise run check`, verifies compatibility, signs the zip, creates the bare
`X.Y.Z` GitHub Release with the changelog as its notes, and publishes to the
JetBrains Marketplace default channel.

## One-time setup

1. Create a JetBrains account and vendor profile at
   <https://plugins.jetbrains.com>.
2. Generate a signing key and self-signed certificate chain. You create these
   yourself with `openssl`; JetBrains issues none of them:
   ```bash
   openssl genpkey -aes-256-cbc -algorithm RSA -out private_encrypted.pem -pkeyopt rsa_keygen_bits:4096
   openssl rsa -in private_encrypted.pem -out private.pem
   openssl req -key private.pem -new -x509 -days 3650 -out chain.crt -subj "/CN=Adam Jarvis"
   base64 -i private.pem | tr -d '\n' > private.b64
   base64 -i chain.crt | tr -d '\n' > chain.b64
   ```
   `PRIVATE_KEY_PASSWORD` is the passphrase you type at the first prompt. With
   the unencrypted `private.pem` produced above it is ignored, so any value works.
3. Add repository secrets (`gh secret set <NAME> -R Jarvvski/tokyo-night-intellij`):
   - `CERTIFICATE_CHAIN` = contents of `chain.b64`
   - `PRIVATE_KEY` = contents of `private.b64`
   - `PRIVATE_KEY_PASSWORD` = your passphrase (any value with the unencrypted key)
   - `PUBLISH_TOKEN` = token from <https://plugins.jetbrains.com/author/me/tokens>
4. Upload the first version manually through the Marketplace web UI (JetBrains
   requires the initial publication to be manual). Run the workflow once with
   `dry_run` enabled to produce a signed zip, then upload it from the GitHub
   Release.

## Cutting a release

1. Move the `## Unreleased` changelog section to a dated `## X.Y.Z` heading and
   bump `version` in `gradle.properties`.
2. Land and push.
3. Run the **Release** workflow (Actions > Release > Run workflow).

See [`docs/adr/0005-distribute-via-marketplace-and-releases.md`](adr/0005-distribute-via-marketplace-and-releases.md)
for the rationale.
