import { mutation, query } from "./_generated/server";
import { v } from "convex/values";

const taskStatus = v.union(
  v.literal("not started"),
  v.literal("in progress"),
  v.literal("completed"),
);

const entity = v.union(
  v.literal("dhl"),
  v.literal("jll"),
  v.literal("tiktok"),
  v.literal("cushman-wakefield"),
  v.literal("smrt"),
  v.literal("certis"),
  v.literal("toll-group"),
  v.literal("prudential"),
);

type TaskStatus = "not started" | "in progress" | "completed";

// Helper: resolve entity for backward compatibility (old data = dhl).
// entityTasks is new, so this only kicks in for rows pre-dating the entity
// optionality, but keeping the same pattern as tasks.ts for consistency.
function resolveEntity(e: string | undefined): string {
  return e || "dhl";
}

function matchesEntity(docEntity: string | undefined, filterEntity: string | undefined): boolean {
  return resolveEntity(docEntity) === resolveEntity(filterEntity);
}

// Read all entityTasks for one entity, sorted by id asc, with computed nextId.
export const getByEntity = query({
  args: {
    entity: v.optional(entity),
  },
  handler: async (ctx, args) => {
    const docs = await ctx.db
      .query("entityTasks")
      .withIndex("by_entity", (q) => q.eq("entity", args.entity))
      .collect();

    // If the optional entity arg is omitted, default to "dhl" partition (mirrors tasks.ts).
    const target = resolveEntity(args.entity);

    const filtered = docs.filter((d) => matchesEntity(d.entity, target));
    const sorted = filtered.sort((a, b) => a.id - b.id);
    const nextId = sorted.reduce((max, t) => Math.max(max, t.id), 0) + 1;

    return {
      entity: target,
      nextId,
      tasks: sorted,
    };
  },
});

// Read all entityTasks across all entities (admin/global view).
export const getAll = query({
  args: {},
  handler: async (ctx) => {
    const docs = await ctx.db.query("entityTasks").collect();
    return docs.sort((a, b) => {
      const ea = resolveEntity(a.entity);
      const eb = resolveEntity(b.entity);
      if (ea === eb) return a.id - b.id;
      return ea.localeCompare(eb);
    });
  },
});

// Create a new entityTask. id auto-increments per (entity) when omitted.
export const create = mutation({
  args: {
    entity: v.optional(entity),
    date: v.string(),
    description: v.string(),
    owner: v.string(),
    deadline: v.string(),
    status: taskStatus,
    id: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    const target = resolveEntity(args.entity);
    const now = Date.now();

    // Compute next id for the (entity) partition if not provided.
    let nextId = args.id;
    if (nextId === undefined) {
      const latest = await ctx.db
        .query("entityTasks")
        .withIndex("by_entity_id", (q) => q.eq("entity", target))
        .order("desc")
        .first();
      nextId = (latest?.id ?? 0) + 1;
    }

    return await ctx.db.insert("entityTasks", {
      id: nextId,
      entity: target,
      date: args.date,
      description: args.description,
      owner: args.owner,
      deadline: args.deadline,
      status: args.status,
      createdAt: now,
      updatedAt: now,
    });
  },
});

// Update an entityTask. Required: (entity, id). All other fields optional.
export const update = mutation({
  args: {
    id: v.number(),
    entity: v.optional(entity),
    date: v.optional(v.string()),
    description: v.optional(v.string()),
    owner: v.optional(v.string()),
    deadline: v.optional(v.string()),
    status: v.optional(taskStatus),
  },
  handler: async (ctx, args) => {
    const target = resolveEntity(args.entity);
    const matches = await ctx.db
      .query("entityTasks")
      .withIndex("by_entity_id", (q) => q.eq("entity", target).eq("id", args.id))
      .collect();

    const task = matches.find((t) => matchesEntity(t.entity, target));
    if (!task) {
      throw new Error(`entityTask not found for ${target}:${args.id}`);
    }

    const patch: {
      date?: string;
      description?: string;
      owner?: string;
      deadline?: string;
      status?: TaskStatus;
      updatedAt: number;
    } = {
      updatedAt: Date.now(),
    };

    if (args.date !== undefined) patch.date = args.date;
    if (args.description !== undefined) patch.description = args.description;
    if (args.owner !== undefined) patch.owner = args.owner;
    if (args.deadline !== undefined) patch.deadline = args.deadline;
    if (args.status !== undefined) patch.status = args.status;

    await ctx.db.patch(task._id, patch);
    return { ok: true };
  },
});

// Hard-delete an entityTask by (entity, id).
export const deleteTask = mutation({
  args: {
    id: v.number(),
    entity: v.optional(entity),
  },
  handler: async (ctx, args) => {
    const target = resolveEntity(args.entity);
    const matches = await ctx.db
      .query("entityTasks")
      .withIndex("by_entity_id", (q) => q.eq("entity", target).eq("id", args.id))
      .collect();

    const task = matches.find((t) => matchesEntity(t.entity, target));
    if (!task) {
      return { ok: false, deleted: false };
    }

    await ctx.db.delete(task._id);
    return { ok: true, deleted: true };
  },
});
