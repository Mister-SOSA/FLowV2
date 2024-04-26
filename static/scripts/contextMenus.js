document.addEventListener('DOMContentLoaded', function () {
    const elements = document.querySelectorAll('.tag');
    let openMenu = null;
    let menu = null; // Declare the menu variable

    elements.forEach(function (element) {
        element.addEventListener('contextmenu', function (event) {
            event.preventDefault();

            if (openMenu) {
                openMenu.remove();
            }

            menu = document.createElement('div');
            menu.className = 'custom-context-menu';

            // Add buttons to the menu
            const button1 = document.createElement('div');
            button1.className = 'menu-button';
            button1.innerHTML = `
                <span class="material-symbols-outlined">
                    delete
                </span>
            `;
            button1.addEventListener('click', function () {
                element.remove();
                menu.remove();
            });
            menu.appendChild(button1);

            const x = event.clientX;
            const y = event.clientY;

            menu.style.left = `${x}px`;
            menu.style.top = `${y}px`;

            document.body.appendChild(menu);
            openMenu = menu;

            document.addEventListener('click', function (event) {
                if (menu && !menu.contains(event.target) && event.target !== button1) {
                    menu.remove();
                    openMenu = null;
                }
            });
        });
    });
});
