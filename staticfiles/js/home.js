const closeBtn = document.getElementById('close_btn');
const clearSearchBtn = document.querySelector(".clear_search");
const searchBtn = document.querySelector(".search_btn");
const searchInput = document.getElementById('q');
const body = document.querySelector('body');
const notes = document.querySelectorAll('[data-option-parent]')
const searchForm = document.getElementById('search_form');
const error_message = document.getElementById('error_message');
const currentTheme = document.querySelector("body");
// console.log('fish')

closeBtn.addEventListener('click', () => {
    window.close();
})

searchForm.addEventListener('submit', (e) => {
    e.preventDefault()
    searchText = searchInput.value;
    if(searchText.length == 0){
        error_message.classList.remove('hide');
        setTimeout(() => {error_message.classList.add('hide');}, 3000)
    }
})

searchInput.addEventListener("input", () => {
    let searchText = searchInput.value;
    if(searchText.length > 0){
        clearSearchBtn.classList.remove('hide');
    }else{
        clearSearchBtn.classList.add('hide');
    }
})

clearSearchBtn.addEventListener('click', () =>{
    searchInput.value = ''
    clearSearchBtn.classList.add('hide');
})

const resetOptions = () => {
    for(let content of optionsContent){
        content.classList.add('hide')
    }
}

document.addEventListener('click', e => {
    let menuBtn = e.target.matches('[data-option-btn]');
    if(!menuBtn && e.target.closest('[data-option-parent]') != 'null'){
        resetMenus();
    }

    let currentMenu;
    if(menuBtn){
        currentMenu = e.target;
        currentMenu.classList.toggle('active');
    }
    document.querySelectorAll('[data-option-btn].active').forEach(menubtn =>{
        if(menubtn == currentMenu)return
        menubtn.classList.remove('active');
    })
})

const menuBtns = document.querySelectorAll('[data-option-btn]')

function resetMenus(){
    for(let menuBtn of menuBtns){
        menuBtn.classList.remove('active');
    }
}

const darkMode = () => {
    darkModeBtn.classList.add('hide')
    lightModeBtn.classList.remove('hide')
    currentTheme.classList = 'dark-mode'
    localStorage.setItem('notes_theme', 'dark-mode')
}

const lightMode = () => {
    darkModeBtn.classList.remove('hide')
    lightModeBtn.classList.add('hide')
    currentTheme.classList = 'light-mode'
    localStorage.setItem('notes_theme', 'light-mode')
}

darkModeBtn.addEventListener('click', () => {
    darkMode()
})

lightModeBtn.addEventListener('click', () => {
    lightMode()
})