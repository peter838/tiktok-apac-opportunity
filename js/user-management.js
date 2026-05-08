// === User Management System for TikTok Dashboard ===
// CRUD operations for dashboard access management

const COUNTRY_NAMES = {
  cn: 'China',
  jp: 'Japan',
  au: 'Australia',
  my: 'Malaysia',
  id: 'Indonesia',
  in: 'India',
  sg: 'Singapore',
  hk: 'Hong Kong',
  th: 'Thailand',
};

const ROLE_LABELS = {
  admin: { label: 'Admin', color: '#ef4444', bg: 'rgba(239, 68, 68, 0.15)' },
  editor: { label: 'Editor', color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.15)' },
  viewer: { label: 'Viewer', color: '#22c55e', bg: 'rgba(34, 197, 94, 0.15)' },
};

const STATUS_LABELS = {
  active: { label: 'Active', color: '#22c55e', bg: 'rgba(34, 197, 94, 0.15)' },
  inactive: { label: 'Inactive', color: '#64748b', bg: 'rgba(100, 116, 139, 0.15)' },
  pending: { label: 'Pending', color: '#f59e0b', bg: 'rgba(245, 158, 11, 0.15)' },
};

class UserManagement {
  constructor() {
    this.users = [];
    this.stats = null;
    this.currentUser = null;
    this.isAdmin = false;
    this.container = null;
    this.modal = null;
    this.convex = window.TikTokConvexClient;
  }

  async init() {
    // Check if we're on a page that should have user management
    const path = window.location.pathname;
    const isCountryPage = Object.keys(COUNTRY_NAMES).some(code => 
      path.includes(`/${code}/`) || path.includes(`/${code}.`)
    );
    
    // Only show on main index or country pages
    if (!isCountryPage && !path.endsWith('index.html') && path !== '/') {
      return;
    }

    await this.loadUsers();
    this.render();
    this.attachEventListeners();
  }

  async loadUsers() {
    try {
      if (this.convex?.isConfigured) {
        this.users = await this.convex.query('users:listUsers', {});
        this.stats = await this.convex.query('users:getUserStats', {});
      } else {
        // Fallback to localStorage for local development
        const stored = localStorage.getItem('tiktok_dashboard_users');
        this.users = stored ? JSON.parse(stored) : this.getDefaultUsers();
        this.calculateLocalStats();
      }
    } catch (error) {
      console.error('[UserManagement] Failed to load users:', error);
      this.users = this.getDefaultUsers();
      this.calculateLocalStats();
    }
  }

  getDefaultUsers() {
    return [
      {
        _id: 'default-admin',
        email: 'admin@sourcesage.co',
        name: 'System Administrator',
        role: 'admin',
        status: 'active',
        countries: Object.keys(COUNTRY_NAMES),
        createdAt: Date.now(),
        updatedAt: Date.now(),
      }
    ];
  }

  calculateLocalStats() {
    this.stats = {
      total: this.users.length,
      active: this.users.filter(u => u.status === 'active').length,
      inactive: this.users.filter(u => u.status === 'inactive').length,
      pending: this.users.filter(u => u.status === 'pending').length,
      admins: this.users.filter(u => u.role === 'admin').length,
      editors: this.users.filter(u => u.role === 'editor').length,
      viewers: this.users.filter(u => u.role === 'viewer').length,
    };
  }

  saveLocalUsers() {
    if (!this.convex?.isConfigured) {
      localStorage.setItem('tiktok_dashboard_users', JSON.stringify(this.users));
      this.calculateLocalStats();
    }
  }

  render() {
    // Check if section already exists
    if (document.querySelector('.users-section')) {
      return;
    }

    // Find insertion point - after the tasks section or before footer
    const tasksSection = document.querySelector('.tasks-section');
    const storySection = document.querySelector('.story');
    const ctaSection = document.querySelector('.cta');
    const targetAnchor = tasksSection || storySection || ctaSection;
    
    if (!targetAnchor) return;

    const section = document.createElement('section');
    section.className = 'section users-section';
    section.innerHTML = `
      <div class="container">
        <div class="users-shell reveal">
          <div class="users-head">
            <div>
              <div class="section-label reveal">Access Management</div>
              <h2 class="section-title reveal reveal-delay-1">Dashboard User Management</h2>
              <p class="section-subtitle reveal reveal-delay-2">Manage user access to the TikTok Opportunity Dashboard. Add, edit, or remove users and control their permissions.</p>
            </div>
            <div class="users-actions reveal reveal-delay-3">
              <button type="button" class="users-btn" data-action="add-user">
                <span>+</span> Add User
              </button>
              <button type="button" class="users-btn users-btn-secondary" data-action="refresh">
                ↻ Refresh
              </button>
            </div>
          </div>

          <div class="users-stats reveal reveal-delay-3" data-stats></div>

          <div class="users-table-wrap reveal reveal-delay-4">
            <table class="users-table" aria-label="User management table">
              <thead>
                <tr>
                  <th class="users-col-name">Name</th>
                  <th class="users-col-email">Email</th>
                  <th class="users-col-role">Role</th>
                  <th class="users-col-status">Status</th>
                  <th class="users-col-countries">Markets</th>
                  <th class="users-col-actions">Actions</th>
                </tr>
              </thead>
              <tbody data-users-body></tbody>
            </table>
          </div>

          <div class="users-note reveal reveal-delay-5" data-convex-status>
            ${this.convex?.isConfigured 
              ? 'Connected to Convex: user data persists across sessions.' 
              : 'Local mode: user data stored in browser. Connect Convex for persistence.'}
          </div>
        </div>
      </div>
    `;

    targetAnchor.after(section);
    this.container = section;
    this.renderStats();
    this.renderUsers();
  }

  renderStats() {
    const statsEl = this.container.querySelector('[data-stats]');
    if (!this.stats) return;

    statsEl.innerHTML = `
      <div class="users-stat-item">
        <strong>${this.stats.total}</strong>
        <span>Total Users</span>
      </div>
      <div class="users-stat-item users-stat-active">
        <strong>${this.stats.active}</strong>
        <span>Active</span>
      </div>
      <div class="users-stat-item users-stat-pending">
        <strong>${this.stats.pending}</strong>
        <span>Pending</span>
      </div>
      <div class="users-stat-item users-stat-admin">
        <strong>${this.stats.admins}</strong>
        <span>Admins</span>
      </div>
      <div class="users-stat-item">
        <strong>${this.stats.editors}</strong>
        <span>Editors</span>
      </div>
      <div class="users-stat-item">
        <strong>${this.stats.viewers}</strong>
        <span>Viewers</span>
      </div>
    `;
  }

  renderUsers() {
    const tbody = this.container.querySelector('[data-users-body]');
    
    if (!this.users.length) {
      tbody.innerHTML = `
        <tr class="users-empty-row">
          <td colspan="6">
            <div class="users-empty-state">
              <div class="users-empty-title">No users yet</div>
              <div class="users-empty-copy">Add your first user to grant dashboard access.</div>
            </div>
          </td>
        </tr>`;
      return;
    }

    tbody.innerHTML = this.users.map(user => {
      const roleStyle = ROLE_LABELS[user.role] || ROLE_LABELS.viewer;
      const statusStyle = STATUS_LABELS[user.status] || STATUS_LABELS.pending;
      const countries = user.countries || [];
      const countryTags = countries.map(code => 
        `<span class="users-country-tag" title="${COUNTRY_NAMES[code]}">${code.toUpperCase()}</span>`
      ).join('');

      return `
        <tr data-user-id="${user._id}">
          <td class="users-cell-name">
            <div class="users-name">${this.escapeHtml(user.name)}</div>
          </td>
          <td class="users-cell-email">${this.escapeHtml(user.email)}</td>
          <td class="users-cell-role">
            <span class="users-badge" style="color: ${roleStyle.color}; background: ${roleStyle.bg}; border: 1px solid ${roleStyle.color}30;">
              ${roleStyle.label}
            </span>
          </td>
          <td class="users-cell-status">
            <span class="users-badge" style="color: ${statusStyle.color}; background: ${statusStyle.bg}; border: 1px solid ${statusStyle.color}30;">
              ${statusStyle.label}
            </span>
          </td>
          <td class="users-cell-countries">
            <div class="users-countries">${countryTags || '<span class="users-all-markets">All Markets</span>'}</div>
          </td>
          <td class="users-cell-actions">
            <button type="button" class="users-action-btn" data-action="edit" data-user-id="${user._id}" title="Edit user">
              ✎
            </button>
            <button type="button" class="users-action-btn users-action-btn-danger" data-action="delete" data-user-id="${user._id}" title="Delete user">
              ×
            </button>
          </td>
        </tr>
      `;
    }).join('');
  }

  attachEventListeners() {
    if (!this.container) return;

    // Add user button
    this.container.querySelector('[data-action="add-user"]')?.addEventListener('click', () => {
      this.openModal('create');
    });

    // Refresh button
    this.container.querySelector('[data-action="refresh"]')?.addEventListener('click', async () => {
      await this.loadUsers();
      this.renderStats();
      this.renderUsers();
    });

    // Table actions (edit/delete)
    this.container.querySelector('[data-users-body]')?.addEventListener('click', (e) => {
      const btn = e.target.closest('[data-action]');
      if (!btn) return;

      const action = btn.dataset.action;
      const userId = btn.dataset.userId;

      if (action === 'edit') {
        const user = this.users.find(u => u._id === userId);
        if (user) this.openModal('edit', user);
      } else if (action === 'delete') {
        const user = this.users.find(u => u._id === userId);
        if (user && confirm(`Delete user "${user.name}" (${user.email})?`)) {
          this.deleteUser(userId);
        }
      }
    });
  }

  openModal(mode, user = null) {
    // Remove existing modal
    this.modal?.remove();

    const modal = document.createElement('div');
    modal.className = 'users-modal';
    modal.innerHTML = `
      <div class="users-modal-backdrop"></div>
      <div class="users-modal-content">
        <div class="users-modal-header">
          <h3>${mode === 'create' ? 'Add New User' : 'Edit User'}</h3>
          <button type="button" class="users-modal-close" data-action="close">×</button>
        </div>
        <form class="users-modal-form" data-mode="${mode}">
          <div class="users-form-group">
            <label for="user-name">Full Name</label>
            <input type="text" id="user-name" name="name" value="${user?.name || ''}" required 
                   placeholder="Enter user's full name">
          </div>
          
          <div class="users-form-group">
            <label for="user-email">Email Address</label>
            <input type="email" id="user-email" name="email" value="${user?.email || ''}" required 
                   placeholder="user@company.com" ${mode === 'edit' ? 'readonly' : ''}>
          </div>
          
          <div class="users-form-row">
            <div class="users-form-group">
              <label for="user-role">Role</label>
              <select id="user-role" name="role" required>
                <option value="viewer" ${user?.role === 'viewer' ? 'selected' : ''}>Viewer - Can view dashboard</option>
                <option value="editor" ${user?.role === 'editor' ? 'selected' : ''}>Editor - Can edit tasks</option>
                <option value="admin" ${user?.role === 'admin' ? 'selected' : ''}>Admin - Full access</option>
              </select>
            </div>
            
            <div class="users-form-group">
              <label for="user-status">Status</label>
              <select id="user-status" name="status" required>
                <option value="active" ${user?.status === 'active' ? 'selected' : ''}>Active</option>
                <option value="inactive" ${user?.status === 'inactive' ? 'selected' : ''}>Inactive</option>
                <option value="pending" ${user?.status === 'pending' ? 'selected' : ''}>Pending</option>
              </select>
            </div>
          </div>
          
          <div class="users-form-group">
            <label>Market Access</label>
            <div class="users-countries-grid">
              ${Object.entries(COUNTRY_NAMES).map(([code, name]) => `
                <label class="users-country-checkbox">
                  <input type="checkbox" name="countries" value="${code}" 
                         ${user?.countries?.includes(code) ? 'checked' : ''}>
                  <span class="users-country-flag">${this.getFlag(code)}</span>
                  <span class="users-country-name">${name}</span>
                </label>
              `).join('')}
            </div>
            <div class="users-form-hint">Leave all unchecked to grant access to all markets</div>
          </div>
          
          <div class="users-modal-actions">
            <button type="button" class="users-btn users-btn-secondary" data-action="close">Cancel</button>
            <button type="submit" class="users-btn">
              ${mode === 'create' ? 'Create User' : 'Save Changes'}
            </button>
          </div>
          
          ${mode === 'edit' ? `<input type="hidden" name="userId" value="${user._id}">` : ''}
        </form>
      </div>
    `;

    document.body.appendChild(modal);
    this.modal = modal;

    // Modal event listeners
    modal.querySelector('[data-action="close"]')?.addEventListener('click', () => {
      this.closeModal();
    });

    modal.querySelector('.users-modal-backdrop')?.addEventListener('click', () => {
      this.closeModal();
    });

    modal.querySelector('form')?.addEventListener('submit', (e) => {
      e.preventDefault();
      this.handleFormSubmit(e.target);
    });

    // Focus first input
    modal.querySelector('input')?.focus();
  }

  closeModal() {
    this.modal?.remove();
    this.modal = null;
  }

  async handleFormSubmit(form) {
    const formData = new FormData(form);
    const mode = form.dataset.mode;
    
    const countries = [];
    form.querySelectorAll('input[name="countries"]:checked').forEach(cb => {
      countries.push(cb.value);
    });

    const userData = {
      name: formData.get('name').trim(),
      email: formData.get('email').trim(),
      role: formData.get('role'),
      status: formData.get('status'),
      countries: countries.length > 0 ? countries : Object.keys(COUNTRY_NAMES),
    };

    try {
      if (mode === 'create') {
        await this.createUser(userData);
      } else {
        const userId = formData.get('userId');
        await this.updateUser(userId, userData);
      }
      this.closeModal();
      await this.loadUsers();
      this.renderStats();
      this.renderUsers();
    } catch (error) {
      alert(`Error: ${error.message}`);
    }
  }

  async createUser(userData) {
    if (this.convex?.isConfigured) {
      return await this.convex.mutation('users:createUser', {
        ...userData,
        createdBy: 'admin',
      });
    } else {
      // Local fallback
      const existing = this.users.find(u => u.email === userData.email);
      if (existing) {
        throw new Error('User with this email already exists');
      }
      
      const newUser = {
        _id: 'local-' + Date.now(),
        ...userData,
        createdAt: Date.now(),
        updatedAt: Date.now(),
        createdBy: 'admin',
      };
      
      this.users.push(newUser);
      this.saveLocalUsers();
      return { id: newUser._id };
    }
  }

  async updateUser(userId, userData) {
    if (this.convex?.isConfigured) {
      return await this.convex.mutation('users:updateUser', {
        id: userId,
        ...userData,
      });
    } else {
      // Local fallback
      const index = this.users.findIndex(u => u._id === userId);
      if (index === -1) {
        throw new Error('User not found');
      }
      
      // Check email uniqueness if changing
      if (userData.email !== this.users[index].email) {
        const existing = this.users.find(u => u.email === userData.email);
        if (existing) {
          throw new Error('User with this email already exists');
        }
      }
      
      this.users[index] = {
        ...this.users[index],
        ...userData,
        updatedAt: Date.now(),
      };
      
      this.saveLocalUsers();
      return { ok: true };
    }
  }

  async deleteUser(userId) {
    try {
      if (this.convex?.isConfigured) {
        await this.convex.mutation('users:deleteUser', { id: userId });
      } else {
        // Local fallback
        const index = this.users.findIndex(u => u._id === userId);
        if (index > -1) {
          this.users.splice(index, 1);
          this.saveLocalUsers();
        }
      }
      
      await this.loadUsers();
      this.renderStats();
      this.renderUsers();
    } catch (error) {
      alert(`Error deleting user: ${error.message}`);
    }
  }

  getFlag(code) {
    const flags = {
      cn: '🇨🇳', jp: '🇯🇵', au: '🇦🇺', my: '🇲🇾',
      id: '🇮🇩', in: '🇮🇳', sg: '🇸🇬', hk: '🇭🇰', th: '🇹🇭',
    };
    return flags[code] || '🌐';
  }

  escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
  }
}

// Initialize when DOM is ready
function initUserManagement() {
  const um = new UserManagement();
  um.init();
}

// Auto-initialize if loaded after DOM ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initUserManagement);
} else {
  initUserManagement();
}

// Also expose for manual initialization
window.UserManagement = UserManagement;
window.initUserManagement = initUserManagement;
