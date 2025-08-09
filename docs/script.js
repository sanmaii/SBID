const navLinks = document.querySelectorAll('.nav-link');
const sections = document.querySelectorAll('.section');
const particlesContainer = document.getElementById('particles-container');

let currentSlide = 0;
let particleCount = 0;
// 最大粒子數量為視窗闊度除以15且向上取整
const maxParticles = Math.ceil(window.innerWidth / 15);
let backgroundImages = [];
let totalImages = 0;
let lastIsPortrait = window.innerHeight > window.innerWidth;
let isTransitioning = false;
let resizeTimeout = null;
let sliderInterval = null;

// 初始化
document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initCursor();
    initParticles();
    loadBackgroundImages().then(() => {
        initBackgroundSlider();
    });
    changeScreenSize();
    initGotoHome();
    initGotoDownloadPage();
    copytoClipboard();
});

// 主頁右上角的導航功能
function initNavigation() {
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            // 移除所有頁面的 active
            navLinks.forEach(nav => nav.classList.remove('active'));
            sections.forEach(section => section.classList.remove('active'));

            // 為目前的 nav 添加 active
            this.classList.add('active');
            const targetId = this.getAttribute('href').substring(1);
            const targetSection = document.getElementById(targetId);

            // 為目前的頁面添加 active
            if (targetSection) targetSection.classList.add('active');
        });
    });
}

// 鼠標
function initCursor() {
    function throttle(func, limit) {
        let inThrottle;
        return function() {
            if(!inThrottle) {
                func.apply(this, arguments);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }
    const cursor = document.querySelector('.cursor');
    document.addEventListener('mousemove', throttle((e) => {
        cursor.style.transform = `translate(${e.clientX}px, ${e.clientY}px)`;
    }, 16)); // 16ms
}

// 粒子系統
function initParticles() {
    setInterval(() => {
        if (particleCount < maxParticles) {
            createParticle();
        } else {
            // 達到上限時減少一半
            particleCount = maxParticles / 2;
        }
    }, 300);
}

// 創建粒子
function createParticle() {
    const particle = document.createElement('div');
    particle.className = 'particle';

    // 隨機粒子位置
    const startX = Math.random() * window.innerWidth;
    const startY = Math.random() * window.innerHeight;
    particle.style.left = `${startX}px`;
    particle.style.top = `${startY}px`;

    // 隨機大小
    const size = Math.random() * 6 + 2; // 2-8 px
    particle.style.width = `${size}px`;
    particle.style.height = `${size}px`;

    // 隨機透明度
    const opacity = Math.random() * 0.5 + 0.3; // 0.3-0.8
    particle.style.backgroundColor = `rgba(255, 255, 255, ${opacity})`;

    // 加入到畫面
    particlesContainer.appendChild(particle);
    particleCount++;

    // 隨機方向及速度
    const angle = Math.random() * 360; // 0-360度
    const speed = Math.random() * 1.5 + 0.5; // 0.5-2

    // 換算成位移
    const vx = Math.cos(angle) * speed;
    const vy = Math.sin(angle) * speed;

    // 漸變移動效果
    let frame = 0;
    const maxFrames = 1200; // 持續的幀數

    function move() {
        if (frame >= maxFrames) {
            // 達到持續時間上限時移除粒子
            particle.remove();
            particleCount--;
            return;
        }
        const currentX = parseFloat(particle.style.left);
        const currentY = parseFloat(particle.style.top);
        particle.style.left = `${currentX + vx}px`;
        particle.style.top = `${currentY + vy}px`;
        frame++;
        requestAnimationFrame(move);
    }
    move();
}

// 載入背景圖片
async function loadBackgroundImages() {
    // 添加多個 bg-slide
    const bgContainer = document.getElementById('background-slider');
    bgContainer.innerHTML = '<div class="bg-slide active"></div>';
    let html = '';
    for (let i = 0; i < 100; i++) {
        html += '<div class="bg-slide"></div>';
    }
    bgContainer.innerHTML += html;
    const bgSlides = document.querySelectorAll('.bg-slide');
    function isPortrait() {
        return (window.innerHeight) > window.innerWidth;
    }
    const folder = isPortrait() ? 'portrait' : 'landscape';
    const basePath = `images/${folder}/`;
    const extensions = ['.jpg', '.png'];
    const images = [];
    let loadedCount = 0;

    for (let i = 1; i <= bgSlides.length; i++) {
        for (const j of extensions) {
            const imagePath = `${basePath}${i}${j}`;
            const isAvailable = await checkImageExists(imagePath);
            if (isAvailable) {
                images.push(imagePath);
                loadedCount++;
                break;
            }
        }
    }     

    if (images.length === 0) {
        console.warn('無法載入本地圖片，使用備用漸變背景');
        setupFallbackBackgrounds();
    } else {
        backgroundImages = images;
        totalImages = images.length;
        console.log(`成功載入 ${totalImages} 張背景圖片`);
        setupBackgroundSlides();
    }
    console.log(bgSlides.length);
}

// 檢查圖片是否存在
function checkImageExists(imagePath) {
    return new Promise((resolve) => {
        const img = new Image();
        img.onload = () => resolve(true);
        img.onerror = () => resolve(false);
        img.src = imagePath;
        setTimeout(() => resolve(false), 1000);
    });
}

function setupBackgroundSlides() {
    const slides = document.querySelectorAll('.bg-slide');
    // 檢查圖片還是 bg-slide 的數量較少
    const slidesNeeded = Math.min(backgroundImages.length, slides.length);
    backgroundImages.slice(0, slidesNeeded).forEach((imagePath, index) => {
        if (slides[index]) {
            slides[index].style.backgroundImage = `url("${imagePath}")`;
        }
    });
    // 停用多餘的 bg-slide
    for (let i = slidesNeeded; i < slides.length; i++) {
        slides[i].style.display = 'none';
    }
}

function setupFallbackBackgrounds() {
    const slides = document.querySelectorAll('.bg-slide');
    const gradients = [
        'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        'linear-gradient(135deg, #f093fb 0%, #f5576c 100%)',
        'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
        'linear-gradient(135deg, #43e97b 0%, #38f9d7 100%)',
        'linear-gradient(135deg, #fa709a 0%, #fee140 100%)',
        'linear-gradient(135deg, #a8edea 0%, #fed6e3 100%)',
        'linear-gradient(135deg, #ff9a9e 0%, #fecfef 100%)',
        'linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%)'
    ];

    slides.forEach((slide, index) => {
        if (gradients[index]) {
            slide.style.background = gradients[index];
        }
    });

    backgroundImages = gradients;
    totalImages = gradients.length;
}

// 初始化背景輪換系統
function initBackgroundSlider() {
    if (totalImages === 0) return;
    if (sliderInterval) clearInterval(sliderInterval);
    // 每隔10秒更換背景
    sliderInterval = setInterval(() => {
        const slides = document.querySelectorAll('.bg-slide');
        // 只選擇已使用的 bg-slide
        const visibleSlides = Array.from(slides).filter(slide => slide.style.display !== 'none');
        if (visibleSlides.length === 0) return;
        visibleSlides[currentSlide].classList.remove('active');
        currentSlide = (currentSlide + 1) % visibleSlides.length; // 即便 currentSlide 的數值大於 visibleSlides 的長度仍可以進行輪換
        visibleSlides[currentSlide].classList.add('active');
    }, 10000);
}

// 更改畫面大小時自然過渡背景圖片
function backgroundTransition() {
    return new Promise((resolve) => {
        const slides = document.querySelectorAll('.bg-slide');
        slides.forEach(slide => {
            slide.classList.remove('active');
        });
        setTimeout(() => {
            resolve();
        }, 2000);
    });
};

// 監聽用戶更改畫面大小
function changeScreenSize() {     
    // 如果方向沒有變動，則不用重載
    window.addEventListener("resize", function() {

        //先取消之前的 resizeTimeout() 防止閃爍     
        clearTimeout(resizeTimeout);
        resizeTimeout = setTimeout(async () => {

            // 重新判斷使用直向抑或橫向圖片
            const nowIsPortrait = window.innerHeight > window.innerWidth;

            // 如果方向不變則不變
            if (lastIsPortrait === nowIsPortrait) return;
            lastIsPortrait = nowIsPortrait;

            // 偵測是否正在進行背景切換
            if (isTransitioning) return;
            isTransitioning = true;

            // 過渡背景          
            await backgroundTransition();
            await loadBackgroundImages();
            initBackgroundSlider();
            isTransitioning = false;
            }, 2000);
        });
    }

// 按左上角圖標顯示主頁
function initGotoHome() {
    const homelogo = document.querySelector('.logo');
    homelogo.addEventListener('click', function (e) {
        e.preventDefault();

        // 移除所有 nav 和 section 的 active
        navLinks.forEach(nav => nav.classList.remove('active'));
        sections.forEach(section => section.classList.remove('active'));

        // 激活主頁
        const homeNav = document.querySelector('a[href="#home"]');
        if (homeNav) homeNav.classList.add('active');

        // 顯示主頁
        const targetSection = document.getElementById('home');
        if (targetSection) {
            targetSection.classList.add('active');
        }
    });
}

// 按主頁“線上體驗”按鈕顯示下載頁面
function initGotoDownloadPage() {
    const gotoDownloadBtn = document.getElementById('go-to-download');
    gotoDownloadBtn.addEventListener('click', function (e) {
        e.preventDefault();

        // 移除所有 nav 和 section 的 active
        navLinks.forEach(nav => nav.classList.remove('active'));
        sections.forEach(section => section.classList.remove('active'));

        // 激活下載頁面
        const crawlerNav = document.querySelector('a[href="#download"]');
        if (crawlerNav) crawlerNav.classList.add('active');

        // 顯示下載頁面
        const targetSection = document.getElementById('download');
        if (targetSection) {
            targetSection.classList.add('active');
        }
    });
}

// 代碼複製
function copytoClipboard() {
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', function (e) {
            e.preventDefault();
            const content = btn.previousElementSibling.innerText;
            navigator.clipboard.writeText(content).then(() => {
                btn.innerHTML = '<i class="fa-solid fa-check"></i>';
                setTimeout(() => {
                    btn.innerHTML = '<i class="fa-regular fa-copy"></i>';
                }, 1500);
            });
        });
    });
}

console.log(window.innerHeight, window.innerWidth);
