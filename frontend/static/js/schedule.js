// frontend/static/js/schedule.js
import { getSchedule, ApiError, URLS } from './api.js';

/* ============ Дни недели ============ */
/* apiName — как приходит с backend, short — как показываем */
const DAYS = [
  { id: 1, short: 'Пн', full: 'Понедельник', apiName: 'Пн' },
  { id: 2, short: 'Вт', full: 'Вторник',     apiName: 'Вт' },
  { id: 3, short: 'Ср', full: 'Среда',       apiName: 'Ср' },
  { id: 4, short: 'Чт', full: 'Четверг',     apiName: 'Чт' },
  { id: 5, short: 'Пт', full: 'Пятница',     apiName: 'Пт' },
  { id: 6, short: 'Сб', full: 'Суббота',     apiName: 'Сб' },
];

const PAIR_SLOTS = [
  { number: 1, start: '08:00', end: '09:30' },
  { number: 2, start: '09:40', end: '11:10' },
  { number: 3, start: '11:20', end: '12:50' },
];

const MAX_PAIRS = PAIR_SLOTS.length;   // = 3

/* ============ Состояние ============ */
let currentLessons = [];
let currentMonday = getMonday();
let currentSlots = [];

/* ============ Утилиты ============ */
function subjectStyle(name = '') {
  const n = name.toLowerCase();
  if (n.includes('матем') || n.includes('алгебр') || n.includes('геометр'))
    return { key: 'math', icon: '√' };
  if (n.includes('русск') || n.includes('литерат'))
    return { key: 'rus', icon: '📖' };
  if (n.includes('хим')) return { key: 'chem', icon: '🧪' };
  if (n.includes('истор') || n.includes('обществ')) return { key: 'hist', icon: '🌐' };
  if (n.includes('информ') || n.includes('программ')) return { key: 'inf', icon: '💻' };
  if (n.includes('физкульт') || n.includes('спорт')) return { key: 'phys', icon: '🏃' };
  if (n.includes('физик')) return { key: 'phys', icon: '⚛️' };
  if (n.includes('англ') || n.includes('нем') || n.includes('язык'))
    return { key: 'lang', icon: '🌍' };
  return { key: 'default', icon: '📘' };
}

function getMonday(date = new Date()) {
  const d = new Date(date);
  const dow = d.getDay() || 7;
  if (dow !== 1) d.setDate(d.getDate() - (dow - 1));
  d.setHours(0, 0, 0, 0);
  return d;
}

function formatWeekRange(monday) {
  const sat = new Date(monday);
  sat.setDate(monday.getDate() + 5);
  const months = ['января','февраля','марта','апреля','мая','июня',
                  'июля','августа','сентября','октября','ноября','декабря'];
  const m1 = months[monday.getMonth()];
  const m2 = months[sat.getMonth()];
  return m1 === m2
    ? `${monday.getDate()} — ${sat.getDate()} ${m1}`
    : `${monday.getDate()} ${m1} — ${sat.getDate()} ${m2}`;
}

/* ============ Сборка сетки ============ */
function buildGrid(lessons) {
  const grid = {};
  const slotsMap = new Map();

  const MAX_PAIRS = 3;   // ← ограничиваем до 3 пар в день

  lessons.forEach((lesson) => {
    const dayObj = DAYS.find((d) => d.apiName === lesson.day);
    if (!dayObj) return;

    const pairNum = Number(lesson.number);

    // ❗ Пропускаем пары выше MAX_PAIRS
    if (pairNum > MAX_PAIRS) return;

    if (!slotsMap.has(pairNum)) {
      slotsMap.set(pairNum, {
        number: pairNum,
        start: lesson.start,
        end: lesson.end,
      });
    }

    if (!grid[dayObj.id]) grid[dayObj.id] = {};
    grid[dayObj.id][pairNum] = lesson;
  });

  currentSlots = PAIR_SLOTS;
  return grid;
}
/* ============ Рендер ============ */
function renderGrid() {
  const gridEl = document.getElementById('week-grid');
  const rangeEl = document.getElementById('week-range');

  if (!currentLessons.length) {
    gridEl.innerHTML = `
      <p class="muted" style="grid-column:1/-1; text-align:center; padding:32px;">
        Расписание пусто. Обратитесь к завучу.
      </p>`;
    rangeEl.textContent = formatWeekRange(currentMonday);
    return;
  }

  const grid = buildGrid(currentLessons);
  const slots = currentSlots;

  // Колонки: время + 6 дней
  gridEl.style.gridTemplateColumns =
    `90px repeat(${DAYS.length}, minmax(110px, 1fr))`;

  let html = `<div class="week-corner"></div>`;

  // Заголовки дней
  DAYS.forEach((d, i) => {
    const date = new Date(currentMonday);
    date.setDate(currentMonday.getDate() + i);
    const dd = String(date.getDate()).padStart(2, '0');
    const mm = String(date.getMonth() + 1).padStart(2, '0');
    html += `
      <div class="week-day" data-day="${d.id}">
        <div class="day-name">${d.short}</div>
        <div class="day-date">${dd}.${mm}</div>
      </div>`;
  });

  // Строки: время + уроки по каждому дню
  slots.forEach((slot) => {
    html += `
      <div class="time-cell">
        <span class="time-start">${slot.number} пара</span>
        <span class="time-end">${slot.start}–${slot.end}</span>
      </div>`;

    DAYS.forEach((d) => {
      const lesson = grid[d.id] && grid[d.id][slot.number];
      if (lesson) {
        const style = subjectStyle(lesson.subject_name);
        const teacher = (lesson.teacher || '').trim() || `#${lesson.teacher_id}`;
        html += `
          <div class="lesson-tile" data-subj="${style.key}"
               data-day="${d.id}" data-pair="${slot.number}">
            <div class="lesson-icon">${style.icon}</div>
            <div class="lesson-name">${lesson.subject_name}</div>
            <div class="lesson-teacher">${teacher}</div>
          </div>`;
      } else {
        html += `<div class="lesson-tile empty"></div>`;
      }
    });
  });

  gridEl.innerHTML = html;
  rangeEl.textContent = formatWeekRange(currentMonday);

  const subEl = document.getElementById('topbar-sub');
  if (subEl) {
    subEl.textContent = `Уроков на неделе: ${currentLessons.length}`;
  }
}

/* ============ Модалка ============ */
function openModal(lesson, dayId, pairNum) {
  const day = DAYS.find((d) => d.id === dayId);
  const style = subjectStyle(lesson.subject_name);
  const iconEl = document.getElementById('m-icon');

  iconEl.textContent = style.icon;
  iconEl.style.background = `var(--subj-${style.key}-bg)`;
  iconEl.style.color = `var(--subj-${style.key}-fg)`;

  document.getElementById('m-subject').textContent = lesson.subject_name;
  document.getElementById('m-when').textContent = `${day.full}, ${pairNum}-я пара`;
  document.getElementById('m-time').textContent = `${lesson.start} — ${lesson.end}`;
  document.getElementById('m-teacher').textContent =
    (lesson.teacher || '').trim() || `ID учителя: ${lesson.teacher_id}`;

  document.getElementById('lesson-modal').classList.remove('hidden');
}

function closeModal() {
  document.getElementById('lesson-modal').classList.add('hidden');
}

/* ============ Загрузка с API ============ */
async function loadSchedule() {
  const gridEl = document.getElementById('week-grid');
  if (!gridEl) return;

  gridEl.innerHTML = `
    <p class="muted" style="grid-column:1/-1; text-align:center; padding:32px;">
      Загрузка…
    </p>`;

  try {
    const data = await getSchedule();
    currentLessons = Array.isArray(data) ? data : [];
    renderGrid();
  } catch (err) {
    const msg = err instanceof ApiError ? err.message : String(err);
    gridEl.innerHTML = `
      <p class="error" style="grid-column:1/-1; text-align:center; padding:32px;">
        Ошибка загрузки: ${msg}
      </p>`;
  }
}

/* ============ Инициализация ============ */
function init() {
  // Клик по паре
  const gridEl = document.getElementById('week-grid');
  if (gridEl) {
    gridEl.addEventListener('click', (e) => {
      const tile = e.target.closest('.lesson-tile');
      if (!tile || tile.classList.contains('empty')) return;

      const dayId = Number(tile.dataset.day);
      const pairNum = Number(tile.dataset.pair);

      const lesson = currentLessons.find((l) => {
        const dayObj = DAYS.find((d) => d.id === dayId);
        return l.day === dayObj?.apiName && Number(l.number) === pairNum;
      });

      if (lesson) openModal(lesson, dayId, pairNum);
    });
  }

  // Escape закрывает модалку
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeModal();
  });

  // Стрелки недели
  const prevBtn = document.getElementById('prev-week');
  const nextBtn = document.getElementById('next-week');
  if (prevBtn) {
    prevBtn.addEventListener('click', () => {
      currentMonday.setDate(currentMonday.getDate() - 7);
      renderGrid();
    });
  }
  if (nextBtn) {
    nextBtn.addEventListener('click', () => {
      currentMonday.setDate(currentMonday.getDate() + 7);
      renderGrid();
    });
  }

  // Кнопка обновления
  const refreshBtn = document.getElementById('refresh-btn');
  if (refreshBtn) refreshBtn.addEventListener('click', loadSchedule);

  // Старт
  loadSchedule();
}

document.addEventListener('DOMContentLoaded', init);

export { loadSchedule, closeModal };