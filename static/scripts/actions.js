document.addEventListener('DOMContentLoaded', () => {
    const handleFolderOpen = (action) => {
        const project = action.closest('.project');
        const projectPath = project.getAttribute('project_path');
        const folderPath = projectPath.substring(0, projectPath.lastIndexOf('/'));

        fetch('/open-folder', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                folder_path: folderPath
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Folder opened:', projectPath);
                }
            })
            .catch(error => {
                console.error(error);
            });
    };

    const handleProjectOpen = (action) => {
        const project = action.closest('.project');
        const projectPath = project.getAttribute('project_path');

        fetch('/open-project', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                project_path: projectPath
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Project opened:', projectPath);
                }
            })
            .catch(error => {
                console.error(error);
            });
    };

    const handleClearCache = () => {
        fetch('/clear-cache')
            .then(response => response.json())
            .then(data => {
                window.location.href = '/';
            })
            .catch(error => {
                console.error(error);
            });
    };

    const handleColorChange = (color, project) => {
        const colorBar = project.querySelector('.color-bar');
        const colorName = color.getAttribute('data-color');

        colorBar.style.backgroundColor = `var(--color-${colorName})`;

        fetch('/change-color', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                project_id: project.getAttribute('project_id'),
                color: colorName
            })
        })
            .then(response => response.json())
            .then(data => {
                if (data.success) {
                    console.log('Color changed:', colorName);
                }
            })
            .catch(error => {
                console.error('Error changing color:', error);
            });
    };

    document.querySelectorAll('.action.folder-open').forEach(action => {
        action.addEventListener('click', () => {
            handleFolderOpen(action);
        });
    });

    document.querySelectorAll('.action.open').forEach(action => {
        action.addEventListener('click', () => {
            handleProjectOpen(action);
        });
    });

    document.querySelector('.action.clear-cache').addEventListener('click', () => {
        handleClearCache();
    });

    tippy('.color-bar', {
        content: `
        <div class="color-picker">
            <div class="color" data-color="blue" style="background-color: var(--color-blue);"></div>
            <div class="color" data-color="green" style="background-color: var(--color-green);"></div>
            <div class="color" data-color="red" style="background-color: var(--color-red);"></div>
            <div class="color" data-color="yellow" style="background-color: var(--color-yellow);"></div>
            <div class="color" data-color="grey" style="background-color: var(--color-grey);"></div>
            <div class="color" data-color="purple" style="background-color: var(--color-purple);"></div>
            <div class="color" data-color="orange" style="background-color: var(--color-orange);"></div>
            <div class="color" data-color="pink" style="background-color: var(--color-pink);"></div>
            <div class="color" data-color="cyan" style="background-color: var(--color-cyan);"></div>
            <div class="color" data-color="teal" style="background-color: var(--color-teal);"></div>
            <div class="color" data-color="lime" style="background-color: var(--color-lime);"></div>
            <div class="color" data-color="amber" style="background-color: var(--color-amber);"></div>
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
        onShown(instance) {
            instance.popper.querySelectorAll('.color').forEach(color => {
                color.addEventListener('click', () => {
                    const project = instance.reference.closest('.project');
                    handleColorChange(color, project);
                });
            });
        }
    });
});
