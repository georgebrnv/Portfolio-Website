// Navbar collapsing by clicking outside
document.addEventListener('click', function(event) {
    var navbarToggler = document.querySelector('.navbar-toggler');
    var navbarMenu = document.querySelector('.navbar-collapse');
    if (navbarToggler.contains(event.target) || navbarMenu.contains(event.target)) {
        return;
    }
    navbarMenu.classList.remove('show');
});