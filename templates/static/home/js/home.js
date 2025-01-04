function saberMais() {
    const insights2 = document.querySelector('.insights2');
    const icon = document.querySelector('.saber-mais i');
    
    insights2.classList.toggle('visible');
    
    if (insights2.classList.contains('visible')) {
        icon.classList.remove('fa-chevron-down');
        icon.classList.add('fa-chevron-up');
    } else {
        icon.classList.remove('fa-chevron-up');
        icon.classList.add('fa-chevron-down');
    }
}