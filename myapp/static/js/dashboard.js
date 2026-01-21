function toggleSidebar() {
    document.getElementById("sidebar").classList.toggle("hide");
}

function toggleMode() {
    document.body.classList.toggle("dark");
    document.body.classList.toggle("light");
}

function toggleProfile() {
    const menu = document.getElementById("profileMenu");
    menu.style.display = menu.style.display === "block" ? "none" : "block";
}
