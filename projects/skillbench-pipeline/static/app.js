/* SkillBench Pipeline — Dashboard JS */

const API = '';  // Same origin
const TOKEN = new URLSearchParams(window.location.search).get('token') || '';
const STAGES = ['lead', 'qualified', 'proposal', 'negotiation', 'won', 'lost'];
const STAGE_COLORS = {
  lead: '#5a6078', qualified: '#43BBEA', proposal: '#7b68ee',
  negotiation: '#f39c12', won: '#27ae60', lost: '#e74c3c',
};
const TYPE_ICONS = {
  email: '\u2709\ufe0f', meeting: '\ud83d\udcc5', call: '\ud83d\udcde',
  slack: '\ud83d\udcac', note: '\u270f\ufe0f', document: '\ud83d\udcc4', other: '\ud83d\udccc',
};

let allOrgs = [];
let allOpps = [];

// ── Utilities ──────────────────────────────────────────────────

function $(sel) { return document.querySelector(sel); }
function $$(sel) { return document.querySelectorAll(sel); }

function fmtDollars(cents) {
  if (!cents) return '$0';
  return '$' + (cents / 100).toLocaleString('en-US', { maximumFractionDigits: 0 });
}

function daysAgo(isoDate) {
  if (!isoDate) return '?';
  const diff = (Date.now() - new Date(isoDate + 'Z').getTime()) / 86400000;
  const d = Math.max(0, Math.floor(diff));
  if (d === 0) return 'today';
  if (d === 1) return '1 day';
  return d + ' days';
}

function fmtDate(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric' });
}

function fmtDateTime(iso) {
  if (!iso) return '';
  const d = new Date(iso);
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: 'numeric', minute: '2-digit' });
}

async function api(path, opts = {}) {
  const sep = path.includes('?') ? '&' : '?';
  const url = API + path + (TOKEN ? `${sep}token=${TOKEN}` : '');
  const res = await fetch(url, {
    headers: { 'Content-Type': 'application/json', ...opts.headers },
    ...opts,
  });
  if (!res.ok) throw new Error(`API ${res.status}: ${await res.text()}`);
  return res.json();
}

// ── Tab Navigation ─────────────────────────────────────────────

$$('nav button').forEach(btn => {
  btn.addEventListener('click', () => {
    $$('nav button').forEach(b => b.classList.remove('active'));
    $$('section').forEach(s => s.classList.remove('active'));
    btn.classList.add('active');
    const tab = btn.dataset.tab;
    $(`#tab-${tab}`).classList.add('active');
    window.location.hash = tab;
    loadTab(tab);
  });
});

function loadTab(tab) {
  if (tab === 'pipeline') loadPipeline();
  else if (tab === 'activity') loadActivities();
  else if (tab === 'directory') loadDirectory();
  else if (tab === 'reminders') loadReminders();
}

// ── Header Summary ─────────────────────────────────────────────

async function loadSummary() {
  const s = await api('/api/dashboard/summary');
  $('#stat-deals').textContent = s.active_deals;
  $('#stat-value').textContent = fmtDollars(s.active_value_cents);
  $('#stat-weighted').textContent = fmtDollars(s.weighted_value_cents);
  $('#stat-reminders').textContent = s.overdue_reminders;
}

// ── Pipeline Board ─────────────────────────────────────────────

async function loadPipeline() {
  const opps = await api('/api/opps');
  allOpps = opps;
  const board = $('#pipeline-board');
  board.innerHTML = '';

  STAGES.forEach(stage => {
    const col = document.createElement('div');
    col.className = 'stage-column';
    col.dataset.stage = stage;

    const stageOpps = opps.filter(o => o.stage === stage);
    const total = stageOpps.reduce((s, o) => s + (o.value_cents || 0), 0);

    col.innerHTML = `
      <div class="stage-header">
        <span>${stage} (${stageOpps.length})</span>
        <span class="stage-total">${fmtDollars(total)}</span>
      </div>
      <div class="stage-body" data-stage="${stage}"></div>
    `;

    const body = col.querySelector('.stage-body');

    // Drop zone
    body.addEventListener('dragover', e => {
      e.preventDefault();
      body.classList.add('drag-over');
    });
    body.addEventListener('dragleave', () => body.classList.remove('drag-over'));
    body.addEventListener('drop', async e => {
      e.preventDefault();
      body.classList.remove('drag-over');
      const oppId = e.dataTransfer.getData('text/plain');
      if (oppId) {
        await api(`/api/opps/${oppId}/stage`, {
          method: 'PATCH',
          body: JSON.stringify({ stage }),
        });
        loadPipeline();
        loadSummary();
      }
    });

    // Deal cards
    stageOpps.forEach(opp => {
      const card = document.createElement('div');
      card.className = 'deal-card';
      card.draggable = true;
      card.dataset.id = opp.id;
      const stale = opp.days_since_contact;
      const staleClass = stale > 30 ? 'stale-red' : stale > 14 ? 'stale-amber' : '';
      const staleLabel = stale > 30 ? `${stale}d stale` : stale > 14 ? `${stale}d quiet` : '';
      const notesSnippet = opp.notes ? opp.notes.split('.')[0].substring(0, 80) : '';
      card.className = `deal-card ${staleClass}`;
      card.innerHTML = `
        <div class="deal-card-top">
          <div class="org-name">${opp.org_name || ''}</div>
          ${staleLabel ? `<span class="stale-badge ${staleClass}">${staleLabel}</span>` : ''}
        </div>
        <div class="deal-title">${opp.title}</div>
        ${notesSnippet ? `<div class="deal-context">${notesSnippet}</div>` : ''}
        <div class="deal-meta">
          <span class="deal-value">${fmtDollars(opp.value_cents)}</span>
          <span class="deal-prob">${opp.probability || 0}%</span>
          <span class="deal-days">${opp.last_activity ? fmtDate(opp.last_activity) : 'no activity'}</span>
        </div>
      `;
      card.addEventListener('dragstart', e => {
        e.dataTransfer.setData('text/plain', opp.id);
        card.classList.add('dragging');
      });
      card.addEventListener('dragend', () => card.classList.remove('dragging'));
      card.addEventListener('click', e => {
        if (e.target.closest('[draggable]') && !card.classList.contains('dragging')) {
          openEditDealModal(opp);
        }
      });
      body.appendChild(card);
    });

    board.appendChild(col);
  });

  // Funnel
  renderFunnel(opps);
}

function renderFunnel(opps) {
  const funnel = $('#funnel');
  const activeStages = STAGES.filter(s => s !== 'won' && s !== 'lost');
  const maxVal = Math.max(...activeStages.map(s =>
    opps.filter(o => o.stage === s).reduce((sum, o) => sum + (o.value_cents || 0), 0)
  ), 1);

  let html = '<h3>Pipeline Funnel</h3>';
  activeStages.forEach(stage => {
    const stageOpps = opps.filter(o => o.stage === stage);
    const total = stageOpps.reduce((s, o) => s + (o.value_cents || 0), 0);
    const pct = Math.max((total / maxVal) * 100, 8);
    html += `
      <div class="funnel-bar">
        <span class="bar-label">${stage}</span>
        <div class="bar-fill" style="width:${pct}%;background:${STAGE_COLORS[stage]}">
          ${stageOpps.length}
        </div>
        <span class="bar-amount">${fmtDollars(total)}</span>
      </div>`;
  });
  funnel.innerHTML = html;
}

// ── Activities ─────────────────────────────────────────────────

async function loadActivities() {
  const type = $('#filter-type').value;
  const days = $('#filter-days').value;
  let path = '/api/activities?limit=50';
  if (type) path += `&activity_type=${type}`;
  if (days) path += `&days=${days}`;

  const activities = await api(path);
  const list = $('#activity-list');

  if (!activities.length) {
    list.innerHTML = '<div class="empty-state">No activities yet. Log one or wait for scheduled scans.</div>';
    return;
  }

  list.innerHTML = activities.map(a => `
    <div class="activity-item">
      <div class="activity-icon">${TYPE_ICONS[a.activity_type] || '\ud83d\udccc'}</div>
      <div class="activity-content">
        <div class="activity-org">${a.org_name || 'Unknown'}</div>
        <div class="activity-summary">${a.subject ? `<strong>${a.subject}</strong> — ` : ''}${a.summary || ''}</div>
        <div class="activity-time">${fmtDateTime(a.occurred_at)}${a.direction ? ` \u00b7 ${a.direction}` : ''}</div>
      </div>
    </div>
  `).join('');
}

$('#filter-type').addEventListener('change', loadActivities);
$('#filter-days').addEventListener('change', loadActivities);

// ── Directory ──────────────────────────────────────────────────

let selectedOrgId = null;

async function loadDirectory() {
  allOrgs = await api('/api/orgs');
  renderOrgList(allOrgs);
}

function renderOrgList(orgs) {
  const body = $('#org-list-body');
  body.innerHTML = orgs.map(o => `
    <div class="org-list-item${o.id === selectedOrgId ? ' active' : ''}" data-id="${o.id}">
      <span class="org-item-name">${o.name}</span>
      ${o.deal_count ? `<span class="org-item-badge">${o.deal_count} deal${o.deal_count > 1 ? 's' : ''}</span>` : ''}
    </div>
  `).join('');

  body.querySelectorAll('.org-list-item').forEach(item => {
    item.addEventListener('click', () => {
      selectedOrgId = parseInt(item.dataset.id);
      renderOrgList(allOrgs);
      loadOrgDetail(selectedOrgId);
    });
  });
}

$('#org-search').addEventListener('input', e => {
  const q = e.target.value.toLowerCase();
  renderOrgList(allOrgs.filter(o => o.name.toLowerCase().includes(q)));
});

async function loadOrgDetail(orgId) {
  const [org, contacts, opps, activities] = await Promise.all([
    api(`/api/orgs/${orgId}`),
    api(`/api/contacts?org_id=${orgId}`),
    api(`/api/opps?org_id=${orgId}`),
    api(`/api/activities?org_id=${orgId}&limit=10`),
  ]);

  const detail = $('#org-detail');
  detail.innerHTML = `
    <h2>${org.name}</h2>
    <div class="org-meta">
      ${org.domain ? org.domain + ' \u00b7 ' : ''}${org.size_tier || ''}
      ${org.drive_folder_path ? ' \u00b7 <a href="#" style="color:var(--cyan)">Google Drive</a>' : ''}
    </div>

    <div class="detail-section">
      <h3>Contacts (${contacts.length})</h3>
      ${contacts.length ? contacts.map(c => `
        <div style="margin-bottom:6px;">
          <strong>${c.name}</strong>${c.role_type ? `<span class="contact-badge ${c.role_type}">${c.role_type.replace('_', ' ')}</span>` : ''}
          ${c.title ? `<div style="font-size:0.75rem;color:var(--charcoal-light)">${c.title}</div>` : ''}
          ${c.email ? `<div style="font-size:0.75rem;color:var(--charcoal-light)">${c.email}</div>` : ''}
        </div>
      `).join('') : '<div class="empty-state" style="padding:10px">No contacts yet</div>'}
    </div>

    <div class="detail-section">
      <h3>Deals (${opps.length})</h3>
      ${opps.map(o => `
        <div style="margin-bottom:6px;display:flex;justify-content:space-between;">
          <span>${o.title}</span>
          <span style="font-weight:600;color:${STAGE_COLORS[o.stage]}">${o.stage} \u00b7 ${fmtDollars(o.value_cents)}</span>
        </div>
      `).join('') || '<div class="empty-state" style="padding:10px">No deals</div>'}
    </div>

    <div class="detail-section">
      <h3>Recent Activity</h3>
      ${activities.length ? activities.map(a => `
        <div style="margin-bottom:6px;font-size:0.8rem;">
          ${TYPE_ICONS[a.activity_type] || ''} ${a.summary || a.subject || 'Activity'}
          <span style="color:var(--charcoal-light);margin-left:6px">${fmtDate(a.occurred_at)}</span>
        </div>
      `).join('') : '<div class="empty-state" style="padding:10px">No activity recorded</div>'}
    </div>
  `;
}

// ── Reminders ──────────────────────────────────────────────────

async function loadReminders() {
  const reminders = await api('/api/reminders');
  const container = $('#reminders-container');

  const today = new Date().toISOString().split('T')[0];
  const weekFromNow = new Date(Date.now() + 7 * 86400000).toISOString().split('T')[0];

  const overdue = reminders.filter(r => r.due_date < today);
  const todayItems = reminders.filter(r => r.due_date === today);
  const upcoming = reminders.filter(r => r.due_date > today && r.due_date <= weekFromNow);
  const later = reminders.filter(r => r.due_date > weekFromNow);

  let html = '';

  if (overdue.length) {
    html += `<div class="reminder-section overdue">
      <h3>\u26a0\ufe0f Overdue (${overdue.length})</h3>
      ${overdue.map(r => reminderHTML(r, 'overdue')).join('')}
    </div>`;
  }

  if (todayItems.length) {
    html += `<div class="reminder-section today">
      <h3>\ud83d\udcc5 Due Today (${todayItems.length})</h3>
      ${todayItems.map(r => reminderHTML(r, 'today')).join('')}
    </div>`;
  }

  if (upcoming.length) {
    html += `<div class="reminder-section">
      <h3>Upcoming 7 Days (${upcoming.length})</h3>
      ${upcoming.map(r => reminderHTML(r)).join('')}
    </div>`;
  }

  if (later.length) {
    html += `<div class="reminder-section">
      <h3>Later (${later.length})</h3>
      ${later.map(r => reminderHTML(r)).join('')}
    </div>`;
  }

  if (!html) {
    html = '<div class="empty-state">No reminders. Create one to track follow-ups.</div>';
  }

  container.innerHTML = html;

  container.querySelectorAll('.btn-complete').forEach(btn => {
    btn.addEventListener('click', async () => {
      await api(`/api/reminders/${btn.dataset.id}/complete`, { method: 'PATCH' });
      loadReminders();
      loadSummary();
    });
  });
}

function reminderHTML(r, cls = '') {
  return `
    <div class="reminder-item ${cls}">
      <div style="flex:1">
        <div class="reminder-text">${r.reminder_text}</div>
        <div class="reminder-context">${r.opp_title || r.org_name || ''}</div>
      </div>
      <span class="reminder-date">${fmtDate(r.due_date)}</span>
      <button class="btn-complete" data-id="${r.id}">Done</button>
    </div>`;
}

// ── Modals ─────────────────────────────────────────────────────

function closeModal(id) {
  document.getElementById(id).classList.remove('open');
}

async function populateOrgDropdowns() {
  if (!allOrgs.length) allOrgs = await api('/api/orgs');
  const opts = allOrgs.map(o => `<option value="${o.id}">${o.name}</option>`).join('');
  ['deal-org', 'act-org', 'rem-org'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      const hasEmpty = id === 'rem-org';
      el.innerHTML = (hasEmpty ? '<option value="">None</option>' : '') + opts;
    }
  });
}

async function populateDealDropdowns() {
  if (!allOpps.length) allOpps = await api('/api/opps');
  const opts = allOpps
    .filter(o => !['won', 'lost'].includes(o.stage))
    .map(o => `<option value="${o.id}">${o.org_name}: ${o.title}</option>`)
    .join('');
  const el = document.getElementById('rem-deal');
  if (el) el.innerHTML = '<option value="">None</option>' + opts;
}

function openNewDealModal() {
  populateOrgDropdowns();
  $('#modal-new-deal').classList.add('open');
}

function openLogActivityModal() {
  populateOrgDropdowns();
  $('#modal-log-activity').classList.add('open');
}

function openNewReminderModal() {
  populateOrgDropdowns();
  populateDealDropdowns();
  $('#rem-date').value = new Date(Date.now() + 7 * 86400000).toISOString().split('T')[0];
  $('#modal-new-reminder').classList.add('open');
}

async function saveDeal() {
  const body = {
    org_id: parseInt($('#deal-org').value),
    title: $('#deal-title').value,
    value_cents: (parseInt($('#deal-value').value) || 0) * 100,
    deal_type: $('#deal-type').value,
    stage: $('#deal-stage').value,
    probability: parseInt($('#deal-probability').value) || 0,
    notes: $('#deal-notes').value || undefined,
  };
  await api('/api/opps', { method: 'POST', body: JSON.stringify(body) });
  closeModal('modal-new-deal');
  loadPipeline();
  loadSummary();
}

async function saveActivity() {
  const body = {
    org_id: parseInt($('#act-org').value),
    activity_type: $('#act-type').value,
    direction: $('#act-direction').value,
    summary: $('#act-summary').value,
    occurred_at: new Date().toISOString(),
  };
  await api('/api/activities', { method: 'POST', body: JSON.stringify(body) });
  closeModal('modal-log-activity');
  loadActivities();
  loadSummary();
}

async function saveReminder() {
  const body = {
    due_date: $('#rem-date').value,
    reminder_text: $('#rem-text').value,
    org_id: $('#rem-org').value ? parseInt($('#rem-org').value) : undefined,
    opportunity_id: $('#rem-deal').value ? parseInt($('#rem-deal').value) : undefined,
  };
  await api('/api/reminders', { method: 'POST', body: JSON.stringify(body) });
  closeModal('modal-new-reminder');
  loadReminders();
  loadSummary();
}

// ── Edit / Delete Deals ────────────────────────────────────────

function openEditDealModal(opp) {
  $('#edit-deal-id').value = opp.id;
  $('#edit-deal-heading').textContent = `${opp.org_name}: ${opp.title}`;
  $('#edit-deal-title').value = opp.title;
  $('#edit-deal-value').value = Math.round((opp.value_cents || 0) / 100);
  $('#edit-deal-type').value = opp.deal_type || 'other';
  $('#edit-deal-stage').value = opp.stage;
  $('#edit-deal-probability').value = opp.probability || 0;
  $('#edit-deal-notes').value = opp.notes || '';
  $('#modal-edit-deal').classList.add('open');
}

async function updateDeal() {
  const id = $('#edit-deal-id').value;
  const newStage = $('#edit-deal-stage').value;
  const opp = allOpps.find(o => o.id == id);

  // Update fields
  const body = {
    title: $('#edit-deal-title').value,
    value_cents: (parseInt($('#edit-deal-value').value) || 0) * 100,
    deal_type: $('#edit-deal-type').value,
    probability: parseInt($('#edit-deal-probability').value) || 0,
    notes: $('#edit-deal-notes').value || '',
  };
  await api(`/api/opps/${id}`, { method: 'PUT', body: JSON.stringify(body) });

  // Move stage if changed
  if (opp && opp.stage !== newStage) {
    await api(`/api/opps/${id}/stage`, {
      method: 'PATCH',
      body: JSON.stringify({ stage: newStage }),
    });
  }

  closeModal('modal-edit-deal');
  loadPipeline();
  loadSummary();
}

async function deleteDeal() {
  const id = $('#edit-deal-id').value;
  const title = $('#edit-deal-title').value;
  if (!confirm(`Delete "${title}"? This cannot be undone.`)) return;
  await api(`/api/opps/${id}`, { method: 'DELETE' });
  closeModal('modal-edit-deal');
  loadPipeline();
  loadSummary();
}

// ── Init ───────────────────────────────────────────────────────

(async function init() {
  loadSummary();
  const hash = window.location.hash.slice(1);
  if (hash && ['pipeline', 'activity', 'directory', 'reminders'].includes(hash)) {
    $$('nav button').forEach(b => b.classList.remove('active'));
    $$('section').forEach(s => s.classList.remove('active'));
    $(`nav button[data-tab="${hash}"]`).classList.add('active');
    $(`#tab-${hash}`).classList.add('active');
    loadTab(hash);
  } else {
    loadPipeline();
  }
})();
