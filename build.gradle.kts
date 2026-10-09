plugins {
    kotlin("jvm") version "2.4.21"
    id("org.jetbrains.intellij.platform") version "2.19.0"
}

group = "dev.jarvis.tokyonight"
version = providers.gradleProperty("version").get()

repositories {
    mavenCentral()
    intellijPlatform {
        defaultRepositories()
    }
}

dependencies {
    intellijPlatform {
        // Target the 2026.3 line (build 263). A bare "2026.3" is not a resolvable
        // artifact version - EAP builds are published as concrete 263.x builds - so
        // pin the newest 263 EAP multi-OS archive. Re-pin as newer 263 builds land.
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

        vendor {
            name = "Adam Jarvis"
            url = "https://github.com/jarvvski"
        }

        ideaVersion {
            sinceBuild = "263"
            untilBuild = provider { null }
        }
    }
}
