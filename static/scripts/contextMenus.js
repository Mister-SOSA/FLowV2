document.addEventListener('DOMContentLoaded', function () {
    const container = document.querySelector('.tags-container'); // Ensure this container exists
    let openMenu = null; // Initialize the variable to keep track of the open menu

    container.addEventListener('contextmenu', function (event) {
        let tagElement = event.target.closest('.tag'); // Use closest to ensure we get the .tag regardless of the specific child element clicked
        if (tagElement) {
            event.preventDefault();

            // Remove any previously opened menu
            if (openMenu) {
                openMenu.remove();
            }

            // Create the menu element
            const menu = document.createElement('div');
            menu.className = 'custom-context-menu';

            // Create and append the delete button to the menu
            const button1 = document.createElement('div');
            button1.className = 'menu-button';
            button1.innerHTML = `
                <span class="material-symbols-outlined">
                    delete
                </span>
            `;
            button1.addEventListener('click', function () {
                tagElement.remove(); // Remove the tag element
                menu.remove(); // Remove the menu itself
                openMenu = null; // Reset the openMenu variable

                console.log('Deleting tag:', tagElement.querySelector('.tag-text').textContent); // Log the tag being deleted (optional

                // Send a request to the server to delete the tag
                fetch('/delete-tag', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        tag: tagElement.querySelector('.tag-text').textContent,
                        project_id: container.closest('.project').getAttribute('project_id')
                    })
                })
                    .then(response => response.json())
                    .then(data => {
                        if (data.success) {
                            console.log('Tag deleted:', tagElement.querySelector('.tag-text').textContent);
                        }
                    })
                    .catch(error => {
                        console.error('Error deleting tag:', error);
                    });
            });
            menu.appendChild(button1);

            // Position the menu based on mouse coordinates
            const x = event.clientX;
            const y = event.clientY;
            menu.style.left = `${x}px`;
            menu.style.top = `${y}px`;

            // Append the menu to the document body and store it as the currently open menu
            document.body.appendChild(menu);
            openMenu = menu;

            // Add a listener to close the menu when clicking outside
            document.addEventListener('click', function (outerEvent) {
                if (menu && !menu.contains(outerEvent.target) && outerEvent.target !== button1) {
                    menu.remove();
                    openMenu = null;
                }
            }, { once: true }); // Use once:true to auto-remove this listener after firing
        }
    });
});
