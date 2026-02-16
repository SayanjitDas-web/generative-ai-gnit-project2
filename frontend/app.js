const API_URL = window.location.origin === 'null' || window.location.protocol === 'file:' ? 'http://localhost:8000' : window.location.origin;
let token = localStorage.getItem('token');
let currentSessionId = null;

// DOM Elements
const landingSection = document.getElementById('landing-section');
const authSection = document.getElementById('auth-section');
const dashboardSection = document.getElementById('dashboard-section');
const chatSection = document.getElementById('chat-section');
const resultsSection = document.getElementById('results-section');

const authForm = document.getElementById('auth-form');
const authSubmit = document.getElementById('auth-submit');
const authToggle = document.getElementById('auth-toggle');
const emailInput = document.getElementById('email');

const getStartedBtn = document.getElementById('get-started-btn');

// App Initialization
async function init() {
    if (token) {
        showDashboard();
    } else {
        showLanding();
    }
}

// Navigation
function showLanding() {
    hideAll();
    landingSection.style.display = 'flex';
}

function showAuth() {
    hideAll();
    authSection.style.display = 'block';
}

async function showDashboard() {
    hideAll();
    dashboardSection.style.display = 'block';
    loadSessions();
}

function showChat(sessionId, topic) {
    hideAll();
    currentSessionId = sessionId;
    document.getElementById('chat-topic').textContent = topic;
    chatSection.style.display = 'flex';
    loadChatHistory(sessionId);
}

const mainNav = document.getElementById('main-nav');
const navLogin = document.getElementById('nav-login');
const navCta = document.getElementById('nav-cta');

function hideAll() {
    landingSection.style.display = 'none';
    authSection.style.display = 'none';
    dashboardSection.style.display = 'none';
    chatSection.style.display = 'none';
    resultsSection.style.display = 'none';
    mainNav.style.display = 'none';
}

function showLanding() {
    hideAll();
    landingSection.style.display = 'flex';
    mainNav.style.display = 'flex';
}

function showAuth() {
    hideAll();
    authSection.style.display = 'block';
    mainNav.style.display = 'flex';
}

function showDashboard() {
    hideAll();
    dashboardSection.style.display = 'block';
    loadSessions();
}

getStartedBtn.addEventListener('click', showAuth);
navLogin.addEventListener('click', (e) => { e.preventDefault(); showAuth(); });
navCta.addEventListener('click', showAuth);

// Auth Logic
authToggle.addEventListener('click', (e) => {
    e.preventDefault();
    const isLogin = authSubmit.textContent === 'Login';
    authSubmit.textContent = isLogin ? 'Sign Up' : 'Login';
    document.getElementById('auth-title').textContent = isLogin ? 'Create Account' : 'Welcome Back';
    emailInput.style.display = isLogin ? 'block' : 'none';
    authToggle.textContent = isLogin ? 'Login' : 'Sign Up';
    document.getElementById('auth-toggle-text').textContent = isLogin ? 'Already have an account?' : "Don't have an account?";
});

authForm.addEventListener('submit', async (e) => {
    e.preventDefault();
    const mode = authSubmit.textContent === 'Login' ? 'login' : 'register';
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    const email = emailInput.value;

    try {
        if (mode === 'register') {
            await fetch(`${API_URL}/auth/register`, {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ username, email, password })
            });
            alert('Account created! Please login.');
            authToggle.click();
        } else {
            const formData = new FormData();
            formData.append('username', username);
            formData.append('password', password);

            const res = await fetch(`${API_URL}/auth/login`, {
                method: 'POST',
                body: formData
            });
            const data = await res.json();
            if (data.access_token) {
                token = data.access_token;
                localStorage.setItem('token', token);
                showDashboard();
            } else {
                alert(data.detail || 'Login failed');
            }
        }
    } catch (err) {
        alert('Authentication error');
    }
});

document.getElementById('logout-btn').addEventListener('click', () => {
    localStorage.removeItem('token');
    token = null;
    showAuth();
});

// Dashboard Logic
async function loadSessions() {
    const res = await fetch(`${API_URL}/sessions/`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const sessions = await res.json();
    const grid = document.getElementById('sessions-grid');
    grid.innerHTML = sessions.map(s => `
        <div class="session-card glass animate-fade" onclick="showChat(${s.id}, '${s.topic}')">
            <h3>${s.topic}</h3>
            <p style="color: var(--text-muted)">Difficulty: ${s.difficulty}</p>
            <p style="margin-top: 1rem; font-weight: 600; color: ${s.status === 'Completed' ? '#10b981' : '#6366f1'}">${s.status}</p>
        </div>
    `).join('');
}

document.getElementById('create-session-btn').addEventListener('click', async () => {
    const topic = document.getElementById('new-topic').value;
    const difficulty = document.getElementById('new-difficulty').value;
    if (!topic) return alert('Enter a topic');

    const res = await fetch(`${API_URL}/sessions/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ topic, difficulty })
    });
    const session = await res.json();
    showChat(session.id, topic);
});

// Chat Logic
async function loadChatHistory(sessionId) {
    const res = await fetch(`${API_URL}/sessions/${sessionId}/history`, {
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const messages = await res.json();
    const historyDiv = document.getElementById('chat-history');
    historyDiv.innerHTML = messages.map(m => `
        <div class="message ${m.role}">
            ${m.content}
        </div>
    `).join('');
    historyDiv.scrollTop = historyDiv.scrollHeight;
}

document.getElementById('send-msg-btn').addEventListener('click', sendMessage);
document.getElementById('chat-input').addEventListener('keypress', (e) => {
    if (e.key === 'Enter') sendMessage();
});

async function sendMessage() {
    const input = document.getElementById('chat-input');
    const content = input.value;
    if (!content) return;

    input.value = '';

    // Optimistic UI
    const historyDiv = document.getElementById('chat-history');
    historyDiv.innerHTML += `<div class="message user">${content}</div>`;
    historyDiv.scrollTop = historyDiv.scrollHeight;

    const res = await fetch(`${API_URL}/sessions/${currentSessionId}/chat`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ role: 'user', content })
    });
    const aiMsg = await res.json();
    historyDiv.innerHTML += `<div class="message assistant">${aiMsg.content}</div>`;
    historyDiv.scrollTop = historyDiv.scrollHeight;
}

document.getElementById('end-interview-btn').addEventListener('click', async () => {
    if (!confirm('Are you sure you want to end this session and generate feedback?')) return;

    const res = await fetch(`${API_URL}/sessions/${currentSessionId}/analyze`, {
        method: 'POST',
        headers: { 'Authorization': `Bearer ${token}` }
    });
    const session = await res.json();
    showResults(session);
});

function showResults(session) {
    hideAll();
    resultsSection.style.display = 'block';
    const content = document.getElementById('results-content');
    const f = session.feedback;

    content.innerHTML = `
        <div class="glass" style="padding: 2rem; grid-column: 1 / -1; text-align: center;">
            <h1 style="font-size: 4rem; color: var(--primary);">${f.overall_score}/100</h1>
            <p>Overall Performance Score</p>
        </div>
        <div class="glass" style="padding: 2rem;">
            <h3 style="color: #10b981; margin-bottom: 1rem;">Strengths</h3>
            <ul>${f.strengths.map(s => `<li>${s}</li>`).join('')}</ul>
        </div>
        <div class="glass" style="padding: 2rem;">
            <h3 style="color: #ef4444; margin-bottom: 1rem;">Areas for Improvement</h3>
            <ul>${f.weaknesses.map(w => `<li>${w}</li>`).join('')}</ul>
        </div>
        <div class="glass" style="padding: 2rem; grid-column: 1 / -1;">
            <h3 style="margin-bottom: 1rem;">Recommendations</h3>
            <p>${f.recommendations.join('. ')}</p>
        </div>
    `;
}

document.getElementById('back-to-dashboard').addEventListener('click', showDashboard);
document.getElementById('results-back-btn').addEventListener('click', showDashboard);

init();
