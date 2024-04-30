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

function handleAddTag(instance) {
    const addTagField = instance.popper.querySelector('.add-tag-field');
    const tagInput = addTagField.querySelector('.tag-input');
    const addTagButton = addTagField.querySelector('.add-tag-confirm');

    // Event listener to handle clicking the "Add" button
    addTagButton.addEventListener('click', () => {
        addTag(instance, tagInput, addTagButton);
    });

    // Event listener for the Enter key in the input field
    tagInput.addEventListener('keydown', (event) => {
        if (event.key === "Enter") {
            event.preventDefault(); // Prevents the default action of Enter key in a form
            addTag(instance, tagInput, addTagButton);
        }
    });
}

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
