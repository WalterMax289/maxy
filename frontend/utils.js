/**
 * MAXY Shared Frontend Utilities
 */

// --- TOAST NOTIFICATIONS ---
function showToast(message, type = 'info') {
    const container = document.getElementById('toastContainer') || createToastContainer();
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;

    const icon = {
        success: '✅',
        error: '❌',
        info: 'ℹ️',
        warning: '⚠️'
    }[type] || 'ℹ️';

    toast.innerHTML = `
        <span class="toast-icon">${icon}</span>
        <span class="toast-message">${message}</span>
    `;

    container.appendChild(toast);
    setTimeout(() => toast.classList.add('show'), 100);

    setTimeout(() => {
        toast.classList.remove('show');
        setTimeout(() => toast.remove(), 400);
    }, 4000);
}

function createToastContainer() {
    const container = document.createElement('div');
    container.id = 'toastContainer';
    container.className = 'toast-container';
    document.body.appendChild(container);
    return container;
}

// --- DAILY UPDATES ---
async function fetchDailyUpdates() {
    try {
        const baseUrl = typeof API_BASE_URL !== 'undefined' ? API_BASE_URL : (localStorage.getItem('maxyBackendUrl') || 'http://localhost:8000');
        const response = await fetch(`${baseUrl}/api/updates`);
        if (!response.ok) throw new Error('Failed to fetch updates');
        return await response.json();
    } catch (error) {
        console.error('Error fetching updates:', error);
        return null;
    }
}

function updateDailyUpdatesUI(data, listElementId = 'updatesHoverList') {
    const listElement = document.getElementById(listElementId);
    if (!data || !data.updates || data.updates.length === 0 || !listElement) return;

    listElement.innerHTML = '';

    const techUpdates = data.updates.filter(u => u.type === 'tech' || u.type === 'feature' || u.type === 'improvement');
    const bengaluruUpdates = data.updates.filter(u => u.type === 'bengaluru' || u.type === 'happening');

    const createSection = (title, updates, titleIcon = '🚀') => {
        if (updates.length > 0) {
            const header = document.createElement('div');
            header.className = 'updates-hover-section-header';
            header.innerHTML = `<span>${titleIcon}</span> ${title}`;
            listElement.appendChild(header);

            updates.forEach(update => {
                const item = document.createElement('div');
                item.className = 'update-hover-item';
                let badgeClass = 'badge-feature';
                if (update.type === 'tech') badgeClass = 'badge-tech';
                if (update.type === 'bengaluru') badgeClass = 'badge-newsflash';

                item.innerHTML = `
                    <div class="update-hover-badge ${badgeClass}">${update.type || 'update'}</div>
                    <div class="update-hover-title">${update.title}</div>
                    <div class="update-hover-desc">${update.description}</div>
                `;
                listElement.appendChild(item);
            });
        }
    };

    createSection('Industry & Tech Updates', techUpdates, '🌐');
    createSection('Bengaluru News Flash', bengaluruUpdates, '⚡');
}
