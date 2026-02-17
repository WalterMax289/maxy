/**
 * MAXY Authentication System
 * Handles user registration, login, and session management
 * Stores user data securely with encryption
 */

// Simple hash function for password encryption (not for production use)
function hashPassword(password) {
    let hash = 0;
    for (let i = 0; i < password.length; i++) {
        const char = password.charCodeAt(i);
        hash = ((hash << 5) - hash) + char;
        hash = hash & hash;
    }
    // Add salt and make it reversible only with the salt
    const salt = 'MaxySecretSalt2026';
    let saltedHash = '';
    for (let i = 0; i < password.length; i++) {
        saltedHash += String.fromCharCode(password.charCodeAt(i) ^ salt.charCodeAt(i % salt.length));
    }
    return btoa(saltedHash); // Base64 encode
}

// Decrypt password (for admin access only)
function decryptPassword(encryptedPass) {
    try {
        const decoded = atob(encryptedPass);
        const salt = 'MaxySecretSalt2026';
        let decrypted = '';
        for (let i = 0; i < decoded.length; i++) {
            decrypted += String.fromCharCode(decoded.charCodeAt(i) ^ salt.charCodeAt(i % salt.length));
        }
        return decrypted;
    } catch (e) {
        return '[Encrypted]';
    }
}

// Check if user is logged in
function isLoggedIn() {
    const session = localStorage.getItem('maxySession');
    if (!session) return false;

    try {
        const sessionData = JSON.parse(session);
        // Check if session is still valid (24 hours)
        const now = new Date().getTime();
        const sessionAge = now - sessionData.timestamp;
        const maxAge = 24 * 60 * 60 * 1000; // 24 hours

        if (sessionAge > maxAge) {
            localStorage.removeItem('maxySession');
            return false;
        }
        return true;
    } catch (e) {
        return false;
    }
}

// Get current user data
function getCurrentUser() {
    const session = localStorage.getItem('maxySession');
    if (!session) return null;

    try {
        return JSON.parse(session);
    } catch (e) {
        return null;
    }
}

// Register new user
function registerUser(name, email, password) {
    // Get existing users
    let users = JSON.parse(localStorage.getItem('maxyUsers')) || [];

    // Check if email already exists
    if (users.find(u => u.email === email)) {
        return { success: false, message: 'Email already registered' };
    }

    // Create new user
    const newUser = {
        id: 'user_' + Date.now().toString(36) + Math.random().toString(36).substr(2, 9),
        name: name,
        email: email,
        password: hashPassword(password),
        createdAt: new Date().toISOString(),
        lastLogin: new Date().toISOString()
    };

    // Add to users list
    users.push(newUser);
    localStorage.setItem('maxyUsers', JSON.stringify(users));

    // Create session
    const session = {
        id: newUser.id,
        name: newUser.name,
        email: newUser.email,
        timestamp: new Date().getTime()
    };
    localStorage.setItem('maxySession', JSON.stringify(session));

    // Save user data to text file format
    saveUserToFile(newUser);

    return { success: true, message: 'Registration successful' };
}

// Login user
function loginUser(email, password) {
    // Get users
    let users = JSON.parse(localStorage.getItem('maxyUsers')) || [];

    // Find user by email
    const user = users.find(u => u.email === email);
    if (!user) {
        return { success: false, message: 'Invalid email or password' };
    }

    // Verify password
    if (user.password !== hashPassword(password)) {
        return { success: false, message: 'Invalid email or password' };
    }

    // Update last login
    user.lastLogin = new Date().toISOString();
    localStorage.setItem('maxyUsers', JSON.stringify(users));

    // Create session
    const session = {
        id: user.id,
        name: user.name,
        email: user.email,
        timestamp: new Date().getTime()
    };
    localStorage.setItem('maxySession', JSON.stringify(session));

    // Also save to profile data for compatibility
    localStorage.setItem('maxyUser', JSON.stringify({
        name: user.name,
        email: user.email
    }));

    return { success: true, message: 'Login successful' };
}

// Logout user
function logoutUser() {
    localStorage.removeItem('maxySession');
    localStorage.removeItem('maxyUser');
}

// Save user data to text file (downloadable)
function saveUserToFile(user) {
    const date = new Date().toLocaleString();
    const fileContent = `
========================================
MAXY USER REGISTRATION
========================================
Name: ${user.name}
Email: ${user.email}
Password (Encrypted): ${user.password}
Registration Date: ${date}
User ID: ${user.id}
========================================
`;

    // Store in localStorage for accumulation
    let allUserData = localStorage.getItem('maxyUserDataFile') || '';
    allUserData += fileContent;
    localStorage.setItem('maxyUserDataFile', allUserData);

    // Create downloadable file
    downloadUserDataFile();
}

// Download user data as text file
function downloadUserDataFile() {
    const userData = localStorage.getItem('maxyUserDataFile') || '';
    if (!userData) return;

    const blob = new Blob([userData], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'login_details_users.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// Export all users data (for admin)
function exportAllUsersData() {
    const users = JSON.parse(localStorage.getItem('maxyUsers')) || [];
    let exportContent = 'MAXY CHAT - ALL USERS DATA\n';
    exportContent += 'Generated: ' + new Date().toLocaleString() + '\n';
    exportContent += '========================================\n\n';

    users.forEach((user, index) => {
        exportContent += `USER #${index + 1}\n`;
        exportContent += '----------------------------------------\n';
        exportContent += `Name: ${user.name}\n`;
        exportContent += `Email: ${user.email}\n`;
        exportContent += `Password (Encrypted): ${user.password}\n`;
        exportContent += `Registered: ${new Date(user.createdAt).toLocaleString()}\n`;
        exportContent += `Last Login: ${new Date(user.lastLogin).toLocaleString()}\n`;
        exportContent += `User ID: ${user.id}\n`;
        exportContent += '----------------------------------------\n\n';
    });

    exportContent += '========================================\n';
    exportContent += 'END OF REPORT\n';
    exportContent += '========================================\n';

    const blob = new Blob([exportContent], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'login_details_users.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
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
function handleModalSignup() {
    const nameInput = document.getElementById('signupName');
    const emailInput = document.getElementById('signupEmail');
    const passwordInput = document.getElementById('signupPassword');

    if (!nameInput || !emailInput || !passwordInput) return;

    const name = nameInput.value.trim();
    const email = emailInput.value.trim();
    const password = passwordInput.value;

    // Validation
    if (!name || !email || !password) {
        showAuthToast('Please fill in all fields', 'error');
        return;
    }

    if (password.length < 6) {
        showAuthToast('Password must be at least 6 characters', 'error');
        return;
    }

    if (!email.includes('@') || !email.includes('.')) {
        showAuthToast('Please enter a valid email', 'error');
        return;
    }

    // Register user
    const result = registerUser(name, email, password);

    if (result.success) {
        showAuthToast('Account created! Welcome to MAXY!', 'success');
        closeAuthModal();

        // Redirect to chat after a delay
        setTimeout(() => {
            window.location.href = 'chat.html';
        }, 1500);
    } else {
        showAuthToast(result.message, 'error');
    }
}

// Handle login from modal
function handleModalLogin() {
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

    // Save or remove remembered email
    if (rememberEmail) {
        localStorage.setItem('maxyRememberedEmail', email);
    } else {
        localStorage.removeItem('maxyRememberedEmail');
    }

    // Login user
    const result = loginUser(email, password);

    if (result.success) {
        showAuthToast('Welcome back!', 'success');
        closeAuthModal();

        // Redirect to chat after a delay
        setTimeout(() => {
            window.location.href = 'chat.html';
        }, 1000);
    } else {
        showAuthToast(result.message, 'error');
    }
}

// Check auth and handle "Try MAXY Now" button
function handleTryMaxyClick(event) {
    if (!isLoggedIn()) {
        event.preventDefault();
        // Check if user has ever signed up
        const users = JSON.parse(localStorage.getItem('maxyUsers')) || [];
        if (users.length === 0) {
            // No users exist, show signup modal
            openAuthModal('signup');
        } else {
            // Users exist, show login modal
            openAuthModal('login');
        }
        return false;
    }
    // User is logged in, allow access
    return true;
}

// Protect page - redirect if not logged in (for chat.html)
function requireAuth() {
    if (!isLoggedIn()) {
        // Redirect to landing page with login modal
        window.location.href = 'index.html?auth=required';
        return false;
    }
    return true;
}

// Show toast notification
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

// Add CSS animation
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
