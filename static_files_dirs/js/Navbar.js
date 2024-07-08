const Navbar = document.getElementById("Navbar");
const NavbarLinksList = document.querySelectorAll(".navbar__links-list > li");


NavbarLinksList.forEach(element => {
    element.addEventListener("click", (e) => {
        NavbarSetActiveLink(element);
    });
});

function NavbarSetActiveLink(currentTab) {
    NavbarLinksList.forEach(element => { element.classList.remove("active") })
    console.log(currentTab);
    currentTab.classList.add("active");
}