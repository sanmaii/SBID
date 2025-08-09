// This script is for download panel

// Select group
const select = document.getElementById('select-group');
const blog = document.getElementById('select-blog');
select.addEventListener('change', function () {
    switch (select.value) {
        case 'nogi':
            nogiMember();
            break;
        case 'sakura':
            sakuraMember();
            break;
        case 'hinata':
            hinataMember();
            break;
    }
});

// Case Nogizaka46
function nogiMember() {
    const member = document.getElementById('select-member');
    member.innerHTML = `
    <option value="" disabled selected hidden>請選擇:</option>
    <option value="nagi">井上 和</option>
    <option value="shiori">久保 史緒里</option>
    <option value="mayu">田村 真佑</option>`
    ;
    member.removeAttribute('disabled');
    member.addEventListener('change', function () {
        switch (member.value) {
            case 'nagi':
                nagiBlog();
                break;
            case 'shiori':
                shioriBlog();
                break;
            case 'mayu':
                mayuBlog();
                break;
        };
    });
    blog.innerHTML = '';
    blog.setAttribute('disabled', true);
}

// Case Sakurazaka46
function sakuraMember() {
    const member = document.getElementById('select-member');
    member.innerHTML = `
    <option value="" disabled selected hidden>請選擇:</option>
    <option value="kira">増本 綺良</option>
    <option value="rena">守屋 麗奈</option>
    <option value="airi">谷口 愛季</option>`
    ;
    member.removeAttribute('disabled');
    member.addEventListener('change', function () {
        switch (member.value) {
            case 'kira':
                kiraBlog();
                break;
            case 'rena':
                renaBlog();
                break;
            case 'airi':
                airiBlog();
                break;
        };
    });
    blog.innerHTML = '';
    blog.setAttribute('disabled', true);
}

// Case Hinatazaka46
function hinataMember() {
    const member = document.getElementById('select-member');
    member.innerHTML = `
    <option value="" disabled selected hidden>請選擇:</option>
    <option value="miku">金村 美玖</option>
    <option value="sumire">宮地 すみれ</option>
    <option value="yuu">佐藤 優羽</option>`
    ;
    member.removeAttribute('disabled');
    member.addEventListener('change', function () {
        switch (member.value) {
            case 'miku':
                mikuBlog();
                break;
            case 'sumire':
                sumireBlog();
                break;
            case 'yuu':
                yuuBlog();
                break;
        };
    });
    blog.innerHTML = '';
    blog.setAttribute('disabled', true);
}

function nagiBlog() {
    const blog = document.getElementById('select-blog');
    blog.innerHTML = `
    <option value="" disabled selected hidden>請選擇:</option>
    <option value="zankou">103387 --- 残香 2025/04/26 21:30 (GMT+9)</option>`
    ;
    blog.removeAttribute('disabled');
}

function shioriBlog() {
    const blog = document.getElementById('select-blog');
    blog.innerHTML = `
    <option value="" disabled selected hidden>請選擇:</option>
    <option value="mottainai">103241 --- 勿体無いを時間をかけてやりたい 2025/03/02 19:52 (GMT+9)</option>`
    ;
    blog.removeAttribute('disabled');
}

function mayuBlog() {
    const blog = document.getElementById('select-blog');
    blog.innerHTML = `
    <option value="" disabled selected hidden>請選擇:</option>
    <option value="tanjoubi">103032 --- 1月１２日は何の日？？ 2025/01/12 19:19 (GMT+9)</option>`
    ;
    blog.removeAttribute('disabled');
}

function kiraBlog() {
    const blog = document.getElementById('select-blog');
    blog.innerHTML = `
    <option value="" disabled selected hidden>請選擇:</option>
    <option value="yaho">56473 --- やほー 2024/06/28 19:44 (GMT+9)</option>`
    ;
    blog.removeAttribute('disabled');
}

function renaBlog() {
    const blog = document.getElementById('select-blog');
    blog.innerHTML = `
    <option value="" disabled selected hidden>請選擇:</option>
    <option value="cooking">60261 --- クッキング🍳 2025/05/27 18:13 (GMT+9)</option>`
    ;
    blog.removeAttribute('disabled');
}

function airiBlog() {
    const blog = document.getElementById('select-blog');
    blog.innerHTML = `
    <option value="" disabled selected hidden>請選擇:</option>
    <option value="ribbon">58785 --- 🎀 2025/01/23 19:08 (GMT+9)</option>`
    ;
    blog.removeAttribute('disabled');
}

function mikuBlog() {
    const blog = document.getElementById('select-blog');
    blog.innerHTML = `
    <option value="" disabled selected hidden>請選擇:</option>
    <option value="loveyourself">60108 --- #みくふぉと_Loveyourself! 2025/05/18 17:33 (GMT+9)</option>`
    ;
    blog.removeAttribute('disabled');
}

function sumireBlog() {
    const blog = document.getElementById('select-blog');
    blog.innerHTML = `
    <option value="" disabled selected hidden>請選擇:</option>
    <option value="anone">60226 --- あのね　そのね 2025/05/24 22:27 (GMT+9)</option>`
    ;
    blog.removeAttribute('disabled');
}

function yuuBlog() {
    const blog = document.getElementById('select-blog');
    blog.innerHTML = `
    <option value="" disabled selected hidden>請選擇:</option>
    <option value="bluedream">59761 --- 碧い夢を見た。佐藤優羽 2025/04/21 21:24 (GMT+9)</option>`
    ;
    blog.removeAttribute('disabled');
}

// Simulate download progress
const blogNum = document.getElementById('input-photo-num');
const startdlBtn = document.getElementById('start-dl');
const stopdlBtn = document.getElementById('stop-dl');
const progressFill = document.querySelector('.progress-fill');
const statusText = document.querySelector('.status-text');
const resultsContainer = document.querySelector('.results-container');
let progress = 0;
let interval;
startdlBtn.addEventListener('click', function () {
    console.log(blogNum.value);
    // Ensure a blog is selected and a valid number is entered
    if (!blog.value.trim() || ((!blogNum.value.trim()) || (blogNum.value < 0 || blogNum.value >1000000))) {
        statusText.textContent = '請先選擇所有必要項目！';
        return;
    };
    // Initialize
    progress = 0;
    progressFill.style.width = '0%';
    startdlBtn.setAttribute('disabled', true);
    stopdlBtn.removeAttribute('disabled');
    resultsContainer.innerHTML = '';
    statusText.textContent = '正在下載...';
    // Add random progress per 0.5s
    interval = setInterval(() => {
        progress += Math.random() * 30; // 0-30
        if (progress >= 100) {
            progress = 100;
            clearInterval(interval);
            startdlBtn.removeAttribute('disabled');
            stopdlBtn.setAttribute('disabled', true);
            statusText.textContent = '下載完成！';
            resultsContainer.innerHTML = 
            `
            <p class="result-text">圖片已下載！請點擊<a href="https://github.com/sanmaii/SBID/tree/main/docs/images/trial/${blog.value}">這裏</a>查看！</p>`
        }
        // Modify the width of progressFill
        progressFill.style.width = `${progress}%`
    }, 500);
});
stopdlBtn.addEventListener('click', function () {
    // Stop the progress immediately
    clearInterval(interval);
    statusText.textContent = '下載已中止';
    startdlBtn.removeAttribute('disabled');
    stopdlBtn.setAttribute('disabled', true);
});