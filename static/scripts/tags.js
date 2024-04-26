document.addEventListener('DOMContentLoaded', () => {
    tippy('.add-tag-button', {
        content: `
        <div class="add-tag-field">
            <input type="text" class="tag-input" placeholder="Add a tag">
            <button class="add-tag-button">Add</button>
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
        onShown: handleAddTag
    });
});

function handleAddTag(instance) {
    const addTagField = instance.popper.querySelector('.add-tag-field');
    const tagInput = addTagField.querySelector('.tag-input');
    const addTagButton = addTagField.querySelector('.add-tag-button');

    addTagButton.addEventListener('click', () => {
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
    });
}

function createTagElement(tagText) {
    const tag = document.createElement('div');
    tag.classList.add('tag');
    tag.innerHTML = `
        <span class="material-symbols-outlined tag-icon">
            shoppingmode
        </span>
        <span class="tag-text">${tagText}</span>
    `;
    return tag;
}

function addTagToServer(projectId, tagText) {
    return fetch('/add-tag', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            project_id: projectId,
            tag: tagText
        })
    })
        .then(response => response.json());
}
