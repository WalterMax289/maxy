/**
 * MAXY Authentication System - Supabase Integration
 * Handles user registration, login, and session management using Supabase
 */

// Supabase client initialization (Variables loaded from config.js)
let supabaseClient = null;
try {
    const hasUrl = typeof SUPABASE_URL !== 'undefined' && SUPABASE_URL;
    const hasKey = typeof SUPABASE_ANON_KEY !== 'undefined' && SUPABASE_ANON_KEY;
    const hasSDK = typeof window.supabase !== 'undefined';

    if (hasUrl && hasKey && hasSDK) {
        supabaseClient = window.supabase.createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
        console.log('✅ Supabase initialized successfully');
    } else {
        if (!hasUrl) console.error('❌ Supabase Error: SUPABASE_URL is missing or empty.');
        if (!hasKey) console.error('❌ Supabase Error: SUPABASE_ANON_KEY is missing or empty.');
        if (!hasSDK) console.error('❌ Supabase Error: Supabase SDK (window.supabase) is not loaded.');
        console.warn('⚠️ Authentication features will be disabled due to missing configuration.');
    }
} catch (e) {
    console.error('❌ Error during Supabase initialization:', e);
}

// Check if user is logged in
async function isLoggedIn() {
    if (!supabaseClient) return false;
    const { data: { session } } = await supabaseClient.auth.getSession();
    return !!session;
}

// Get current user data
async function getCurrentUser() {
    if (!supabaseClient) return null;
    const { data: { user } } = await supabaseClient.auth.getUser();
    if (!user) return null;

    return {
        id: user.id,
        name: user.user_metadata.full_name || user.email.split('@')[0],
        email: user.email,
        createdAt: user.created_at
    };
}

// Register new user
async function registerUser(name, email, password) {
    if (!supabaseClient) return { success: false, message: 'Supabase not initialized' };

    const { data, error } = await supabaseClient.auth.signUp({
        email: email,
        password: password,
        options: {
            data: {
                full_name: name,
                join_date: new Date().toISOString()
            }
        }
    });

    if (error) {
        return { success: false, message: error.message };
    }

    // Success - user might need to verify email depending on Supabase settings
    if (data.user && data.session) {
        // Logged in immediately
        updateLocalState(data.user);
        return { success: true, message: 'Registration successful' };
    } else {
        return { success: true, message: 'Registration successful! Please check your email for verification.' };
    }
}

// Login user
async function loginUser(email, password) {
    if (!supabaseClient) return { success: false, message: 'Supabase not initialized' };

    const { data, error } = await supabaseClient.auth.signInWithPassword({
        email: email,
        password: password
    });

    if (error) {
        return { success: false, message: error.message };
    }

    updateLocalState(data.user);
    return { success: true, message: 'Login successful' };
}

// Update local state for compatibility with chat.js
function updateLocalState(user) {
    if (!user) return;

    const userData = {
        id: user.id,
        name: user.user_metadata.full_name || user.email.split('@')[0],
        email: user.email,
        timestamp: new Date().getTime()
    };

    localStorage.setItem('maxySession', JSON.stringify(userData));
    localStorage.setItem('maxyUser', JSON.stringify({
        name: userData.name,
        email: userData.email
    }));

    // Synchronize userId with chat.js persistent ID
    localStorage.setItem('maxyUserId', user.id);
}

// Logout user
async function logoutUser() {
    if (supabaseClient) {
        await supabaseClient.auth.signOut();
    }
    localStorage.removeItem('maxySession');
    localStorage.removeItem('maxyUser');
    localStorage.removeItem('maxyUserId'); // Allow chat.js to generate a new one if needed or just keep it cleared
}

// Modal-based authentication handlers
function openAuthModal(type = 'login') {
    const modal = document.getElementById('authModal');
    const loginForm = document.getElementById('loginForm');
    const signupForm = document.getElementById('signupForm');

    if (!modal) return;

    modal.style.display = 'flex';

    if (type === 'login') {
        if (loginForm) loginForm.style.display = 'block';
        if (signupForm) signupForm.style.display = 'none';

        // Autofill email if remembered
        const rememberedEmail = localStorage.getItem('maxyRememberedEmail');
        const emailInput = document.getElementById('loginEmail');
        const rememberCheckbox = document.getElementById('rememberEmail');

        if (rememberedEmail && emailInput) {
            emailInput.value = rememberedEmail;
            if (rememberCheckbox) rememberCheckbox.checked = true;
        }
    } else {
        if (loginForm) loginForm.style.display = 'none';
        if (signupForm) signupForm.style.display = 'block';
    }
}

function closeAuthModal() {
    const modal = document.getElementById('authModal');
    if (modal) modal.style.display = 'none';
}

// Handle signup from modal
async function handleModalSignup() {
    const nameInput = document.getElementById('signupName');
    const emailInput = document.getElementById('signupEmail');
    const passwordInput = document.getElementById('signupPassword');

    if (!nameInput || !emailInput || !passwordInput) return;

    const name = nameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value;

    if (!name || !email || !password) {
        showAuthToast('Please fill in all fields', 'error');
        return;
    }

    if (password.length < 6) {
        showAuthToast('Password must be at least 6 characters', 'error');
        return;
    }

    // Register user
    showAuthToast('Creating account...', 'info');
    const result = await registerUser(name, email, password);

    if (result.success) {
        showAuthToast(result.message, 'success');
        if (result.message.includes('check your email')) {
            // Wait a bit then close
            setTimeout(closeAuthModal, 3000);
        } else {
            closeAuthModal();
            setTimeout(() => {
                window.location.href = 'chat.html';
            }, 1500);
        }
    } else {
        showAuthToast(result.message, 'error');
    }
}

// Handle login from modal
async function handleModalLogin() {
    const emailInput = document.getElementById('loginEmail');
    const passwordInput = document.getElementById('loginPassword');
    const rememberCheckbox = document.getElementById('rememberEmail');

    if (!emailInput || !passwordInput) return;

    const email = emailInput.value.trim();
    const password = passwordInput.value;
    const rememberEmail = rememberCheckbox ? rememberCheckbox.checked : false;

    if (!email || !password) {
        showAuthToast('Please enter email and password', 'error');
        return;
    }

    if (rememberEmail) {
        localStorage.setItem('maxyRememberedEmail', email);
    } else {
        localStorage.removeItem('maxyRememberedEmail');
    }

    // Login user
    showAuthToast('Logging in...', 'info');
    const result = await loginUser(email, password);

    if (result.success) {
        showAuthToast('Welcome back!', 'success');
        closeAuthModal();
        setTimeout(() => {
            window.location.href = 'chat.html';
        }, 1000);
    } else {
        showAuthToast(result.message, 'error');
    }
}

// Redirect if not logged in
async function requireAuth() {
    const loggedIn = await isLoggedIn();
    if (!loggedIn) {
        window.location.href = 'index.html?auth=required';
        return false;
    }
    return true;
}

// Toast notification
function showAuthToast(message, type = 'info') {
    const existingToast = document.querySelector('.auth-toast');
    if (existingToast) existingToast.remove();

    const toast = document.createElement('div');
    toast.className = `auth-toast ${type}`;
    toast.textContent = message;
    toast.style.cssText = `
        position: fixed;
        top: 100px;
        left: 50%;
        transform: translateX(-50%);
        background: ${type === 'error' ? '#ef4444' : type === 'success' ? '#22c55e' : '#6b7280'};
        color: white;
        padding: 16px 32px;
        border-radius: 12px;
        font-weight: 600;
        z-index: 10000;
        animation: slideDown 0.3s ease;
        box-shadow: 0 10px 40px rgba(0,0,0,0.3);
    `;

    document.body.appendChild(toast);

    setTimeout(() => {
        toast.style.animation = 'slideUp 0.3s ease';
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

// Initial check when auth.js loads
(async () => {
    const loggedIn = await isLoggedIn();
    if (loggedIn && supabaseClient) {
        const user = await getCurrentUser();
        // Since getCurrentUser returns our simplified object, we need to pass a "user-like" object to updateLocalState
        // or just call updateLocalState with the raw user from Supabase if we had it.
        // Actually, let's just use the session data if available.
        const { data: { user: sbUser } } = await supabaseClient.auth.getUser();
        if (sbUser) updateLocalState(sbUser);
    }
})();

// CSS Animations
const authStyle = document.createElement('style');
authStyle.textContent = `
    @keyframes slideDown {
        from { transform: translateX(-50%) translateY(-100%); opacity: 0; }
        to { transform: translateX(-50%) translateY(0); opacity: 1; }
    }
    @keyframes slideUp {
        from { transform: translateX(-50%) translateY(0); opacity: 1; }
        to { transform: translateX(-50%) translateY(-100%); opacity: 0; }
    }
`;
document.head.appendChild(authStyle);
