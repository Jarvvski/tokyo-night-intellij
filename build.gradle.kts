plugins {
    kotlin("jvm") version "2.4.21"
    id("org.jetbrains.intellij.platform") version "2.19.0"
}

group = "dev.jarvis.tokyonight"
version = providers.gradleProperty("version").get()

val pluginVersion = providers.gradleProperty("version")

// Marketplace change notes come from the CHANGELOG.md section for the version
// being built (single source of truth). fileContents tracks the file as a
// configuration-cache input so edits invalidate the task correctly.
val changeNotesFromChangelog = providers.fileContents(
    layout.projectDirectory.file("CHANGELOG.md"),
).asText.map { raw ->
    raw.split(Regex("(?m)^## "))
        .drop(1)
        .firstOrNull { section ->
            val heading = section.lineSequence().first().trim()
            heading == pluginVersion.get() || heading.startsWith("${pluginVersion.get()} ")
        }
        ?.lineSequence()
        ?.drop(1)
        ?.joinToString("\n")
        ?.trim()
        .orEmpty()
}

repositories {
    mavenCentral()
    intellijPlatform {
        defaultRepositories()
    }
}

dependencies {
    intellijPlatform {
        // Build against the newest pinned archive so resources are validated on the
        // latest platform, while supporting installation back to IDEA 2026.2 (build
        // 262). A bare "2026.3" is not a resolvable artifact version - EAP builds are
        // published as concrete 263.x builds - so pin the newest multi-OS EAP archive.
        // Re-pin as newer builds land.
        intellijIdea("263.6259.32-EAP") {
            useInstaller = false
        }
    }
}

kotlin {
    jvmToolchain(21)
}

intellijPlatform {
    instrumentCode = false
    buildSearchableOptions = false

    pluginConfiguration {
        id = "dev.jarvis.tokyonight"
        name = "Tokyo Night"
        version = project.version.toString()
        changeNotes.set(changeNotesFromChangelog)

        vendor {
            name = "Adam Jarvis"
            url = "https://github.com/jarvvski"
        }

        ideaVersion {
            sinceBuild = "262"
            untilBuild = provider { null }
        }
    }

    // Secrets are supplied by environment variables (locally or from GitHub
    // Actions secrets). When they are absent, signing and publishing stay
    // skipped, so an ordinary buildPlugin needs no credentials.
    signing {
        certificateChain.set(providers.environmentVariable("CERTIFICATE_CHAIN"))
        privateKey.set(providers.environmentVariable("PRIVATE_KEY"))
        password.set(providers.environmentVariable("PRIVATE_KEY_PASSWORD"))
    }

    publishing {
        token.set(providers.environmentVariable("PUBLISH_TOKEN"))
    }
}
