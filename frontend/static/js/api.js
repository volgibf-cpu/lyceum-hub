// frontend/static/js/api.js

const API_BASE = localStorage.getItem('api_base') || 'http://127.0.0.1:8000';
const LOGIN_URL = '/app/login.html';
const AFTER_LOGIN_URL = '/app/schedule.html';

export class ApiError extends Error {
  constructor(message, status = 0, payload = null) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.payload = payload;
  }
}

/**
 * Универсальный запрос к API.
 * credentials: 'include' — JWT в cookie, отправляем их с каждым запросом.
 */
export async function apiRequest(path, options = {}) {
  const url = `${API_BASE}${path}`;

  const headers = {
    'Accept': 'application/json',
    ...(options.headers || {}),
  };
  if (options.body) headers['Content-Type'] = 'application/json';

  let response;
  try {
    response = await fetch(url, {
      method: options.method || 'GET',
      headers,
      body: options.body ? JSON.stringify(options.body) : undefined,
      credentials: 'include',
    });
  } catch (networkErr) {
    throw new ApiError('Не удалось связаться с сервером', 0, networkErr);
  }

  // 401 → редирект на страницу логина
  if (response.status === 401) {
    // Только если мы НЕ на странице логина — иначе цикл
    if (!location.pathname.endsWith('login.html')) {
      location.href = LOGIN_URL;
    }
    throw new ApiError('Сессия истекла', 401);
  }

  if (response.status === 204) return null;

  const text = await response.text();
  let data = null;
  try { data = text ? JSON.parse(text) : null; } catch { data = text; }

  if (!response.ok) {
    const detail = data && data.detail ? data.detail : response.statusText;
    throw new ApiError(detail || 'Ошибка запроса', response.status, data);
  }
  return data;
}

/* ============ AUTH ============ */
export async function login(email, password) {
  // Бэкенд ставит cookie сам, нам достаточно дернуть эндпоинт
  return apiRequest('/auth', {
    method: 'POST',
    body: { email, password },
  });
}

export async function logout() {
  try {
    await fetch(`${API_BASE}/auth/logout`, {
      method: 'POST',
      credentials: 'include',
    });
  } catch (e) {
    // даже если ошибка — всё равно редирект
    console.warn('Logout request failed:', e);
  } finally {
    location.href = LOGIN_URL;
  }
}

/* ============ SCHEDULE ============ */
export function getSchedule() {
  return apiRequest('/pair/');
}

/* ============ USERS ============ */
export function getMe() {
  return apiRequest('/users/me');
}

export function updateMe(payload) {
  return apiRequest('/users/me', { method: 'PATCH', body: payload });
}

/* ============ GRADES ============ */
export function getMyGrades() {
  return apiRequest('/grade/me');
}

/* ============ Константы для редиректов ============ */
export const URLS = {
  login: LOGIN_URL,
  afterLogin: AFTER_LOGIN_URL,
  schedule: '/app/schedule.html',
  grades: '/app/grades.html',
  profile: '/app/profile.html',
  index: '/app/index.html',
};