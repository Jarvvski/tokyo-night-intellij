export interface User {
  id: number;
  name: string;
  email?: string;
}

export type Result<T> =
  | { ok: true; value: T }
  | { ok: false; error: string };

const BASE_URL = "/api/users";

/**
 * Fetches one user by id.
 */
export async function fetchUser(id: number): Promise<Result<User>> {
  const response = await fetch(`${BASE_URL}/${id}`);
  if (!response.ok) {
    return { ok: false, error: `HTTP ${response.status}` };
  }
  return { ok: true, value: await response.json() };
}

export function slugify(names: readonly string[]): string {
  return names.map((name) => name.trim().toLowerCase()).join("-");
}
