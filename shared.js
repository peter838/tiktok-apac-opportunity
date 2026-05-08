// === Shared utilities for TikTok Opportunity Intelligence ===

const TASK_TRACKER_DATA = window.TikTok_TASK_TRACKER_DATA || {
  countries: {
    cn: 'China',
    jp: 'Japan',
    au: 'Australia',
    my: 'Malaysia',
    id: 'Indonesia',
    in: 'India',
    sg: 'Singapore',
    hk: 'Hong Kong',
    th: 'Thailand',
  },
  seeds: {
    hk: {
      nextId: 12,
      tasks: [
        {
          id: 1,
          date: '2026-01-13',
          description: 'Contact PIC, JK, and Jian Min again to ensure their attendance for the annual business review and future project reviews.',
          owner: 'Catherine',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 2,
          date: '2026-01-13',
          description: 'Forward the Macau vendor registration link/system to Jian Min\'s email (jian.SIM@sausage.co) for completion.',
          owner: 'Lai',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 3,
          date: '2026-01-13',
          description: 'Forward the Macau vendor registration link/system to both Jian Min and Jackie.',
          owner: 'Catherine',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 4,
          date: '2026-01-13',
          description: 'Check with the team whether they can provide product price comparisons or cost-saving information to users, including cases where SourceSage offers better prices than the market, and consider referencing other online platforms\' promotional strategies.',
          owner: 'Catherine',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 5,
          date: '2026-01-13',
          description: 'Investigate the reasons for the 5 canceled orders in the past year to understand user issues or product selection problems.',
          owner: 'SourceSage team',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 6,
          date: '2026-01-13',
          description: 'Conduct one-to-one interviews or feedback sessions with selected existing and new users, including top spenders and those who have never used the platform, to identify obstacles, concerns, and potential improvements for SourceSage usage in Hong Kong.',
          owner: 'SourceSage team',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 7,
          date: '2026-01-13',
          description: 'Consider implementing regular monthly newsletters or targeted communications to end users highlighting new products, sales, or advantages of using SourceSage, as suggested by Gigi and Lai.',
          owner: 'SourceSage team',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 8,
          date: '2026-01-13',
          description: 'Review and improve response time and accuracy of replies, especially for urgent requests, from the Peter email address, including evaluating the hybrid human/AI support process.',
          owner: 'SourceSage team',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 9,
          date: '2026-01-13',
          description: 'In future, share any catering-related requests with SourceSage team via the designated email for quotation and sourcing support.',
          owner: 'Lai',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 10,
          date: '2026-01-13',
          description: 'Check internal inquiries to assess what types of items are frequently requested and discuss with SourceSage whether they can support these categories.',
          owner: 'Gigi / Lai',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 11,
          date: '2026-01-13',
          description: 'For IT equipment/hardware inquiries, provide support for sourcing and ensure product originality and quantity, as requested by Gigi and Lai.',
          owner: 'SourceSage team',
          deadline: '2026-03-31',
          status: 'in progress',
        },
      ],
      history: [],
    },
    sg: {
      nextId: 11,
      tasks: [
        {
          id: 1,
          date: '2026-04-04',
          description: 'Share detailed information (including previous purchasing data) for the top 6 users who have stopped or reduced buying from SourceSage, focusing on what items they were buying previously, with Janice and Ameer site to review.',
          owner: 'Jian',
          deadline: '2026-04-30',
          status: 'in progress',
        },
        {
          id: 2,
          date: '2026-04-04',
          description: 'Check if the identified users are currently buying certain items and report findings to the group.',
          owner: 'Ameer site',
          deadline: '2026-04-30',
          status: 'in progress',
        },
        {
          id: 3,
          date: '2026-04-04',
          description: 'Send product codes and corresponding unit rates (and available volume data) for Kumpulan products to Janice for competitive price review.',
          owner: 'Jian',
          deadline: '2026-04-30',
          status: 'in progress',
        },
        {
          id: 4,
          date: '2026-04-04',
          description: 'Initiate informal interviews or re-engagement (via email as first step) with PICs from each entity in Q1 2026 to understand user experience, bottlenecks, and 2026 sourcing opportunities.',
          owner: 'Jian/nuraina',
          deadline: '2026-04-30',
          status: 'in progress',
        },
        {
          id: 5,
          date: '2026-04-04',
          description: 'Suggest to the Singapore team what key actions led to success in Malaysia, and share learnings that could be applied in Singapore.',
          owner: 'nuraina',
          deadline: '2026-04-30',
          status: 'in progress',
        },
        {
          id: 6,
          date: '2026-04-04',
          description: 'Resend meeting invitations (including to Geraldine) for future quarterly meetings to ensure all relevant procurement/management contacts are included.',
          owner: 'Catherine',
          deadline: '2026-04-30',
          status: 'in progress',
        },
        {
          id: 7,
          date: '2026-04-04',
          description: 'Review and consider improvements to the ordering process for urgent/weekend items (e.g., flowers/reefs), including possible catalog creation for faster PO generation, as per Geraldine\'s feedback.',
          owner: 'Jian/SourceSage team',
          deadline: '2026-04-30',
          status: 'in progress',
        },
        {
          id: 8,
          date: '2026-04-04',
          description: 'Plan and execute outreach (email/Teams call) to top 6 declined users, with TikTok procurement team facilitating as needed, and report back on user feedback before the next meeting.',
          owner: 'All',
          deadline: '2026-04-30',
          status: 'in progress',
        },
        {
          id: 9,
          date: '2026-04-04',
          description: 'Inform SourceSage team of any upcoming RFPs or sourcing opportunities where SourceSage could participate.',
          owner: 'Janice/Ameer',
          deadline: '2026-04-30',
          status: 'in progress',
        },
        {
          id: 10,
          date: '2026-04-04',
          description: 'Meet again in April for the Quarter One project review.',
          owner: 'All',
          deadline: '2026-04-30',
          status: 'in progress',
        },
      ],
      history: [],
    },
    th: {
      nextId: 10,
      tasks: [
        {
          id: 1,
          date: '2026-01-14',
          description: 'Send Catherine the updated name list of relevant procurement team contacts for newsletter/announcement distribution after the call.',
          owner: 'Martin',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 2,
          date: '2026-01-14',
          description: 'Send email to thitikorn (Jack) with contact details for POCs at TikTok Express, Superchain, and DGF for follow-up on potential needs and increased POs.',
          owner: 'Yasha',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 3,
          date: '2026-01-14',
          description: 'Check with the sourcing manager responsible for MRO category regarding the next cycle of RFP 70 MRO orders and report back to Yasha_SourceSage.',
          owner: 'Martin',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 4,
          date: '2026-01-14',
          description: 'Document and circulate in writing the proposal for conducting online interviews with Thai users (with Thai translator) to understand barriers to using SourceSage, and coordinate next steps with TikTok Thailand team.',
          owner: 'Jian',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 5,
          date: '2026-01-14',
          description: 'Send meeting minutes to thitikorn (Jack) for coordination with PIC of e-commerce entity to schedule first training and provide guidebook for new users.',
          owner: 'Catherine',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 6,
          date: '2026-01-14',
          description: 'Provide PIC contact details to Catherine for onboarding/training of new e-commerce entity users.',
          owner: 'thitikorn (Jack)',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 7,
          date: '2026-01-14',
          description: 'Review internal data to identify categories/suppliers with low spend or one-time purchases, and shortlist users/requesters for potential redirection to SourceSage, supporting the increase in platform usage.',
          owner: 'Martin and TikTok Thailand team',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 8,
          date: '2026-01-14',
          description: 'Convey to Thai buyer team the recommendation to direct one-time/low-spend purchases to SourceSage when appropriate in 2026.',
          owner: 'Martin',
          deadline: '2026-03-31',
          status: 'in progress',
        },
        {
          id: 9,
          date: '2026-01-14',
          description: 'Discuss with catalog/category owner and provide feedback on desired improvements for the SourceSage platform and services for 2026.',
          owner: 'thitikorn (Jack)',
          deadline: '2026-03-31',
          status: 'in progress',
        },
      ],
      history: [],
    },
  },
};

const TASK_TRACKER_COUNTRIES = TASK_TRACKER_DATA.countries;
const TASK_TRACKER_SEEDS = TASK_TRACKER_DATA.seeds;

function initReveal() {
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible');
        if (entry.target.closest('.categories') || entry.target.classList.contains('category-list')) {
          document.querySelectorAll('.bar-fill').forEach(bar => {
            const w = bar.getAttribute('data-width');
            if (w) bar.style.width = w + '%';
          });
        }
      }
    });
  }, { threshold: 0.1, rootMargin: '0px 0px -50px 0px' });
  document.querySelectorAll('.reveal').forEach(el => observer.observe(el));
}

function initNav() {
  window.addEventListener('scroll', () => {
    const nav = document.getElementById('nav');
    if (nav) nav.classList.toggle('scrolled', window.scrollY > 50);
  });
}

function initBars() {
  window.addEventListener('load', () => {
    setTimeout(() => {
      document.querySelectorAll('.bar-fill').forEach(bar => {
        const rect = bar.getBoundingClientRect();
        if (rect.top < window.innerHeight) {
          const w = bar.getAttribute('data-width');
          if (w) bar.style.width = w + '%';
        }
      });
    }, 500);
  });
}

function formatQ1Month(month) {
  if (!month) return '';
  // Handle both "YYYY-MM" and "YYYY-MM-DD" formats
  const datePart = month.split('T')[0]; // Remove time component if present
  const parts = datePart.split('-');
  const year = parts[0];
  const mon = parts[1]; // Take only the month part, ignore day if present
  const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const idx = Math.max(0, Math.min(11, Number(mon || 1) - 1));
  return `${monthNames[idx]} ${year}`;
}

function initQ1Tooltips() {
  const points = document.querySelectorAll('.q1-chart-svg circle[data-month]');
  if (!points.length) return;

  let tooltip = document.querySelector('.q1-tooltip');
  if (!tooltip) {
    tooltip = document.createElement('div');
    tooltip.className = 'q1-tooltip';
    tooltip.setAttribute('role', 'status');
    tooltip.setAttribute('aria-live', 'polite');
    tooltip.innerHTML = '<div class="q1-tooltip-month"></div><div class="q1-tooltip-row"><span>PO count</span><strong></strong></div><div class="q1-tooltip-row"><span>PO value</span><strong></strong></div>';
    document.body.appendChild(tooltip);
  }

  const monthEl = tooltip.querySelector('.q1-tooltip-month');
  const countEl = tooltip.querySelectorAll('.q1-tooltip-row strong')[0];
  const valueEl = tooltip.querySelectorAll('.q1-tooltip-row strong')[1];

  const position = (point, event) => {
    const pad = 16;
    const rect = tooltip.getBoundingClientRect();
    const source = event && typeof event.clientX === 'number'
      ? { x: event.clientX, y: event.clientY }
      : (() => {
          const r = point.getBoundingClientRect();
          return { x: r.left + r.width / 2, y: r.top + r.height / 2 };
        })();
    const x = Math.min(window.innerWidth - rect.width - pad, source.x + 18);
    const y = Math.min(window.innerHeight - rect.height - pad, source.y + 18);
    tooltip.style.left = `${Math.max(pad, x)}px`;
    tooltip.style.top = `${Math.max(pad, y)}px`;
  };

  const show = (point, event) => {
    const month = formatQ1Month(point.dataset.month);
    monthEl.textContent = month;
    countEl.textContent = point.dataset.countLabel || '';
    valueEl.textContent = point.dataset.valueLabel || '';
    tooltip.classList.add('is-visible');
    position(point, event);
  };

  const hide = () => tooltip.classList.remove('is-visible');

  points.forEach((point) => {
    point.setAttribute('tabindex', '0');
    point.setAttribute('focusable', 'true');
    point.addEventListener('mouseenter', (event) => show(point, event));
    point.addEventListener('mousemove', (event) => position(point, event));
    point.addEventListener('mouseleave', hide);
    point.addEventListener('focus', (event) => show(point, event));
    point.addEventListener('blur', hide);
  });

  document.addEventListener('scroll', hide, { passive: true });
  window.addEventListener('resize', hide);
}

function fmtK(v) {
  if (v >= 1000) return (v / 1000).toFixed(1).replace(/\.0$/, '') + 'M';
  return Math.round(v) + 'K';
}

function fmtSGD(v) {
  return 'SGD ' + fmtK(v);
}

function fmtCostSaving(v) {
  if (v < 1) return 'SGD ' + (v * 1000).toFixed(0);
  return 'SGD ' + fmtK(v);
}

function fmtExact(v) {
  if (v === null || v === undefined) return null;
  return 'SGD ' + v.toLocaleString('en-US', {minimumFractionDigits: 2, maximumFractionDigits: 2});
}

// Load site data for cost savings and other metrics
let SITE_DATA_CACHE = null;
async function loadSiteData() {
  if (SITE_DATA_CACHE) return SITE_DATA_CACHE;
  try {
    const response = await fetch('../site-data.json');
    if (!response.ok) throw new Error('Failed to load site data');
    SITE_DATA_CACHE = await response.json();
    return SITE_DATA_CACHE;
  } catch (error) {
    console.warn('Could not load site data:', error);
    return {};
  }
}

function getCountryCostSaving(countryCode, siteData) {
  const data = siteData?.[countryCode];
  if (!data || data.cost_saving_k === undefined) return null;
  return {
    amount: data.cost_saving_k,
    percentage: data.cost_saving_pct || 0,
    formatted: fmtCostSaving(data.cost_saving_k),
    formattedPct: (data.cost_saving_pct || 0).toFixed(1) + '%'
  };
}

function renderCategoryBars(categories, containerID, regionalTotal) {
  var totalSpend = regionalTotal || 0;
  var maxP = Math.max(...categories.map(function(c) { return c.potential; }));
  // Use regional total if provided, otherwise fall back to max potential
  var scaleBase = totalSpend > 0 ? totalSpend : maxP;
  var el = document.getElementById(containerID);
  if (!el) return;
  categories.forEach(function(cat) {
    var gap = cat.potential - cat.observed;
    var pct = ((cat.observed / cat.potential) * 100).toFixed(0);
    var obsW = (cat.observed / scaleBase) * 100;
    var gapW = (gap / scaleBase) * 100;

    let obsLabel = '';
    let obsBadge = '';
    if (cat.observedExact !== null && cat.observedExact !== undefined) {
      obsLabel = fmtExact(cat.observedExact);
      obsBadge = '<span class="actual-badge">ACTUAL</span>';
    } else if (cat.isApproximate) {
      obsLabel = '~' + fmtSGD(cat.observed);
      obsBadge = '<span class="approx-badge">APPROX</span>';
    } else {
      obsLabel = fmtSGD(cat.observed);
    }

    el.innerHTML += `
      <div class="category-item">
        <div class="category-name">${cat.name}</div>
        <div class="category-bars split-lines">
          <div class="bar-row">
            <span class="bar-series-label observed-inline">Observed</span>
            <div class="bar-track" style="background:rgba(15, 23, 42, 0.06);">
              <div class="bar-fill observed" data-width="${obsW}" style="width:0%"></div>
            </div>
            <span class="bar-inline-label observed-inline">${obsLabel}</span>
            ${obsBadge}
          </div>
          <div class="bar-row">
            <span class="bar-series-label potential-inline">Gap</span>
            <div class="bar-track potential-track">
              <div class="bar-fill potential" data-width="${gapW}" style="width:0%"></div>
            </div>
            <span class="bar-inline-label potential-inline">${fmtSGD(gap)} gap</span>
          </div>
          <div class="bar-row bar-row-meta">
            <span class="bar-type-tag">Both lines scaled to ${fmtSGD(cat.potential)} total potential</span>
          </div>
        </div>
        <div class="category-gap">
          <span class="gap-value">${fmtSGD(gap)}</span>
          <span class="gap-pct">(${pct}% captured)</span>
        </div>
      </div>`;
  });
}

function renderHeatmap(categories, tbodyID) {
  const tbody = document.getElementById(tbodyID);
  if (!tbody) return;
  categories.forEach((cat, i) => {
    const gap = cat.potential - cat.observed;
    const capture = ((cat.observed / cat.potential) * 100).toFixed(1);
    let cc = 'capture-low';
    if (capture > 30) cc = 'capture-med';
    if (capture > 50) cc = 'capture-high';
    const hw = Math.min((gap / Math.max(...categories.map(c => c.potential - c.observed))) * 60, 80);
    tbody.innerHTML += `
      <tr>
        <td style="color:var(--text-muted);font-family:var(--font-mono);font-size:12px;">${i + 1}</td>
        <td class="cat-name">${cat.name}</td>
        <td class="cat-observed" style="text-align:right">${fmtSGD(cat.observed)}</td>
        <td class="cat-potential" style="text-align:right">${fmtSGD(cat.potential)}</td>
        <td class="cat-gap" style="text-align:right">
          ${fmtSGD(gap)}
          <span class="heat-bar" style="width:${hw}px;background:${gap > 300 ? 'var(--red-soft)' : gap > 100 ? 'var(--amber)' : 'var(--text-muted)'};"></span>
        </td>
        <td class="cat-capture ${cc}" style="text-align:right">${capture}%</td>
      </tr>`;
  });
}

function getCountryCodeFromPath() {
  const parts = window.location.pathname.split('/').filter(Boolean);
  if (!parts.length) return null;
  const candidate = parts[0].toLowerCase();
  return TASK_TRACKER_COUNTRIES[candidate] ? candidate : null;
}

function cloneTaskState(countryCode) {
  const seed = TASK_TRACKER_SEEDS[countryCode];
  if (!seed) return { nextId: 1, tasks: [], history: [], past: [] };
  return {
    nextId: seed.nextId,
    tasks: seed.tasks.map(task => ({ ...task })),
    history: [],
    past: [],
  };
}

function cloneTaskSnapshot(state) {
  return {
    nextId: Number(state?.nextId) || 1,
    tasks: Array.isArray(state?.tasks) ? state.tasks.map(task => ({ ...task })) : [],
  };
}

function normalizeTask(task) {
  return {
    id: Number(task?.id) || Date.now(),
    date: task?.date || '',
    description: task?.description || '',
    owner: task?.owner || '',
    deadline: task?.deadline || '',
    status: ['not started', 'in progress', 'completed'].includes(task?.status) ? task.status : 'in progress',
  };
}

function normalizeTaskState(countryCode, state) {
  const seedState = cloneTaskState(countryCode);
  const tasks = Array.isArray(state?.tasks) ? state.tasks.map(normalizeTask) : seedState.tasks;
  const past = Array.isArray(state?.past)
    ? state.past.slice(-20).map((snapshot) => cloneTaskSnapshot(snapshot))
    : seedState.past;
  return {
    nextId: Number(state?.nextId) || (tasks.reduce((max, task) => Math.max(max, Number(task.id) || 0), 0) + 1),
    tasks,
    history: Array.isArray(state?.history) ? state.history.slice(-100) : seedState.history,
    past,
  };
}

async function loadSharedTaskState(countryCode) {
  const seedState = cloneTaskState(countryCode);
  if (!countryCode) return seedState;
  const convex = window.TikTokConvexClient;
  if (!convex?.isConfigured) return seedState;
  try {
    const payload = await convex.query('tasks:getTasksByCountry', { countryCode });
    return normalizeTaskState(countryCode, {
      nextId: Number(payload?.nextId) || seedState.nextId,
      tasks: Array.isArray(payload?.tasks) ? payload.tasks : seedState.tasks,
      history: seedState.history,
      past: seedState.past,
    });
  } catch (error) {
    return seedState;
  }
}

async function syncSharedTaskState(countryCode, state) {
  if (!countryCode) return false;
  const convex = window.TikTokConvexClient;
  if (!convex?.isConfigured) return false;
  try {
    const remote = await convex.query('tasks:getTasksByCountry', { countryCode });
    const remoteMap = new Map((remote?.tasks || []).map((task) => [Number(task.id), task]));
    const localMap = new Map((state?.tasks || []).map((task) => [Number(task.id), task]));

    for (const remoteTask of remote?.tasks || []) {
      if (!localMap.has(Number(remoteTask.id))) {
        await convex.mutation('tasks:deleteTask', {
          countryCode,
          id: Number(remoteTask.id),
        });
      }
    }

    for (const localTask of state?.tasks || []) {
      const id = Number(localTask.id);
      const remoteTask = remoteMap.get(id);
      if (!remoteTask) {
        await convex.mutation('tasks:createTask', {
          countryCode,
          id,
          date: localTask.date || '',
          description: localTask.description || '',
          owner: localTask.owner || '',
          deadline: localTask.deadline || '',
          status: localTask.status || 'in progress',
        });
        continue;
      }

      if (
        remoteTask.date !== localTask.date ||
        remoteTask.description !== localTask.description ||
        remoteTask.owner !== localTask.owner ||
        remoteTask.deadline !== localTask.deadline ||
        remoteTask.status !== localTask.status
      ) {
        await convex.mutation('tasks:updateTask', {
          countryCode,
          id,
          date: localTask.date || '',
          description: localTask.description || '',
          owner: localTask.owner || '',
          deadline: localTask.deadline || '',
          status: localTask.status || 'in progress',
        });
      }
    }

    return true;
  } catch (error) {
    return false;
  }
}

function formatGMT8(date = new Date()) {
  const parts = new Intl.DateTimeFormat('en-GB', {
    timeZone: 'Asia/Singapore',
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  }).formatToParts(date).reduce((acc, part) => {
    if (part.type !== 'literal') acc[part.type] = part.value;
    return acc;
  }, {});
  return `${parts.day}/${parts.month}/${parts.year} ${parts.hour}:${parts.minute}:${parts.second} GMT+8`;
}

function formatTaskDate(iso) {
  if (!iso) return '-';
  const [year, month, day] = iso.split('-');
  if (!year || !month || !day) return iso;
  return `${day}/${month}/${year}`;
}

function escapeHTML(value) {
  return String(value ?? '').replace(/[&<>"']/g, ch => ({
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#39;'
  }[ch]));
}

function displayHistoryValue(field, value) {
  const safe = value || '-';
  if ((field === 'date' || field === 'deadline') && value) return formatTaskDate(value);
  return safe;
}

function pushUndoSnapshot(state) {
  const snapshot = cloneTaskSnapshot(state);
  state.past = [...(Array.isArray(state.past) ? state.past : []), snapshot].slice(-20);
}

function restoreUndoSnapshot(state, snapshot) {
  if (!snapshot) return false;
  state.nextId = Number(snapshot.nextId) || 1;
  state.tasks = Array.isArray(snapshot.tasks) ? snapshot.tasks.map(task => ({ ...task })) : [];
  return true;
}

function makeHistoryEntry(message, meta = {}) {
  return {
    id: `${Date.now()}-${Math.random().toString(16).slice(2)}`,
    when: new Date().toISOString(),
    whenLabel: formatGMT8(),
    message,
    meta,
  };
}

function appendHistory(state, entry) {
  state.history = [...state.history, entry].slice(-100);
}

function injectTaskTrackerSection(countryCode) {
  console.log('[TaskTracker] injectTaskTrackerSection called with:', countryCode);
  const countryName = TASK_TRACKER_COUNTRIES[countryCode];
  console.log('[TaskTracker] Country name:', countryName);
  console.log('[TaskTracker] TASK_TRACKER_COUNTRIES:', TASK_TRACKER_COUNTRIES);
  if (!countryName) {
    console.log('[TaskTracker] No country name found for code:', countryCode);
    return null;
  }
  if (document.querySelector('.tasks-section')) {
    console.log('[TaskTracker] tasks-section already exists');
    return null;
  }

  const state = cloneTaskState(countryCode);
  const existingAnnual = document.querySelector('section.annual-section');
  console.log('[TaskTracker] Found annual-section:', !!existingAnnual);
  const targetAnchor = existingAnnual || document.querySelector('section.story');
  console.log('[TaskTracker] Target anchor found:', !!targetAnchor);
  if (!targetAnchor) {
    console.log('[TaskTracker] No target anchor found');
    return null;
  }

  const section = document.createElement('section');
  section.className = 'section tasks-section';
  section.dataset.country = countryCode;
  section.innerHTML = `
    <div class="container">
      <div class="tasks-shell reveal">
        <div class="tasks-head">
          <div>
            <div class="section-label reveal">Tasks</div>
            <h2 class="section-title reveal reveal-delay-1">Editable task tracker - ${countryName}</h2>
            <p class="section-subtitle reveal reveal-delay-2">Inline edits sync to shared storage so the same tasks and history appear across browsers and devices, stamped in GMT+8.</p>
          </div>
          <div class="tasks-actions reveal reveal-delay-3">
            <button type="button" class="tasks-btn" data-action="add">Add task</button>
            <button type="button" class="tasks-btn tasks-btn-secondary" data-action="history" aria-expanded="false" aria-controls="tasks-history-panel">History Tracker</button>
            <button type="button" class="tasks-btn tasks-btn-secondary" data-action="undo" disabled>Undo</button>
          </div>
        </div>

        <div class="tasks-summary reveal reveal-delay-3" data-summary></div>

        <p class="sr-only" id="tasks-date-hint">Date fields use the browser calendar picker. Choose a date from the popup instead of typing free text.</p>

        <div class="tasks-table-wrap reveal reveal-delay-4">
          <table class="tasks-table" aria-label="Task tracker table">
            <thead>
              <tr>
                <th class="tasks-col-no">No.</th>
                <th class="tasks-col-date">Date</th>
                <th class="tasks-col-desc">Task Description</th>
                <th class="tasks-col-owner">Task Owner</th>
                <th class="tasks-col-deadline">Deadline</th>
                <th class="tasks-col-status">Status</th>
              </tr>
            </thead>
            <tbody data-tasks-body></tbody>
          </table>
        </div>

        <div class="tasks-history" data-history-panel id="tasks-history-panel" hidden>
          <div class="tasks-history-header">
            <div>
              <div class="tasks-history-title">History Tracker</div>
              <div class="tasks-history-subtitle">Every edit, add, and undo - newest first, recorded in GMT+8.</div>
            </div>
            <button type="button" class="tasks-history-close" data-action="history-close">Close</button>
          </div>
          <div class="tasks-history-list" data-history-list></div>
        </div>

        <div class="tasks-note reveal reveal-delay-5" data-convex-status>
          Loading connection status...
        </div>
      </div>
    </div>`;

  targetAnchor.after(section);

  // Update convex connection status
  const convexStatusEl = section.querySelector('[data-convex-status]');
  if (convexStatusEl) {
    const isConfigured = window.TikTokConvexClient?.isConfigured;
    convexStatusEl.textContent = isConfigured
      ? 'Connected to Convex: edits persist across sessions.'
      : 'Local mode: tasks work in this browser. Run locally with Convex for persistence.';
    convexStatusEl.style.color = isConfigured ? 'var(--green-soft)' : 'var(--amber)';
  }

  const summaryEl = section.querySelector('[data-summary]');
  const tbodyEl = section.querySelector('[data-tasks-body]');
  const historyPanel = section.querySelector('[data-history-panel]');
  const historyList = section.querySelector('[data-history-list]');
  const historyButton = section.querySelector('[data-action="history"]');
  const addButton = section.querySelector('[data-action="add"]');
  const undoButton = section.querySelector('[data-action="undo"]');

  const renderSummary = () => {
    const counts = state.tasks.reduce((acc, task) => {
      const key = ['not started', 'in progress', 'completed'].includes(task.status) ? task.status : 'in progress';
      acc[key] += 1;
      return acc;
    }, { 'not started': 0, 'in progress': 0, completed: 0 });
    const total = state.tasks.length;
    summaryEl.innerHTML = `
      <div class="tasks-summary-item"><strong>${total}</strong><span>Total tasks</span></div>
      <div class="tasks-summary-item"><strong>${counts.completed}</strong><span>Completed</span></div>
      <div class="tasks-summary-item"><strong>${counts['in progress']}</strong><span>In progress</span></div>
      <div class="tasks-summary-item"><strong>${counts['not started']}</strong><span>Not started</span></div>
    `;
  };

  const renderHistory = () => {
    if (!state.history.length) {
      historyList.innerHTML = '<div class="tasks-history-empty">No edits yet. Every save, add, and undo will appear here in reverse chronological order.</div>';
      return;
    }
    historyList.innerHTML = state.history.slice().reverse().map(entry => `
      <article class="tasks-history-entry">
        <div class="tasks-history-meta">
          <span>${escapeHTML(entry.whenLabel)}</span>
          <span>${escapeHTML(entry.meta?.rowLabel || 'Tracker')}${entry.meta?.field ? ` · ${escapeHTML(entry.meta.field)}` : ''}</span>
        </div>
        <div class="tasks-history-change">${escapeHTML(entry.message)}</div>
      </article>
    `).join('');
  };

  const renderRows = () => {
    if (!state.tasks.length) {
      tbodyEl.innerHTML = `
        <tr class="tasks-empty-row">
          <td colspan="6">
            <div class="tasks-empty-state">
            <div class="tasks-empty-title">No tasks yet</div>
              <div class="tasks-empty-copy">Add a task to start tracking work for this country page.</div>
            </div>
          </td>
        </tr>`;
      renderSummary();
      renderHistory();
      return;
    }

    tbodyEl.innerHTML = state.tasks.map((task, index) => `
      <tr data-task-id="${task.id}">
        <td class="tasks-cell-no">${index + 1}</td>
        <td><input class="tasks-input tasks-date" type="date" data-field="date" value="${escapeHTML(task.date || '')}" aria-label="Task ${index + 1} date" aria-describedby="tasks-date-hint"></td>
        <td><textarea class="tasks-textarea" data-field="description" rows="3" aria-label="Task ${index + 1} description">${escapeHTML(task.description || '')}</textarea></td>
        <td><input class="tasks-input" type="text" data-field="owner" value="${escapeHTML(task.owner || '')}" aria-label="Task ${index + 1} owner"></td>
        <td><input class="tasks-input tasks-date" type="date" data-field="deadline" value="${escapeHTML(task.deadline || '')}" aria-label="Task ${index + 1} deadline" aria-describedby="tasks-date-hint"></td>
        <td>
          <select class="tasks-select" data-field="status" aria-label="Task ${index + 1} status">
            <option value="completed" ${task.status === 'completed' ? 'selected' : ''}>completed</option>
            <option value="in progress" ${task.status === 'in progress' ? 'selected' : ''}>in progress</option>
            <option value="not started" ${task.status === 'not started' ? 'selected' : ''}>not started</option>
          </select>
        </td>
      </tr>
    `).join('');

    tbodyEl.querySelectorAll('textarea.tasks-textarea').forEach((textarea) => {
      autoGrowTextarea(textarea);
      textarea.addEventListener('input', () => autoGrowTextarea(textarea));
    });
    tbodyEl.querySelectorAll('input.tasks-date').forEach((input) => {
      const openPicker = () => {
        if (typeof input.showPicker === 'function') {
          try { input.showPicker(); } catch (error) { /* ignore */ }
        }
      };
      input.addEventListener('click', openPicker);
      input.addEventListener('focus', openPicker);
    });

    renderSummary();
    renderHistory();
    if (undoButton) undoButton.disabled = !state.past.length;
  };

  const autoGrowTextarea = (el) => {
    el.style.height = 'auto';
    el.style.height = `${Math.max(84, el.scrollHeight)}px`;
  };

  const recordAndRender = async (task, field, previous, next) => {
    if (previous === next) return;
    hasLocalChanges = true;
    lastSyncTime = Date.now();
    const rowLabel = `Task ${state.tasks.findIndex(item => item.id === task.id) + 1}`;
    const fieldNames = { date: 'Date', description: 'Task Description', owner: 'Task Owner', deadline: 'Deadline', status: 'Status' };
    appendHistory(state, makeHistoryEntry(
      `${rowLabel} ${fieldNames[field]} changed from "${displayHistoryValue(field, previous)}" to "${displayHistoryValue(field, next)}".`,
      { rowLabel, field: fieldNames[field] }
    ));
    renderRows();
    try {
      await window.TikTokConvexClient?.mutation('tasks:updateTask', {
        countryCode,
        id: Number(task.id),
        [field]: next,
      });
    } catch (error) {
      // Keep local edits if backend is temporarily unavailable.
    }
  };

  tbodyEl.addEventListener('change', (event) => {
    const target = event.target;
    if (!target.matches('[data-field]')) return;
    const row = target.closest('tr[data-task-id]');
    if (!row) return;
    const task = state.tasks.find(item => String(item.id) === row.dataset.taskId);
    if (!task) return;
    const field = target.dataset.field;
    const previous = task[field] || '';
    const next = field === 'description' ? target.value : target.value.trim();
    if (previous === next) return;
    hasLocalChanges = true;
    lastSyncTime = Date.now();
    pushUndoSnapshot(state);
    task[field] = next;
    void recordAndRender(task, field, previous, next);
  });

  addButton.addEventListener('click', () => {
    pushUndoSnapshot(state);
    hasLocalChanges = true;
    lastSyncTime = Date.now();
    const newTask = {
      id: state.nextId++,
      date: '',
      description: '',
      owner: '',
      deadline: '',
      status: 'in progress',
    };
    state.tasks.push(newTask);
    renderRows();
    appendHistory(state, makeHistoryEntry(
      `Added Task ${state.tasks.length} as a new editable row.`,
      { rowLabel: `Task ${state.tasks.length}`, field: 'Row added' }
    ));
    
    // Async sync to Convex (if available)
    void (async () => {
      try {
        await window.TikTokConvexClient?.mutation('tasks:createTask', {
          countryCode,
          id: newTask.id,
          date: newTask.date,
          description: newTask.description,
          owner: newTask.owner,
          deadline: newTask.deadline,
          status: newTask.status,
        });
        lastSyncTime = Date.now();
      } catch (error) {
        // Keep local task even if backend sync fails
      }
    })();
    
    // Focus the new task's description field
    const newRow = tbodyEl.querySelector(`tr[data-task-id="${newTask.id}"] textarea`);
    if (newRow) newRow.focus();
  });

  historyButton.addEventListener('click', () => {
    const show = historyPanel.hidden;
    historyPanel.hidden = !show;
    historyButton.setAttribute('aria-expanded', String(show));
    if (show) {
      renderHistory();
      historyPanel.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
    }
  });

  section.querySelector('[data-action="history-close"]').addEventListener('click', () => {
    historyPanel.hidden = true;
    historyButton.setAttribute('aria-expanded', 'false');
  });

  undoButton.addEventListener('click', () => {
    const previousState = state.past?.length ? state.past[state.past.length - 1] : null;
    if (!previousState) return;
    hasLocalChanges = true;
    lastSyncTime = Date.now();
    state.past = state.past.slice(0, -1);
    restoreUndoSnapshot(state, previousState);
    appendHistory(state, makeHistoryEntry('Undid the last change and restored the previous saved state.', { rowLabel: 'Tracker', field: 'Undo' }));
    renderRows();
    void syncSharedTaskState(countryCode, state);
    historyPanel.hidden = false;
    historyButton.setAttribute('aria-expanded', 'true');
  });

  // Track if user has made local edits that haven't been synced
  let hasLocalChanges = false;
  let lastSyncTime = 0;

  // Initial load from remote
  loadSharedTaskState(countryCode).then((remoteState) => {
    // Only overwrite if we haven't made local changes yet
    if (!hasLocalChanges) {
      state.nextId = remoteState.nextId;
      state.tasks = remoteState.tasks;
      renderRows();
    }
  });

  // Only poll for remote updates if Convex is configured
  if (window.TikTokConvexClient?.isConfigured) {
    setInterval(() => {
      // Skip poll if user has made recent local changes (within last 5 seconds)
      if (hasLocalChanges && Date.now() - lastSyncTime < 5000) return;

      void loadSharedTaskState(countryCode).then((remoteState) => {
        // Don't overwrite if user is actively editing
        if (hasLocalChanges && Date.now() - lastSyncTime < 5000) return;

        state.nextId = remoteState.nextId;
        state.tasks = remoteState.tasks;
        hasLocalChanges = false;
        renderRows();
      });
    }, 4000);
  }

  renderRows();
  return { section, state };
}

function initTasks() {
  console.log('[TaskTracker] initTasks called');
  const countryCode = getCountryCodeFromPath();
  console.log('[TaskTracker] Country code:', countryCode);
  if (!countryCode) {
    console.log('[TaskTracker] No country code found, exiting');
    return;
  }
  const result = injectTaskTrackerSection(countryCode);
  console.log('[TaskTracker] injectTaskTrackerSection returned:', result ? 'success' : 'null');
}

function initAll() {
  initTasks();
  initReveal();
  initNav();
  initBars();
  initQ1Tooltips();
}
