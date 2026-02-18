// ===== CHAT STATE =====
let chats = JSON.parse(localStorage.getItem('maxyChats')) || [];
let currentChatId = null;
let pendingDeleteId = null;
let currentModel = localStorage.getItem('maxyCurrentModel') || 'maxy1.1';
let editingMessageId = null;

// Generate or retrieve persistent user ID for credit tracking
let userId = localStorage.getItem('maxyUserId');
if (!userId) {
  userId = 'user_' + Date.now().toString(36) + Math.random().toString(36).substr(2, 9);
  localStorage.setItem('maxyUserId', userId);
}

// Backend URL configuration - can be overridden via localStorage or auto-detected
// For production deployment on Vercel, set BACKEND_URL to your deployed backend
// Example: const BACKEND_URL = 'https://your-backend-name.vercel.app';
// Auto-detect: if served by backend (port 8000 or same origin), use relative URLs
// Otherwise default to localhost:8000 for development
const PRODUCTION_BACKEND_URL = ''; // <-- SET YOUR DEPLOYED BACKEND URL HERE (e.g., 'https://maxy-api.vercel.app');

// Auto-detect backend URL based on current location
function detectBackendUrl() {
  // If already on port 8000, use relative URLs (same origin)
  if (window.location.port === '8000' || window.location.port === '8001') {
    return '';
  }
  // If served from static path, backend is likely on same host
  if (window.location.pathname.includes('/static/')) {
    return '';
  }
  // Check localStorage for manual override
  const stored = localStorage.getItem('maxyBackendUrl');
  if (stored) return stored;
  // Default to localhost
  return 'http://localhost:8000';
}

const BACKEND_URL = PRODUCTION_BACKEND_URL || detectBackendUrl();
console.log('Backend URL configured as:', BACKEND_URL || '(same origin - relative URLs)');
let isBackendConnected = false;
let connectionCheckInterval = null;

// Credit system - persists across new chats via userId
let userCredits = {
  enabled: false,
  credits_remaining: 30,
  max_credits: 30,
  refresh_hours: 3,
  next_refresh: null
};
let creditsCheckInterval = null;

// ===== AUTHENTICATION & NAVIGATION =====
// API Base URL for production deployment
const API_BASE_URL = window.location.hostname === 'localhost'
  ? (BACKEND_URL || 'http://localhost:8000')
  : 'https://your-backend-name.onrender.com';  // <-- UPDATE THIS WITH YOUR RENDER BACKEND URL

// Check if user is authenticated (has active session in localStorage)
function isAuthenticated() {
  const session = localStorage.getItem('maxySession');
  if (!session) return false;

  try {
    const sessionData = JSON.parse(session);
    // userId is synchronized with Supabase UUID in auth.js
    userId = localStorage.getItem('maxyUserId');
    return !!sessionData.id && !!userId;
  } catch (e) {
    return false;
  }
}

// Redirect to landing page if not authenticated
function checkAuthAndRedirect() {
  // Only check on chat page
  const isChatPage = window.location.pathname.includes('chat.html') || window.location.pathname === '/chat';
  if (isChatPage) {
    if (!isAuthenticated()) {
      // Redirect to landing page
      window.location.href = 'index.html?auth=required';
      return false;
    }
  }
  return true;
}

// Run auth check immediately
checkAuthAndRedirect();

// ===== DOM ELEMENTS =====
const textarea = document.getElementById("messageInput");
const welcome = document.getElementById("welcome");
const messagesContainer = document.getElementById("messages");
const sendBtn = document.getElementById("sendBtn");
const newChatBtn = document.getElementById("newChatBtn");
const recentsList = document.getElementById("recentsList");
const uploadBtn = document.querySelector(".upload-btn");
const submenu = document.querySelector(".upload-submenu");
const submenuButtons = document.querySelectorAll(".upload-submenu button");
const deleteModal = document.getElementById("deleteModal");
const cancelDelete = document.getElementById("cancelDelete");
const confirmDelete = document.getElementById("confirmDelete");

// MAXY Selector Elements (unified dropdown)
const maxyTrigger = document.getElementById('maxyTrigger');
const maxyMenu = document.getElementById('maxyMenu');
const maxyVersion = document.getElementById('maxyVersion');

// User Profile Elements (Header)
const profileBtnHeader = document.getElementById('profileBtnHeader');
const mobileSidebarToggle = document.getElementById('mobileSidebarToggle');
const sidebarToggleDesktop = document.getElementById('sidebarToggleDesktop');
const sidebar = document.querySelector('.sidebar');
const sidebarBackdrop = document.getElementById('sidebarBackdrop');
const chatContent = document.querySelector('.chat-content');

// File upload variables
let uploadedFile = null;
let uploadedFileContent = null;

const fileIndicator = document.getElementById('fileIndicator');
const fileName = document.getElementById('fileName');
const fileIcon = document.getElementById('fileIcon');
const clearFileBtn = document.getElementById('clearFileBtn');

// User Profile Elements
const userProfileBtn = document.getElementById('userProfileBtn');
const userMenu = document.getElementById('userMenu');

// ===== UTILITY FUNCTIONS =====
function formatTime(date) {
  const now = new Date();
  const d = new Date(date);
  const today = now.toDateString() === d.toDateString();
  const yesterday = new Date(now.setDate(now.getDate() - 1)).toDateString() === d.toDateString();
  if (today) {
    return d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  } else if (yesterday) {
    return 'Yesterday';
  } else {
    return d.toLocaleDateString([], { month: 'short', day: 'numeric' });
  }
}

function formatFullTime(date) {
  const d = new Date(date);
  return d.toLocaleString([], {
    month: 'short',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  });
}

function generateId() {
  return Date.now().toString(36) + Math.random().toString(36).substr(2);
}

// ===== CONNECTION STATUS - Color Only =====
// Red = Disconnected, Orange = Connecting, Green = Connected
function updateConnectionStatus(status, message) {
  const dot = document.getElementById('statusDot');
  const statusContainer = document.getElementById('connectionStatus');
  const banner = document.getElementById('connectionBanner');
  if (!dot) return;

  if (status === 'connected') {
    dot.style.background = '#22c55e'; // Green
    dot.style.boxShadow = '0 0 10px #22c55e';
    isBackendConnected = true;
    if (statusContainer) {
      statusContainer.title = 'Connected to backend - Click to refresh';
    }
    // Hide banner when connected
    if (banner) banner.style.display = 'none';
  } else if (status === 'disconnected') {
    dot.style.background = '#ef4444'; // Red
    dot.style.boxShadow = '0 0 10px #ef4444';
    isBackendConnected = false;
    if (statusContainer) {
      statusContainer.title = 'Not connected - Click to retry';
    }
    // Show banner when disconnected
    if (banner) banner.style.display = 'block';
  } else {
    dot.style.background = '#f59e0b'; // Orange/Yellow
    dot.style.boxShadow = '0 0 10px #f59e0b';
    if (statusContainer) {
      statusContainer.title = 'Connecting...';
    }
  }
}

async function checkBackendConnection() {
  try {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), 3000);

    // Use relative URL if BACKEND_URL is empty (when frontend is served by backend)
    // Try health endpoint first, then fallback to root API endpoint
    const urls = BACKEND_URL ?
      [`${BACKEND_URL}/health`, `${BACKEND_URL}/api`] :
      ['/health', '/api'];

    let lastError = null;
    for (const url of urls) {
      try {
        const response = await fetch(url, {
          method: 'GET',
          signal: controller.signal,
          headers: {
            'Accept': 'application/json'
          }
        });

        clearTimeout(timeoutId);

        if (response.ok) {
          const data = await response.json();
          const status = data.status || 'healthy';
          updateConnectionStatus('connected', `Connected (${status})`);
          console.log('✅ Backend connected:', url, data);

          // Show connection restored message if was disconnected
          if (!isBackendConnected) {
            showToast('Connected to backend!');
          }
          return true;
        }
      } catch (err) {
        lastError = err;
        console.log('Connection attempt failed:', url, err.message);
        continue;
      }
    }

    throw lastError || new Error('All connection attempts failed');

  } catch (error) {
    updateConnectionStatus('disconnected', 'Backend Offline');
    console.error('Backend connection error:', error);
    console.log('Current BACKEND_URL:', BACKEND_URL || '(relative - served by backend)');
    console.log('Make sure to start the backend server: python backend/server.py');
    return false;
  }
}

function startConnectionMonitoring() {
  checkBackendConnection();
  connectionCheckInterval = setInterval(checkBackendConnection, 30000);
}

function stopConnectionMonitoring() {
  if (connectionCheckInterval) {
    clearInterval(connectionCheckInterval);
    connectionCheckInterval = null;
  }
}

// ===== CREDIT SYSTEM =====
async function checkCredits() {
  try {
    // Build URL with user_id query parameter for consistent credit tracking
    let url = BACKEND_URL ? `${BACKEND_URL}/credits` : '/credits';
    url += `?user_id=${encodeURIComponent(userId)}`;

    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'X-User-ID': userId
      }
    });

    if (response.ok) {
      const data = await response.json();

      if (data.credits_enabled) {
        userCredits = {
          enabled: true,
          credits_remaining: data.credits_remaining,
          max_credits: data.max_credits,
          refresh_hours: data.refresh_hours,
          next_refresh: data.next_refresh
        };
        updateCreditsDisplay();

        // Show modal if out of credits
        if (userCredits.credits_remaining === 0) {
          showCreditsExhaustedModal();
        }
      } else {
        userCredits.enabled = false;
        hideCreditsDisplay();
      }
    }
  } catch (error) {
    console.log('Credit check failed:', error);
    hideCreditsDisplay();
  }
}

function updateCreditsDisplay() {
  const creditsDisplay = document.getElementById('creditsDisplay');
  const creditsText = document.getElementById('creditsText');

  if (!userCredits.enabled) {
    hideCreditsDisplay();
    return;
  }

  creditsDisplay.style.display = 'flex';

  if (userCredits.credits_remaining === 0) {
    creditsText.textContent = `Out of credits!`;
    creditsText.style.color = '#ff6b6b';
    creditsDisplay.style.background = 'linear-gradient(135deg, rgba(239, 68, 68, 0.9), rgba(185, 28, 28, 0.9))';
  } else if (userCredits.credits_remaining <= 5) {
    creditsText.textContent = `${userCredits.credits_remaining}/${userCredits.max_credits} messages left`;
    creditsText.style.color = '#ffd93d';
    creditsDisplay.style.background = 'linear-gradient(135deg, rgba(245, 158, 11, 0.9), rgba(217, 119, 6, 0.9))';
  } else {
    creditsText.textContent = `${userCredits.credits_remaining}/${userCredits.max_credits} messages`;
    creditsText.style.color = '#fff';
    creditsDisplay.style.background = 'linear-gradient(135deg, rgba(99, 102, 241, 0.9), rgba(168, 85, 247, 0.9))';
  }
}

function hideCreditsDisplay() {
  const creditsDisplay = document.getElementById('creditsDisplay');
  if (creditsDisplay) {
    creditsDisplay.style.display = 'none';
  }
}

// ===== USER PROFILE MANAGEMENT =====
function loadUserProfile() {
  console.log('Loading user profile...');

  const userDataStr = localStorage.getItem('maxyUser');
  console.log('User data from localStorage:', userDataStr);

  const userData = userDataStr ? JSON.parse(userDataStr) : {};
  const profileBtn = document.getElementById('profileBtnHeader');

  console.log('Profile button found:', !!profileBtn);

  if (!profileBtn) {
    console.error('Profile button not found!');
    return;
  }

  const avatarEl = profileBtn.querySelector('.profile-avatar');
  const nameEl = profileBtn.querySelector('.profile-name');

  console.log('Avatar element:', !!avatarEl, 'Name element:', !!nameEl);

  // Update name
  const displayName = userData.name || 'Guest';
  console.log('Display name:', displayName);
  if (nameEl) {
    nameEl.textContent = displayName;
  }

  // Update avatar
  if (avatarEl) {
    if (userData.avatar) {
      console.log('Using custom avatar');
      // User has custom avatar
      avatarEl.innerHTML = `<img src="${userData.avatar}" alt="Profile" style="width: 100%; height: 100%; border-radius: 50%; object-fit: cover;">`;
    } else if (userData.email) {
      console.log('Using email initial');
      // Use first letter of email
      const firstLetter = userData.email.charAt(0).toUpperCase();
      avatarEl.textContent = firstLetter;
    } else {
      console.log('Using default avatar');
      // Default emoji avatar
      avatarEl.textContent = '👤';
    }
  }
}

// Listen for storage changes to update profile in real-time
window.addEventListener('storage', (e) => {
  if (e.key === 'maxyUser') {
    loadUserProfile();
  }
});

// Also reload profile when page becomes visible (user returns from profile page)
document.addEventListener('visibilitychange', () => {
  if (document.visibilityState === 'visible') {
    console.log('Page became visible, reloading profile...');
    loadUserProfile();
  }
});

// Listen for profile updates from other pages (profile.html)
if (typeof BroadcastChannel !== 'undefined') {
  try {
    const profileChannel = new BroadcastChannel('maxy_profile_updates');
    profileChannel.onmessage = (event) => {
      console.log('Received profile update via BroadcastChannel:', event.data);
      if (event.data && event.data.type === 'profile_updated') {
        loadUserProfile();
      }
    };
    console.log('BroadcastChannel initialized');
  } catch (e) {
    console.log('BroadcastChannel not supported');
  }
}

// Fallback: Check for profile updates every 2 seconds
let lastUserData = localStorage.getItem('maxyUser');
setInterval(() => {
  const currentUserData = localStorage.getItem('maxyUser');
  if (currentUserData !== lastUserData) {
    console.log('Profile data changed, reloading...');
    lastUserData = currentUserData;
    loadUserProfile();
  }
}, 2000);

function showCreditsExhaustedModal() {
  const modal = document.getElementById('creditsModal');
  modal.style.display = 'flex';
  startCreditsCountdown();
}

function startCreditsCountdown() {
  if (!userCredits.next_refresh) return;

  const countdownEl = document.getElementById('creditsCountdown');
  const refreshTime = new Date(userCredits.next_refresh).getTime();

  const updateCountdown = () => {
    const now = new Date().getTime();
    const distance = refreshTime - now;

    if (distance <= 0) {
      countdownEl.textContent = '00:00:00';
      checkCredits(); // Refresh credits
      return;
    }

    const hours = Math.floor(distance / (1000 * 60 * 60));
    const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
    const seconds = Math.floor((distance % (1000 * 60)) / 1000);

    countdownEl.textContent =
      `${String(hours).padStart(2, '0')}:${String(minutes).padStart(2, '0')}:${String(seconds).padStart(2, '0')}`;
  };

  updateCountdown();
  creditsCheckInterval = setInterval(updateCountdown, 1000);
}

// Click credits display to refresh
document.addEventListener('DOMContentLoaded', () => {
  const creditsDisplay = document.getElementById('creditsDisplay');
  if (creditsDisplay) {
    creditsDisplay.addEventListener('click', () => {
      checkCredits();
      showToast('Credits refreshed!');
    });
  }
});

function saveChats() {
  localStorage.setItem('maxyChats', JSON.stringify(chats));
}

function updateChatsAndUI() {
  saveChats();
  renderRecents();
}

function scrollToBottom(smooth = true) {
  if (messagesContainer) {
    if (smooth) {
      messagesContainer.scrollTo({
        top: messagesContainer.scrollHeight,
        behavior: 'smooth'
      });
    } else {
      messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
  }
}

function toggleChatView(showMessages) {
  if (showMessages) {
    welcome.classList.add('hidden');
    messagesContainer.classList.add('active');
    messagesContainer.style.display = 'flex';
    setTimeout(() => scrollToBottom(true), 100);
  } else {
    welcome.classList.remove('hidden');
    messagesContainer.classList.remove('active');
    messagesContainer.style.display = 'none';
  }
}

function autoGrow() {
  textarea.style.height = "auto";
  textarea.style.height = Math.min(textarea.scrollHeight, 150) + "px";
}

function formatFileSize(bytes) {
  if (bytes === 0) return '0 Bytes';
  const k = 1024;
  const sizes = ['Bytes', 'KB', 'MB', 'GB'];
  const i = Math.floor(Math.log(bytes) / Math.log(k));
  return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

// ===== SCROLL TO BOTTOM BUTTON =====
function createScrollToBottomButton() {
  const btn = document.createElement('button');
  btn.className = 'scroll-to-bottom';
  btn.innerHTML = '↓';
  btn.setAttribute('aria-label', 'Scroll to bottom');
  btn.addEventListener('click', () => scrollToBottom(true));
  document.body.appendChild(btn);
  return btn;
}

const scrollToBottomBtn = createScrollToBottomButton();

function updateScrollButton() {
  const isNearBottom = chatContent.scrollHeight - chatContent.scrollTop - chatContent.clientHeight < 100;
  if (isNearBottom) {
    scrollToBottomBtn.classList.remove('visible');
  } else {
    scrollToBottomBtn.classList.add('visible');
  }
}

chatContent.addEventListener('scroll', updateScrollButton);

// ===== CHAT MANAGEMENT =====
function createNewChat() {
  const newChat = {
    id: Date.now(),
    timestamp: new Date().toISOString(),
    title: "New Chat",
    messages: []
  };
  chats.unshift(newChat);
  switchToChat(newChat.id);
  updateChatsAndUI();

  // Visual feedback
  newChatBtn.classList.add('bounce');
  setTimeout(() => newChatBtn.classList.remove('bounce'), 600);
}

function switchToChat(chatId) {
  currentChatId = chatId;
  const chat = chats.find(c => c.id === chatId);
  messagesContainer.innerHTML = "";
  const hasMessages = chat && chat.messages.length > 0;
  toggleChatView(hasMessages);
  if (hasMessages) {
    chat.messages.forEach((msg, index) => {
      setTimeout(() => addMessageToDOM(msg.text, msg.role, msg.id, false), index * 50);
    });
  }
  document.querySelectorAll('.recent-item').forEach(el => el.classList.remove('active'));
  newChatBtn.classList.toggle('active', !chatId);
  if (chatId) {
    const activeRecent = document.querySelector(`.recent-item[data-id="${chatId}"]`);
    if (activeRecent) activeRecent.classList.add('active');
  }
  textarea.focus();
  setTimeout(() => scrollToBottom(false), 100);
}

function renderRecents() {
  recentsList.innerHTML = "";
  chats.forEach((chat, index) => {
    const div = document.createElement('div');
    div.className = 'recent-item';
    div.dataset.id = chat.id;
    div.style.animationDelay = `${index * 0.05}s`;

    const title = document.createElement('span');
    title.className = 'recent-title';
    title.textContent = chat.title;

    const deleteBtn = document.createElement('button');
    deleteBtn.className = 'recent-item-delete';
    deleteBtn.innerHTML = '×';
    deleteBtn.title = 'Delete chat';
    deleteBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      pendingDeleteId = chat.id;
      deleteModal.classList.add('active');
    });

    div.appendChild(title);
    div.appendChild(deleteBtn);
    div.addEventListener('click', () => switchToChat(chat.id));
    recentsList.appendChild(div);
  });
}

// ===== MESSAGE HANDLING =====
function escapeHtml(text) {
  const div = document.createElement('div');
  div.textContent = text;
  return div.innerHTML;
}

function createMessageActions(text, role, messageId) {
  const actionsDiv = document.createElement('div');
  actionsDiv.className = 'message-actions';
  actionsDiv.style.cssText = `
    position: absolute;
    ${role === 'user' ? 'left: -40px' : 'right: -40px'};
    top: 50%;
    transform: translateY(-50%) scale(0.8);
    opacity: 0;
    display: flex;
    flex-direction: column;
    gap: 4px;
    transition: all 0.2s ease;
    z-index: 10;
  `;

  // Copy button
  const copyBtn = document.createElement('button');
  copyBtn.innerHTML = '📋';
  copyBtn.title = 'Copy message';
  copyBtn.style.cssText = `
    background: rgba(255,255,255,0.1);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 50%;
    width: 32px;
    height: 32px;
    cursor: pointer;
    font-size: 14px;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: all 0.2s ease;
  `;
  copyBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    copyToClipboard(text.replace(/<[^>]*>/g, ''));
    showToast('Copied to clipboard!');
  });
  copyBtn.addEventListener('mouseenter', () => {
    copyBtn.style.background = 'rgba(255,255,255,0.2)';
    copyBtn.style.transform = 'scale(1.1)';
  });
  copyBtn.addEventListener('mouseleave', () => {
    copyBtn.style.background = 'rgba(255,255,255,0.1)';
    copyBtn.style.transform = 'scale(1)';
  });
  actionsDiv.appendChild(copyBtn);

  if (role === 'ai') {
    // Like button
    const likeBtn = document.createElement('button');
    likeBtn.innerHTML = '👍';
    likeBtn.title = 'Good response';
    likeBtn.style.cssText = copyBtn.style.cssText;
    likeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      likeBtn.style.background = 'rgba(16, 185, 129, 0.3)';
      showToast('Thanks for your feedback!');
    });
    likeBtn.addEventListener('mouseenter', () => {
      likeBtn.style.background = 'rgba(255,255,255,0.2)';
      likeBtn.style.transform = 'scale(1.1)';
    });
    likeBtn.addEventListener('mouseleave', () => {
      if (!likeBtn.style.background.includes('16, 185, 129')) {
        likeBtn.style.background = 'rgba(255,255,255,0.1)';
      }
      likeBtn.style.transform = 'scale(1)';
    });
    actionsDiv.appendChild(likeBtn);

    // Dislike button
    const dislikeBtn = document.createElement('button');
    dislikeBtn.innerHTML = '👎';
    dislikeBtn.title = 'Bad response';
    dislikeBtn.style.cssText = copyBtn.style.cssText;
    dislikeBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      dislikeBtn.style.background = 'rgba(239, 68, 68, 0.3)';
      showToast('Thanks for your feedback!');
    });
    dislikeBtn.addEventListener('mouseenter', () => {
      dislikeBtn.style.background = 'rgba(255,255,255,0.2)';
      dislikeBtn.style.transform = 'scale(1.1)';
    });
    dislikeBtn.addEventListener('mouseleave', () => {
      if (!dislikeBtn.style.background.includes('239, 68, 68')) {
        dislikeBtn.style.background = 'rgba(255,255,255,0.1)';
      }
      dislikeBtn.style.transform = 'scale(1)';
    });
    actionsDiv.appendChild(dislikeBtn);

    // Regenerate button
    const regenBtn = document.createElement('button');
    regenBtn.innerHTML = '🔄';
    regenBtn.title = 'Regenerate response';
    regenBtn.style.cssText = copyBtn.style.cssText;
    regenBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      regenerateResponse(messageId);
    });
    regenBtn.addEventListener('mouseenter', () => {
      regenBtn.style.background = 'rgba(255,255,255,0.2)';
      regenBtn.style.transform = 'scale(1.1)';
    });
    regenBtn.addEventListener('mouseleave', () => {
      regenBtn.style.background = 'rgba(255,255,255,0.1)';
      regenBtn.style.transform = 'scale(1)';
    });
    actionsDiv.appendChild(regenBtn);
  } else {
    // Edit button for user messages
    const editBtn = document.createElement('button');
    editBtn.innerHTML = '✏️';
    editBtn.title = 'Edit message';
    editBtn.style.cssText = copyBtn.style.cssText;
    editBtn.addEventListener('click', (e) => {
      e.stopPropagation();
      editMessage(messageId, text);
    });
    editBtn.addEventListener('mouseenter', () => {
      editBtn.style.background = 'rgba(255,255,255,0.2)';
      editBtn.style.transform = 'scale(1.1)';
    });
    editBtn.addEventListener('mouseleave', () => {
      editBtn.style.background = 'rgba(255,255,255,0.1)';
      editBtn.style.transform = 'scale(1)';
    });
    actionsDiv.appendChild(editBtn);
  }

  return actionsDiv;
}

function createMessageElement(text, role, messageId = null, animate = true) {
  const messageDiv = document.createElement("div");
  messageDiv.className = `message ${role}`;
  messageDiv.dataset.messageId = messageId || generateId();
  messageDiv.style.position = 'relative';

  // Handle HTML content or plain text
  if (text.includes('<') && text.includes('>')) {
    messageDiv.innerHTML = text;
  } else {
    messageDiv.innerHTML = escapeHtml(text).replace(/\n/g, '<br>');
  }

  // Add timestamp tooltip
  const timestamp = document.createElement('div');
  timestamp.className = 'message-timestamp';
  timestamp.textContent = formatFullTime(new Date());
  timestamp.style.cssText = `
    position: absolute;
    ${role === 'user' ? 'right: 0' : 'left: 0'};
    bottom: -20px;
    font-size: 11px;
    color: rgba(255,255,255,0.4);
    opacity: 0;
    transition: opacity 0.2s ease;
    white-space: nowrap;
  `;
  messageDiv.appendChild(timestamp);

  // Add actions
  const actions = createMessageActions(text, role, messageDiv.dataset.messageId);
  messageDiv.appendChild(actions);

  // Hover effects
  messageDiv.addEventListener('mouseenter', () => {
    actions.style.opacity = '1';
    actions.style.transform = 'translateY(-50%) scale(1)';
    timestamp.style.opacity = '1';
  });
  messageDiv.addEventListener('mouseleave', () => {
    actions.style.opacity = '0';
    actions.style.transform = 'translateY(-50%) scale(0.8)';
    timestamp.style.opacity = '0';
  });

  return messageDiv;
}

function addMessageToDOM(text, role, messageId = null, animate = true) {
  const messageDiv = createMessageElement(text, role, messageId, animate);

  if (!animate) {
    messageDiv.style.animation = 'none';
  }

  messagesContainer.appendChild(messageDiv);
  scrollToBottom(true);
  updateScrollButton();

  return messageDiv.dataset.messageId;
}

function showTypingIndicator() {
  const indicator = document.createElement("div");
  indicator.className = "typing-indicator-container";
  indicator.id = "typingIndicator";
  indicator.style.cssText = `
    align-self: flex-start;
    background: var(--ai-bg);
    color: var(--ai-text);
    padding: 16px 24px;
    border-radius: 20px;
    border-bottom-left-radius: 6px;
    box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    animation: fadeInUp 0.3s ease;
  `;
  indicator.innerHTML = `
    <div class="typing-indicator" style="display: flex; gap: 4px; align-items: center;">
      <span style="width: 8px; height: 8px; background: #999; border-radius: 50%; animation: typing 1.4s infinite;"></span>
      <span style="width: 8px; height: 8px; background: #999; border-radius: 50%; animation: typing 1.4s infinite 0.2s;"></span>
      <span style="width: 8px; height: 8px; background: #999; border-radius: 50%; animation: typing 1.4s infinite 0.4s;"></span>
    </div>
  `;
  messagesContainer.appendChild(indicator);
  scrollToBottom(true);
}

function hideTypingIndicator() {
  const indicator = document.getElementById("typingIndicator");
  if (indicator) {
    indicator.style.opacity = '0';
    indicator.style.transform = 'translateY(10px)';
    setTimeout(() => indicator.remove(), 300);
  }
}

function addMessage(text, role) {
  if (!currentChatId) createNewChat();
  const chat = chats.find(c => c.id === currentChatId);
  const timestamp = new Date().toISOString();
  const messageId = generateId();
  chat.messages.push({ text, role, time: timestamp, id: messageId });
  chat.timestamp = timestamp;
  if (chat.messages.length === 1 && role === 'user') {
    chat.title = text.substring(0, 30) + (text.length > 30 ? '...' : '');
  }
  addMessageToDOM(text, role, messageId);
  updateChatsAndUI();
  return messageId;
}

function regenerateResponse(messageId) {
  const chat = chats.find(c => c.id === currentChatId);
  if (!chat) return;

  // Find the user message that prompted this AI response
  const messageIndex = chat.messages.findIndex(m => m.id === messageId);
  if (messageIndex <= 0) return;

  // Find the previous user message
  let userMessageIndex = messageIndex - 1;
  while (userMessageIndex >= 0 && chat.messages[userMessageIndex].role !== 'user') {
    userMessageIndex--;
  }

  if (userMessageIndex < 0) return;

  const userMessage = chat.messages[userMessageIndex];

  // Remove the old AI response
  chat.messages.splice(messageIndex, 1);

  // Remove from DOM
  const messageEl = document.querySelector(`[data-message-id="${messageId}"]`);
  if (messageEl) {
    messageEl.style.opacity = '0';
    messageEl.style.transform = 'scale(0.9)';
    setTimeout(() => messageEl.remove(), 300);
  }

  // Resend the user message
  textarea.value = userMessage.text;
  sendMessage();

  showToast('Regenerating response...');
}

function editMessage(messageId, currentText) {
  const cleanText = currentText.replace(/<[^>]*>/g, '');
  textarea.value = cleanText;
  textarea.focus();
  autoGrow();
  editingMessageId = messageId;
  showToast('Edit your message and press Enter to send');
}

// ===== QUICK REPLIES =====
function showQuickReplies(suggestions) {
  const existingQuickReplies = document.querySelector('.quick-replies');
  if (existingQuickReplies) existingQuickReplies.remove();

  const quickRepliesDiv = document.createElement('div');
  quickRepliesDiv.className = 'quick-replies';
  quickRepliesDiv.style.cssText = `
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
    margin-top: 12px;
    padding: 0 24px;
    animation: fadeInUp 0.4s ease;
  `;

  suggestions.slice(0, 3).forEach((suggestion, index) => {
    const btn = document.createElement('button');
    btn.textContent = suggestion;
    btn.style.cssText = `
      background: rgba(255,255,255,0.08);
      border: 1px solid rgba(255,255,255,0.15);
      border-radius: 16px;
      padding: 8px 16px;
      color: var(--text);
      font-size: 13px;
      cursor: pointer;
      transition: all 0.2s ease;
      opacity: 0;
      animation: fadeInUp 0.3s ease forwards;
      animation-delay: ${index * 0.1}s;
    `;
    btn.addEventListener('mouseenter', () => {
      btn.style.background = 'rgba(255,255,255,0.15)';
      btn.style.borderColor = 'rgba(255,255,255,0.3)';
      btn.style.transform = 'translateY(-2px)';
    });
    btn.addEventListener('mouseleave', () => {
      btn.style.background = 'rgba(255,255,255,0.08)';
      btn.style.borderColor = 'rgba(255,255,255,0.15)';
      btn.style.transform = 'translateY(0)';
    });
    btn.addEventListener('click', () => {
      textarea.value = suggestion;
      sendMessage();
      quickRepliesDiv.remove();
    });
    quickRepliesDiv.appendChild(btn);
  });

  messagesContainer.appendChild(quickRepliesDiv);
  scrollToBottom(true);
}

// ===== CLIPBOARD FUNCTIONS =====
async function copyToClipboard(text) {
  try {
    await navigator.clipboard.writeText(text);
  } catch (err) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    document.execCommand('copy');
    document.body.removeChild(textArea);
  }
}

function showToast(message) {
  const existingToast = document.querySelector('.toast-notification');
  if (existingToast) existingToast.remove();

  const toast = document.createElement('div');
  toast.className = 'toast-notification';
  toast.textContent = message;
  toast.style.cssText = `
    position: fixed;
    bottom: 100px;
    left: 50%;
    transform: translateX(-50%) translateY(20px);
    background: rgba(30, 30, 30, 0.95);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.1);
    padding: 12px 24px;
    border-radius: 10px;
    color: #fff;
    font-size: 14px;
    z-index: 1000;
    opacity: 0;
    transition: all 0.3s ease;
    box-shadow: 0 10px 40px rgba(0,0,0,0.4);
  `;

  document.body.appendChild(toast);

  requestAnimationFrame(() => {
    toast.style.opacity = '1';
    toast.style.transform = 'translateX(-50%) translateY(0)';
  });

  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(-50%) translateY(20px)';
    setTimeout(() => toast.remove(), 300);
  }, 2000);
}

// ===== FALLBACK AI RESPONSES =====
const FALLBACK_RESPONSES = [
  "I'm here to help! What would you like to know?",
  "That's an interesting question. Let me think about it...",
  "I understand. Please tell me more.",
  "I'd be happy to assist you with that.",
  "Could you provide more details so I can help better?",
  "I'm processing your request...",
  "Great question! Here's what I think...",
  "I'm analyzing that for you...",
];

const QUICK_REPLY_SUGGESTIONS = [
  "Tell me more",
  "Can you explain that?",
  "What do you mean?",
  "Give me an example",
  "Why is that?",
  "How does it work?",
];

// ===== MESSAGE SENDING =====
async function sendMessage() {
  const text = textarea.value.trim();
  if (!text && !uploadedFile) return;

  // Check credits first
  if (userCredits.enabled && userCredits.credits_remaining <= 0) {
    showCreditsExhaustedModal();
    showToast('You have no credits remaining. Please wait for refresh.');
    return;
  }

  // Check backend connection
  const isConnected = await checkBackendConnection();

  // Show warning if not connected
  if (!isConnected) {
    showToast('Not connected to backend. Starting in offline mode...');
  }

  if (!currentChatId) createNewChat();

  // Handle editing
  if (editingMessageId) {
    const chat = chats.find(c => c.id === currentChatId);
    const messageIndex = chat.messages.findIndex(m => m.id === editingMessageId);
    if (messageIndex !== -1) {
      // Remove the old message and its AI response
      chat.messages.splice(messageIndex, 2);
      // Remove from DOM
      const messageEl = document.querySelector(`[data-message-id="${editingMessageId}"]`);
      if (messageEl) {
        const aiResponseEl = messageEl.nextElementSibling;
        messageEl.style.opacity = '0';
        messageEl.style.transform = 'scale(0.9)';
        setTimeout(() => messageEl.remove(), 300);
        if (aiResponseEl && aiResponseEl.classList.contains('ai')) {
          aiResponseEl.style.opacity = '0';
          aiResponseEl.style.transform = 'scale(0.9)';
          setTimeout(() => aiResponseEl.remove(), 300);
        }
      }
    }
    editingMessageId = null;
  }

  if (text) {
    addMessage(text, "user");
  }

  textarea.value = "";
  autoGrow();
  toggleChatView(true);
  showTypingIndicator();
  sendBtn.disabled = true;

  // Remove existing quick replies
  const existingQuickReplies = document.querySelector('.quick-replies');
  if (existingQuickReplies) existingQuickReplies.remove();

  // If not connected to backend, still try to send the request
  // The backend might be running even if the initial check failed
  if (!isConnected) {
    console.log('Initial connection check failed, but attempting to send request anyway...');
    showToast('Attempting to connect to backend...');
  }

  const chat = chats.find(c => c.id === currentChatId);
  const history = chat.messages.slice(0, -1).map(m => ({
    role: m.role === 'user' ? 'user' : 'assistant',
    content: m.text.replace(/<[^>]*>/g, '')
  }));

  const controller = new AbortController();
  const timeoutId = setTimeout(() => controller.abort(), 30000);

  try {
    const requestBody = {
      message: text || "Please analyze the uploaded file.",
      model: currentModel,
      history: history,
      user_id: userId  // Include user ID for credit tracking
    };

    if (uploadedFile && uploadedFileContent) {
      const maxSize = 10 * 1024 * 1024;
      if (uploadedFile.size > maxSize) {
        hideTypingIndicator();
        addMessage(`❌ File too large. Maximum size is 10MB. Your file is ${formatFileSize(uploadedFile.size)}.`, "ai");
        sendBtn.disabled = false;
        return;
      }

      requestBody.file = {
        name: uploadedFile.name,
        type: uploadedFile.type,
        size: uploadedFile.size,
        content: uploadedFileContent
      };
    }

    const chatUrl = BACKEND_URL ? `${BACKEND_URL}/chat` : '/chat';
    const response = await fetch(chatUrl, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(requestBody),
      signal: controller.signal
    });

    clearTimeout(timeoutId);
    hideTypingIndicator();

    if (!response.ok) {
      const errorData = await response.json().catch(() => ({}));
      const errorMessage = errorData.detail || `Server error: ${response.status}`;

      if (response.status === 413) {
        addMessage(`❌ ${errorMessage}`, "ai");
      } else if (response.status === 429) {
        addMessage(`⏳ Rate limit exceeded. Please wait a moment before trying again.`, "ai");
      } else if (response.status >= 500) {
        addMessage(`❌ Server error (${response.status}). Please try again later.`, "ai");
      } else {
        addMessage(`❌ ${errorMessage}`, "ai");
      }
      sendBtn.disabled = false;
      return;
    }

    const data = await response.json();

    addMessage(data.response || "No response received.", "ai");

    if (data.charts && data.charts.length > 0) {
      data.charts.forEach(chart => {
        const chartHtml = `<img src="data:image/png;base64,${chart.base64_image}" alt="${chart.description}" style="max-width: 100%; border-radius: 8px; margin-top: 10px;" />`;
        addMessageToDOM(chartHtml, "ai");
      });
    }

    if (data.suggestions && data.suggestions.length > 0) {
      showQuickReplies(data.suggestions);
    } else {
      showQuickReplies(QUICK_REPLY_SUGGESTIONS);
    }

    if (uploadedFile && data.fileProcessed) {
      clearUploadedFile();
    }

    sendBtn.disabled = false;
  } catch (err) {
    clearTimeout(timeoutId);
    hideTypingIndicator();
    sendBtn.disabled = false;

    if (err.name === 'AbortError') {
      addMessage("⏱️ Request timed out. The server took too long to respond. Please try again.", "ai");
    } else if (err.message && err.message.includes('fetch')) {
      // Backend not available - use offline fallback responses
      console.log('Backend not available, using offline mode');
      const lowerText = text.toLowerCase();
      let response = FALLBACK_RESPONSES[Math.floor(Math.random() * FALLBACK_RESPONSES.length)];

      if (lowerText.includes('hello') || lowerText.includes('hi')) {
        response = "Hello! Nice to meet you! How can I help you today?";
      } else if (lowerText.includes('help')) {
        response = "I'm here to help! I can answer questions, have conversations, or just chat. What do you need?";
      } else if (lowerText.includes('time')) {
        response = `The current time is ${new Date().toLocaleTimeString()}.`;
      } else if (lowerText.includes('date') || lowerText.includes('day')) {
        response = `Today is ${new Date().toLocaleDateString('en-US', { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' })}.`;
      } else if (lowerText.includes('your name')) {
        response = "I'm MAXY, your AI assistant! I'm running in offline mode right now since the backend server isn't connected. Start the server by running START_SERVER.bat";
      } else if (lowerText.includes('thank')) {
        response = "You're welcome! Happy to help!";
      } else if (lowerText.includes('bye')) {
        response = "Goodbye! Have a great day!";
      } else if (lowerText.includes('server') || lowerText.includes('backend') || lowerText.includes('connect')) {
        response = "To connect to the backend:\n1. Close this browser tab\n2. Run START_SERVER.bat\n3. Wait for 'Uvicorn running' message\n4. Refresh this page";
      }

      addMessage(response + "\n\n⚠️ Running in offline mode. Start the server for full AI features.", "ai");
      updateConnectionStatus('disconnected', 'Connection Failed');
    } else {
      console.error("Backend error:", err);
      addMessage("❌ An unexpected error occurred. Please try again.", "ai");
    }
  }
}

// ===== FILE UPLOAD FUNCTIONS =====
function showFileIndicator(file) {
  fileIndicator.classList.add('visible');
  fileName.textContent = file.name;

  if (file.type.startsWith('image/')) {
    fileIcon.textContent = '🖼️';
  } else if (file.type === 'application/pdf') {
    fileIcon.textContent = '📄';
  } else if (file.type.includes('word') || file.name.endsWith('.doc') || file.name.endsWith('.docx')) {
    fileIcon.textContent = '📝';
  } else if (file.type.includes('text') || file.name.endsWith('.txt')) {
    fileIcon.textContent = '📃';
  } else {
    fileIcon.textContent = '📎';
  }

  uploadBtn.style.background = 'var(--primary)';
  uploadBtn.style.borderColor = 'var(--primary)';
}

function clearUploadedFile() {
  uploadedFile = null;
  uploadedFileContent = null;
  fileIndicator.classList.remove('visible');
  fileName.textContent = '';
  document.querySelectorAll('.hidden-file-input').forEach(input => input.value = '');
  uploadBtn.style.background = '';
  uploadBtn.style.borderColor = '';
}

// ===== MODEL SELECTION =====
function syncModelUI() {
  document.querySelectorAll('.model-option').forEach(o => {
    o.classList.remove('selected');
    o.style.transform = '';
  });
  const selectedOption = document.querySelector(`.model-option[data-model="${currentModel}"]`);
  if (selectedOption) {
    selectedOption.classList.add('selected');

    // Update version display in the trigger button
    const modelName = selectedOption.querySelector('.model-name').textContent;
    const version = modelName.replace('MAXY ', '');
    if (maxyVersion) {
      maxyVersion.textContent = version;
    }

    // Add visual feedback
    selectedOption.style.transform = 'translateX(10px)';
    setTimeout(() => {
      selectedOption.style.transform = '';
    }, 300);
  }
}

// ===== DRAG AND DROP =====
function setupDragAndDrop() {
  const inputContainer = document.querySelector('.input-container');

  ['dragenter', 'dragover', 'dragleave', 'drop'].forEach(eventName => {
    inputContainer.addEventListener(eventName, preventDefaults, false);
    document.body.addEventListener(eventName, preventDefaults, false);
  });

  function preventDefaults(e) {
    e.preventDefault();
    e.stopPropagation();
  }

  ['dragenter', 'dragover'].forEach(eventName => {
    inputContainer.addEventListener(eventName, highlight, false);
  });

  ['dragleave', 'drop'].forEach(eventName => {
    inputContainer.addEventListener(eventName, unhighlight, false);
  });

  function highlight(e) {
    inputContainer.classList.add('drag-over');
  }

  function unhighlight(e) {
    inputContainer.classList.remove('drag-over');
  }

  inputContainer.addEventListener('drop', handleDrop, false);

  function handleDrop(e) {
    const dt = e.dataTransfer;
    const files = dt.files;

    if (files.length > 0) {
      handleFiles(files[0]);
    }
  }

  function handleFiles(file) {
    uploadedFile = file;
    showFileIndicator(file);

    const reader = new FileReader();

    if (file.type.startsWith('image/')) {
      reader.onload = (event) => {
        uploadedFileContent = event.target.result;
        addMessageToDOM(`<img src="${event.target.result}" style="max-width: 300px; max-height: 200px; border-radius: 12px; margin-top: 10px;" />`, "user");
        addMessage("Image uploaded successfully! What would you like to know about it?", "ai");
      };
      reader.readAsDataURL(file);
    } else {
      reader.onload = (event) => {
        uploadedFileContent = event.target.result;
        addMessage(`📎 File "${file.name}" ready (${formatFileSize(file.size)}). This file will be sent with your next message.`, "user");
      };
      reader.readAsDataURL(file);
    }

    showToast(`File "${file.name}" ready to upload`);
  }
}

// ===== EVENT LISTENERS =====

// Textarea
textarea.addEventListener("input", autoGrow);
textarea.addEventListener("keydown", e => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage();
  }
});

// Send button
sendBtn.addEventListener("click", sendMessage);

// Chat management
newChatBtn.addEventListener('click', createNewChat);

// Upload button
uploadBtn.addEventListener("click", (e) => {
  e.stopPropagation();
  submenu.classList.toggle("open");
});

document.addEventListener("click", () => {
  submenu.classList.remove("open");
});

submenuButtons.forEach(btn => {
  btn.addEventListener("click", () => {
    const type = btn.dataset.type;
    let inputId;
    if (type === "image") inputId = "file-image";
    else if (type === "pdf") inputId = "file-pdf";
    else if (type === "doc") inputId = "file-doc";
    else inputId = "file-any";
    document.getElementById(inputId).click();
    submenu.classList.remove("open");
  });
});

// File clear button
clearFileBtn.addEventListener('click', clearUploadedFile);

// File input change listeners
document.querySelectorAll(".hidden-file-input").forEach(input => {
  input.addEventListener("change", async (e) => {
    if (e.target.files.length > 0) {
      const file = e.target.files[0];
      uploadedFile = file;

      showFileIndicator(file);

      const reader = new FileReader();

      if (file.type.startsWith('image/')) {
        reader.onload = (event) => {
          uploadedFileContent = event.target.result;
          addMessageToDOM(`<img src="${event.target.result}" style="max-width: 300px; max-height: 200px; border-radius: 12px; margin-top: 10px;" />`, "user");
          addMessage("Image uploaded successfully! What would you like to know about it?", "ai");
        };
        reader.readAsDataURL(file);
      } else if (file.type === 'application/pdf' || file.type.includes('text') || file.name.endsWith('.txt') || file.name.endsWith('.doc') || file.name.endsWith('.docx')) {
        reader.onload = (event) => {
          uploadedFileContent = event.target.result;
          addMessage(`📄 Document "${file.name}" ready for analysis (${formatFileSize(file.size)})`, "user");
        };
        reader.readAsDataURL(file);
      } else {
        reader.onload = (event) => {
          uploadedFileContent = event.target.result;
          addMessage(`📎 File "${file.name}" ready (${formatFileSize(file.size)}). This file will be sent with your next message.`, "user");
        };
        reader.readAsDataURL(file);
      }
    }
  });
});

// Delete modal
cancelDelete.addEventListener('click', () => {
  deleteModal.classList.remove('active');
  pendingDeleteId = null;
});

confirmDelete.addEventListener('click', () => {
  if (!pendingDeleteId) return;
  chats = chats.filter(c => c.id !== pendingDeleteId);
  updateChatsAndUI();
  if (currentChatId === pendingDeleteId) {
    currentChatId = null;
    messagesContainer.innerHTML = "";
    toggleChatView(false);
    newChatBtn.classList.add('active');
  }
  deleteModal.classList.remove('active');
  pendingDeleteId = null;
  showToast('Chat deleted');
});

// MAXY Selector Dropdown (unified)
maxyTrigger.addEventListener('click', (e) => {
  e.stopPropagation();
  const isOpen = maxyMenu.classList.contains('active');
  maxyMenu.classList.toggle('active', !isOpen);
  maxyTrigger.setAttribute('aria-expanded', !isOpen);
});

document.addEventListener('click', (e) => {
  if (!e.target.closest('.maxy-selector')) {
    maxyMenu.classList.remove('active');
    maxyTrigger.setAttribute('aria-expanded', 'false');
  }
});

document.querySelectorAll('.model-option').forEach(option => {
  option.addEventListener('click', () => {
    currentModel = option.dataset.model;
    localStorage.setItem('maxyCurrentModel', currentModel);
    syncModelUI();
    maxyMenu.classList.remove('active');
    maxyTrigger.setAttribute('aria-expanded', 'false');
    showToast(`Switched to ${option.querySelector('.model-name').textContent}`);
  });
});

// Mobile sidebar toggle
mobileSidebarToggle.addEventListener('click', (e) => {
  e.stopPropagation();
  sidebar.classList.toggle('open');
  mobileSidebarToggle.classList.toggle('active');
  sidebarBackdrop.classList.toggle('active');
  document.body.style.overflow = sidebar.classList.contains('open') ? 'hidden' : '';
});

// Desktop sidebar toggle
sidebarToggleDesktop.addEventListener('click', (e) => {
  e.stopPropagation();
  sidebar.classList.toggle('collapsed');
});

// Close sidebar when clicking backdrop
sidebarBackdrop.addEventListener('click', () => {
  sidebar.classList.remove('open');
  mobileSidebarToggle.classList.remove('active');
  sidebarBackdrop.classList.remove('active');
  document.body.style.overflow = '';
});

// Close sidebar when clicking outside (mobile only)
document.addEventListener('click', (e) => {
  if (window.innerWidth <= 768 && !e.target.closest('.sidebar') && !e.target.closest('.mobile-sidebar-toggle')) {
    sidebar.classList.remove('open');
    mobileSidebarToggle.classList.remove('active');
    sidebarBackdrop.classList.remove('active');
    document.body.style.overflow = '';
  }
});

// User Profile Menu (Sidebar)
if (userProfileBtn && userMenu) {
  userProfileBtn.addEventListener('click', (e) => {
    e.stopPropagation();
    const isOpen = userMenu.classList.contains('active');
    userMenu.classList.toggle('active', !isOpen);
    userProfileBtn.setAttribute('aria-expanded', !isOpen);
  });

  // Close user menu when clicking outside
  document.addEventListener('click', (e) => {
    if (!e.target.closest('.sidebar-footer')) {
      userMenu.classList.remove('active');
      userProfileBtn.setAttribute('aria-expanded', 'false');
    }
  });

  // User menu item handlers
  document.querySelectorAll('.user-menu-item').forEach(item => {
    item.addEventListener('click', (e) => {
      // Don't handle click if it has an onclick attribute (like profile link)
      if (item.hasAttribute('onclick')) {
        return;
      }

      const action = item.dataset.action;
      if (action === 'settings') {
        showToast('Settings feature coming soon!');
      } else if (action === 'logout') {
        showToast('Logged out successfully!');
        // Clear any user data
        localStorage.removeItem('maxyUser');
      }
      userMenu.classList.remove('active');
      userProfileBtn.setAttribute('aria-expanded', 'false');
    });
  });
}

// Header Profile Button - Now redirects to profile.html directly (no dropdown needed)

// Keyboard shortcuts
document.addEventListener('keydown', (e) => {
  // Ctrl/Cmd + K for search
  if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
    e.preventDefault();
    document.querySelector('.search-bar input').focus();
  }

  // Escape to close modals and dropdowns
  if (e.key === 'Escape') {
    deleteModal.style.display = 'none';
    maxyMenu.classList.remove('active');
    maxyTrigger.setAttribute('aria-expanded', 'false');
    userMenu.classList.remove('active');
    userProfileBtn.setAttribute('aria-expanded', 'false');
    submenu.classList.remove('open');
    // Close mobile sidebar
    if (window.innerWidth <= 768) {
      sidebar.classList.remove('open');
      mobileSidebarToggle.classList.remove('active');
      sidebarBackdrop.classList.remove('active');
      document.body.style.overflow = '';
    }
  }

  // Ctrl/Cmd + N for new chat
  if ((e.ctrlKey || e.metaKey) && e.key === 'n') {
    e.preventDefault();
    createNewChat();
  }

  // Ctrl/Cmd + / for help
  if ((e.ctrlKey || e.metaKey) && e.key === '/') {
    e.preventDefault();
    showToast('Keyboard shortcuts: Ctrl+K (Search), Ctrl+N (New Chat), Ctrl+/ (Help), Esc (Close)');
  }
});

// ===== INITIALIZATION =====
document.addEventListener('DOMContentLoaded', () => {
  console.log('DOM loaded, initializing...');
  syncModelUI();
  renderRecents();
  startConnectionMonitoring();
  setupDragAndDrop();
  loadUserProfile(); // Load user profile data

  // Add click handler to connection status for manual retry
  const statusContainer = document.getElementById('connectionStatus');
  if (statusContainer) {
    statusContainer.addEventListener('click', async () => {
      showToast('Checking connection...');
      const connected = await checkBackendConnection();
      if (connected) {
        showToast('Connected!');
        checkCredits();
      } else {
        showToast('Not connected. Make sure server is running.');
      }
    });
  }

  // Check credits on load with a slight delay to ensure backend is ready
  setTimeout(() => {
    checkCredits();
  }, 1000);

  // Initial connection check with retry
  checkBackendConnection().then(connected => {
    if (!connected) {
      console.log('Initial connection failed. Will retry automatically...');
      // Retry after 3 seconds
      setTimeout(() => {
        checkBackendConnection();
      }, 3000);
    }
  });
});

// Periodically check credits
setInterval(checkCredits, 30000); // Check every 30 seconds

// Cleanup on page unload
window.addEventListener('beforeunload', () => {
  stopConnectionMonitoring();
  if (creditsCheckInterval) clearInterval(creditsCheckInterval);
});

// Initial scroll to bottom update
updateScrollButton();

// Add CSS for enhanced animations
const style = document.createElement('style');
style.textContent = `
  @keyframes messageSlideIn {
    from {
      opacity: 0;
      transform: translateY(20px) scale(0.95);
    }
    to {
      opacity: 1;
      transform: translateY(0) scale(1);
    }
  }
  
  .message {
    animation: messageSlideIn 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  }
  
  /* Connection status dot pulse animation */
  @keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.7; transform: scale(1.1); }
  }
  
  .status-dot {
    animation: pulse 2s ease-in-out infinite;
  }
  
  .scroll-to-bottom {
    position: fixed;
    bottom: 100px;
    right: 30px;
    width: 44px;
    height: 44px;
    border-radius: 50%;
    background: rgba(30, 30, 30, 0.9);
    border: 1px solid rgba(255,255,255,0.1);
    color: white;
    font-size: 20px;
    cursor: pointer;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    transform: translateY(20px);
    transition: all 0.3s ease;
    z-index: 100;
    box-shadow: 0 4px 12px rgba(0,0,0,0.3);
  }
  
  .scroll-to-bottom.visible {
    opacity: 1;
    transform: translateY(0);
  }
  
  .scroll-to-bottom:hover {
    background: rgba(50, 50, 50, 0.95);
    transform: translateY(-2px);
  }
  
  /* Credits display styles */
  .credits-display {
    transition: all 0.3s ease;
  }
  
  .credits-display:hover {
    background: rgba(0,0,0,0.9) !important;
    transform: scale(1.05);
  }
  
  /* Credits modal animation */
  @keyframes modalFadeIn {
    from {
      opacity: 0;
      transform: scale(0.9);
    }
    to {
      opacity: 1;
      transform: scale(1);
    }
  }
  
  #creditsModal > div {
    animation: modalFadeIn 0.3s ease;
  }
`;
document.head.appendChild(style);
