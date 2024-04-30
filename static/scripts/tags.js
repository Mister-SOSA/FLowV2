/**
 * Initializes the tooltips for the add tag buttons.
 */
function initializeTooltips() {
    document.addEventListener('DOMContentLoaded', () => {
        tippy('.add-tag-button', {
            content: `
            <div class="add-tag-field">
                <input type="text" class="tag-input" placeholder="Add a tag">
                <button class="add-tag-confirm">Add</button>
            </div>
            `,
            placement: 'bottom',
            theme: 'light',
            animation: 'scale',
            arrow: true,
            duration: 200,
            interactive: true,
            trigger: 'click',
            allowHTML: true,
            onShown: instance => {
                handleAddTag(instance);
                // Auto-focus the input when the tooltip is shown
                const tagInput = instance.popper.querySelector('.tag-input');
                tagInput.focus();
            }
        });
    });
}

/**
 * Handles the events for adding a tag.
 * @param {Object} instance - The tooltip instance.
 */
function handleAddTag(instance) {
    const addTagField = instance.popper.querySelector('.add-tag-field');
    const tagInput = addTagField.querySelector('.tag-input');
    const addTagButton = addTagField.querySelector('.add-tag-confirm');

    // Event listener to handle clicking the "Add" button
    addTagButton.addEventListener('click', () => {
        addTag(instance, tagInput);
    });

    // Event listener for the Enter key in the input field
    tagInput.addEventListener('keydown', (event) => {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevents the default action of Enter key in a form
            addTag(instance, tagInput);
        }
    });
}

/**
 * Adds a tag to the project.
 * @param {Object} instance - The tooltip instance.
 * @param {Object} tagInput - The input field for the tag.
 */
function addTag(instance, tagInput) {
    const project = instance.reference.closest('.project');
    const tagsContainer = project.querySelector('.tags-container');
    const tagText = tagInput.value.trim();

    if (tagText) {
        const tag = createTagElement(tagText);
        tagsContainer.insertBefore(tag, tagsContainer.lastElementChild);

        addTagToServer(project.getAttribute('project_id'), tagText)
            .then(data => {
                if (data.success) {
                    console.log('Tag added:', tagText);
                }
            })
            .catch(error => {
                console.error('Error adding tag:', error);
            });

        tagInput.value = '';
        instance.hide();
    }
}

/**
 * Sends a request to the server to add a tag to the project.
 * @param {string} projectId - The ID of the project.
 * @param {string} tagText - The text of the tag.
 * @returns {Promise} - A promise that resolves with the server response.
 */
async function addTagToServer(projectId, tagText) {
    const response = await fetch('/add-tag', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            project_id: projectId,
            tag: tagText
        })
    });
    return response.json();
}

/**
 * Creates a tag element.
 * @param {string} tagText - The text of the tag.
 * @returns {Object} - The created tag element.
 */
function createTagElement(tagText) {
    const tag = document.createElement('div');
    tag.className = 'tag';
    tag.innerHTML = `
                <span class="material-symbols-outlined tag-icon">
                    shoppingmode
                </span>
                <span class="tag-text">${tagText}</span>
    `;
    return tag;
}
