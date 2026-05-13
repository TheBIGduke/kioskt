// Made by Kaléin Tamaríz
const API = "/api";
let currentProducts = [];
const DEFAULT_IMAGE = '/default_product.svg';
let currentAudio = null;

async function init() {
    const [cats, prods] = await Promise.all([
        fetch(`${API}/categories`).then(r => r.json()),
        fetch(`${API}/products`).then(r => r.json())
    ]);
    renderFilters(cats);
    renderProducts(prods);
    checkDbStatus();
    setupEventListeners();
}

function playProductAudio(id) {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio = null;
    }
    currentAudio = new Audio(`/audio-assets/${id}.mp3`);
    currentAudio.play().catch(err => console.log("Audio playback not started (Interaction required or file missing)"));
}

function stopProductAudio() {
    if (currentAudio) {
        currentAudio.pause();
        currentAudio = null;
    }
}

function setupEventListeners() {
    // Close button
    document.getElementById('close-detail')?.addEventListener('click', closeDetail);

    // Close on background click (optional but nice)
    document.getElementById('product-detail-view')?.addEventListener('click', (e) => {
        if (e.target.id === 'product-detail-view') closeDetail();
    });

    // Close on Escape key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') closeDetail();
    });
}

async function checkDbStatus() {
    try {
        const res = await fetch(`${API}/db-status`);
        const data = await res.json();
        if (data.status === 'fallback') {
            const badge = document.getElementById('db-status-badge');
            badge.style.display = 'inline-block';
            if (data.error) {
                badge.title = `Database Error: ${data.error}\n\nA database is required for live data synchronization.`;
            }
        }
    } catch (e) {
        console.error("Failed to check DB status", e);
    }
}

let filterDockClickBound = false;

function renderFilters(cats) {
    const dock = document.getElementById('filter-dock');
    dock.innerHTML = '<button class="filter-btn active" data-category-id="null">TODOS</button>';
    cats.forEach(c => {
        dock.innerHTML += `<button class="filter-btn" data-category-id="${c.id}">${c.name}</button>`;
    });

    if (!filterDockClickBound) {
        filterDockClickBound = true;
        dock.addEventListener('click', (e) => {
            const btn = e.target.closest('.filter-btn');
            if (!btn) return;
            const id = btn.dataset.categoryId === 'null' ? null : btn.dataset.categoryId;
            filter(id, btn);
        });
    }
}

async function filter(id, el) {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    el.classList.add('active');
    spawnRipple(el.getBoundingClientRect().left + el.offsetWidth / 2,
        el.getBoundingClientRect().top + el.offsetHeight / 2);
    const url = id ? `${API}/products?category_id=${id}` : `${API}/products`;
    const res = await fetch(url);
    renderProducts(await res.json());
}

function renderProducts(prods) {
    currentProducts = prods;
    const grid = document.getElementById('catalog-grid');
    grid.innerHTML = prods.map(p => {
        const img = (p.primary_image && p.primary_image !== '') ? p.primary_image : DEFAULT_IMAGE;
        return `
            <div class="col">
                <div class="card h-100" data-product-id="${p.id}">
                    <img src="${img}" class="card-img-top product-img" onerror="this.src='${DEFAULT_IMAGE}'">
                    <div class="card-body d-flex flex-column">
                        <h5 class="card-title">${p.name}</h5>
                        <p class="card-text small mb-4">${p.description || 'No description available.'}</p>
                        <div class="mt-auto d-flex justify-content-between align-items-center">
                            <span class="price-tag">$${p.price.toLocaleString()}</span>
                            <div class="tags">${p.categories.map(c => `<span class="custom-badge me-1">${c}</span>`).join('')}</div>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }).join('');

    // Delegate card clicks
    grid.querySelectorAll('.card').forEach(card => {
        card.addEventListener('click', () => {
            showDetail(parseInt(card.dataset.productId));
        });
    });

    attachTiltEffects();
}

function showDetail(id) {
    const product = currentProducts.find(p => p.id === id);
    if (!product) return;

    const detailView = document.getElementById('product-detail-view');
    const container = document.getElementById('detail-container');

    let media = [];
    if (product.media && Array.isArray(product.media) && product.media.length > 0) {
        media = [...product.media];
    } else if (product.primary_image && product.primary_image !== '') {
        media = [{ media_url: product.primary_image, is_primary: true }];
    } else {
        media = [{ media_url: DEFAULT_IMAGE, is_primary: true }];
    }

    media.sort((a, b) => (b.is_primary ? 1 : 0) - (a.is_primary ? 1 : 0));

    const carouselId = `carousel-${id}`;
    const indicators = media.map((_, i) => `
        <button type="button" data-bs-target="#${carouselId}" data-bs-slide-to="${i}" class="${i === 0 ? 'active' : ''}" aria-label="Slide ${i + 1}"></button>
    `).join('');

    const slides = media.map((m, i) => `
        <div class="carousel-item ${i === 0 ? 'active' : ''}">
            <img src="${m.media_url || DEFAULT_IMAGE}" class="detail-img" onerror="this.src='${DEFAULT_IMAGE}'">
        </div>
    `).join('');

    container.innerHTML = `
        <div class="detail-img-container">
            <div id="${carouselId}" class="carousel slide" data-bs-ride="carousel">
                <div class="carousel-indicators">
                    ${indicators}
                </div>
                <div class="carousel-inner">
                    ${slides}
                </div>
                ${media.length > 1 ? `
                    <button class="carousel-control-prev" type="button" data-bs-target="#${carouselId}" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Previous</span>
                    </button>
                    <button class="carousel-control-next" type="button" data-bs-target="#${carouselId}" data-bs-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Next</span>
                    </button>
                ` : ''}
            </div>
        </div>
        <div class="detail-body">
            <div class="detail-body-inner">
                <div class="detail-sheet-handle" aria-hidden="true"></div>
                <div class="detail-tags">
                    ${product.categories.map(c => `<span class="custom-badge">${c}</span>`).join('')}
                </div>
                <header class="detail-intro">
                    <h1 class="detail-title">${product.name}</h1>
                    <div class="detail-price-row">
                        <span class="detail-price">$${product.price.toLocaleString()}</span>
                    </div>
                </header>
                <p class="detail-desc">${product.description || 'No detailed description available for this item.'}</p>
            </div>
        </div>
    `;

    detailView.classList.add('active');
    document.body.classList.add('detail-open');
    document.body.style.overflow = 'hidden';

    if (media.length > 1) {
        new bootstrap.Carousel(document.getElementById(carouselId), {
            interval: 5000,
            ride: 'carousel'
        });
    }

    playProductAudio(id);
}

function closeDetail() {
    const detailView = document.getElementById('product-detail-view');
    detailView.classList.remove('active');
    document.body.classList.remove('detail-open');
    document.body.style.overflow = '';
    stopProductAudio();
}

init();

// ─── Touch Ripple Helper ───────────────────────────────────────────────
function spawnRipple(x, y) {
    const ring = document.createElement('div');
    ring.className = 'ripple-ring';
    ring.style.left = x + 'px';
    ring.style.top = y + 'px';
    document.body.appendChild(ring);
    ring.addEventListener('animationend', () => ring.remove());
}

// ─── Particle Background ───────────────────────────────────────────────
const canvas = document.getElementById('bg-canvas');
const ctx = canvas.getContext('2d');
let width, height, particles;

let touch = { x: -1000, y: -1000, active: false };

document.addEventListener('touchmove', (e) => {
    if (e.touches.length > 0) {
        touch.x = e.touches[0].clientX;
        touch.y = e.touches[0].clientY;
        touch.active = true;
    }
}, { passive: true });

document.addEventListener('touchstart', (e) => {
    if (e.touches.length > 0) {
        touch.x = e.touches[0].clientX;
        touch.y = e.touches[0].clientY;
        touch.active = true;
        spawnRipple(touch.x, touch.y);
        burstParticles(touch.x, touch.y);
    }
}, { passive: true });

document.addEventListener('touchend', () => {
    touch.active = false;
    touch.x = -1000;
    touch.y = -1000;
});

function burstParticles(cx, cy) {
    if (!particles) return;
    particles.forEach(p => {
        const dx = p.x - cx;
        const dy = p.y - cy;
        const dist = Math.hypot(dx, dy);
        if (dist < 200) {
            const force = (200 - dist) / 200;
            p.vx += (dx / dist) * force * 8;
            p.vy += (dy / dist) * force * 8;
        }
    });
}

function initParticles() {
    width = canvas.width = window.innerWidth;
    height = canvas.height = window.innerHeight;
    particles = [];
    const numParticles = Math.floor((width * height) / 7000);
    for (let i = 0; i < numParticles; i++) {
        particles.push({
            x: Math.random() * width,
            y: Math.random() * height,
            vx: (Math.random() - 0.5) * 1.2,
            vy: (Math.random() - 0.5) * 1.2,
            radius: Math.random() * 2 + 0.4,
            maxSpeed: 1.2 + Math.random() * 0.8
        });
    }
}

function animateParticles() {
    requestAnimationFrame(animateParticles);
    if (!ctx) return;
    ctx.clearRect(0, 0, width, height);

    const LINK_DIST = 120;
    const REPEL_DIST = 130;
    const ATTRACT_DIST = 180;

    for (let i = 0; i < particles.length; i++) {
        const p = particles[i];

        p.vx *= 0.97;
        p.vy *= 0.97;
        const speed = Math.hypot(p.vx, p.vy);
        if (speed > p.maxSpeed) {
            p.vx = (p.vx / speed) * p.maxSpeed;
            p.vy = (p.vy / speed) * p.maxSpeed;
        }

        p.x += p.vx;
        p.y += p.vy;

        if (p.x < 0 || p.x > width) p.vx *= -1;
        if (p.y < 0 || p.y > height) p.vy *= -1;

        if (touch.active) {
            const dxT = touch.x - p.x;
            const dyT = touch.y - p.y;
            const distT = Math.hypot(dxT, dyT);

            if (distT < REPEL_DIST) {
                p.vx -= (dxT / distT) * 0.6;
                p.vy -= (dyT / distT) * 0.6;
            } else if (distT < ATTRACT_DIST) {
                p.vx += (dxT / distT) * 0.08;
                p.vy += (dyT / distT) * 0.08;
            }
        }

        const dxT2 = touch.x - p.x;
        const dyT2 = touch.y - p.y;
        const distT2 = Math.hypot(dxT2, dyT2);
        const touchProx = touch.active && distT2 < ATTRACT_DIST;
        const alpha = touchProx ? 1 : 0.75;
        const r = touchProx ? p.radius * 1.8 : p.radius;

        ctx.fillStyle = `rgba(0, 210, 255, ${alpha})`;
        ctx.beginPath();
        ctx.arc(p.x, p.y, r, 0, Math.PI * 2);
        ctx.fill();

        for (let j = i + 1; j < particles.length; j++) {
            const p2 = particles[j];
            const dist = Math.hypot(p.x - p2.x, p.y - p2.y);
            if (dist < LINK_DIST) {
                const opacity = (1 - dist / LINK_DIST) * 0.3;
                ctx.strokeStyle = `rgba(0, 210, 255, ${opacity})`;
                ctx.lineWidth = 0.8;
                ctx.beginPath();
                ctx.moveTo(p.x, p.y);
                ctx.lineTo(p2.x, p2.y);
                ctx.stroke();
            }
        }

        if (touch.active && distT2 < ATTRACT_DIST) {
            const beamAlpha = (1 - distT2 / ATTRACT_DIST) * 0.8;
            ctx.strokeStyle = `rgba(0, 210, 255, ${beamAlpha})`;
            ctx.lineWidth = 1.2;
            ctx.beginPath();
            ctx.moveTo(p.x, p.y);
            ctx.lineTo(touch.x, touch.y);
            ctx.stroke();
        }
    }
}

window.addEventListener('resize', initParticles);
initParticles();
animateParticles();

// ─── Reactive 3D Tilt + Glow (touch only) ─────────────────────────────
function attachTiltEffects() {
    const cards = document.querySelectorAll('.card');
    cards.forEach(card => {
        const handleTouchMove = (e) => {
            if (e.touches.length === 0) return;
            card.classList.add('touch-active');
            const rect = card.getBoundingClientRect();
            const x = e.touches[0].clientX - rect.left;
            const y = e.touches[0].clientY - rect.top;
            const cx = rect.width / 2;
            const cy = rect.height / 2;
            const rotateX = ((y - cy) / cy) * -8;
            const rotateY = ((x - cx) / cx) * 8;
            card.style.transform =
                `perspective(900px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.04, 1.04, 1.04)`;
        };

        const handleTouchStart = (e) => {
            if (e.touches.length > 0) {
                spawnRipple(e.touches[0].clientX, e.touches[0].clientY);
            }
            handleTouchMove(e);
        };

        const handleTouchEnd = () => {
            card.classList.remove('touch-active');
            card.style.transform = `perspective(900px) rotateX(0deg) rotateY(0deg) scale3d(1,1,1)`;
            setTimeout(() => { card.style.transform = ''; }, 350);
        };

        card.addEventListener('touchmove', handleTouchMove, { passive: true });
        card.addEventListener('touchstart', handleTouchStart, { passive: true });
        card.addEventListener('touchend', handleTouchEnd);
        card.addEventListener('touchcancel', handleTouchEnd);
    });
}
