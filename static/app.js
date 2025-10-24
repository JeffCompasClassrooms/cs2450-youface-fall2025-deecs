document.addEventListener('DOMContentLoaded', () => {
// Navbar collapse toggle
document.querySelectorAll('.navbar-toggler').forEach(btn => {
btn.addEventListener('click', () => {
const targetSel = btn.getAttribute('data-target');
if (!targetSel) return;
const target = document.querySelector(targetSel);
if (!target) return;
target.classList.toggle('show');
});
});

// Dismissible alerts
document.querySelectorAll('.alert .close[data-dismiss="alert"]').forEach(btn => {
btn.addEventListener('click', () => {
const alert = btn.closest('.alert');
if (!alert) return;
if (alert.classList.contains('fade')) {
alert.classList.remove('show');
alert.addEventListener('transitionend', () => alert.remove(), { once: true });
} else {
alert.remove();
}
});
});
});