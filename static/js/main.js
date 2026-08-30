document.getElementById('navBurger')?.addEventListener('click', () => {
    document.getElementById('mobileMenu')?.classList.toggle('open');
});

setTimeout(() => {
    document.querySelectorAll('.flash').forEach(el => el.remove());
}, 4000);

function handleNewsletter(e){
    e.preventDefault();
    alert('Thanks for subscribing! 🎉');
    e.target.reset();
}


document.querySelectorAll('.view-btn').forEach(btn =>{
    btn.addEventListener('click', () =>{
        document.querySelectorAll('.view-btn').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const grid = document.getElementById('productGrid');
        if(grid){
            grid.style.gridTemplateColumns = btn.dataset.view === 'list' ? '1fr' : '';
        }
    });
});