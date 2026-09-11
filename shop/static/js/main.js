document.addEventListener('DOMContentLoaded', function () {
    const navbar = document.querySelector('.navbar');
    if (navbar && !navbar.querySelector('.nav-toggle')) {
        const toggle = document.createElement('button');
        toggle.className = 'nav-toggle';
        toggle.type = 'button';
        toggle.textContent = '☰';
        navbar.prepend(toggle);
        toggle.addEventListener('click', function () {
            navbar.classList.toggle('nav-open');
        });
    }

    document.querySelectorAll('.dropdown > a').forEach(function (link) {
        link.addEventListener('click', function (e) {
            if (window.innerWidth <= 768) {
                e.preventDefault();
                link.parentElement.classList.toggle('open');
            }
        });
    });
});
