// ================================================================
//  SIMS — Main JavaScript
//  Premium Dashboard Interactions
// ================================================================

// ================================================================
//  SIDEBAR COLLAPSE
// ================================================================
const sidebar    = document.getElementById('sidebar');
const mainWrap   = document.getElementById('mainWrapper');
const toggleBtn  = document.getElementById('sidebarToggle');
const mobileOverlay = document.getElementById('mobileOverlay');

function isMobile() { return window.innerWidth <= 768; }

if (toggleBtn) {
  toggleBtn.addEventListener('click', function () {
    if (isMobile()) {
      sidebar.classList.toggle('mobile-open');
      mobileOverlay.classList.toggle('active');
    } else {
      sidebar.classList.toggle('collapsed');
      localStorage.setItem('sidebarCollapsed', sidebar.classList.contains('collapsed'));
    }
  });
}

if (mobileOverlay) {
  mobileOverlay.addEventListener('click', function () {
    sidebar.classList.remove('mobile-open');
    mobileOverlay.classList.remove('active');
  });
}

// Restore sidebar state on load
(function () {
  if (!isMobile() && localStorage.getItem('sidebarCollapsed') === 'true') {
    if (sidebar) sidebar.classList.add('collapsed');
  }
})();

// ================================================================
//  DARK MODE TOGGLE
// ================================================================
const darkBtn = document.getElementById('darkModeToggle');

function applyDarkMode(dark) {
  document.body.classList.toggle('dark-mode', dark);
  if (darkBtn) {
    const icon = darkBtn.querySelector('[data-icon]');
    if (icon) icon.setAttribute('data-icon', dark ? 'sun' : 'moon');
    // swap SVG
    const sunSvg  = '<svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>';
    const moonSvg = '<svg xmlns="http://www.w3.org/2000/svg" width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12.79A9 9 0 1 1 11.21 3 7 7 0 0 0 21 12.79z"/></svg>';
    darkBtn.innerHTML = dark ? sunSvg : moonSvg;
  }
}

(function () {
  const saved = localStorage.getItem('darkMode') === 'true';
  applyDarkMode(saved);
})();

if (darkBtn) {
  darkBtn.addEventListener('click', function () {
    const isDark = !document.body.classList.contains('dark-mode');
    applyDarkMode(isDark);
    localStorage.setItem('darkMode', isDark);
  });
}

// ================================================================
//  DROPDOWN MENUS
// ================================================================
function initDropdown(btnId, dropId) {
  const btn  = document.getElementById(btnId);
  const drop = document.getElementById(dropId);
  if (!btn || !drop) return;

  btn.addEventListener('click', function (e) {
    e.stopPropagation();
    const open = drop.classList.contains('open');
    // Close all dropdowns first
    document.querySelectorAll('.user-dropdown, .notif-dropdown').forEach(d => d.classList.remove('open'));
    document.querySelectorAll('.user-menu-btn').forEach(b => b.classList.remove('open'));
    if (!open) {
      drop.classList.add('open');
      btn.classList.add('open');
    }
  });
}

initDropdown('userMenuBtn', 'userDropdown');
initDropdown('notifBtn',    'notifDropdown');

document.addEventListener('click', function () {
  document.querySelectorAll('.user-dropdown, .notif-dropdown').forEach(d => d.classList.remove('open'));
  document.querySelectorAll('.user-menu-btn').forEach(b => b.classList.remove('open'));
});

// ================================================================
//  DELETE CONFIRM MODAL
// ================================================================
function confirmDelete(formId, itemName) {
  const modal    = document.getElementById('deleteModal');
  const nameEl   = document.getElementById('deleteItemName');
  const confirmBtn = document.getElementById('confirmDeleteBtn');
  if (!modal) return;
  if (nameEl) nameEl.textContent = itemName || 'this record';
  modal.classList.add('active');
  if (confirmBtn) {
    confirmBtn.onclick = function () {
      document.getElementById(formId).submit();
    };
  }
}

function closeModal(modalId) {
  const m = document.getElementById(modalId);
  if (m) m.classList.remove('active');
}

document.addEventListener('click', function (e) {
  if (e.target.classList.contains('modal-overlay')) {
    e.target.classList.remove('active');
  }
});

document.addEventListener('keydown', function (e) {
  if (e.key === 'Escape') {
    document.querySelectorAll('.modal-overlay.active').forEach(m => m.classList.remove('active'));
    document.querySelectorAll('.user-dropdown.open, .notif-dropdown.open').forEach(d => d.classList.remove('open'));
  }
});

// ================================================================
//  AUTO-DISMISS ALERTS
// ================================================================
document.addEventListener('DOMContentLoaded', function () {
  setTimeout(function () {
    document.querySelectorAll('.alert').forEach(function (el) {
      el.style.transition = 'opacity 0.5s, transform 0.5s';
      el.style.opacity    = '0';
      el.style.transform  = 'translateY(-8px)';
      setTimeout(() => el.remove(), 500);
    });
  }, 4000);
});

// ================================================================
//  TABLE SEARCH (local)
// ================================================================
function filterTable(inputId, tableId) {
  const input = document.getElementById(inputId);
  const table = document.getElementById(tableId);
  if (!input || !table) return;
  input.addEventListener('input', function () {
    const filter = this.value.toLowerCase();
    table.querySelectorAll('tbody tr').forEach(function (row) {
      row.style.display = row.textContent.toLowerCase().includes(filter) ? '' : 'none';
    });
  });
}

// ================================================================
//  MINI CALENDAR WIDGET
// ================================================================
(function () {
  const calGridEl   = document.getElementById('calGrid');
  const calMonthEl  = document.getElementById('calMonth');
  const calPrevBtn  = document.getElementById('calPrev');
  const calNextBtn  = document.getElementById('calNext');
  if (!calGridEl) return;

  const today   = new Date();
  let   current = new Date(today.getFullYear(), today.getMonth(), 1);

  const MONTHS = ['January','February','March','April','May','June',
                  'July','August','September','October','November','December'];

  function renderCalendar(d) {
    if (calMonthEl) calMonthEl.textContent = MONTHS[d.getMonth()] + ' ' + d.getFullYear();
    const firstDay = new Date(d.getFullYear(), d.getMonth(), 1).getDay();
    const daysInMonth = new Date(d.getFullYear(), d.getMonth() + 1, 0).getDate();
    const dayNames = ['Su','Mo','Tu','We','Th','Fr','Sa'];
    let html = dayNames.map(n => `<div class="cal-day-name">${n}</div>`).join('');
    for (let i = 0; i < firstDay; i++) html += '<div class="cal-day other-month"></div>';
    for (let i = 1; i <= daysInMonth; i++) {
      const isToday = i === today.getDate() && d.getMonth() === today.getMonth() && d.getFullYear() === today.getFullYear();
      html += `<div class="cal-day${isToday ? ' today' : ''}">${i}</div>`;
    }
    calGridEl.innerHTML = html;
  }

  renderCalendar(current);

  if (calPrevBtn) calPrevBtn.addEventListener('click', function () {
    current = new Date(current.getFullYear(), current.getMonth() - 1, 1);
    renderCalendar(current);
  });

  if (calNextBtn) calNextBtn.addEventListener('click', function () {
    current = new Date(current.getFullYear(), current.getMonth() + 1, 1);
    renderCalendar(current);
  });
})();

// ================================================================
//  STAGGER ANIMATION ON SCROLL
// ================================================================
(function () {
  const observer = new IntersectionObserver(function (entries) {
    entries.forEach(function (entry) {
      if (entry.isIntersecting) {
        entry.target.style.animationPlayState = 'running';
        observer.unobserve(entry.target);
      }
    });
  }, { threshold: 0.1 });

  document.querySelectorAll('.stat-card, .card, .fade-in-up').forEach(function (el) {
    el.style.animationPlayState = 'paused';
    observer.observe(el);
  });
})();
