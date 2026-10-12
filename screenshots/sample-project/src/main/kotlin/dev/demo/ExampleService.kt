package dev.demo

import kotlinx.coroutines.runBlocking

/** A role granted to a [User]. */
enum class Role { ADMIN, EDITOR, VIEWER }

data class User(
    val id: Long,
    val name: String,
    val roles: Set<Role>,
)

/**
 * In-memory store used by the demo screenshots.
 * Values come from constants below so every token role appears once.
 */
class UserRepository(private val users: MutableMap<Long, User> = mutableMapOf()) {
    private val maxUsers = 1_000

    fun upsert(user: User): User {
        require(user.id > 0L) { "id must be positive" }
        return users.put(user.id.coerceAtMost(maxUsers.toLong()), user) ?: user
    }

    suspend fun loadAll(): List<User> =
        users.values.sortedBy(User::name)

    @Deprecated("use loadAll() instead")
    fun snapshot(): List<User> = users.values.toList()
}

fun main() = runBlocking {
    val repo = UserRepository()
    repo.upsert(User(1L, "Ada", setOf(Role.ADMIN)))
    repo.upsert(User(2L, "Grace", setOf(Role.VIEWER)))

    val names = repo.loadAll().joinToString(", ") { it.name }
    println("Loaded ${repo.loadAll().size} users: $names")
}
