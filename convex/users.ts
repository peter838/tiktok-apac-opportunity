import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

const userRole = v.union(
  v.literal("admin"),
  v.literal("viewer"),
  v.literal("editor"),
  v.literal("staff"),
);

const userStatus = v.union(
  v.literal("active"),
  v.literal("inactive"),
  v.literal("pending"),
);

const countryCode = v.union(
  v.literal("cn"),
  v.literal("jp"),
  v.literal("au"),
  v.literal("my"),
  v.literal("id"),
  v.literal("in"),
  v.literal("sg"),
  v.literal("hk"),
  v.literal("th"),
  v.literal("vn"),
);

const entity = v.union(
  v.literal("dhl"),
  v.literal("tiktok"),
);

// Helper: resolve entity for backward compatibility (old data = dhl)
function resolveEntity(e: string | undefined): string {
  return e || "dhl";
}

function matchesEntity(docEntity: string | undefined, filterEntity: string | undefined): boolean {
  return resolveEntity(docEntity) === resolveEntity(filterEntity);
}

// Get all users for an entity
export const listUsers = query({
  args: {
    entity: v.optional(entity),
  },
  handler: async (ctx, args) => {
    const users = await ctx.db.query("users").collect();
    const filtered = users.filter((u) => matchesEntity(u.entity, args.entity));
    return filtered.sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0));
  },
});

// Get users by status for an entity
export const listUsersByStatus = query({
  args: {
    status: userStatus,
    entity: v.optional(entity),
  },
  handler: async (ctx, args) => {
    const users = await ctx.db
      .query("users")
      .withIndex("by_status", (q) => q.eq("status", args.status))
      .collect();
    const filtered = users.filter((u) => matchesEntity(u.entity, args.entity));
    return filtered.sort((a, b) => (b.createdAt || 0) - (a.createdAt || 0));
  },
});

// Get user by email for an entity
export const getUserByEmail = query({
  args: {
    email: v.string(),
    entity: v.optional(entity),
  },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_email", (q) => q.eq("email", args.email))
      .first();
    if (!user) return null;
    return matchesEntity(user.entity, args.entity) ? user : null;
  },
});

// Get user by ID
export const getUserById = query({
  args: {
    id: v.id("users"),
    entity: v.optional(entity),
  },
  handler: async (ctx, args) => {
    const user = await ctx.db.get(args.id);
    if (!user) return null;
    return matchesEntity(user.entity, args.entity) ? user : null;
  },
});

// Create a new user for an entity
export const createUser = mutation({
  args: {
    email: v.string(),
    name: v.string(),
    role: userRole,
    status: v.optional(userStatus),
    countries: v.optional(v.array(countryCode)),
    createdBy: v.optional(v.string()),
    entity: v.optional(entity),
  },
  handler: async (ctx, args) => {
    const targetEntity = resolveEntity(args.entity);

    // Check if user already exists for this entity
    const existing = await ctx.db
      .query("users")
      .withIndex("by_email", (q) => q.eq("email", args.email))
      .first();

    if (existing && matchesEntity(existing.entity, args.entity)) {
      throw new Error(`User with email ${args.email} already exists for ${targetEntity}`);
    }

    const now = Date.now();
    const userId = await ctx.db.insert("users", {
      email: args.email,
      name: args.name,
      entity: targetEntity,
      role: args.role,
      status: args.status || "active",
      countries: args.countries || [],
      createdAt: now,
      updatedAt: now,
      createdBy: args.createdBy || "system",
    });

    return { id: userId, email: args.email };
  },
});

// Update user
export const updateUser = mutation({
  args: {
    id: v.id("users"),
    entity: v.optional(entity),
    email: v.optional(v.string()),
    name: v.optional(v.string()),
    role: v.optional(userRole),
    status: v.optional(userStatus),
    countries: v.optional(v.array(countryCode)),
  },
  handler: async (ctx, args) => {
    const user = await ctx.db.get(args.id);
    if (!user) {
      throw new Error("User not found");
    }
    if (!matchesEntity(user.entity, args.entity)) {
      throw new Error(`User does not belong to ${resolveEntity(args.entity)}`);
    }

    // Check email uniqueness if changing email
    if (args.email && args.email !== user.email) {
      const existing = await ctx.db
        .query("users")
        .withIndex("by_email", (q) => q.eq("email", args.email))
        .first();
      if (existing && matchesEntity(existing.entity, args.entity)) {
        throw new Error(`User with email ${args.email} already exists for ${resolveEntity(args.entity)}`);
      }
    }

    const patch: {
      email?: string;
      name?: string;
      role?: "admin" | "viewer" | "editor";
      status?: "active" | "inactive" | "pending";
      countries?: ("cn" | "jp" | "au" | "my" | "id" | "in" | "sg" | "hk" | "th")[];
      updatedAt: number;
    } = {
      updatedAt: Date.now(),
    };

    if (args.email !== undefined) patch.email = args.email;
    if (args.name !== undefined) patch.name = args.name;
    if (args.role !== undefined) patch.role = args.role;
    if (args.status !== undefined) patch.status = args.status;
    if (args.countries !== undefined) patch.countries = args.countries;

    await ctx.db.patch(args.id, patch);
    return { ok: true, id: args.id };
  },
});

// Delete user
export const deleteUser = mutation({
  args: {
    id: v.id("users"),
    entity: v.optional(entity),
  },
  handler: async (ctx, args) => {
    const user = await ctx.db.get(args.id);
    if (!user) {
      return { ok: false, deleted: false, error: "User not found" };
    }
    if (!matchesEntity(user.entity, args.entity)) {
      return { ok: false, deleted: false, error: `User does not belong to ${resolveEntity(args.entity)}` };
    }

    await ctx.db.delete(args.id);
    return { ok: true, deleted: true, email: user.email };
  },
});

// Record user login
export const recordLogin = mutation({
  args: {
    email: v.string(),
    entity: v.optional(entity),
  },
  handler: async (ctx, args) => {
    const user = await ctx.db
      .query("users")
      .withIndex("by_email", (q) => q.eq("email", args.email))
      .first();

    if (!user || !matchesEntity(user.entity, args.entity)) {
      return { ok: false, error: "User not found" };
    }

    await ctx.db.patch(user._id, {
      lastLoginAt: Date.now(),
      updatedAt: Date.now(),
    });

    return { ok: true };
  },
});

// Get user stats for an entity
export const getUserStats = query({
  args: {
    entity: v.optional(entity),
  },
  handler: async (ctx, args) => {
    const users = await ctx.db.query("users").collect();
    const filtered = users.filter((u) => matchesEntity(u.entity, args.entity));

    return {
      total: filtered.length,
      active: filtered.filter((u) => u.status === "active").length,
      inactive: filtered.filter((u) => u.status === "inactive").length,
      pending: filtered.filter((u) => u.status === "pending").length,
      admins: filtered.filter((u) => u.role === "admin").length,
      editors: filtered.filter((u) => u.role === "editor").length,
      viewers: filtered.filter((u) => u.role === "viewer").length,
    };
  },
});

// Seed initial admin user (for setup)
export const seedInitialAdmin = mutation({
  args: {
    email: v.string(),
    name: v.string(),
    entity: v.optional(entity),
  },
  handler: async (ctx, args) => {
    const targetEntity = resolveEntity(args.entity);
    const existing = await ctx.db
      .query("users")
      .withIndex("by_email", (q) => q.eq("email", args.email))
      .first();

    if (existing && matchesEntity(existing.entity, args.entity)) {
      return { ok: false, message: "Admin user already exists for this entity" };
    }

    const now = Date.now();
    const userId = await ctx.db.insert("users", {
      email: args.email,
      name: args.name,
      entity: targetEntity,
      role: "admin",
      status: "active",
      countries: ["cn", "jp", "au", "my", "id", "in", "sg", "hk", "th"],
      createdAt: now,
      updatedAt: now,
      createdBy: "system",
    });

    return { ok: true, id: userId, email: args.email };
  },
});
