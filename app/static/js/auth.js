const API_BASE = '';

function setAccessToken(token) {
  try { localStorage.setItem('access_token', token); } catch (_) {}
}
function getAccessToken() {
  try { return localStorage.getItem('access_token'); } catch (_) { return null; }
}
function clearTokens() {
  try { localStorage.removeItem('access_token'); } catch (_) {}
}
function logout() { clearTokens(); }

async function apiFetch(path, options = {}) {
  const headers = new Headers(options.headers || {});
  headers.set('Content-Type', 'application/json');
  const token = getAccessToken();
  if (token) headers.set('Authorization', `Bearer ${token}`);
  const res = await fetch(`${API_BASE}${path}`, { ...options, headers, credentials: 'same-origin' });
  if (!res.ok) throw new Error((await safeMessage(res)) || `HTTP ${res.status}`);
  return res;
}

async function login(usernameOrEmail, password) {
  const payload = { username: usernameOrEmail, password };
  const res = await fetch('/api/auth/login', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.message || 'Login failed');
  if (!data.access_token) throw new Error('No access token received');
  setAccessToken(data.access_token);
  return data;
}

async function register(username, email, password) {
  const payload = { username, email, password };
  const res = await fetch('/api/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(payload),
  });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.message || 'Registration failed');
  return data;
}

async function safeMessage(res) {
  try {
    const data = await res.json();
    return data && data.message ? data.message : null;
  } catch (_) { return null; }
}

// Basic HTML escaping
function escapeHtml(str) {
  if (str == null) return '';
  return String(str)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;')
    .replaceAll("'", '&#039;');
}
