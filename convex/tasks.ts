import { mutation, query } from "./_generated/server";
import { v } from "convex/values";
import { COUNTRY_NAMES, TASK_SEEDS } from "./seedData";

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

type CountryCode = "cn" | "jp" | "au" | "my" | "id" | "in" | "sg" | "hk" | "th";
type TaskStatus = "not started" | "in progress" | "completed";

function normalizeStatus(status: string | undefined): TaskStatus {
  if (status === "completed" || status === "done") return "completed";
  if (status === "in progress") return "in progress";
  if (status === "delayed" || status === "not started") return "not started";
  return "in progress";
}

export const getTasksByCountry = query({
  args: { countryCode },
  handler: async (ctx, args) => {
    const tasks = await ctx.db
      .query("tasks")
      .withIndex("by_country_and_id", (q) => q.eq("countryCode", args.countryCode))
      .collect();

    const sorted = tasks.sort((a, b) => a.id - b.id);
    const nextId = sorted.reduce((max, task) => Math.max(max, task.id), 0) + 1;

    return {
      countryCode: args.countryCode,
      nextId,
      tasks: sorted,
    };
  },
});

export const getAllTasks = query({
  args: {},
  handler: async (ctx) => {
    const tasks = await ctx.db.query("tasks").collect();
    return tasks.sort((a, b) => {
      if (a.countryCode === b.countryCode) return a.id - b.id;
      return a.countryCode.localeCompare(b.countryCode);
    });
  },
});

export const createTask = mutation({
  args: {
    countryCode,
    date: v.string(),
    description: v.string(),
    owner: v.string(),
    deadline: v.string(),
    status: taskStatus,
    id: v.optional(v.number()),
  },
  handler: async (ctx, args) => {
    const latest = await ctx.db
      .query("tasks")
      .withIndex("by_country_and_id", (q) => q.eq("countryCode", args.countryCode))
      .order("desc")
      .first();

    const nextId = (latest?.id ?? 0) + 1;
    const now = Date.now();

    return await ctx.db.insert("tasks", {
      id: args.id ?? nextId,
      countryCode: args.countryCode,
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

export const updateTask = mutation({
  args: {
    id: v.number(),
    countryCode,
    date: v.optional(v.string()),
    description: v.optional(v.string()),
    owner: v.optional(v.string()),
    deadline: v.optional(v.string()),
    status: v.optional(taskStatus),
  },
  handler: async (ctx, args) => {
    const task = await ctx.db
      .query("tasks")
      .withIndex("by_country_and_id", (q) => q.eq("countryCode", args.countryCode).eq("id", args.id))
      .first();

    if (!task) {
      throw new Error(`Task not found for ${args.countryCode}:${args.id}`);
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

export const deleteTask = mutation({
  args: {
    id: v.number(),
    countryCode,
  },
  handler: async (ctx, args) => {
    const task = await ctx.db
      .query("tasks")
      .withIndex("by_country_and_id", (q) => q.eq("countryCode", args.countryCode).eq("id", args.id))
      .first();

    if (!task) {
      return { ok: false, deleted: false };
    }

    await ctx.db.delete(task._id);
    return { ok: true, deleted: true };
  },
});

export const seedTasks = mutation({
  args: {},
  handler: async (ctx) => {
    const now = Date.now();
    const countryCodes = Object.keys(COUNTRY_NAMES) as CountryCode[];

    let countriesInserted = 0;
    for (const code of countryCodes) {
      const existingCountry = await ctx.db
        .query("countries")
        .withIndex("by_code", (q) => q.eq("code", code))
        .first();

      if (!existingCountry) {
        await ctx.db.insert("countries", {
          code,
          name: COUNTRY_NAMES[code],
        });
        countriesInserted += 1;
      }
    }

    let tasksInserted = 0;
    for (const [code, state] of Object.entries(TASK_SEEDS) as [CountryCode, (typeof TASK_SEEDS)[CountryCode]][]) {
      for (const task of state.tasks) {
        const existing = await ctx.db
          .query("tasks")
          .withIndex("by_country_and_id", (q) => q.eq("countryCode", code).eq("id", Number(task.id)))
          .first();

        if (existing) continue;

        await ctx.db.insert("tasks", {
          id: Number(task.id),
          countryCode: code,
          date: task.date || "",
          description: task.description || "",
          owner: task.owner || "",
          deadline: task.deadline || "",
          status: normalizeStatus(task.status) as TaskStatus,
          createdAt: now,
          updatedAt: now,
        });
        tasksInserted += 1;
      }
    }

    return {
      ok: true,
      countriesInserted,
      tasksInserted,
      totalCountries: countryCodes.length,
    };
  },
});
