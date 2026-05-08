import { ConvexHttpClient } from "convex/browser";

const convexUrl =
  (globalThis as { CONVEX_URL?: string }).CONVEX_URL ||
  "";

if (!convexUrl) {
  throw new Error("Convex URL is not configured. Set globalThis.CONVEX_URL.");
}

export const convexClient = new ConvexHttpClient(convexUrl);

export async function convexQuery<T>(name: string, args?: Record<string, unknown>): Promise<T> {
  return convexClient.query(name, args || {}) as Promise<T>;
}

export async function convexMutation<T>(name: string, args?: Record<string, unknown>): Promise<T> {
  return convexClient.mutation(name, args || {}) as Promise<T>;
}
