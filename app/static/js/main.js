document.addEventListener('DOMContentLoaded', () => {
    initResizer();
    init();
});

function initResizer() {
    const resizer = document.getElementById('resizer');
    const sidebar = document.getElementById('sidebar');
    if (!resizer || !sidebar) return;

    const MIN_WIDTH = 150;
    const MAX_WIDTH = 600;
    let dragging = false;

    const onMouseMove = (e) => {
        if (!dragging) return;
        const newWidth = e.clientX - sidebar.getBoundingClientRect().left;
        const clamped = Math.max(MIN_WIDTH, Math.min(MAX_WIDTH, newWidth));
        sidebar.style.width = `${clamped}px`;
    };

    const stopDrag = () => {
        dragging = false;
        resizer.classList.remove('dragging');
        document.body.classList.remove('resizing');
        document.removeEventListener('mousemove', onMouseMove);
        document.removeEventListener('mouseup', stopDrag);
    };

    resizer.addEventListener('mousedown', (e) => {
        e.preventDefault();
        dragging = true;
        resizer.classList.add('dragging');
        document.body.classList.add('resizing');
        document.addEventListener('mousemove', onMouseMove);
        document.addEventListener('mouseup', stopDrag);
    });
}

let selectedNode = null;

async function fetchAPI(url) {
    try {
        const response = await fetch(url);
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        return null;
    }
}

async function init() {
    const container = document.getElementById('tree-container');

    if (document.body.dataset.authenticated !== 'true') {
        container.innerHTML = '<div class="loading-text">Please sign in to load collections.</div>';
        return;
    }

    container.innerHTML = '<div class="loading-text">Loading collections...</div>';

    const data = await fetchAPI('/api/collections');
    
    container.innerHTML = '';
    
    if (data && data.data && data.data.collections) {
        const collections = data.data.collections.collections;
        collections.forEach(col => {
            const node = createNode(col.name, 'fa-hubspot', async () => {
                await toggleCollection(col.id, node);
            });
            container.appendChild(node);
        });
    } else {
        container.innerHTML = '<div class="loading-text">No collections found. Check your token.</div>';
    }
}

async function toggleCollection(id, node) {
    const isExpanded = node.classList.toggle('expanded');
    if (!isExpanded) return;

    const children = node.querySelector('.tree-children');
    if (children.innerHTML === '') {
        children.innerHTML = '<div class="loading-text">Loading projects...</div>';
        const data = await fetchAPI(`/api/collections/${id}/projects`);
        children.innerHTML = '';
        
        if (data && data.data && data.data.projectsByCollectionId) {
            const projects = data.data.projectsByCollectionId.projects;
            projects.forEach(proj => {
                const projNode = createNode(proj.name, 'fa-project-diagram', async () => {
                    await toggleProject(proj.id, projNode);
                });
                children.appendChild(projNode);
            });
        }
    }
}

async function toggleProject(projectId, node) {
    const isExpanded = node.classList.toggle('expanded');
    if (!isExpanded) return;

    const childrenContainer = node.querySelector('.tree-children');
    if (childrenContainer.innerHTML === '') {
        childrenContainer.innerHTML = '<div class="loading-text">Loading assets...</div>';
        const data = await fetchAPI(`/api/projects/${projectId}/assets`);
        childrenContainer.innerHTML = '';
        
        if (data && data.data && data.data.assetsByProjectId) {
            const assets = data.data.assetsByProjectId.assets;
            
            // Build hierarchy maps
            const childrenMap = {};
            const roots = [];
            
            assets.forEach(asset => {
                const parentId = asset.parentId;
                if (parentId && parentId.startsWith('urn:medm:project:')) {
                    roots.push(asset);
                } else {
                    if (!childrenMap[parentId]) childrenMap[parentId] = [];
                    childrenMap[parentId].push(asset);
                }
            });

            // Recursive function to render asset nodes
            const renderAssetTree = (asset, container) => {
                let icon = 'fa-cube';
                let isFolder = false;
                
                if (asset.components) {
                    const componentNames = asset.components.map(c => c.name.toLowerCase());
                    if (componentNames.includes('folder') || componentNames.includes('collection') || componentNames.includes('container')) {
                        icon = 'fa-folder';
                        isFolder = true;
                    }
                }

                const subAssets = childrenMap[asset.id] || [];
                const hasChildren = subAssets.length > 0;

                const assetNode = createNode(asset.name, icon, () => {
                    if (hasChildren) {
                        assetNode.classList.toggle('expanded');
                    }
                    selectAsset(asset, assetNode);
                }, !hasChildren);
                
                if (isFolder) {
                    assetNode.querySelector('.type-icon').style.color = '#f39c12';
                }
                
                container.appendChild(assetNode);

                if (hasChildren) {
                    const subContainer = assetNode.querySelector('.tree-children');
                    subAssets.forEach(child => renderAssetTree(child, subContainer));
                }
            };

            roots.forEach(root => renderAssetTree(root, childrenContainer));
        }
    }
}

function selectAsset(asset, node) {
    if (selectedNode) {
        selectedNode.querySelector('.tree-item').classList.remove('selected');
    }
    node.querySelector('.tree-item').classList.add('selected');
    selectedNode = node;

    document.getElementById('welcome-screen').style.display = 'none';
    const card = document.getElementById('details-card');
    card.style.display = 'block';

    document.getElementById('asset-name').textContent = asset.name;
    document.getElementById('asset-id').textContent = asset.id;
    document.getElementById('asset-type-ids').textContent = asset.assetTypeIds && asset.assetTypeIds.length > 0 
        ? asset.assetTypeIds.join(', ') 
        : 'None';

    const components = document.getElementById('components-container');
    components.innerHTML = '';
    if (asset.components && asset.components.length > 0) {
        asset.components.forEach(c => {
            const span = document.createElement('span');
            span.className = 'tag';
            span.textContent = c.name;
            components.appendChild(span);
        });
    } else {
        components.innerHTML = '<span style="color:#999; font-style:italic">No components</span>';
    }
}

function createNode(name, iconClass, onClick, isLeaf = false) {
    const node = document.createElement('div');
    node.className = 'tree-node';
    
    const item = document.createElement('div');
    item.className = 'tree-item';
    
    const toggle = document.createElement('i');
    toggle.className = `fas fa-caret-right toggle-icon ${isLeaf ? 'invisible' : ''}`;
    if (isLeaf) toggle.style.visibility = 'hidden';
    
    const icon = document.createElement('i');
    icon.className = `fas ${iconClass} type-icon`;
    
    const text = document.createElement('span');
    text.textContent = name;
    
    item.appendChild(toggle);
    item.appendChild(icon);
    item.appendChild(text);
    
    item.onclick = (e) => {
        e.stopPropagation();
        onClick();
    };
    
    const children = document.createElement('div');
    children.className = 'tree-children';
    
    node.appendChild(item);
    node.appendChild(children);
    
    return node;
}
