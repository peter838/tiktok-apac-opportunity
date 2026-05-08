import { defineSchema, defineTable } from "convex/server";
import { v } from "convex/values";

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
);

const taskStatus = v.union(
  v.literal("not started"),
  v.literal("in progress"),
  v.literal("completed"),
);

const userRole = v.union(
  v.literal("admin"),
  v.literal("viewer"),
  v.literal("editor"),
);

const userStatus = v.union(
  v.literal("active"),
  v.literal("inactive"),
  v.literal("pending"),
);

export default defineSchema({
  tasks: defineTable({
    id: v.number(),
    countryCode,
    date: v.string(),
    description: v.string(),
    owner: v.string(),
    deadline: v.string(),
    status: taskStatus,
    createdAt: v.number(),
    updatedAt: v.number(),
  })
    .index("by_country", ["countryCode"])
    .index("by_country_and_id", ["countryCode", "id"]),

  countries: defineTable({
    code: countryCode,
    name: v.string(),
  }).index("by_code", ["code"]),

  users: defineTable({
    email: v.string(),
    name: v.string(),
    role: userRole,
    status: userStatus,
    countries: v.optional(v.array(countryCode)),
    createdAt: v.number(),
    updatedAt: v.number(),
    createdBy: v.optional(v.string()),
    lastLoginAt: v.optional(v.number()),
  })
    .index("by_email", ["email"])
    .index("by_status", ["status"])
    .index("by_role", ["role"]),
});
